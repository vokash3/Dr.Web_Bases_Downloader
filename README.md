# _Dr.Web Bases Downloader_
Модули для загрузки обновлений БВС Dr.Web

#  ✰✭ ЗБВС Доктора Веба ✭✰
## _Загрузчик баз вирусных сигнатур антивирусов __[Dr.Web](https://www.drweb.ru/)___

Проект загрузчика представляет собой набор созданных на python модулей, которые обращаются к официальным утилитам скачивания антивирусных баз Dr.Web в локальный репозиторий.
При использовании __ЗБВС Доктора Веба__ отпадает необходимость в нескольких дополнительных компьютерах, которые служат исключительно для получения баз вирусных сигнатур ДВ. Всё выполняется на одном устройстве!

___Разработка и тестирование проводились в среде, использующей программное обеспечение:___

- [Windows 7 Service Pack 1](https://support.microsoft.com/ru-ru/windows/%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%BD%D1%8B%D0%B5-%D1%82%D1%80%D0%B5%D0%B1%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F-%D0%B4%D0%BB%D1%8F-%D0%BE%D1%81-windows-7-df0900f2-3513-a851-13e7-0d50bc24e15f)
- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [JetBrains PyCharm Community Edition 2022.1.2](https://www.jetbrains.com/ru-ru/pycharm/download/other.html)
- [LZMA SDK](https://www.7-zip.org/sdk.html)
- Отдельные модули продуктов [Dr.Web](https://www.drweb.ru/)

#### Список загружаемых БВС:
        - Dr.Web Enterprise Security Suite 11.00.2 (ФСТЭК)
        - Dr.Web Enterprise Security Suite 11 (ФСТЭК)
        - Dr.Web Enterprise Security Suite 10 (ФСТЭК)
        - Dr.Web Security Space 11.5 (ФСТЭК)
        - Dr.Web Security Space 11
        - Dr.Web Security Space 10 (ФСТЭК)
        - Dr.Web Security Space 9
        - Dr.Web Desktop Security Suite (for Lunux) 11 
        - Dr.Web Desktop Security Suite (for Lunux) 10 (ФСТЭК)

##### Требования для успешного запуска и выполнения загрузчика:
- Стабильное интернет соединение
- Операционная система Windows 7 SP 1
- Python 3.8
- Свободное место на накопителе: 6-7 Гб
- __Актуальный ключевой файл [agent.key](https://download.geo.drweb.com/pub/drweb/officeshield/documentation/HTML/ru/index.html?dw_license_key_loading.htm).__
- (GIT)

__Также проведено успешное тестирование на Windows 11 (21H2) с Python 3.10__ 

## Структура проекта

##### ├──DrWeb_Downloaders
_Cодержит директории, где расположены исполняемые модули загрузки локальных репозиториев от DrWeb_

│   ├── __drw110__

│   ├──├────ess11002

│   ├──├────ess11

│   ├──├────ss115

│   ├──├────ss11

│   ├── __drw900__

│   ├──├────ess10

│   ├──├────ss10

│   ├── __drw700__

│   ├──├────ss9

│   ├──├──── ~~drw6~~ _(не используется в работе ЗБВС Доктора Веба)_

│   ├──  ~~drw500~~ _(не используется в работе ЗБВС Доктора Веба)_

 
##### ├──key 
__В директорию key НЕОБХОДИМО поместить актуальный ключевой файл agent.key!__
В противном случае ЗБВС Доктора Веба не произведёт загрузку баз.

│   ├──  agent.key _(ваш файл лицензии)_


##### ├──Utils
_Директория содержит созданные утилитарные python-классы для ведения логгирования проекта (LoggingUtils.py, общий лог-файл ведётся в корне проекта: logfile.log) и очистки директорий (PathUtils.py). В поддиректории bin помещена внешняя утилита 7zr.exe из состава LZMA SDK, которая позволяет распаковывать архивы .lzma формата._

│   ├── __bin__

│   ├──├────7zr.exe

│   ├──├────README.txt

│   ├── __LoggingUtils.py__ _(класс LoggingUtils)_

│   ├── __PathUtils.py__ _(класс PathUtils)_



##### ├──downloaders

_В директории размещены python-классы, содержащие основную логику формирования архивов с БВС. Принцип их работы и взаимодействия описан в разделе __"Принцип работы"__._

│   ├── __drweb_ess11_bases_download.py__ _(класс - родитель DrWebESS11Downloader для ESS загрузчиков)_

│   ├── __drweb_ess10_bases_download.py__ _(класс DrWebESS10Downloader, наследующий DrWebESS11Downloader)_

│   ├── __drweb_ess11002_bases_download.py__ _(класс DrWebESS11002Downloader, наследующий DrWebESS11Downloader)_

│   ├── __drweb_ss_bases_download.py__ _(класс DrWebSSDownloader)_

│   ├── __drweb_linux_bases_creator.py__ _(класс DrWebLinuxBasesCreator)_

##### ├──logfile.log
_Основной лог программы_
##### ├──start_drweb_update.py  (ЗАПУСК)
_Точка входа в программу. Скрипт с единственной функцией main(), в которой выполняется создание объектов классов загрузчиков из директории __downloaders__ и старт их логики. Создание объектов каждого класса обёрнуто в блок try-except._

## Технологии

- [Python 3.8](https://www.python.org/downloads/release/python-380/)
- [LZMA SDK](https://www.7-zip.org/sdk.html)
- [Batch (.bat)](https://en.wikipedia.org/wiki/Batch_file)
- Работа с файловой системой
- ООП :-)

## Установка и запуск

1) Создать копию этого репозитория в отдельной папке

```cmd
git clone https://github.com/vokash3/drweb_bases_updater
```

2) Приобрести лицензию и поместить ключевой файл agent.key в директорию __key__

3) Далее, выполнить start_drweb_update.py в корне проекта, используя python (желательно сразу с правами администратора из командной строки, чтобы исключить подтверждения запуска загрузчиков DrWeb)

```cmd
python3.8 start_drweb_update.py
```
4) _Дополнительно:
Если имеются ранее загруженные репозитории DrWeb Security Space (обычно скачиваются в папку repo загрузчиков), следует скопировать/переместить каталог repo в директории соответсвующих версий ЗБВС Доктора Веба (.../DrWeb_Downloaders/drw110/ss11 и т.п.).
Примерная структура __repo__:_
```
├──repo
│   ├──90
│   ├──certificate.xml
│   ├──repodb.xml
│   ├──script.lua.lzma
│   ├──versions.xml
├─────────────────────────
```
## Принцип работы

Запуск ___start_drweb_update.py___, в котором инициализируются основные переменные относительных путей к докторвебовским загрузчикам, утилите разархивации, создаётся объект логгирования, формирование текущей даты. 

В основной и единственной функции main() производится поочерёдное __создание объектов классов__ DrWebESS11Downloader--DrWebESS11002Downloader--DrWebESS10Downloader--DrWebSSDownloader--DrWebLinuxBasesCreator.
Запуск каждого модуля обёрнут __блоком try-except__
```python
... ... ...
try:
        if DrWebSSDownloader(bases_directory, weekly_bases_directory, ss115dir, "DRW_SS11.5","DRW_SS11.5_").download_bases() is None:
            raise Exception("Returned None!")
        result_string += format_result_string.format('DrWeb SS 11.5', 'OK!')
except Exception as err:
        log.error(err, exc_info=True)
        result_string += format_result_string.format('DrWeb SS 11.5', 'FAIL')
... ... ...
```
Если отсутсвует необходимость загрузки БВС какой-либо версий, то соответсвующий __блок__ следует закомментировать (#)

Все классы загрузчиков из __downloaders__ (* за исключением DrWebLinuxBasesCreator) вызывают в соответсвующих директориях скрипты _START.bat_, в которых описан запуск с параметрами утилит загрузки от Доктор Веб.
Далее, во всех классах реализован одинаковый сценарий:
+ Создание zip-архива с актуальными БВС (+ weekly архив, содержащий файлы не старее 7 дней (можно изменить в переменной novelty_period));
+ Формирование контрольной суммы (md5) архива(-ов);
+ Перемещение zip-архива и md5 в директорию __DrWeb_Bases__ (в __DrWeb_Weekly_Bases__ - для weekly). Директории создаются автоматически при самом первом запуске.

(*) Класс ___DrWebLinuxBasesCreator___ использует уже загруженный репозиторий актуальных баз в процессе выполнения метода ___DrWebSSDownloader.download_bases()___. Поэтому вызов ___DrWebLinuxBasesCreator.create_linux_bases()___ всегда следует после ___DrWebSSDownloader.download_bases()___ для соответсвующих версий (пример из ___start_drweb_update.py___ ниже).
```python
... ... ...
try:
    if DrWebSSDownloader(bases_directory, weekly_bases_directory, ss11dir, "DRW_SS11", "DRW_SS11_").download_bases() is None:
        raise Exception("Returned None!")
    result_string += format_result_string.format('DrWeb SS 11', 'OK!')
except Exception as err:
    log.error(err, exc_info=True)
    result_string += format_result_string.format('DrWeb SS 11', 'FAIL')

try:
    if DrWebLinuxBasesCreator(bases_directory, weekly_bases_directory, ss11dir, "DRW_Linux11", "DRW_Linux11_", util_7zr_path).create_linux_bases() is None:
        raise Exception("Returned None!")
    result_string += format_result_string.format('Linux 11', 'OK!')
except Exception as err:
    log.error(err, exc_info=True)
    result_string += format_result_string.format('Linux 11', 'FAIL')
... ... ...
```
__Результат__ выполнения __ЗБВС Доктор Веба__ можно посмотреть в конце лога ___logfile.log___
``` logfile.log
2022-07-14 16:05 start_drweb_update.py: INFO : 
DrWeb ESS 11     ======================> [ OK!]
DrWeb ESS 11.00.2 ======================> [ OK!]
DrWeb ESS 10     ======================> [ OK!]
DrWeb SS 11.5    ======================> [ OK!]
DrWeb SS 11      ======================> [ OK!]
Linux 11         ======================> [ OK!]
DrWeb SS 10      ======================> [ OK!]
Linux10          ======================> [ OK!]
DrWeb SS 9       ======================> [ OK!]
2022-07-14 16:05 start_drweb_update.py: INFO : 
ВРЕМЯ ВЫПОЛНЕНИЯ ПРОГРАММЫ:            00:19:57
```

## Предупреждения
- Приблизительное время выполнения ЗБВС Доктора Веба - 1.5 часа при первоначальном запуске без имеющихся repo.
- Загрузчики DrWeb SS скачивают актуальные БВС в папки repo, которые "накапливают" последние обновления. Их удалять не рекомендуется, если требуется корректное формирование weekly-архивов. При уже имеющихся repo соответсвующих версий рекомендуется их поместить в директории загрузчиков (ss11, ss10 и т.д.)
- При старте start_drweb_update.py без прав администратора необходимо подтвержать поочерёдный запуск загрузчиков ESS. В случае длительного отсутствия подтверждения от пользователя базы ESS не будут загружены (ESS [FAIL]) 
- В случае обнаружения [FAIL] следует проверить ___logfile.log___, а также логи загрузчиков (drwreploader.log/dwupdater.log) из директории __DrWeb_Downloaders__ и устранить обнаруженные проблемы.
- Каждый запуск ___start_drweb_update.py___ создаёт/очищает от старых загрузок директории __DrWeb_Bases__ и __DrWeb_Weekly_Bases__ перед выполнением основной логики
- Weekly-архивы после первоначального запуска будут иметь большой объём (по содержанию не отличаются от обычных архивов с БВС), так как все загружаемые файлы на момент первоначальной загрузки не старее 7-ми дней (или указанного периода в переменной novelty_period). Внутри директорий модулей загрузки (ss11, ss10 и т.п.) загрузчиком DrWeb создаётся каталог repo с базами. Каждое последующее обновление скачивает только актуальные/новые файлы с серверов DrWeb. 
Таким образом, спустя некоторый период времени repo будет содержать как новые файлы сигнатур, так и файлы без изменений, которые в weekly архивы уже не попадают.
