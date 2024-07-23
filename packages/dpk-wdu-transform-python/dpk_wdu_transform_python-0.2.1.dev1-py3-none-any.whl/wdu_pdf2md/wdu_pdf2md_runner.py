import ast
import sys

from data_processing.runtime.pure_python import PythonTransformLauncher
from data_processing.utils import ParamsUtils
from wdu_pdf2md import WduPdf2MdTransformPythonConfiguration


def run_wdu_pdf2md_transformer(input_folder: str, output_folder: str):
    code_location = {"github": "github", "commit_hash": "12345", "path": "path"}

    local_conf = {
        "input_folder": input_folder,
        "output_folder": output_folder,
    }
    params = {
        "data_local_config": ParamsUtils.convert_to_ast(local_conf),
        "data_files_to_use": ast.literal_eval("['.pdf']"),
        "data_files_to_checkpoint": ast.literal_eval("['.md']"),
        # orchestrator
        "runtime_pipeline_id": "pipeline_id",
        "runtime_job_id": "job_id",
        "runtime_code_location": ParamsUtils.convert_to_ast(code_location),
    }

    sys.argv = ParamsUtils.dict_to_req(d=(params))
    # create launcher
    launcher = PythonTransformLauncher(WduPdf2MdTransformPythonConfiguration())
    # launch
    launcher.launch()
