#  Created by Kashin Vladimir Olegovich.
#
#  June 2022 AC.

import datetime
import hashlib
import os.path
import shutil
import subprocess
import zipfile
import lzma

from Utils.LoggingUtils import LoggingUtils as Log
from Utils.PathUtils import *

today = datetime.date.today().strftime("%Y%m%d")

"""
Класс загрузки БВС для всех версий DrWeb SS.

Конструктор принимает путь к рабочей директории,
тем самым загружает базы определённой версии
"""


class DrWebSSDownloader(object):
    drweb_logfile_name = "dwupdater.log"
    drweb_downloaded_repo_name = "repo"
    drweb_logfile_lastline_success = "Exit code = 0"
    bat_starter_filename = "START.bat"
    log = Log.get_logger(__file__)

    def __init__(self, bases_directory, weekly_bases_directory, workdir_path, drweb_version: str,
                 drweb_archive_prefix: str, novelty_period: int = 7):
        self.lastweek_date = (datetime.date.today() - datetime.timedelta(novelty_period)).strftime("%Y%m%d")
        self.bases_directory = bases_directory
        self.workdir_path = workdir_path
        self.drweb_version = drweb_version
        self.drweb_archive_prefix = drweb_archive_prefix
        self.weekly_bases_directory = weekly_bases_directory

        self.path_repo_downloaded = os.path.join(self.workdir_path, self.drweb_downloaded_repo_name)
        self.archive_name = self.drweb_archive_prefix + today + '.zip'
        self.archive_weekly_name = self.drweb_archive_prefix + "weekly_" + self.lastweek_date + "-" + today + ".zip"
        self.novelty_period = novelty_period

    def download_bases(self):
        """
        1) Загрузка актуальных баз (START.bat -> drwupsrv.exe) в repo
        2) Формирование zip-архивов и хэш-кодов MD5
        3) Перемещение архивов и md5 в DrWeb_Bases/DrWeb_Weekly_Bases
        """
        os.chdir(self.workdir_path)
        log.info("Рабочий каталог изменён на " + self.workdir_path)
        log.debug("Запуск загрузчика " + self.drweb_version + " ... Ожидание!")
        subprocess.call(self.bat_starter_filename)  # эта функция дожидается окончания выполнения скрипта

        # Отключена проверка записей лога, из-за отсутствия единообразного формирования для версий DrWeb SS
        # if not self.check_log():
        #     log.error(self.drweb_version + " STOP DOWNLOAD!")
        #     return None

        md5_file = self.archive_name.split('.zip')[0] + ".md5"
        md5_weekly_file = self.archive_weekly_name.split('.zip')[0] + ".md5"
        path_arch = os.path.abspath(self.archive_name)
        path_weekly_arch = os.path.abspath(self.archive_weekly_name)
        path_md5 = os.path.abspath(md5_file)
        path_weekly_md5 = os.path.abspath(md5_weekly_file)

        PathUtils.check_and_remove_existing_files(path_arch, path_weekly_arch, path_md5,
                                                  path_weekly_md5)  # удаляем существующие архивы и хэши, если имеются

        try:
            if self.create_zip(self.drweb_downloaded_repo_name, self.archive_name) is None:
                return None
        except Exception as err:
            log.error("Ошибка создания " + self.archive_name)
            log.error(err, exc_info=True)
        try:
            if self.create_zip(self.drweb_downloaded_repo_name, self.archive_weekly_name) is None:
                return None
        except Exception as err:
            log.error("Ошибка создания " + self.archive_weekly_name)
            log.error(err, exc_info=True)
        try:
            hashsum_file = open(md5_file, "w+")
            hashsum_file.write(hashlib.md5(open(self.archive_name, 'rb').read()).hexdigest() + " *" + self.archive_name)
            hashsum_file.close()
            log.info("Получена MD5 хэш-сумма архива БВС DrWeb " + self.drweb_version)
            hashsum_weekly_file = open(md5_weekly_file, "w+")
            hashsum_weekly_file.write(
                hashlib.md5(open(self.archive_weekly_name, 'rb').read()).hexdigest() + " *" + self.archive_weekly_name)
            hashsum_weekly_file.close()
            log.info("Получена MD5 хэш-сумма weekly архива БВС DrWeb " + self.drweb_version)
        except Exception as err:
            log.error("ОШИБКА подсчёта хэш-суммы архива(-ов)")
            log.error(err, exc_info=True)
        try:
            shutil.move(self.archive_name, os.path.join(self.bases_directory))
            shutil.move(md5_file, os.path.join(self.bases_directory))
            log.info(self.drweb_version + " БВС и MD5 успешно перемещены в директорию " + self.bases_directory)
        except Exception as err:
            log.error(
                "ОШИБКА перемещения " + self.drweb_version + " БВС и/или MD5 в директорию " + self.bases_directory + ": \n")
            log.error(err, exc_info=True)
        try:
            shutil.move(self.archive_weekly_name, os.path.join(self.weekly_bases_directory))
            shutil.move(md5_weekly_file, os.path.join(self.weekly_bases_directory))
            log.info(
                self.drweb_version + " БВС и MD5 (weekly) успешно перемещены в директорию " + self.weekly_bases_directory)
        except Exception as err:
            log.error(
                "ОШИБКА перемещения " + self.drweb_version + " БВС и/или MD5 (weekly) в директорию " + self.weekly_bases_directory + ": \n")
            log.error(err, exc_info=True)
            return None
        return True

    def create_zip(self, dir_path, archive_name: str):
        if os.path.exists(dir_path):
            log.info("Выполняется создание архива " + archive_name)
            z = zipfile.ZipFile(archive_name, 'w')  # Создание нового архива
            for root, dirs, files in os.walk(dir_path):  # Список всех файлов и папок в директории folder
                for file in files:
                    if archive_name.__contains__(
                            "weekly"):  # Разделение формирования на случай, если отпадёт необходимость формирования недельных баз
                        if (datetime.datetime.today() - datetime.datetime.fromtimestamp(
                                int(os.stat(os.path.join(root, file)).st_mtime))) <= datetime.timedelta(
                            self.novelty_period):
                            z.write(os.path.join(root, file))
                    else:
                        z.write(os.path.join(root, file))
            z.close()
            log.info(archive_name + " успешно создан!")
            return True
        else:
            log.error("Отсутствует директория repo. Прекращение работы модуля загрузки " + self.drweb_version)
            return None
