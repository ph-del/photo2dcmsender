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

###########################################################################

#default configuration and texts in czech and english language

import logging
logger = logging.getLogger(__name__)
import os
import configparser

#Load configure
def load_config():
    config = configparser.ConfigParser()
    configPath = os.path.join(os.getcwd(), "config.ini")
    
    if os.path.exists(configPath):  # Zkontrolujte, zda soubor existuje
        try:
            with open(configPath, 'r', encoding='utf-8') as file:  # Nastavte správné kódování
                config.read_file(file)
        except UnicodeDecodeError as e:
            raise Exception(f"Chyba dekódování souboru {configPath}: {e}")
        except Exception as e:
            raise Exception(f"Obecná chyba při čtení souboru {configPath}: {e}")
    else:
        with open(configPath, "w", encoding="utf-8") as f:
            f.write(default_config)
        logger.info('Default config file was created.')
        return load_config()  # Znovu načte nově vytvořený konfigurační soubor
    return config


#Load translation
def load_text(key):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.getcwd(), "config.ini"))
    lang = config["LANGUAGE"]["language"]
    return texts[key][lang]


## Translations
texts = {
    "btnClear": {"en": "Clear", "cz": "Vyčistit"},
    "btnDefaultFiltres": {"en": "Default", "cz": "Výchozí"},
    "btnLastMonth": {"en": "Last month", "cz": "Minulý měsíc"},
    "btnLastWeek": {"en": "Last week", "cz": "Minulý týden"},
    "btnManualInput": {"en": "Manual input", "cz": "Zadat ručně"},
    "btnSaveInputData": {"en": "Save", "cz": "Uložit"},
    "btnSearch": {"en": "Search", "cz": "Vyhledat"},
    "btnSend": {"en": "Send", "cz": "Odeslat"},
    "btnToday": {"en": "Today", "cz": "Dnes"},

    "stAbout": {"en": "About program", "cz": "O programu"},
    
    "txAccessionNumber": {"en": "Accession number", "cz": "Číslo žádanky"},
    "txEnteredStudy": {"en": "Entered study values", "cz": "Zadané hodnoty studie"}, 
    "txFilesToUpload": {"en": "Files to upload", "cz": "Soubory k odeslání"},
    "txFilters": {"en": "Filters", "cz": "Filtry"},
    "txFirstName": {"en": "First name", "cz": "Křestní jméno"},
    "txLastName": {"en": "Last name", "cz": "Příjmení"},
    "txNoFilesLoaded": {"en": "No supported files not founded", "cz": "Žádné podporované soubory nebyly nalezeny"},
    "txPatientId": {"en": "Patient ID", "cz": "Rodné číslo"},
    "txPatientName": {"en": "Patient name", "cz": "Jméno pacienta"},
    "txPreview": {"en": "Preview", "cz": "Náhled"},
    "txSending": {"en": "Sending", "cz": "Odesílání"},
    "txSpinDateFrom": {"en": "Date from", "cz": "Datum od"}, 
    "txSpinDateTo": {"en": "Date to", "cz": "Datum do"}, 
    "txStudyUid": {"en": "Study UID", "cz": "Study UID"},
    "txWorklist": {"en": "Worklist", "cz": "Worklist"},

    "colAccessionNumber" :{"en": "Accession number", "cz": "Číslo žádanky"},
    "colBirthDate" :{"en": "Birth date", "cz": "Datum narození"},
    "colPatientId" :{"en": "Patient ID", "cz": "Rodné číslo"},
    "colPatientName" :{"en": "Patient name", "cz": "Jméno pacienta"},
    "colReqPhys" :{"en": "Requesting", "cz": "Žádatel"},
    "colStudyDate" :{"en": "Study date", "cz": "Datum studie"},
    "colStudyUid" :{"en": "Study UID", "cz": "Study UID"},

    "titleManualInput" :{"en": "Manual Input of Patient Info", "cz": "Ruční zadání informací o pacientovi"},
    "infoDialog":{"en":"Information - Data was sended", "cz" : "Informace - Data odeslána"},
    "infoAboutProgram" : {"en": 
                        "Photo2DcmSender v1.0\n\n" \
"This program is free software: you can redistribute it and/or modify\n" \
"it under the terms of the GNU General Public License as published by\n" \
"the Free Software Foundation, either version 3 of the License, or\n" \
"(at your option) any later version.\n" \
"\n" \
"This program is distributed in the hope that it will be useful,\n" \
"but WITHOUT ANY WARRANTY; without even the implied warranty of\n" \
"MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n" \
"GNU General Public License for more details.\n" \
"\n" \
"You should have received a copy of the GNU General Public License\n" \
"along with this program. If not, see <https://www.gnu.org/licenses/>\n\n" \
"Source code:\n" \
"https://github.com/ph-del/photo2dcmsender\n\n" \
"pavel.honz@gmail.com\n\n" \
"Copyright (c) 2025 Pavel Honz",
                          "cz": "Photo2DcmSender v1.0\n\n" \
"Tento program je svobodný software: můžete jej šířit a/nebo upravovat\n" \
"podle podmínek GNU General Public License, jak ji zveřejnila\n" \
"Free Software Foundation, buď verze 3 této licence, nebo\n" \
"(podle vašeho výběru) jakákoli pozdější verze.\n" \
"\n" \
"Tento program je distribuován v naději, že bude užitečný,\n" \
"ale BEZ JAKÉKOLI ZÁRUKY; dokonce i bez předpokládané záruky PRODEJNOSTI nebo VHODNOSTI PRO KONKRÉTNÍ ÚČEL. Viz\n" \
"GNU General Public License pro další podrobnosti.\n" \
"\n" \
"Byli byste měli obdržet kopii GNU General Public License\n" \
"spolu s tímto programem. Pokud ne, podívejte se na <https://www.gnu.org/licenses/>\n\n" \
"Zdrojový kód:\n" \
"https://github.com/ph-del/photo2dcmsender\n\n" \
"pavel.honz@gmail.com\n\n" \
"Copyright (c) 2025 Pavel Honz"
},
    "infoAboutProgramTitle" : {"en": "Photo2DcmSender", "cz" : "Photo2DcmSender"},
    "infoSuccessfullySent": {"en": "Images was successfully sended to storage server", "cz":"Snímky byly úspěšně odeslány na úložiště"},
    "warningDialog" :{"en": "Warning - Insufficient data!", "cz": "Upozornění - Nedostatečná data!"},
    "warningFirstName" :{"en": "First name must be filled in.", "cz": "Jméno musí být vyplněno."},
    "warningLastName" :{"en": "Last name must be filled in.", "cz": "Příjmení musí být vyplněno."},
    "warningNoInfoStudy" : { "en" : "Patient info not filled in, please select study from worklist or insert study info manually", 
                           "cz" : "Nejsou vyplněny pacientské údaje. Prosím vyberte studii z worklistu, nebo zadejte informace o studii ručně"},
    "warningNoImageInDir" :{"en": "There are no files, in selected folder. Please select folder with image files",
                            "cz": "V zadané složce nejsou žádné obrázky. Prosím zadejte složku s obrázky"},
    "warningPatientId" :{"en": "Patient ID must be filled in.", "cz": "Rodné číslo musí být vyplněno."},
}

