# This file is part of ctrl_mpexec.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (https://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This software is dual licensed under the GNU General Public License and also
# under a 3-clause BSD license. Recipients may choose which of these licenses
# to use; please see the files gpl-3.0.txt and/or bsd_license.txt,
# respectively.  If you choose the GPL option then the following text applies
# (but note that there is still no warranty even if you opt for BSD instead):
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import annotations

import os
import shutil
import tempfile
import unittest
from typing import Any

import lsst.daf.butler
import lsst.utils.tests
from lsst.ctrl.mpexec import SimplePipelineExecutor
from lsst.pipe.base import PipelineGraph, Struct, TaskMetadata, connectionTypes
from lsst.pipe.base.pipeline_graph import IncompatibleDatasetTypeError
from lsst.pipe.base.tests.no_dimensions import (
    NoDimensionsTestConfig,
    NoDimensionsTestConnections,
    NoDimensionsTestTask,
)
from lsst.utils.introspection import get_full_type_name

TESTDIR = os.path.abspath(os.path.dirname(__file__))


class NoDimensionsTestConnections2(NoDimensionsTestConnections, dimensions=set()):
    """A connections class used for testing."""

    input = connectionTypes.Input(
        name="input", doc="some dict-y input data for testing", storageClass="TaskMetadataLike"
    )


class NoDimensionsTestConfig2(NoDimensionsTestConfig, pipelineConnections=NoDimensionsTestConnections2):
    """A config used for testing."""


class NoDimensionsMetadataTestConnections(NoDimensionsTestConnections, dimensions=set()):
    """Test connection class for metadata.

    Deliberately choose a storage class that does not match the metadata
    default TaskMetadata storage class.
    """

    meta = connectionTypes.Input(
        name="a_metadata", doc="Metadata from previous task", storageClass="StructuredDataDict"
    )


class NoDimensionsMetadataTestConfig(
    NoDimensionsTestConfig, pipelineConnections=NoDimensionsMetadataTestConnections
):
    """A config used for testing the metadata."""


class NoDimensionsMetadataTestTask(NoDimensionsTestTask):
    """A simple pipeline task that can take a metadata as input."""

    ConfigClass = NoDimensionsMetadataTestConfig
    _DefaultName = "noDimensionsMetadataTest"

    def run(self, input: dict[str, int], meta: dict[str, Any]) -> Struct:
        """Run the task, adding the configured key-value pair to the input
        argument and returning it as the output.

        Parameters
        ----------
        input : `dict`
            Dictionary to update and return.
        meta : `dict`
            Metadata to add.

        Returns
        -------
        result : `lsst.pipe.base.Struct`
            Struct with a single ``output`` attribute.
        """
        self.log.info("Run metadata method given data of type: %s", get_full_type_name(input))
        output = input.copy()
        output[self.config.key] = self.config.value

        self.log.info("Received task metadata (%s): %s", get_full_type_name(meta), meta)

        # Can change the return type via configuration.
        if "TaskMetadata" in self.config.outputSC:
            output = TaskMetadata.from_dict(output)
        elif type(output) is TaskMetadata:
            # Want the output to be a dict
            output = output.to_dict()
        self.log.info("Run method returns data of type: %s", get_full_type_name(output))
        return Struct(output=output)


