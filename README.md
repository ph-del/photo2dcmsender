# Photo2DcmSender 

#### cz

## Popis
Photo2DcmSender je program pro převod obrázků na formát DICOM. Umožňuje uživatelům odesílat obrázky ve formátu JPEG, PNG nebo BMP jako DICOM soubory do systému AEC. Program je postaven na knihovně wxPython pro grafické rozhraní a dalších knihovnách pro zpracování souborů a komunikaci.

## Instalace
Pokud chcete spustit tento program, ujistěte se, že máte nainstalovaný Python 3.x a všechny požadované knihovny. Poté můžete nainstalovat závislosti pomocí pip:

```bash
pip install -r requirements.txt
```

## Verze

### Photo2DcmSender 1.1 <small>(25.4.2025)</small>
- Oprava: Prohozené jméno a příjmení při ručním zadání (functions.py)
- Oprava: Výchozí konfigurační soubor: komentář na stejném řádku jako hodnota byl chybně považován za součást hodnoty (dats.py)
- Oprava: V případě ručního vstupu se snímky tvářily jako úspěšně odeslané na PACS, i když nebylo navázáno DICOM spojení kvůli chybné konfiguraci. (functions.py)
- Doplněno: Informační hláška při neúspěšném odeslání dat na PACS. (functions.py)
- Doplněno: Informační hláška při neúspěšném dotazu na Worklist. (functions.py)
- Oprava: Správné načítání ikony programu po vytvoření .exe souboru. (mainwindow.py, gui.py)

### Photo2DcmSender 1.0
- První vydání

### Použité knihovny
- configparser (verze 7.1.0) – MIT License
- czech-holidays (verze 1.0.0) – MIT License
- icecream (verze 2.1.3) – MIT License
- pydicom (verze 2.4.4) – MIT License
- pyinstaller (verze 6.11.1) – GNU General Public License v2 (GPLv2)
- pynetdicom (verze 2.1.1) – MIT License
- typing_extensions (verze 4.12.2) – Python Software Foundation License
- watchdog (verze 6.0.0) – Apache Software License
- wxPython (verze 4.2.2) – wxWindows Library License (https://opensource.org/licenses/wxwindows.php)

## Licence
Tento program je svobodný software: můžete jej šířit a/nebo upravovat podle podmínek GNU General Public License verze 3, jak ji zveřejnila Free Software Foundation.

Tento program je distribuován v naději, že bude užitečný, ale BEZ JAKÉKOLI ZÁRUKY; dokonce i bez předpokládané záruky PRODEJNOSTI nebo VHODNOSTI PRO KONKRÉTNÍ ÚČEL. Viz GNU General Public License pro více detailů.

Měli byste obdržet kopii GNU General Public License spolu s tímto programem. Pokud ne, podívejte se na https://www.gnu.org/licenses/.

## Kontakty
Autor: Pavel Honz<br>
Email: pavel.honz@gmail.com<br>
Zdrojový kód: [GitHub](https://github.com/ph-del/photo2dcmsender)<br>
Copyright (c) 2025 Pavel Honz<br>

---

#### en

## Description
Photo2DcmSender is a program for converting images to DICOM format. It allows users to send JPEG, PNG, or BMP images as DICOM files to an AEC system. The program is built using the wxPython library for the graphical interface, along with other libraries for file processing and communication.

## Installation
To run this program, make sure you have Python 3.x installed and all required dependencies. You can install the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Version

### Photo2DcmSender 1.1 <small>(25.4.2025)</small>
- Fix: Swapped first and last name in manual input (functions.py)
- Fix: In default config file: comment on the same line as a value was being interpreted as part of the value.(dats.py)
- Fix: In manual input mode, images appeared to be sent to PACS even when no DICOM connection was established due to incorrect configuration. (functions.py)
- Added: Info message when sending data to PACS fails. (functions.py)
- Added: Info message when querying the worklist fails. (functions.py)
- Fix: Program icon now loads correctly after building the .exe file. (mainwindow.py, gui.py)


### Photo2DcmSender 1.0
- First release

### Used Libraries
configparser (version 7.1.0) – MIT License
czech-holidays (version 1.0.0) – MIT License
icecream (version 2.1.3) – MIT License
pydicom (version 2.4.4) – MIT License
pyinstaller (version 6.11.1) – GNU General Public License v2 (GPLv2)
pynetdicom (version 2.1.1) – MIT License
typing_extensions (version 4.12.2) – Python Software Foundation License
watchdog (version 6.0.0) – Apache Software License
wxPython (version 4.2.2) – wxWindows Library License (https://opensource.org/licenses/wxwindows.php)

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License version 3, as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

## Contact
Author: Pavel Honz<br>
Email: pavel.honz@gmail.com<br>
Source Code: [GitHub](https://github.com/ph-del/photo2dcmsender)<br>
Copyright (c) 2025 Pavel Honz<br>
