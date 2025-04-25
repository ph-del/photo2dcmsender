import logging
logger = logging.getLogger(__name__)

from pydicom.uid import generate_uid, JPEGExtended12Bit, ExplicitVRLittleEndian, ImplicitVRLittleEndian
from pydicom.dataset import Dataset
from pydicom.encaps import encapsulate
from pynetdicom import AE, StoragePresentationContexts, QueryRetrievePresentationContexts, debug_logger
from pynetdicom.sop_class import ModalityWorklistInformationFind, SecondaryCaptureImageStorage, VLPhotographicImageStorage, CTImageStorage, MRImageStorage


from datetime import datetime
from pathlib import Path
import wx
import os
import io
import shutil

from src.dats import load_config, load_text
from src.gui  import ManualInput

config = load_config()

# # Získání úrovně logování z konfigurace
# log_level = config['LOG_LEVEL']['dicomMwl'].upper()  # Převede na velká písmena pro kompatibilitu

# # Nastavení logování pro pynetdicom podle hodnoty z konfigurace
# logging.getLogger("pynetdicom").setLevel(getattr(logging, log_level))

# Získání loggeru PyNetDicom
pynetDicomLogger = logging.getLogger("pynetdicom")

# Nastavení úrovně loggeru
#pynetDicomLogger.setLevel(getattr(logging, log_level))
for idx, handler in enumerate(logging.getLogger().handlers):
    print(f"Handler {idx}: {handler}")
pynetDicomLogger.addHandler(logging.getLogger().handlers[2]) 

# for handler in pynetDicomLogger.handlers:
#     handler.setLevel(getattr(logging, log_level))


uidPrefix = "1.2.203.93."  #1.2.203 prefix for cz + my favorite

### Filters -----------------------------------
def on_today_click(event, filters, worklist):
    # Set today date to filters
    logging.debug("on_today_click started")
    filters.datePickerFrom.SetValue(wx.DateTime.Today())
    filters.datePickerTo.SetValue(wx.DateTime.Today())

def on_last_week_click(event, filters, worklist):
    # Set last week date to filters
    logging.debug("on_last_week_click started")
    filters.datePickerFrom.SetValue(wx.DateTime.Today().Subtract(wx.TimeSpan().Days(7)))
    filters.datePickerTo.SetValue(wx.DateTime.Today())

def on_last_month_click(event, filters, worklist):
    # Set last month date to filters
    logging.debug("on_last_month_click started")
    filters.datePickerFrom.SetValue(wx.DateTime.Today().Subtract(wx.TimeSpan.Days(31)))
    filters.datePickerTo.SetValue(wx.DateTime.Today())

