#  Created by Kashin Vladimir Olegovich.
#
#  June 2022 AC.
#
# ПОСЛЕДНЕЕ ОБНОВЛЕНИЕ - 07 сентября 2022 г.
"""
Точка входа в программу ( main() )

Задаются основные переменные с путями к загрузчикам DrWeb

Создаются экземпляры классов для загрузки баз различных версий DrWeb ( + вызов их методов)

Все действия LOG'ируются в logfile.log, содержащийся в директории с данным файлом.
"""

import datetime
import time

from Utils.LoggingUtils import LoggingUtils as Log
from Utils.PathUtils import *
from downloaders.drweb_ess10_bases_download import DrWebESS10Downloader
from downloaders.drweb_ess11002_bases_download import DrWebESS11002Downloader
from downloaders.drweb_ess11_bases_download import DrWebESS11Downloader
from downloaders.drweb_linux_bases_creator import DrWebLinuxBasesCreator
from downloaders.drweb_ss_bases_download import DrWebSSDownloader

novelty_period = 7  # дней. Значение переменной МОЖНО ИЗМЕНЯТЬ. default - 7, так как служит для формирования баз с недельными изменениями (weekly)

today = datetime.date.today().strftime("%Y%m%d")  # Текущая дата
log = Log.get_logger(__file__)

directory = os.getcwd()  # получаем текущий рабочий каталог
log.info(directory + " - рабочий каталог!")

bases_directory = directory + "\\DrWeb_Bases"  # Директория загрузки актуальных БВС
weekly_bases_directory = directory + "\\DrWeb_Weekly_Bases"  # Директория загрузки недельных БВС

# Пути к загрузчикам DrWeb.
ess11dir = directory + '\\DrWeb_Downloaders\\drw110\\ess11\\'
ess11002dir = directory + '\\DrWeb_Downloaders\\drw110\\ess11002\\'
ess10dir = directory + '\\DrWeb_Downloaders\\drw900\\ess10\\'
ss115dir = directory + "\\DrWeb_Downloaders\\drw110\\ss115\\"
ss11dir = directory + "\\DrWeb_Downloaders\\drw110\\ss11\\"
ss10dir = directory + "\\DrWeb_Downloaders\\drw900\\ss10\\"
ss9dir = directory + "\\DrWeb_Downloaders\\drw700\\ss9\\"
key = directory + "\\key\\agent.key"

util_7zr_path = directory + "\\Utils\\bin\\7zr.exe"  # Путь к утилите из состава LZMA SDK для распаковки файлов .lzma в составе БВС
format_result_string = '\n{:<16} ======================> [{:>4}]'


