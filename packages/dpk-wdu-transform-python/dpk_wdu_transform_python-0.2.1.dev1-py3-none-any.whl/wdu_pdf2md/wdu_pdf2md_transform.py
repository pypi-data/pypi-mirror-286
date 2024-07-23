# (C) Copyright IBM Corp. 2024.
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#  http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
################################################################################

import base64
import io
import json
import os
import time
import zipfile
from argparse import ArgumentParser, Namespace
from datetime import datetime

# from pathlib import Path
from typing import Any

import pyarrow as pa

# import ray
import requests
from data_processing.data_access import (
    DataAccess,
    DataAccessFactory,
    DataAccessFactoryBase,
)
from data_processing.transform import AbstractBinaryTransform, TransformConfiguration
from data_processing.utils import TransformUtils, get_logger, str2bool


# from data_processing_ray.runtime.ray.runtime_configuration import (
#     RayTransformRuntimeConfiguration,
# )
# from ray.actor import ActorHandle
# from ray.util.metrics import Counter, Gauge


# from data_processing_ibm.ray import TransformLauncherIBM


logger = get_logger(__name__)

shortname = "wdu_pdf2md"


class WduPdf2MdTransform(AbstractBinaryTransform):
    """ """

    def __init__(self, config: dict):
        """
        Initialize based on the dictionary of configuration information.
        This is generally called with configuration parsed from the CLI arguments defined
        by the companion runtime, LangSelectorTransformRuntime.  If running inside the RayMutatingDriver,
        these will be provided by that class with help from the RayMutatingDriver.
        """

        super().__init__(config)
        self.data_access: DataAccess = config.get("data_access", None)
        if self.data_access is None:
            raise RuntimeError("exception getting data access class")

        self.wdu_rest_host = config.get("wdu_rest_host", None)
        self.wdu_rest_port = config.get("wdu_rest_port", None)
        self.wdu_max_retries = config.get("wdu_max_retries", None)
        self.server_version_logged = False

        # self.doc_counter = Counter("worker_pdf_doc_count", "Number of PDF documents converted by the worker")
        # self.page_counter = Counter("worker_pdf_pages_count", "Number of PDF pages converted by the worker")
        # self.page_convert_gauge = Gauge(
        #     "worker_pdf_page_avg_convert_time", "Average time for converting a single PDF page on each worker"
        # )
        # self.doc_convert_gauge = Gauge("worker_pdf_convert_time", "Time spent converting a single document")

    def transform_binary(self, file_name: str, byte_array: bytes) -> tuple[list[tuple[bytes, str]], dict[str, Any]]:
        """
        Converts raw data from a tuple of PDF to Parquet format.
        """
        # data = []
        success_doc_id = []
        failed_doc_id = []
        skipped_doc_id = []
        # number_of_rows = 0

        pdf_file_basename = os.path.basename(file_name)
        if (
            TransformUtils.get_file_extension(file_name)[1] != ".pdf"
            and TransformUtils.get_file_extension(file_name)[1] != ".PDF"
        ):
            logger.warning(f"Got unsupported file type {file_name}, expecting a .pdf or .PDF, skipping")
            skipped_doc_id.append(pdf_file_basename)
            metadata = {"nskipped": len(skipped_doc_id)}
            return [], metadata

        request_params = {
            "options": {
                "languages_list": ["eng"],
                "include_page_images_in_output": True,
                "log_kvps": {
                    "which_file": str(file_name),
                },
            },
            "steps": {
                "ocr_step": {
                    "auto_rotation_correction": True,
                },
                "tables_processing": {"model_id": "table_extraction_gte", "enabled": True},
                "assembly_json": {},
                "assembly_markdown": {},
            },
        }

        rest_target: str = f"http://{self.wdu_rest_host}:{self.wdu_rest_port}/api/v1/task/process"

        pdf_bytes, pdf_retries = self.data_access.get_file(str(file_name))

        if pdf_bytes is None:
            logger.warning(f"No contents in the .pdf file. Skipping.")
            skipped_doc_id.append(pdf_file_basename)
            metadata = {"nskipped": len(skipped_doc_id)}
            return [], metadata

        pdf_file_stream = io.BytesIO(pdf_bytes)
        # Convert PDF to Markdown
        start_time = time.time()
        # Pass all arguments as multipart form data.
        multipart_data = {
            "inputs.file": (pdf_file_basename, pdf_file_stream),
            "inputs": json.dumps({}),
            "parameters": json.dumps(request_params),
            "model_id": "processor",
        }
        status_force_list = [408, 429, 500, 502, 503, 504]
        for _ in range(self.wdu_max_retries):
            # Don't send in "Content-type" in header when using `files=`
            try:
                response = requests.post(
                    url=rest_target,
                    files=multipart_data,
                    timeout=10000,
                )
                if response.status_code in status_force_list:
                    continue
                logger.info(f"response status: {response.status_code}")
                response.raise_for_status()
                break
            except requests.exceptions.RequestException as e:
                logger.warning(f"Failed extraction. Exception {str(e)} processing file {pdf_file_basename}, skipping")
                failed_doc_id.append(pdf_file_basename)
                metadata = {"nfailed": len(failed_doc_id)}
                return [], metadata

        zip_file = zipfile.ZipFile(io.BytesIO(response.content))

        # content_string = zip_file.read("assembly.md").decode("utf-8")
        content_bytes = zip_file.read("assembly.md")
        server_info_json = zip_file.read("server_info.json").decode("utf-8")
        server_info_json_dict = json.loads(server_info_json)
        server_version = server_info_json_dict["server_version"]
        if not self.server_version_logged:
            logger.info(f"WDU server version: {server_version}")
            self.server_version_logged = True
        # server_info = server_info_json_dict[]
        # assembly_json_dict = json.loads(assembly_json)
        # num_pages = assembly_json_dict["metadata"]["num_pages"]

        # elapse_time = time.time() - start_time

        # num_tables = 0
        # num_doc_elements = 0
        success_doc_id.append(pdf_file_basename)

        # self.page_convert_gauge.set(elapse_time / num_pages)
        # self.doc_convert_gauge.set(elapse_time)
        # self.doc_counter.inc(1)
        # self.page_counter.inc(num_pages)

        # row_data = {
        #     "document": TransformUtils.get_file_basename(file_name),
        #     "contents": content_string,
        #     "num_pages": num_pages,
        #     # "num_tables": num_tables,
        #     # "num_doc_elements": num_doc_elements,
        #     # "document_id": TransformUtils.str_to_hash(content_string),
        #     "ext": ".md",
        #     "hash": TransformUtils.str_to_hash(content_string),
        #     "size": len(content_string),
        #     "date_acquired": datetime.now().isoformat(),
        #     "pdf_convert_time": elapse_time,
        # }
        # data.append(row_data)
        # number_of_rows += 1
        # table = pa.Table.from_pylist(data)
        metadata = {
            # "nrows": len(table),
            "nsuccess": len(success_doc_id),
        }
        # return [(TransformUtils.convert_arrow_to_binary(table=table), ".md")], metadata
        return [(content_bytes, ".md")], metadata