def on_search_click(event, filters, worklist):
    # Function start search in dicom worklist and return founded records to panel worklist. Panel worklist is cleared before showing records.
    logging.debug("on_search_click started")
    
    dictFoundsStudies = {}
    # clear ListCtrl worklist
    worklist.dvcWorklist.DeleteAllItems()

    dateFrom = filters.datePickerFrom.GetValue().Format("%Y%m%d")
    dateTo = filters.datePickerTo.GetValue().Format("%Y%m%d")
    patientId = filters.tcPatientId.GetValue()
    lastName = filters.tcLastName.GetValue()
    firstName = filters.tcFirstName.GetValue()
    accessionNumber = filters.tcAccessionNumber.GetValue()

    
    if firstName != "":
        patientName = (lastName + "*" + "^" + firstName + "*").translate(str.maketrans("ěščřžýáíéůúňďťĚŠČŘŽÝÁÍÉŮÚŇĎŤ","escrzyaieuundtESCRZYAIEUUNDT"))
    else:
        patientName = (lastName + "*").translate(str.maketrans("ěščřžýáíéůúňďťĚŠČŘŽÝÁÍÉŮÚŇĎŤ","escrzyaieuundtESCRZYAIEUUNDT"))
    
    logging.debug(f"Filter data: Date: {dateFrom, dateTo}, Patient ID: {patientId}, Last Name: {lastName}, First Name: {firstName}, Accession Number: {accessionNumber}")
    
    # Creating a DICOM Association Application
    ae = AE(config["DICOM_SETTINGS"]["aet"])
    ae.add_requested_context(ModalityWorklistInformationFind)
    
    ds = Dataset()
    if patientName: ds.PatientName = patientName
    if patientId: ds.PatientID = patientId
    if accessionNumber: ds.AccesionNumber = accessionNumber
    if dateFrom:  
        ds.ScheduledProcedureStepSequence = [Dataset()]
        item = ds.ScheduledProcedureStepSequence[0]
        if config.has_option("DICOM_SETTINGS", "mwlScheduledStationAETitle"):
            item.ScheduledStationAETitle = config["DICOM_SETTINGS"]["mwlScheduledStationAETitle"]
        item.ScheduledProcedureStepStartDate = dateFrom + "-" + dateTo
        # item.ScheduledProcedureStepStartTime = datetime(2024, 12, 5, 0, 0).strftime('%H%M%S')
        # item.ScheduledProcedureStepEndDate = datetime.today().strftime("%Y%m%d")
        # item.ScheduledProcedureStepEndTime = datetime(2024, 12, 5, 23, 59).strftime('%H%M%S')
        # item.Modality = 'US' #not needed only if would be generated from KIS   

    dicom_data = []
    assoc = ae.associate(config["DICOM_SETTINGS"]["mwlScpIpAddress"], int(config["DICOM_SETTINGS"]["mwlScpPort"]), None,config["DICOM_SETTINGS"]["mwlScpAet"])

    if assoc.is_established:
        try:
            responses = assoc.send_c_find(ds, ModalityWorklistInformationFind)

            for status, identifier in responses:
                if status and status.Status == 0xFF00:
                    dicom_data.append(identifier)

            assoc.release()
        
        except Exception as e:
            logger.error(f"Error during C-FIND request: {e}")
            assoc.abort()
    else:
        logger.error(f"Nelze se připojit k MWL serveru")
        message = wx.MessageDialog(None, load_text("infoMwlFailed"), load_text("errorDialog"), wx.OK | wx.ICON_ERROR)
        message.ShowModal()
        message.Destroy()

    for i in range(len(dicom_data)-1):
        studyInstanceUid = str(dicom_data[i][0x20, 0x0d].value)
        patientName = str(dicom_data[i][0x10, 0x10].value).replace("^", " ")
        patientId = dicom_data[i][0x10, 0x20].value
        birthDate = dicom_data[i][0x10, 0x30].value
        accessionNumber = dicom_data[i][0x08, 0x50].value
        reqPhys = dicom_data[i][0x32, 0x1032].value
        studyDate = dicom_data[i][0x40,0x100][0][0x40,0x2].value

        if studyInstanceUid not in dictFoundsStudies.keys():
            dictFoundsStudies[studyInstanceUid] = [patientName, patientId, birthDate, accessionNumber, reqPhys, studyDate]
    #print(dictFoundsStudies)
    # Show new records at `list_ctrl`
    for studyInstanceUid, values in dictFoundsStudies.items():
        patientName, patientId, birthDate, accessionNumber, reqPhys, studyDate  = values


        studyDate = datetime.strptime(studyDate,"%Y%m%d").strftime("%d.%m.%Y") 
    
        worklist.dvcWorklist.AppendItem([studyDate, str(patientName), str(patientId), str(birthDate), str(accessionNumber), str(reqPhys), str(studyInstanceUid)])

# -------------------------------------------      

### Worklist --------------------------------- 
     
def clear_entered(entered):
    entered.stPatientNameEntered.SetLabel("")
    entered.stPatientIdEntered.SetLabel("")
    entered.stAccessionNumberEntered.SetLabel("")
    entered.stStudyUidEntered.SetLabel("")

def on_clear_click(event, filters, worklist, entered):
    # Clear worklist and filters
    logging.debug("on_clear_click started")

    filters.datePickerFrom.SetValue(wx.DateTime.Today())
    filters.datePickerTo.SetValue(wx.DateTime.Today())
    filters.tcPatientId.SetValue("")
    filters.tcLastName.SetFocus()
    filters.tcFirstName.SetValue("")
    filters.tcAccessionNumber.SetValue("")
    clear_entered(entered)
    worklist.dvcWorklist.DeleteAllItems()

def on_dvcWorklist_select(event, worklist, entered):
    # Selected record from worklist is passed to entry panel
    logging.debug("on_dvcWorklist_select started")

    selectedIndex = worklist.dvcWorklist.GetSelectedRow()
    
    # if is deselect
    if selectedIndex == -1:
        clear_entered(entered)
        return
    
    entered.stPatientNameEntered.SetLabel(worklist.dvcWorklist.GetTextValue(selectedIndex, get_column_index_by_name(worklist, load_text("colPatientName"))))
    entered.stPatientIdEntered.SetLabel(worklist.dvcWorklist.GetTextValue(selectedIndex, get_column_index_by_name(worklist, load_text("colPatientId"))))
    entered.stAccessionNumberEntered.SetLabel(worklist.dvcWorklist.GetTextValue(selectedIndex, get_column_index_by_name(worklist, load_text("colAccessionNumber"))))
    entered.stStudyUidEntered.SetLabel(worklist.dvcWorklist.GetTextValue(selectedIndex, get_column_index_by_name(worklist, load_text("colStudyUid"))))

