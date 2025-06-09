# photo2dcm_sender

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

# Copyright (c) 2025 Pavel Honz

# pavel.honz@gmail.com

# this project aims to transfer photos from a hot folder to dicom and send them to the pacs server
# for image dicomization it is possible to use the worklist

# v 1.1
# - Fix: Swapped first and last name in manual input (functions.py)
# - Fix: In default config file: comment on the same line as a value was being interpreted as part of the value.(dats.py)
# orrect configuration. (functions.py)
# - Added: Info message when sending data to PACS fails. (functions.py)
# - Added: Info message when querying the worklist fails. (functions.py)
# - Fix: Program icon now loads correctly after building the .exe file. (mainwindow.py, gui.py)

# v1.1 repair
# - Fix: swapped row in functions.py, worklist dont show values in frame

# 25.04.2025

# used commands:
# pyinstaller --icon=src\img\icon-16.png  --noconsole .\photo2dcm_sender.py
# latest:
# pyinstaller --onefile --noconsole --icon=src\img\icon-16.png --add-data "src/img:img" photo2dcm_sender.py

import os
import logging
from logging import config
from datetime import datetime

if not os.path.exists("logs"):
    os.makedirs("logs")

from src.dats import load_config

configLogger = load_config()
programLogLevel = configLogger["LOG_LEVEL"]["programRun"].upper()
mwlLogLevel = configLogger["LOG_LEVEL"]["dicomMwl"].upper()
consoleLevel = configLogger["LOG_LEVEL"]["console"].upper()
logFileName = f'logs/{datetime.now().strftime("%y%m")}.log'


log_config = {
    "version": 1,
    "root": {"handlers": ["console", "file", "pynetFile"], "level": "DEBUG"},
    "handlers": {
        "console": {
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "level": consoleLevel,
        },
        "file": {
            "formatter": "standard",
            "class": "logging.FileHandler",
            "level": programLogLevel,
            "filename": logFileName,
        },
        "pynetFile": {
            "formatter": "standard",
            "class": "logging.FileHandler",
            "level": mwlLogLevel,
            "filename": logFileName,
        },
    },
    "formatters": {
        "extended": {
            "format": "%(asctime)s - [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s",
            "datefmt": "%d-%m-%Y %H:%M:%S",
        },
        "standard": {
            "format": "%(asctime)s - %(levelname)s - %(name)-15s\t -  %(module)s\t| %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
}

config.dictConfig(log_config)

################ Logger #################
logger = logging.getLogger(__name__)
# module logs message, so importing it only after logging has been configured

############# Program start #############
from src import mainwindow

if __name__ == "__main__":
    logger.info("Program started")

    # if not os.path.isfile(cons.CONFIG_FILE) :
    #     create_default_config_file()
    #     print("Default config was made")

    app = mainwindow.RunGui()
    app.MainLoop()  # Spustí hlavní cyklus
    logger.info("Program ended correctly")