def main():
    result_string: str = ""
    start_time = time.monotonic()
    log.info(
        "\n=========================================" + today + "====================================================\n")
    # Грубая проверка наличия файла лицензии (без проверки на валидность и актуальность)
    if not os.path.exists(key):
        log.error(" ОШИБКА: Отсутвует файл лицензии " + key)
        return 1
    # Очистка директорий от старых баз
    if not os.path.exists(bases_directory):
        log.info("Создание директории загрузки БВС " + bases_directory)
        os.mkdir(bases_directory)
    else:
        log.info("Очистка каталога " + bases_directory)
        PathUtils.clear_directory(bases_directory)  # Очистка директории с загруженными базами
    if not os.path.exists(weekly_bases_directory):
        log.info("Создание директории загрузки БВС с недельными изменениями " + weekly_bases_directory)
        os.mkdir(weekly_bases_directory)
    else:
        PathUtils.clear_directory(weekly_bases_directory)
        log.info("Очистка каталога " + bases_directory)

    # Поочерёдный запуск модулей загрузки БВС
    # ESS 11
    try:
        if DrWebESS11Downloader(bases_directory, ess11dir).download_bases() is None:
            raise Exception("Returned None!")
        result_string += format_result_string.format('DrWeb ESS 11', 'OK!')
    except Exception as err:
        log.error(err, exc_info=True)
        result_string += format_result_string.format('DrWeb ESS 11', 'FAIL')
    # ESS 11.00.2
    try:
        if DrWebESS11002Downloader(bases_directory,
                                   ess11002dir).download_bases() is None:  # Запуск загрузки баз DrWeb ESS 11.00.2
            raise Exception("Returned None!")
        result_string += format_result_string.format('DrWeb ESS 11.00.2', 'OK!')
    except Exception as err:
        log.error(err, exc_info=True)
        result_string += format_result_string.format('DrWeb ESS 11.00.2', 'FAIL')
    # ESS 10
    try:
        if DrWebESS10Downloader(bases_directory, ess10dir).download_bases() is None:  # Запуск загрузки баз DrWeb ESS 10
            raise Exception("Returned None!")
        result_string += format_result_string.format('DrWeb ESS 10', 'OK!')
    except Exception as err:
        log.error(err, exc_info=True)
        result_string += format_result_string.format('DrWeb ESS 10', 'FAIL')
    # SS 11.5
    try:
        if DrWebSSDownloader(bases_directory, weekly_bases_directory, ss115dir, "DRW_SS11.5",
                             "DRW_SS11.5_", novelty_period).download_bases() is None:
            raise Exception("Returned None!")
        result_string += format_result_string.format('DrWeb SS 11.5', 'OK!')
    except Exception as err:
        log.error(err, exc_info=True)
        result_string += format_result_string.format('DrWeb SS 11.5', 'FAIL')
    # SS 11
    try:
        if DrWebSSDownloader(bases_directory, weekly_bases_directory, ss11dir, "DRW_SS11",
                             "DRW_SS11_", novelty_period).download_bases() is None:
            raise Exception("Returned None!")
        result_string += format_result_string.format('DrWeb SS 11', 'OK!')
    except Exception as err:
        log.error(err, exc_info=True)
        result_string += format_result_string.format('DrWeb SS 11', 'FAIL')
    # For DSS (Linux 11)
    try:
        if DrWebLinuxBasesCreator(bases_directory, weekly_bases_directory, ss11dir, "DRW_Linux11",
                                  "DRW_Linux11_", util_7zr_path, novelty_period).create_linux_bases() is None:
            raise Exception("Returned None!")
        result_string += format_result_string.format('Linux 11', 'OK!')
    except Exception as err:
        log.error(err, exc_info=True)
        result_string += format_result_string.format('Linux 11', 'FAIL')
    # SS 10
    try:
        if DrWebSSDownloader(bases_directory, weekly_bases_directory, ss10dir, "DRW_SS10",
                             "DRW_SS10_", novelty_period).download_bases() is None:
            raise Exception("Returned None!")
        result_string += format_result_string.format('DrWeb SS 10', 'OK!')
    except Exception as err:
        log.error(err, exc_info=True)
        result_string += format_result_string.format('DrWeb SS 10', 'FAIL')
    # For DSS (Linux 10)
    try:
        if DrWebLinuxBasesCreator(bases_directory, weekly_bases_directory, ss10dir, "DRW_Linux10",
                                  "DRW_Linux10_", util_7zr_path, novelty_period).create_linux_bases() is None:
            raise Exception("Returned None!")
        result_string += format_result_string.format('Linux10', 'OK!')
    except Exception as err:
        log.error(err, exc_info=True)
        result_string += format_result_string.format('Linux10', 'FAIL')
    # SS 9
    try:
        if DrWebSSDownloader(bases_directory, weekly_bases_directory, ss9dir, "DRW_SS9",
                             "DRW_SS9_", novelty_period).download_bases() is None:
            raise Exception("Returned None!")
        result_string += format_result_string.format('DrWeb SS 9', 'OK!')
    except Exception as err:
        log.error(err, exc_info=True)
        result_string += format_result_string.format('DrWeb SS 9', 'FAIL')

    log.info(result_string)

    log.info("\nВРЕМЯ ВЫПОЛНЕНИЯ ПРОГРАММЫ:            " + time.strftime("%H:%M:%S", time.gmtime(time.monotonic() -
                                                                                                 start_time)) + "\n")

    log.info(
        "\n=============================================================================================\n")


if __name__ == '__main__':
    main()