def get_column_index_by_name(worklist, columnName):
    # Scans all columns and returns the index if the column name matches
    for col_index in range(worklist.dvcWorklist.GetColumnCount()):
        if worklist.dvcWorklist.GetColumn(col_index).GetTitle() == columnName: 
            return col_index
    return -1  # If a column with this name was not found


# def on_dvcWorklist_deselect(entered):
#     # Deselected selected record from worklist and clear entry panel
#     logging.debug("on_dvcWorklist_deselect started")

#     clear_entered(entered)
    

# --------------------------------------------  

### Manual input -----------------------------  
def on_manual_input_click(event, settings, mainWindow, entered):
    # Show manual input window
    logging.debug("on_manual_input started")
    
    dialog = ManualInput(mainWindow)

    # Centering dialog to app
    dialog.CenterOnParent()
   
    #settings.manual_input_settings(parent.manual_input_dialog)
    settings.manual_input_settings(dialog, entered)
    
    dialog.ShowModal()

def on_save_input_data_click(event, dialog, entered):
    # Save manual input data to entered
    logging.debug("on_save_input_data_click started")

    patientId = dialog.tcPatientId.GetValue()
    firstName = dialog.tcFirstName.GetValue()
    lastName = dialog.tcLastName.GetValue()
    accessionNumber = dialog.tcAccessionNumber.GetValue()

    if patientId != "" and firstName != "" and lastName != "":
        entered.stPatientIdEntered.SetLabel(patientId)
        entered.stPatientNameEntered.SetLabel(lastName + " " + firstName)
        entered.stAccessionNumberEntered.SetLabel(accessionNumber)
        entered.stStudyUidEntered.SetLabel(uidPrefix + generate_uid().split('.')[-1])   
        dialog.Close()
    
    else:
        message = ""
        if patientId == "":
            message += load_text("warningPatientId") + "\n"
        if firstName == "":
            message += load_text("warningFirstName") + "\n"
        if lastName == "":
            message += load_text("warningLastName") + "\n"

        dialog = wx.MessageDialog(dialog, message, load_text("warningDialog"), wx.OK | wx.ICON_WARNING)
        dialog.ShowModal()
        dialog.Destroy()

# -------------------------------------------  

### Loaded files ----------------------------
def load_files_in_directory(files2send):
    directory = files2send.dpcSelectedFolder.GetPath()  # Získáme vybranou složku
    if os.path.isdir(directory):
        # Načteme soubory v této složce
        validExtensions = ['.jpg', '.png', '.bmp', ".jpeg"]
        files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and os.path.splitext(f)[1].lower() in validExtensions]
        
        if files:
            files2send.lbLoadedFiles.Set(files)  # Nastavíme soubory do ListBoxu
            files2send.directory = directory
        else:
            files2send.lbLoadedFiles.Set([load_text("txNoFilesLoaded")]) 


def set_initial_directory(files):
    logging.debug("set_initial_directory started") 
    #return config["FILES_SETTINGS"]["hotFolder"] if os.path.isdir(config["FILES_SETTINGS"]["hotFolder"]) else os.getcwd()
    hot_folder = config["FILES_SETTINGS"]["hotFolder"]
    # Ošetření cesty pomocí pathlib
    hot_folder = str(Path(hot_folder))

    if not os.path.isdir(hot_folder):  
        try:
            os.makedirs(hot_folder, exist_ok=True)
            logger.info(f"Folder {hot_folder} was created.")
        except Exception as e:
            logger.warning(f"Cannot create a folder {hot_folder}: {e}")
            hot_folder = os.getcwd()

    logger.debug(f"Folder {hot_folder} was loaded.")
    return hot_folder

    
def on_directory_changed(event, files):
    load_files_in_directory(files)
# ------------------------------------------  

