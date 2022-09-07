#  Created by Kashin Vladimir Olegovich.
#
#  June 2022 AC.

from Utils.LoggingUtils import LoggingUtils as Log
from downloaders.drweb_ess11_bases_download import DrWebESS11Downloader


class DrWebESS10Downloader(DrWebESS11Downloader):

    def __init__(self, bases_directory, workdir_path):
        super().__init__(bases_directory, workdir_path)
        DrWebESS11Downloader.log = Log.get_logger(__file__)
        DrWebESS11Downloader.drweb_version = "DrWeb ESS 10"
        DrWebESS11Downloader.drweb_logfile_name = "drwreploader.log"
        DrWebESS11Downloader.drweb_archive_prefix = "DRW_ESS10_"
        DrWebESS11Downloader.drweb_downloaded_repo_name = "repository.zip"
        DrWebESS11Downloader.drweb_logfile_lastline_success = "Exit code: 0 (Success)"
        DrWebESS11Downloader.bat_starter_filename = "START.bat"
