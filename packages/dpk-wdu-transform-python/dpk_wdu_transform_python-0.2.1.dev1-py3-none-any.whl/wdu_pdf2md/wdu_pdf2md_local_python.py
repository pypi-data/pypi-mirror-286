import ast
import os
import sys

from data_processing.runtime.pure_python import PythonTransformLauncher
from data_processing.utils import ParamsUtils
from wdu_pdf2md import WduPdf2MdTransformPythonConfiguration

# create parameters

input_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../test-data/input"))
output_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), "../output"))
local_conf = {
    "input_folder": input_folder,
    "output_folder": output_folder,
}
# worker_options = {"num_cpus": 0.8}
code_location = {"github": "github", "commit_hash": "12345", "path": "path"}
# ingest_config = {
#     supported_langs_file_cli_key: supported_languages_file,
#     detect_programming_lang_cli_key: True,
#     # snapshot_key: "github",
#     # domain_key: "code",
# }

params = {
    # Data access. Only required parameters are specified
    "data_local_config": ParamsUtils.convert_to_ast(local_conf),
    "data_files_to_use": ast.literal_eval("['.pdf', '.PDF']"),
    "data_files_to_checkpoint": ast.literal_eval("['.md']"),
    # orchestrator
    "runtime_pipeline_id": "pipeline_id",
    "runtime_job_id": "job_id",
    "runtime_code_location": ParamsUtils.convert_to_ast(code_location),
}

if __name__ == "__main__":
    sys.argv = ParamsUtils.dict_to_req(d=(params))
    # create launcher
    launcher = PythonTransformLauncher(WduPdf2MdTransformPythonConfiguration())
    # launch
    launcher.launch()
