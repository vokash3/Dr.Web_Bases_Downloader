#  Created by Kashin Vladimir Olegovich.
#
#  June 2022 AC.

import datetime
import hashlib
import lzma
import os
import shutil
import zipfile

from Utils.LoggingUtils import LoggingUtils as Log
from Utils.PathUtils import *

today = datetime.date.today().strftime("%Y%m%d")

"""
Класс формирования БВС для Linux версий DrWeb.
Использет уже загруженные БВС для версий SS классом DrWebSSDownloader

"""


class DrWebLinuxBasesCreator(object):
    log = Log.get_logger(__file__)

    def __init__(self, bases_directory, weekly_bases_directory, workdir_path, drweb_version: str,
                 drweb_archive_prefix: str, util_7zr_path, novelty_period: int = 7):
        self.lastweek_date = (datetime.date.today() - datetime.timedelta(novelty_period)).strftime("%Y%m%d")
        self.bases_directory = bases_directory
        self.weekly_bases_directory = weekly_bases_directory
        self.workdir_path = workdir_path
        self.drweb_version = drweb_version
        self.drweb_archive_prefix = drweb_archive_prefix
        self.drweb_bases_repo_path = os.path.join(self.workdir_path + "\\repo\\90\\av-engine\\9\\common")
        self.drweb_temp_lzma_dirpath = os.path.join(self.workdir_path + "temp_lzma")
        self.archive_name = self.drweb_archive_prefix + today + '.zip'
        self.archive_weekly_name = self.drweb_archive_prefix + "weekly_" + self.lastweek_date + "-" + today + ".zip"
        self.util_7zr = util_7zr_path
        self.novelty_period = novelty_period

    def create_linux_bases(self):
        """
                1) Формирование zip-архивов и хэш-кодов MD5 БВС из repo, загруженными ранее в DrWebSSDownloader
                2) Перемещение архивов и md5 в DrWeb_Bases/DrWeb_Weekly_Bases
        """
        os.chdir(self.workdir_path)
        log.info("Рабочий каталог изменён на " + self.workdir_path)
        md5_file = self.archive_name.split('.zip')[0] + ".md5"
        md5_weekly_file = self.archive_weekly_name.split('.zip')[0] + ".md5"
        path_arch = os.path.abspath(self.archive_name)
        path_weekly_arch = os.path.abspath(self.archive_weekly_name)
        path_md5 = os.path.abspath(md5_file)
        path_weekly_md5 = os.path.abspath(md5_weekly_file)

        PathUtils.check_and_remove_existing_files(path_arch, path_weekly_arch, path_md5,
                                                  path_weekly_md5)  # удаляем существующие архивы и хэши, если имеются
        # Порядок создания AllBases (1) и Weekly (2) важен!
        try:
            if self.create_zip(self.drweb_bases_repo_path, self.archive_name) is None:  # (1)
                return None
        except Exception as err:
            log.error("Ошибка создания " + self.archive_name)
            log.error(err, exc_info=True)
        try:
            if self.create_zip(self.drweb_temp_lzma_dirpath, self.archive_weekly_name) is None:  # (2)
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
            log.info("Выполняется создание архива (с промежуточной распаковкой .lzma файлов)" + archive_name)
            z = zipfile.ZipFile(archive_name, 'w')  # Создание нового архива

            if archive_name.__contains__("weekly"):  # (2)
                for root, dirs, files in os.walk(dir_path):  # Список всех файлов и папок в директории folder
                    for file in files:
                        if (datetime.datetime.today() - datetime.datetime.fromtimestamp(
                                int(os.stat(os.path.join(root, file)).st_mtime))) <= datetime.timedelta(
                            self.novelty_period):
                            z.write(os.path.join(root, file), "\\bases\\" + file)
                self.clear_temp_lzma_dir()  # Очистка директории с временными файлами из .lzma
            else:  # (1)
                for root, dirs, files in os.walk(dir_path):  # Список всех файлов и папок в директории folder
                    for file in files:
                        if os.path.splitext(file)[1] == ".lzma":
                            vdb_file = self.decompress_lzma_and_return_pathfile(root, file)
                            z.write(vdb_file, "\\bases\\" + os.path.basename(vdb_file))
                        else:
                            z.write(os.path.join(root, file), "\\bases\\" + file)
            z.close()
            log.info(archive_name + " успешно создан!")
            return True
        else:
            log.error(
                "Отсутствует директория repo (и/или temp_lzma для weekly). Прекращение работы модуля загрузки " + self.drweb_version)
            return None

    # Возвращает полный путь к распакованному файлу .vdb
    def decompress_lzma_and_return_pathfile(self, root, file):
        temp_dir: str = "temp_lzma"
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)
        os.system(self.util_7zr + " -y " + "-o" + temp_dir + " x " + root + "\\" + file)
        vdb_filename = os.path.splitext(file)[0]  # Убираем расширение из имени файла
        vdb_file_path = temp_dir + "\\" + vdb_filename
        return vdb_file_path

    def clear_temp_lzma_dir(self):
        PathUtils.clear_directory(self.drweb_temp_lzma_dirpath)
        log.info("Директория временных файлов " + self.drweb_temp_lzma_dirpath + " очищена!")
