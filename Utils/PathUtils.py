# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 14:13:37 2022

@author: v.kashin
"""

#  Created by Kashin Vladimir Olegovich.
#
#  June 2022 AC.

import os
from Utils.LoggingUtils import *

log = LoggingUtils.get_logger(__file__)


class PathUtils(object):
    """
    Класс вспомогательных методов (типа удаления/очистки директорий, получения ссылок и т.п.)
    """

    @staticmethod
    def clear_directory(directory_path):
        """
        Очистка директории, переданной в кач-ве аргумента
        """
        for the_file in os.listdir(directory_path):
            file_path = os.path.join(directory_path, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
                # elif os.path.isdir(file_path): shutil.rmtree(file_path)
            except Exception as err:
                log.error(err, exc_info=True)

    @staticmethod
    def check_and_remove_existing_files(*files_path):
        """
        Очистка ранее загруженных БВС
        """
        for file in files_path:
            if os.path.exists(file):
                log.info("Обнаружены ранее загруженные файлы ... Производится удаление!")
                os.remove(file)