### Preview --------------------------------  
def preview_selected_image(event, files, preview):
        """Show selected image from loaded files"""
        logging.debug("preview_selected_image started")

        selected_file = files.lbLoadedFiles.GetStringSelection()
        if not files.directory or not selected_file or "Žádné podporované" in selected_file:
            return

        # Vytvoříme plnou cestu k souboru
        image_path = os.path.join(files.directory, selected_file)
        bitmap = resize_image(image_path)
        preview.imDisplay.SetBitmap(bitmap)
        preview.Layout()

def preview_deselect_image(event, files, preview):
        """Deselect image from preview"""
        logging.debug("preview_deselect_image started")
        index = files.lbLoadedFiles.HitTest(event.GetPosition())

        if index == wx.NOT_FOUND:  # Kliknutí mimo položky
            files.lbLoadedFiles.SetSelection(-1)  # Zruší výběr
            preview.imDisplay.SetBitmap(wx.NullBitmap)  # Nastaví prázdný bitmapový objekt
            preview.Layout()
        else:
            event.Skip()  # Předá událost dál, aby se normálně vybral soubor
        

def resize_image(imagePath, maxSize = 600):
    # Načteme obrázek
    image = wx.Image(imagePath, wx.BITMAP_TYPE_ANY)
    width, height = image.GetWidth(), image.GetHeight()

    if width > height:
        new_width = maxSize
        new_height = int(height * (maxSize / width))
    else:
        new_height = maxSize
        new_width = int(width * (maxSize / height))

    image = image.Scale(new_width, new_height, wx.IMAGE_QUALITY_HIGH)
    return image.ConvertToBitmap()
# ------------------------------------------  

### Send to PACS functions

def convert_to_dicom(file, patientName, patientId, accessionNumber, studyDate, studyTime, studyUid, seriesUid, fileNumber):
    """ Function to convert image to dicom"""
    logging.debug("convert_to_dicom started")

    def ensure_even(stream):
        # Very important for some viewers
        if len(stream) % 2:
            return stream + b"\x00"
        return stream

    # Check type loaded files and load images
    if os.path.splitext(file)[1].lower() in [".jpg", ".jpeg"]:
        logger.debug(f"Attempting to load JPG image... {file}")
        image = wx.Image(file, wx.BITMAP_TYPE_JPEG)
    elif os.path.splitext(file)[1].lower() == ".png":
        logger.debug(f"Attempting to load PNG image... {file}")
        image = wx.Image(file, wx.BITMAP_TYPE_PNG)
    elif os.path.splitext(file)[1].lower() == ".bmp":
        logger.debug(f"Attempting to load BMP image... {file}")
        image = wx.Image(file, wx.BITMAP_TYPE_BMP)

    # Check image was loaded
    if image.IsOk():
        logger.debug("Image was loaded succesfully")
    else:
        logger.debug("Error: No image was loaded!")
    
    ds = Dataset()
    ds.PatientName = patientName
    ds.PatientID = patientId
    ds.AccessionNumber = accessionNumber
    ds.StudyDate = studyDate
    ds.StudyTime = studyTime
    ds.StudyInstanceUID = studyUid
    ds.is_little_endian = True
    ds.is_implicit_VR = True
    ds.SOPClassUID = SecondaryCaptureImageStorage
    ds.SOPInstanceUID = seriesUid + "." + str(fileNumber)
    ds.SeriesInstanceUID = seriesUid
    ds.fix_meta_info()
    ds.file_meta.TransferSyntaxUID = ExplicitVRLittleEndian
    #ds.file_meta.ImplementationVersionName = "Pavel Honz Image Sender pavel.honz@gmail.com"
    #ds.file_meta.PrivateInformation = "Pavel Honz Image Sender pavel.honz@gmail.com"
    #ds.file_meta.ImplementationVersionName = "MadeByPavelHonz"
    ds.Manufacturer = "Image Dicom Sender pavel.honz@gmail.com"
    ds.Modality = config["DICOM_SETTINGS"]["modalityType"] 
    ds.SamplesPerPixel = 3
    ds.BitsAllocated = 8
    ds.BitsStored = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PlanarConfiguration = 0
    ds.PhotometricInterpretation = "RGB"
    ds.Rows = image.GetSize().Height
    ds.Columns = image.GetSize().Width
    if config["DICOM_SETTINGS"]["institutionName"] : ds.InstitutionName =  config["DICOM_SETTINGS"]["institutionName"] 
    if config["DICOM_SETTINGS"]["institutionAddress"] : ds.InstitutionAddress =  config["DICOM_SETTINGS"]["institutionAddress"] 

    output = io.BytesIO()
    image.SaveFile(output, wx.BITMAP_TYPE_JPEG)
    
    # encapsulate() requires a list of bytes, one item per frame
    ds.PixelData = encapsulate([ensure_even(output.getvalue())])
    # Need to set this flag to indicate the Pixel Data is compressed
    ds['PixelData'].is_undefined_length = True  # Only needed for < v1.4
    ds.is_implicit_VR = False
    ds.PhotometricInterpretation = "YBR_FULL_422"
    ds.file_meta.TransferSyntaxUID = JPEGExtended12Bit
    
    logger.debug("Function jpeg2dcm was ended succesfully. Dicom file was created.")

    return ds