class WduPdf2MdTransformConfiguration(TransformConfiguration):
    """
    Provides support for configuring and using the associated Transform class include
    configuration with CLI args and combining of metadata.
    """

    def __init__(self):
        super().__init__(
            name=shortname,
            transform_class=WduPdf2MdTransform,
            # remove_from_metadata=[ingest_data_factory_key],
        )
        self.daf = None

    def add_input_params(self, parser: ArgumentParser) -> None:
        """
        Add Transform-specific arguments to the given parser.
        By convention a common prefix should be used for all mutator-specific CLI args
        (e.g, noop_, pii_, etc.)
        """
        parser.add_argument(
            "--wdu_rest_host",
            type=str,
            help="WDU REST API host name",
            default="main-service-multi.apps.fmaas-instructlab-01.fmaas.res.ibm.com",
            required=False,
        )
        parser.add_argument(
            "--wdu_rest_port",
            type=str,
            help="WDU REST API port number",
            required=False,
            default="80",
        )
        parser.add_argument(
            "--wdu_max_retries",
            type=int,
            help="WDU REST call max retries",
            required=False,
            default=3,
        )
        # # Create the DataAccessFactor to use CLI args
        # self.daf = DataAccessFactory(cli_prefix, False)
        # # Add the DataAccessFactory parameters to the transform's configuration parameters.
        # self.daf.add_input_params(parser)

    def apply_input_params(self, args: Namespace) -> bool:
        """
        Validate and apply the arguments that have been parsed
        :param args: user defined arguments.
        :return: True, if validate pass or False otherwise
        """
        self.params["wdu_rest_host"] = args.wdu_rest_host
        self.params["wdu_rest_port"] = args.wdu_rest_port
        self.params["wdu_max_retries"] = args.wdu_max_retries
        logger.info(f"Transform configuration {self.params}")
        return True
