import logging

import wx.dataview
logger = logging.getLogger(__name__)

import wx
import wx.adv

import src.functions as fn

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.dats import load_text

class FolderWatcher(FileSystemEventHandler):
    def __init__(self, files):
        logger.debug(f"{self.__class__.__name__} started")
        self.files = files  # Store reference to the files object

    def on_modified(self, event):
        # Handle file modifications
        logger.debug(f"FolderWatcher: Folder has changed! Event: {event}")
        fn.load_files_in_directory(self.files)  # Reload files after a directory change
      

    def on_deleted(self, event):
        # Handle file deletions
        logger.debug(f"FolderWatcher: File moved or deleted: {event.src_path}")
        fn.load_files_in_directory(self.files)  # Reload files after a file deletion


class Settings(wx.Panel):
    def __init__(self, parent, filters, worklist, entered, send, files, preview):
        super().__init__(parent)
        logger.debug(f"{self.__class__.__name__} started")


        ## Settings worklist filtres --------------
        filters.tcLastName.SetFocus()
        filters.tcPatientId.Bind(wx.EVT_TEXT_ENTER, lambda event: fn.on_search_click(event, filters, worklist))
        filters.tcLastName.Bind(wx.EVT_TEXT_ENTER, lambda event: fn.on_search_click(event, filters, worklist))
        filters.tcFirstName.Bind(wx.EVT_TEXT_ENTER, lambda event: fn.on_search_click(event, filters, worklist))
        filters.tcAccessionNumber.Bind(wx.EVT_TEXT_ENTER, lambda event: fn.on_search_click(event, filters, worklist))
        filters.btnToday.Bind(wx.EVT_BUTTON, lambda event: fn.on_today_click(event, filters, worklist) )
        filters.btnLastWeek.Bind(wx.EVT_BUTTON, lambda event: fn.on_last_week_click(event, filters, worklist))
        filters.btnLastMonth.Bind(wx.EVT_BUTTON, lambda event: fn.on_last_month_click(event, filters, worklist))
        filters.btnSearch.Bind(wx.EVT_BUTTON, lambda event: fn.on_search_click(event, filters, worklist))
                       
        # ----------------------------------------

        ## Settings worklist DataViewCtrl--------------
        worklist.dvcWorklist.AppendTextColumn(load_text("colStudyDate"), width = -2)
        worklist.dvcWorklist.AppendTextColumn(load_text("colPatientName"), width = 180)
        worklist.dvcWorklist.AppendTextColumn(load_text("colPatientId"), width = 80)
        worklist.dvcWorklist.AppendTextColumn(load_text("colBirthDate"), width = -2)
        worklist.dvcWorklist.AppendTextColumn(load_text("colAccessionNumber"), width = -2)
        worklist.dvcWorklist.AppendTextColumn(load_text("colReqPhys"), width = 100)
        worklist.dvcWorklist.AppendTextColumn(load_text("colStudyUid"), flags = wx.dataview.DATAVIEW_COL_HIDDEN)

        # Bind worklist ListCtrl
        worklist.dvcWorklist.Bind(wx.dataview.EVT_DATAVIEW_SELECTION_CHANGED, lambda event: fn.on_dvcWorklist_select(event, worklist, entered))
        
        # btnClear
        worklist.btnClear.Bind(wx.EVT_BUTTON, lambda event: fn.on_clear_click(event, filters, worklist, entered))
        # ----------------------------------------

        ## Settings Manual Input------------------
        entered.btnManualInput.Bind(wx.EVT_BUTTON, lambda event: fn.on_manual_input_click(event, self, parent, entered))
        # ----------------------------------------

        ## Setting Send --------------------------
        send.btnSend.Bind(wx.EVT_BUTTON, lambda event: fn.send_to_aec(event, entered, files, preview))
        # ----------------------------------------

        ## Settings Files to upload -------------
         # Initialize directory picker
        files.dpcSelectedFolder.SetPath(fn.set_initial_directory(files))
        files.dpcSelectedFolder.Bind(wx.EVT_DIRPICKER_CHANGED, lambda event: fn.on_directory_changed(event, files))
        
        fn.load_files_in_directory(files)
        
        # Get folder to watch
        files.folderToWatch = files.dpcSelectedFolder.GetPath()
        logger.debug(f"Watching folder: {files.folderToWatch}")
        
        # Initialize the FolderWatcher with the 'files' object
        files.eventHandler = FolderWatcher(files)
        
        # Initialize the observer and schedule it to monitor the folder
        files.observer = Observer()
        files.observer.schedule(files.eventHandler, files.folderToWatch, recursive=True)
        
        # Start the observer in a separate thread
        files.observer.start()

        # Bind close event to stop observer when the window is closed
        files.Bind(wx.EVT_CLOSE, self.on_close)
        
        # Bind listbox selection event
        files.lbLoadedFiles.Bind(wx.EVT_LISTBOX, lambda event: fn.preview_selected_image(event, files, preview))
        files.lbLoadedFiles.Bind(wx.EVT_LEFT_DOWN, lambda event: fn.preview_deselect_image(event, files, preview))
        files.Layout()
        files.Refresh()

         # Přidání události pro kliknutí na StaticText
        preview.stInfo.Bind(wx.EVT_LEFT_UP, lambda event: fn.on_click_static_text(event,entered))
             

    def on_close(self, event):
        logger.debug("Closing window and stopping observer")
        self.observer.stop()  # Stop the observer
        self.observer.join()  # Wait for the observer thread to finish
        self.Destroy()  # Destroy the wx.Panel


    def manual_input_settings(self, dialog, entered):
        # Settings for manual input, manual input is not initialized after start. It is initialized after clicked on button Manual Input
        logger.debug("manual_input_settings started")

        # entry manual input
        dialog.tcPatientId.Bind(wx.EVT_TEXT_ENTER, lambda event: fn.on_save_input_data_click(event, dialog, entered) )
        dialog.tcFirstName.Bind(wx.EVT_TEXT_ENTER, lambda event: fn.on_save_input_data_click(event, dialog, entered) )
        dialog.tcLastName.Bind(wx.EVT_TEXT_ENTER, lambda event: fn.on_save_input_data_click(event, dialog, entered) )
        dialog.tcAccessionNumber.Bind(wx.EVT_TEXT_ENTER, lambda event: fn.on_save_input_data_click(event, dialog, entered) )
        
        # btn Save input data
        dialog.btnSaveInputData.Bind(wx.EVT_BUTTON, lambda event: fn.on_save_input_data_click(event, dialog, entered))

        
        

        