def send_dicom_file(ds, file):
    """Function realize sending to specified AEC"""
    logging.debug("Function send_dicom_file has been started")
    
    if config["DEVELOPMENT_TOOLS"].getboolean("sendDicomFileOff") == True:
        return

    #Detailed debugger of dicom communication
    debug_logger()
    ae = AE(ae_title=config["DICOM_SETTINGS"]["aet"])

    #ae.requested_contexts = [build_context(Verification)]
    # We can also do the same thing with the requested contexts
    #ae.requested_contexts = VerificationPresentationContexts
    #ae.requested_contexts = StoragePresentationContexts[:1]
    # Or we can use inbuilt objects like CTImageStorage.
    # The requested presentation context's transfer syntaxes can also
    #   be specified using a str/UID or list of str/UIDs
    #ae.add_requested_context(CTImageStorage,transfer_syntax=ImplicitVRLittleEndian)
    # Adding a presentation context with multiple transfer syntaxes
    #ae.add_requested_context(MRImageStorage,transfer_syntax=[ImplicitVRLittleEndian,'1.2.840.10008.1.2.1'])
    ae.add_requested_context(SecondaryCaptureImageStorage, transfer_syntax=JPEGExtended12Bit)
    #ae.add_requested_context(VLPhotographicImageStorage, transfer_syntax=ImplicitVRLittleEndian)
    #ae.add_supported_context(VerificationSOPClass)

    logger.debug(f"Attempting to send DICOM file {file}")
   
    assoc = ae.associate(config["DICOM_SETTINGS"]["ipAddress"], int(config["DICOM_SETTINGS"]["port"]), None, config["DICOM_SETTINGS"]["aec"])
    if assoc.is_established:
        try:
            dataset = ds
            status = assoc.send_c_store(dataset)
            assoc.release()

            if status and status.Status in [0x0000]:  # success
                logger.info(f"Dicomized file {file} was successfully sent to PACS")
                return True
            else:
                logger.warning(f"Failed to store DICOM file {file}. Status: {status}")
                return False

        except Exception as e:
            logger.error(f"Error during C-STORE for file {file}: {e}")
            assoc.abort()
            return False

    else:
        logger.error(f"Association could not be established for file {file}")
        return False


def send_to_aec(event, entered, files, preview):
    """Function send dicom file to specified AEC"""
    logging.debug("send_to_aec")

    patientName = entered.stPatientNameEntered.GetLabel().replace(" ","^")
    patientId = entered.stPatientIdEntered.GetLabel()
    accessionNumber = entered.stAccessionNumberEntered.GetLabel()
    studyDate = datetime.now().strftime("%Y%m%d")
    studyTime = datetime.now().strftime("%H%M%S")
    studyUid = entered.stStudyUidEntered.GetLabel()
    seriesUid = uidPrefix + generate_uid().split('.')[-1]
    
    if patientName == "" and patientId == "":
        entered = wx.MessageDialog(entered, load_text("warningNoInfoStudy"), load_text("warningDialog"), wx.OK | wx.ICON_WARNING)
        entered.ShowModal()
        entered.Destroy()
        return
    
    if files.lbLoadedFiles.GetString(0) == load_text("txNoFilesLoaded"):
        files = wx.MessageDialog(entered, load_text("warningNoImageInDir"), load_text("warningDialog"), wx.OK | wx.ICON_WARNING)
        files.ShowModal()
        files.Destroy()
        return
    
    logging.info(f"Study info: patient name: {patientName}, patient id: {patientId}, acc no: {accessionNumber}, date: {studyDate},time: {studyTime}, uid: {studyUid } ")
    
    file_count = len(files.lbLoadedFiles.GetItems())
    dlg = wx.ProgressDialog(load_text("infoFileProcessing"), load_text("infoFileSendings"),  file_count, entered,  style=wx.PD_AUTO_HIDE | wx.PD_APP_MODAL)
    
    fileNumber = 1
    for image in files.lbLoadedFiles.GetItems():
        file = os.path.join(files.dpcSelectedFolder.GetPath(), image)
        dicomFile = convert_to_dicom(file, patientName, patientId, accessionNumber, studyDate, studyTime, studyUid, seriesUid, fileNumber)
        statusSend = send_dicom_file(dicomFile, file)
        if statusSend:
            after_send_dicom_file_proccess(dicomFile, file)
            fileNumber += 1
            # Aktualizace ProgressDialogu s aktuálním pokrokem
            dlg.Update(fileNumber-1)  # Aktualizuje hodnotu pokroku
        else:
            break

    dlg.Destroy()  # Zavře ProgressDialog
    after_send_dicom_study_proccess(entered, preview, statusSend)
    return

