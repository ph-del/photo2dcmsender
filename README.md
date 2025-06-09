# Photo2DcmSender 

#### cz

## Popis
Photo2DcmSender je program pro převod obrázků formátu JPEG, PNG nebo BMP do DICOM s následnou možnosti odeslat tyto DICOM data do PACSu, přičemž umožňuje práci s worklistem. Program je postaven na knihovně wxPython pro grafické rozhraní a dalších knihovnách pro zpracování souborů a komunikaci.

## Instalace
Pokud chcete spustit tento program, ujistěte se, že máte nainstalovaný Python 3.x a všechny požadované knihovny. Poté můžete nainstalovat závislosti pomocí pip:

```bash
pip install -r requirements.txt
```

## Verze

### Photo2DcmSender 1.2 <small>(5.6.2025)</small>
- Oprava: Nezobrazoval se worklist ve verzi 1.1, prohozený řádek kódu (functions.py)
- Aktualizace: knihovna pydicom 2.4.4 nahrazena pydicom 3.0.1. Pracuji jinak s meta_files. Byla přizpůsobena funkce convert_to_dicom (functions.py)
- Přidáno: ikony aplikace ve formátu .ICO
- Doplněno: Podpora formátů obrázků GIF, TIF, TGA. Neplatné nebo poškozené obrázky se nezobrazí ani neodešlou. (functions.py)


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
- Python 3.13.2
- czech-holidays (verze 1.0.0) – MIT License
- icecream (verze 2.1.4) – MIT License
- pydicom (verze 3.0.1) – MIT License
- pyinstaller (verze 6.13.0) – GNU General Public License v2 (GPLv2)
- pynetdicom (verze 3.0.1) – MIT License
- typing_extensions (verze 4.12.2) – Python Software Foundation License
- watchdog (verze 6.0.0) – Apache Software License
- wxPython (verze 4.2.3) – wxWindows Library License (https://opensource.org/licenses/wxwindows.php)

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
Photo2DcmSender is a program for converting JPEG, PNG or BMP images to DICOM format with the possibility to send the DICOM data to PACS, while allowing worklist work. The program is based on the wxPython library for the graphical interface and other libraries for file processing and communication.

## Installation
To run this program, make sure you have Python 3.x installed and all required dependencies. You can install the dependencies using pip:

```bash
pip install -r requirements.txt
```

## Version

### Photo2DcmSender 1.2 <small>(June 5, 2025)</small>
- Fix: Worklist was not displayed – corrected a misplaced line of code in (functions.py).
- Update: Replaced pydicom version 2.4.4 with version 3.0.1. Adjusted handling of meta_files and updated the convert_to_dicom function in (functions.py).
- Added: aplication icon in ICO format
- Added: Support for image formats GIF, TIF, TGA. Invalid or corrupted images will not be displayed or sent. (functions.py)

### Photo2DcmSender 1.1 <small>(25.4.2025)</small>
- Fix: Swapped first and last name in manual input in version 1.1 (functions.py)
- Fix: In default config file: comment on the same line as a value was being interpreted as part of the value.(dats.py)
- Fix: In manual input mode, images appeared to be sent to PACS even when no DICOM connection was established due to incorrect configuration. (functions.py)
- Added: Info message when sending data to PACS fails. (functions.py)
- Added: Info message when querying the worklist fails. (functions.py)
- Fix: Program icon now loads correctly after building the .exe file. (mainwindow.py, gui.py)


### Photo2DcmSender 1.0
- First release

### Used Libraries
- Python 3.13.2
- czech-holidays (verze 1.0.0) – MIT License
- icecream (verze 2.1.4) – MIT License
- pydicom (verze 3.0.1) – MIT License
- pyinstaller (verze 6.13.0) – GNU General Public License v2 (GPLv2)
- pynetdicom (verze 3.0.1) – MIT License
- typing_extensions (verze 4.12.2) – Python Software Foundation License
- watchdog (verze 6.0.0) – Apache Software License
- wxPython (verze 4.2.3) – wxWindows Library License (https://opensource.org/licenses/wxwindows.php)

## License
This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License version 3, as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

## Contact
Author: Pavel Honz<br>
Email: pavel.honz@gmail.com<br>
Source Code: [GitHub](https://github.com/ph-del/photo2dcmsender)<br>
Copyright (c) 2025 Pavel Honz<br>