class SimplePipelineExecutorTests(lsst.utils.tests.TestCase):
    """Test the SimplePipelineExecutor API with a trivial task."""

    def setUp(self):
        self.path = tempfile.mkdtemp()
        # standalone parameter forces the returned config to also include
        # the information from the search paths.
        config = lsst.daf.butler.Butler.makeRepo(
            self.path, standalone=True, searchPaths=[os.path.join(TESTDIR, "config")]
        )
        self.butler = SimplePipelineExecutor.prep_butler(config, [], "fake")
        self.butler.registry.registerDatasetType(
            lsst.daf.butler.DatasetType(
                "input",
                dimensions=self.butler.dimensions.empty,
                storageClass="StructuredDataDict",
            )
        )
        self.butler.put({"zero": 0}, "input")

    def tearDown(self):
        shutil.rmtree(self.path, ignore_errors=True)

    def test_from_task_class(self):
        """Test executing a single quantum with an executor created by the
        `from_task_class` factory method, and the
        `SimplePipelineExecutor.as_generator` method.
        """
        executor = SimplePipelineExecutor.from_task_class(NoDimensionsTestTask, butler=self.butler)
        (quantum,) = executor.as_generator(register_dataset_types=True)
        self.assertEqual(self.butler.get("output"), {"zero": 0, "one": 1})

    def _configure_pipeline(self, config_a_cls, config_b_cls, storageClass_a=None, storageClass_b=None):
        """Configure a pipeline with from_pipeline_graph."""
        config_a = config_a_cls()
        config_a.connections.output = "intermediate"
        if storageClass_a:
            config_a.outputSC = storageClass_a
        config_b = config_b_cls()
        config_b.connections.input = "intermediate"
        if storageClass_b:
            config_b.outputSC = storageClass_b
        config_b.key = "two"
        config_b.value = 2
        pipeline_graph = PipelineGraph()
        pipeline_graph.add_task("a", NoDimensionsTestTask, config_a)
        pipeline_graph.add_task("b", NoDimensionsTestTask, config_b)
        executor = SimplePipelineExecutor.from_pipeline_graph(pipeline_graph, butler=self.butler)
        return executor

    def _test_logs(self, log_output, input_type_a, output_type_a, input_type_b, output_type_b):
        """Check the expected input types received by tasks A and B.

        Note that these are the types as seen from the perspective of the task,
        so they must be consistent with the task's connections, but may not be
        consistent with the registry dataset types.
        """
        all_logs = "\n".join(log_output)
        self.assertIn(f"lsst.a:Run method given data of type: {input_type_a}", all_logs)
        self.assertIn(f"lsst.b:Run method given data of type: {input_type_b}", all_logs)
        self.assertIn(f"lsst.a:Run method returns data of type: {output_type_a}", all_logs)
        self.assertIn(f"lsst.b:Run method returns data of type: {output_type_b}", all_logs)

    def test_from_pipeline(self):
        """Test executing a two quanta from different configurations of the
        same task, with an executor created by the `from_pipeline` factory
        method, and the `SimplePipelineExecutor.run` method.
        """
        executor = self._configure_pipeline(
            NoDimensionsTestTask.ConfigClass, NoDimensionsTestTask.ConfigClass
        )

        with self.assertLogs("lsst", level="INFO") as cm:
            quanta = executor.run(register_dataset_types=True, save_versions=False)
        self._test_logs(cm.output, "dict", "dict", "dict", "dict")

        self.assertEqual(len(quanta), 2)
        self.assertEqual(self.butler.get("intermediate"), {"zero": 0, "one": 1})
        self.assertEqual(self.butler.get("output"), {"zero": 0, "one": 1, "two": 2})

    def test_from_pipeline_intermediates_differ(self):
        """Run pipeline but intermediates definition in registry differs."""
        # Pre-define the "intermediate" storage class to be something that is
        # like a dict but is not a dict. This will fail unless storage
        # class conversion is supported in put and get.
        self.butler.registry.registerDatasetType(
            lsst.daf.butler.DatasetType(
                "intermediate",
                dimensions=self.butler.dimensions.empty,
                storageClass="TaskMetadataLike",
            )
        )
        executor = self._configure_pipeline(
            NoDimensionsTestTask.ConfigClass,
            NoDimensionsTestTask.ConfigClass,
            storageClass_b="TaskMetadataLike",
        )
        with self.assertLogs("lsst", level="INFO") as cm:
            quanta = executor.run(register_dataset_types=True, save_versions=False)
        # A dict is given to task a without change.
        # A returns a dict because it has not been told to do anything else.
        # That does not match the storage class so it will be converted
        # on put.
        # b is given a dict, because that's what its connection asks for.
        # b returns a TaskMetadata because that's how we configured it, and
        # since its output wasn't registered in advance, it will have been
        # registered as TaskMetadata and will now be received as TaskMetadata.
        self._test_logs(cm.output, "dict", "dict", "dict", "lsst.pipe.base.TaskMetadata")

        self.assertEqual(len(quanta), 2)
        self.assertEqual(self.butler.get("intermediate"), TaskMetadata.from_dict({"zero": 0, "one": 1}))
        self.assertEqual(self.butler.get("output"), TaskMetadata.from_dict({"zero": 0, "one": 1, "two": 2}))

    def test_from_pipeline_output_differ(self):
        """Run pipeline but output definition in registry differs."""
        # Pre-define the "output" storage class to be something that is
        # like a dict but is not a dict. This will fail unless storage
        # class conversion is supported in put and get.
        self.butler.registry.registerDatasetType(
            lsst.daf.butler.DatasetType(
                "output",
                dimensions=self.butler.dimensions.empty,
                storageClass="TaskMetadataLike",
            )
        )
        executor = self._configure_pipeline(
            NoDimensionsTestTask.ConfigClass,
            NoDimensionsTestTask.ConfigClass,
            storageClass_a="TaskMetadataLike",
        )
        with self.assertLogs("lsst", level="INFO") as cm:
            quanta = executor.run(register_dataset_types=True, save_versions=False)
        # a has been told to return a TaskMetadata but this will convert to
        # dict on read by b.
        # b returns a dict and that is converted to TaskMetadata on put.
        self._test_logs(cm.output, "dict", "lsst.pipe.base.TaskMetadata", "dict", "dict")

        self.assertEqual(len(quanta), 2)
        self.assertEqual(self.butler.get("intermediate").to_dict(), {"zero": 0, "one": 1})
        self.assertEqual(self.butler.get("output").to_dict(), {"zero": 0, "one": 1, "two": 2})

    def test_from_pipeline_input_differ(self):
        """Run pipeline but input definition in registry differs."""
        # This config declares that the pipeline takes a TaskMetadata
        # as input but registry already thinks it has a StructureDataDict.
        executor = self._configure_pipeline(NoDimensionsTestConfig2, NoDimensionsTestTask.ConfigClass)

        with self.assertLogs("lsst", level="INFO") as cm:
            quanta = executor.run(register_dataset_types=True, save_versions=False)
        self._test_logs(cm.output, "lsst.pipe.base.TaskMetadata", "dict", "dict", "dict")

        self.assertEqual(len(quanta), 2)
        self.assertEqual(self.butler.get("intermediate"), {"zero": 0, "one": 1})
        self.assertEqual(self.butler.get("output"), {"zero": 0, "one": 1, "two": 2})

    def test_from_pipeline_incompatible(self):
        """Test that we cannot make a QG if the registry and pipeline have
        incompatible storage classes for a dataset type.
        """
        # Incompatible output dataset type.
        self.butler.registry.registerDatasetType(
            lsst.daf.butler.DatasetType(
                "output",
                dimensions=self.butler.dimensions.empty,
                storageClass="StructuredDataList",
            )
        )
        with self.assertRaisesRegex(
            IncompatibleDatasetTypeError, "Incompatible definition.*StructuredDataDict.*StructuredDataList.*"
        ):
            self._configure_pipeline(NoDimensionsTestTask.ConfigClass, NoDimensionsTestTask.ConfigClass)

    def test_from_pipeline_registry_changed(self):
        """Run pipeline, but change registry dataset types between making the
        QG and executing it.

        This only fails with full-butler execution; we don't have a way to
        prevent it with QBB.
        """
        executor = self._configure_pipeline(
            NoDimensionsTestTask.ConfigClass, NoDimensionsTestTask.ConfigClass
        )
        self.butler.registry.registerDatasetType(
            lsst.daf.butler.DatasetType(
                "output",
                dimensions=self.butler.dimensions.empty,
                storageClass="TaskMetadataLike",  # even compatible is not okay
            )
        )
        with self.assertRaisesRegex(
            lsst.daf.butler.registry.ConflictingDefinitionError,
            ".*definition in registry has changed.*StructuredDataDict.*TaskMetadataLike.*",
        ):
            executor.run(register_dataset_types=True, save_versions=False)

    def test_from_pipeline_metadata(self):
        """Test two tasks where the output uses metadata from input."""
        # Must configure a special pipeline for this test.
        config_a = NoDimensionsTestTask.ConfigClass()
        config_a.connections.output = "intermediate"
        config_b = NoDimensionsMetadataTestTask.ConfigClass()
        config_b.connections.input = "intermediate"
        config_b.key = "two"
        config_b.value = 2
        pipeline_graph = PipelineGraph()
        pipeline_graph.add_task("a", NoDimensionsTestTask, config=config_a)
        pipeline_graph.add_task("b", NoDimensionsMetadataTestTask, config=config_b)
        executor = SimplePipelineExecutor.from_pipeline_graph(pipeline_graph, butler=self.butler)

        with self.assertLogs("test_simple_pipeline_executor", level="INFO") as cm:
            quanta = executor.run(register_dataset_types=True, save_versions=False)
        self.assertIn(f"Received task metadata ({get_full_type_name(dict)})", "".join(cm.output))

        self.assertEqual(len(quanta), 2)
        self.assertEqual(self.butler.get("intermediate"), {"zero": 0, "one": 1})
        self.assertEqual(self.butler.get("output"), {"zero": 0, "one": 1, "two": 2})

    def test_from_pipeline_file(self):
        """Test executing a two quanta from different configurations of the
        same task, with an executor created by the `from_pipeline_filename`
        factory method, and the `SimplePipelineExecutor.run` method.
        """
        filename = os.path.join(self.path, "pipeline.yaml")
        with open(filename, "w") as f:
            f.write(
                """
                description: test
                tasks:
                    a:
                        class: "lsst.pipe.base.tests.no_dimensions.NoDimensionsTestTask"
                        config:
                            connections.output: "intermediate"
                    b:
                        class: "lsst.pipe.base.tests.no_dimensions.NoDimensionsTestTask"
                        config:
                            connections.input: "intermediate"
                            key: "two"
                            value: 2
                """
            )
        executor = SimplePipelineExecutor.from_pipeline_filename(filename, butler=self.butler)
        quanta = executor.run(register_dataset_types=True, save_versions=False)
        self.assertEqual(len(quanta), 2)
        self.assertEqual(self.butler.get("intermediate"), {"zero": 0, "one": 1})
        self.assertEqual(self.butler.get("output"), {"zero": 0, "one": 1, "two": 2})


class MemoryTester(lsst.utils.tests.MemoryTestCase):
    """Generic tests for file leaks."""


def setup_module(module):
    """Set up the module for pytest.

    Parameters
    ----------
    module : `~types.ModuleType`
        Module to set up.
    """
    lsst.utils.tests.init()


if __name__ == "__main__":
    lsst.utils.tests.init()
    unittest.main()
