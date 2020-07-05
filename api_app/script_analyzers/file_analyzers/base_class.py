import logging
import time

from api_app.script_analyzers import general
from api_app.script_analyzers.classes import BaseAnalyzerMixin


logger = logging.getLogger(__name__)


class FileAnalyzer(BaseAnalyzerMixin):
    """
    Abstract class for File Analyzers.
    Inherit from this branch when defining a file analyzer.
    Need to overrwrite `set_config(self, additional_config_params)`
     and `run(self)` functions.
    """

    md5: str
    filepath: str
    filename: str

    def __init__(
        self, analyzer_name, job_id, fpath, fname, md5, additional_config_params
    ):
        super().__init__(analyzer_name, job_id, additional_config_params)
        self.md5 = md5
        self.filepath = fpath
        self.filename = fname

    def before_run(self):
        logger.info(f"started analyzer: {self.analyzer_name}, job_id: {self.job_id}")
        self.report = general.get_basic_report_template(self.analyzer_name)

    def after_run(self):
        # add process time
        self.report["process_time"] = time.time() - self.report["started_time"]
        general.set_report_and_cleanup(self.job_id, self.report)

        logger.info(
            f"ended analyzer: {self.analyzer_name}, job_id: {self.job_id},"
            f"md5: {self.md5} ,filename: {self.filename}"
        )
