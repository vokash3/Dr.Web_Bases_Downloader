# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 13:30:29 2022

@author: v.kashin
"""

import sys
import logging


class LoggingUtils(object):
    """
    Утилитарный Класс логирования.
    
    Содержит единственный static метод, возвращающий объект класса Logger
    
    """

    @staticmethod
    def get_logger(name, file='logfile.log', encoding='utf-8'):
        """
        Parameters
        ----------
        name : TYPE строка
            DESCRIPTION. Название файла скрипта(класса), в котором необходимо вести логирование
        file : TYPE, optional строка 
            DESCRIPTION. The default is 'logfile.log'.
        encoding : TYPE, optional
            DESCRIPTION. The default is 'utf-8'.

        Returns
        -------
        log : TYPE Logger
            DESCRIPTION.

        """
        log = logging.getLogger(name)
        log.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(asctime)s %(filename)s: %(levelname)-5s: %(message)s',
                                      datefmt='%Y-%m-%d %H:%M', )

        fh = logging.FileHandler(file, encoding=encoding)
        fh.setFormatter(formatter)
        log.addHandler(fh)

        sh = logging.StreamHandler(stream=sys.stdout)
        sh.setFormatter(formatter)
        log.addHandler(sh)

        return log
