#  Created by Kashin Vladimir Olegovich.
#
#  June 2022 AC.

import subprocess
import datetime
import hashlib
import shutil

from Utils.LoggingUtils import LoggingUtils as Log
from Utils.PathUtils import *

today = datetime.date.today().strftime("%Y%m%d")

"""
Класс загрузки БВС для DrWeb ESS 11.

Является родителем для классов загрузки других версий ESS,
которые переопределяют поля родителя

"""


class DrWebESS11Downloader(object):
    drweb_version = "DrWeb ESS 11"
    drweb_logfile_name = "drwreploader.log"
    drweb_archive_prefix = "DRW_ESS11_"
    drweb_downloaded_repo_name = "repository.zip"
    drweb_logfile_lastline_success = "Exit code: 0 (Success)"
    bat_starter_filename = "START.bat"
    log = Log.get_logger(__file__)

    def __init__(self, bases_directory, workdir_path):
        self.bases_directory = bases_directory
        self.workdir_path = workdir_path

    def download_bases(self):
        os.chdir(self.workdir_path)
        log.info("Рабочий каталог изменён на " + self.workdir_path)
        log.debug("Запуск загрузчика " + self.drweb_version + " ... Ожидание!")
        subprocess.call(self.bat_starter_filename)  # эта функция дожидается окончания выполнения скрипта

        if not self.check_log():
            log.error(self.drweb_version + " STOP DOWNLOAD!")
            return None

        archive_name = self.drweb_archive_prefix + today + '.zip'
        md5_file = archive_name.split('.zip')[0] + ".md5"

        path_arch = os.path.join(os.path.abspath(os.path.dirname(__file__)), archive_name)
        path_md5 = os.path.join(os.path.abspath(os.path.dirname(__file__)), md5_file)

        PathUtils.check_and_remove_existing_files(path_arch, path_md5)

        os.rename(self.drweb_downloaded_repo_name, archive_name)
        try:
            hashsum_file = open(md5_file, "w+")
            hashsum_file.write(hashlib.md5(open(archive_name, 'rb').read()).hexdigest() + " *" + archive_name)
            hashsum_file.close()
            log.info("Получена MD5 хэш-сумма архива БВС DrWeb " + self.drweb_version)
        except Exception as err:
            log.error("ОШИБКА подсчёта хэш-суммы архива")
            log.error(err, exc_info=True)

        try:
            shutil.move(archive_name, os.path.join(self.bases_directory))
            shutil.move(md5_file, os.path.join(self.bases_directory))
            log.info(self.drweb_version + " БВС и MD5 успешно перемещены в директорию " + self.bases_directory)
        except Exception as err:
            log.error(
                "ОШИБКА перемещения " + self.drweb_version + " БВС и/или MD5 в директорию " + self.bases_directory + ": \n")
            log.error(err, exc_info=True)
            return None
        return True

    def check_log(self):
        try:
            f_read = open(self.drweb_logfile_name, "r")  # открываем лог
            last_line = f_read.readlines()[-1]  # читаем последнюю строку
            if last_line.find(self.drweb_logfile_lastline_success) == -1:
                log.error(
                    'ОШИБКА загрузки БВС ' + self.drweb_version + '. См. лог ' + self.workdir_path + self.drweb_logfile_name)
                return False
            else:
                log.info("БВС " + self.drweb_version + " успешно загружены!")
                return True
        except Exception as err:
            log.error(err, exc_info=True)
