# WDU_PDF2MD Annotation
Please see the set of
[transform project conventions](../../README.md)
for details on general project conventions, transform configuration,
testing and IDE set up.

## Summary 
The `wdu_pdf2md` `transform` takes an input folder containing a collection of `.pdf` files, extracts the markdown (MD) 
text of a PDF file and creates a parquet file for the PDF file and write them in the output folder.
The MD is stored on the column `contents`. The conversion of a PDF file to its MD is done via sending an HTTP
request to the `REST` endpoint of a Watson Document Understanding (`WDU`) server. The WDU REST endpoint is specified 
with two command-line arguments: the host name via `--wdu_rest_host` and the port number `--wdu_rest_port`. The HTTP
request can be retried for `--wdu_max_retries` times, under some conditions. We assume
that there is a `WDU` server up and running and this `wdu_pdf2md` transform can send the request for PDF extraction 
to the REST endpoint of the WDU server.

## Running
You can run the [wdu_pdf2md_local_python](src/wdu_pdf2md/wdu_pdf2md_local_python.py) to
transform PDF to MD in the [input](test-data/input) 
to the [output](output) directory. This output directory will contain both the transformed (extracted)
parquet files `jsonschema.parquet`, `pytorch_2.parquet`, `test_1.parquet` and the `metadata.json` file. 
<pre>
% cd python/src
% python3 wdu_pdf2md_local_python.py
15:07:03 INFO - Transform configuration {'wdu_rest_host': 'main-service-multi.apps.fmaas-instructlab-01.fmaas.res.ibm.com', 'wdu_rest_port': '80', 'wdu_max_retries': 3}
15:07:03 INFO - pipeline id pipeline_id
15:07:03 INFO - job details {'job category': 'preprocessing', 'job name': 'wdu_pdf2md', 'job type': 'pure python', 'job id': 'job_id'}
15:07:03 INFO - code location {'github': 'github', 'commit_hash': '12345', 'path': 'path'}
15:07:03 INFO - data factory data_ is using local data access: input_folder - /Users/kun-lungwu-m1/GUF_dev_klwu/dev_wdu/data-prep-kit-inner/transforms/universal/wdu_pdf2md/python/test-data/input output_folder - /Users/kun-lungwu-m1/GUF_dev_klwu/dev_wdu/data-prep-kit-inner/transforms/universal/wdu_pdf2md/python/output
15:07:03 INFO - data factory data_ max_files -1, n_sample -1
15:07:03 INFO - data factory data_ Not using data sets, checkpointing False, max files -1, random samples -1, files to use ['.pdf'], files to checkpoint ['.parquet']
15:07:03 INFO - orchestrator wdu_pdf2md started at 2024-07-08 15:07:03
15:07:03 INFO - Number of files is 3, source profile {'max_file_size': 0.8499183654785156, 'min_file_size': 0.010259628295898438, 'total_file_size': 1.351797103881836}
15:07:23 INFO - response status: 200
15:07:23 INFO - Completed 1 files (33.333333333333336%) in 0.32982168197631834 min
15:09:56 INFO - response status: 200
15:09:56 INFO - Completed 2 files (66.66666666666667%) in 2.8846205989519755 min
15:09:59 INFO - response status: 200
15:09:59 INFO - Completed 3 files (100.0%) in 2.9272643327713013 min
15:09:59 INFO - done flushing in 3.981590270996094e-05 sec
15:09:59 INFO - Completed execution in 2.9272976994514464 min, execution result 0
</pre>