def after_send_dicom_study_proccess(entered,preview, statusSend):
    """Function proccessing study ater send to dicom aet"""
    if statusSend:
        message = wx.MessageDialog(entered, load_text("infoSuccessfullySent"), load_text("infoDialog"), wx.OK | wx.ICON_INFORMATION)
        message.ShowModal()
        message.Destroy()

        clear_entered(entered)
        preview.imDisplay.SetBitmap(wx.NullBitmap)  # Nastaví prázdný bitmapový objekt
        preview.Layout()
        
    else:
        message = wx.MessageDialog(entered, load_text("infoSendingFailed"), load_text("errorDialog"), wx.OK | wx.ICON_ERROR)
        message.ShowModal()
        message.Destroy()

def after_send_dicom_file_proccess(ds, file):
    """Function proccessing file ater send to dicom aet"""
    logger.info("after_send_dicom_file_proccess started")

    if config["FILES_SETTINGS"].getboolean("saveDicomizedImages") == True:
        save_dicom_file(file, ds)

    if config["FILES_SETTINGS"].getboolean("deleteImagesAfterSend") == True:
        remove_image(file)
      
    if config["FILES_SETTINGS"].getboolean("moveImagesAfterSend") == True and config["FILES_SETTINGS"].getboolean("deleteImagesAfterSend") == False:
        move_with_rename(file)
     
    return
                 
def save_dicom_file(file, ds):
    "Function save dicomized file to the local storage"
    logger.debug("save_dicom_file started")

    try:
        destination = config["FILES_SETTINGS"]["folderToSaveDicomizedImages"]
        destination = destination + "\\" + os.path.basename(os.path.splitext(file)[0]) + ".dcm"
    except:
        destination = os.getcwd() + "\\proccessed_dicom\\" + os.path.basename(os.path.splitext(file)[0]) + ".dcm"
    
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    counter = 1
    while os.path.exists(destination):
        # Vytvoření nového názvu souboru s číslovkou
        new_name = f"{os.path.basename(os.path.splitext(file)[0])}_{counter}.dcm"
        destination = os.path.join(os.path.dirname(destination), new_name)
        counter += 1
    ds.save_as(destination, write_like_original=False)
    
    logger.debug(f"Dicom file {destination} was saved.")

def remove_image(file):
    """Function remove source image from directory after dicomizing"""
    logger.debug("remove_image started")
    
    os.remove(file)
    logger.debug(f"{file} was deleted")

def move_with_rename(source):
    """Function move file to specified directory, if file exists in specified directory, function renamed source file"""
    logger.debug("move_with_rename started")

    try:
        destination = config["FILES_SETTINGS"]["folderToMoveImages"]
        destination = destination + "\\" + os.path.basename(source)
    except:
        destination = os.getcwd() + "\\proccessed_images\\" + os.path.basename(source)

    os.makedirs(os.path.dirname(destination), exist_ok=True)

    counter = 1
    while os.path.exists(destination):
        # Vytvoření nového názvu souboru s číslovkou
        new_name = f"{os.path.basename(os.path.splitext(source)[0])}_{counter}{os.path.splitext(source)[1]}"
        destination = os.path.join(os.path.dirname(destination), new_name)
        counter += 1

    # Přesun souboru
    shutil.move(source, destination)

    logger.debug(f"{source} was moved to {destination}")

def on_click_static_text(event,entered):
        logger.debug("on_click_static_text started")
        # Funkce, která se spustí po kliknutí na StaticText
        dialog = wx.MessageDialog(entered, load_text("infoAboutProgram"), load_text("infoAboutProgramTitle"), wx.OK)
        dialog.ShowModal()
        dialog.Destroy()