default_config = """
"!! Any further comments must not contain diacritics !!"

[LANGUAGE]

# possible values: cz, en 
language = cz

[DICOM_SETTINGS]

### STORE
# aet: this program
aet = TEST_1

# ip address store server
ipAddress = 10.10.10.200

# port store server
port = 5380

# aet store server
aec = DPGW_5251_PU


### MWL
# aet mwl server
mwlScpAet = DPGW_5251_PU

# ip address mwl server
mwlScpIpAddress = 10.10.10.200

# port mwl server
mwlScpPort = 5380

# front 
# (musi byt nastaveno na strane PACS napr. UZCUP, pokud neni na strane PACS nastaveno, je nutno toto nastaveni zakomentovat)
mwlScheduledStationAETitle = TEST_1


# additional information for created dicom studies
institutionName = NEMPK
institutionAddress = Kyjevska 44, 530 02 Pardubice
modalityType = XC       # XC, OT, ST

[FILES_SETTINGS]
# hotFolder = path (e.g. C:\my folder)
# Default folder for image files that should be dicomized. If this option is not set or folder is not existing, the default folder will be the folder where the program is running.
hotFolder = C:\hot_folder

# deleteImagesAfterSend = True | False  
# If true, image files in hot folder will be deleted after sending (default True)
deleteImagesAfterSend = True        

# moveImagesAfterSend  = True | False
# If true, image files in hot folder will be moved to the specified folder after sending (default False)
# !!! For apply this rule deleteImagesAfterSend must be False
moveImagesAfterSend = False
folderToMoveImages = C:\dicomized

# saveDicomizedImages = True | False
# If true, dicomized image save to local storage (default False)
saveDicomizedImages = False
folderToSaveDicomizedImages =  C:\dicomized

[LOG_LEVEL]
# possible values: DEBUG, INFO, WARNING, ERROR, CRITICAL
dicomMwl = INFO

[MWL_COLUMN_ORDER]
# order columns mwl
studyDate = 0
patientId = 1
patientName = 2
birthDate = 3
accessionNumber = 4 
reqPhys = 5

[DEVELOPMENT_TOOLS]
# sendDicomFileOff = True | False
# If true, dicomized data will not be send to AEC (default False)
sendDicomFileOff = False

"""


    