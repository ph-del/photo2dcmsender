import logging


logger = logging.getLogger(__name__)

import os
import wx
import sys
import wx.adv

from src.dats import load_text

class Filters(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        logger.debug(f"{self.__class__.__name__} started")

        # Widgets initialize
        # sb.Filters --------------------
        self.sbFilters = wx.StaticBox(self, label = load_text("txFilters"))
        self.stDateFrom = wx.StaticText(self, label=load_text("txSpinDateFrom") + ": ")
        self.datePickerFrom = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY, size = (-1,-1))
        self.stDateTo = wx.StaticText(self, label=load_text("txSpinDateTo") + ": ")
        self.datePickerTo = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DROPDOWN | wx.adv.DP_SHOWCENTURY, size = (-1,-1))
        self.btnToday = wx.Button(self, label=load_text("btnToday"))
        self.btnLastWeek = wx.Button(self, label=load_text("btnLastWeek"))
        self.btnLastMonth = wx.Button(self, label=load_text("btnLastMonth"))
        #self.btnLastYear = wx.Button(self, label=load_text("btnLastMonth"))
        self.stPatientId = wx.StaticText(self, label=load_text("txPatientId") + ":")
        self.tcPatientId = wx.TextCtrl(self, size=(150, -1), style=wx.TE_PROCESS_ENTER)
        self.stLastName = wx.StaticText(self, label=load_text("txLastName") + ": ")
        self.tcLastName = wx.TextCtrl(self, size=(150, -1), style=wx.TE_PROCESS_ENTER)
        self.stFirstName = wx.StaticText(self, label=load_text("txFirstName") + ": ")
        self.tcFirstName = wx.TextCtrl(self, size=(150, -1), style=wx.TE_PROCESS_ENTER)
        self.stAccessionNumber = wx.StaticText(self, label=load_text("txAccessionNumber") + ": ")
        self.tcAccessionNumber = wx.TextCtrl(self, size=(150, -1), style=wx.TE_PROCESS_ENTER)
        self.btnSearch = wx.Button(self, label=load_text("btnSearch"))
        #---------------------------------

        # Widget sizers
        #|sbSizer filters-----|
        #||gbSizerFiltr -------|
        #|||R0,C0|R0,C1|R0,C2||
        #|||R1,C0|R1,C1|R1,C2||
        #|||R2,C0|R2,C1|R2,C2||


        # sbSizerFiltres------------------
        self.sbSizerFilters = wx.StaticBoxSizer(self.sbFilters, wx.VERTICAL)
        gbSizerFiltresWidgets = wx.GridBagSizer(vgap=0, hgap=5)
        gbSizerFiltresWidgets.Add(self.stDateFrom, pos=(0, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.datePickerFrom, pos=(0, 2), flag=wx.EXPAND | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.stDateTo, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.datePickerTo, pos=(1, 2), flag=wx.EXPAND | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.btnToday, pos=(0, 0), flag=wx.EXPAND | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.btnLastWeek, pos=(1, 0), flag=wx.EXPAND | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.btnLastMonth, pos=(2, 0), flag=wx.EXPAND | wx.ALL, border=3)
        #gbSizerFiltresWidgets.Add(self.btnLastYear, pos=(3, 1), flag=wx.EXPAND | wx.ALL, border=5)
        gbSizerFiltresWidgets.Add(self.stPatientId, pos=(0, 3), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.tcPatientId, pos=(0, 4), flag=wx.EXPAND | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.stLastName, pos=(1, 3), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.tcLastName, pos=(1, 4), flag=wx.EXPAND | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.stFirstName, pos=(2, 3), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.tcFirstName, pos=(2, 4), flag=wx.EXPAND | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.stAccessionNumber, pos=(0, 5), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.tcAccessionNumber, pos=(0, 6), flag=wx.EXPAND | wx.ALL, border=3)
        gbSizerFiltresWidgets.Add(self.btnSearch, pos=(2, 5), span=(1, 2), flag=wx.ALIGN_RIGHT | wx.ALL, border=3)
        self.sbSizerFilters.Add(gbSizerFiltresWidgets, 1, wx.EXPAND | wx.ALL | wx.CENTER, border=3)
        #self.sbSizerFilters.SetMinSize((0,225))
        # --------------------------------

        # sbSizers to main sizer widget
        #mainSizer.Add(self.sbSizerFiltres, 0, wx.ALL | wx.EXPAND)

        # Set sizer for panel
        self.SetSizerAndFit(self.sbSizerFilters)

class Worklist(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        logger.debug(f"{self.__class__.__name__} started")

        # Widgets initialize

        #sbWorklist-----------------------
        self.sbWorklist = wx.StaticBox(self, label = load_text("txWorklist"))
        #self.lcWorklist = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL, size = (-1, 250))
        self.dvcWorklist = wx.dataview.DataViewListCtrl(self, style=wx.dataview.DV_VERT_RULES | wx.dataview.DV_SINGLE, size=( 0, 250))
        self.btnClear = wx.Button(self, label = load_text("btnClear"))
        #---------------------------------

        # Widget sizers
        #|mainsizer------------|
        #||sbSizer worklist----|
        #|||bSizer worklist----|
        #|||bSizer button------|
        #|---------------------|

        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # sbSizerWorklist-----------------
        sbSizerWorklist = wx.StaticBoxSizer(self.sbWorklist, wx.VERTICAL)
        bSizerWorklist = wx.BoxSizer(wx.VERTICAL)
        bSizerButton = wx.BoxSizer(wx.VERTICAL)
        bSizerWorklist.Add(self.dvcWorklist, 0, wx.EXPAND | wx.ALL, border = 5)
        bSizerButton.Add(self.btnClear, 0, wx.ALL | wx.ALIGN_RIGHT, border = 5)
        sbSizerWorklist.Add(bSizerWorklist, 0,  wx.ALL | wx.EXPAND)
        sbSizerWorklist.Add(bSizerButton, 0, wx.ALL | wx.EXPAND)
        # --------------------------------

        # sbSizers to main sizer widget
        mainSizer.Add(sbSizerWorklist, 0, wx.ALL | wx.EXPAND)

        # Set sizer for panel
        self.SetSizerAndFit(mainSizer)
        self.Layout()

class EnteredStudy(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        logger.debug(f"{self.__class__.__name__} started")

        # Widgets initialize
        
        #sbEntered-------------------------
        self.sbEntered = wx.StaticBox(self, label = load_text("txEnteredStudy"))
        self.stPatientName = wx.StaticText(self, label = load_text("txPatientName") + ": ")
        self.stPatientNameEntered = wx.StaticText(self, size=(150, -1))
        self.stPatientId = wx.StaticText(self, label = load_text("txPatientId") + ": ")
        self.stPatientIdEntered = wx.StaticText(self, size=(150, -1))
        self.stAccessionNumber = wx.StaticText(self, label = load_text("txAccessionNumber") + ": ")
        self.stAccessionNumberEntered = wx.StaticText(self, size=(150, -1))
        self.stStudyUid = wx.StaticText(self, label = load_text("txStudyUid") + ": ")
        self.stStudyUidEntered = wx.StaticText(self, size=(-1, -1))
        self.btnManualInput = wx.Button(self, label = load_text("btnManualInput"))
        #-----------------------------------

        # Widget sizers
        #|mainsizer------------|
        #||sbSizer entered----|
        #|||gbSizer -----------|
        #||||R0,C0|R0,C1|R0,C2||
        #||||R1,C0|R1,C1|R1,C2||
        #||||R2,C0|R2,C1|R2,C2||
        #||||R3,C0/2-btnManual||
                
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        #sbSizerPatientStudyData----------------------
        sbSizerEntered = wx.StaticBoxSizer(self.sbEntered, wx.VERTICAL)
        gbSizerEntered = wx.GridBagSizer(vgap=0, hgap=3)
        gbSizerEntered.Add(self.stPatientName, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        gbSizerEntered.Add(self.stPatientNameEntered, pos=(0, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        gbSizerEntered.Add(self.stPatientId, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        gbSizerEntered.Add(self.stPatientIdEntered, pos=(1, 1), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        gbSizerEntered.Add(self.stAccessionNumber, pos=(0, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        gbSizerEntered.Add(self.stAccessionNumberEntered, pos=(0, 3), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        gbSizerEntered.Add(self.stStudyUid, pos=(1, 2), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        gbSizerEntered.Add(self.stStudyUidEntered, pos=(1, 3), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=5)
        sbSizerEntered.Add(gbSizerEntered, 0, wx.HORIZONTAL | wx.EXPAND | wx.CENTER)
        sbSizerEntered.Add(self.btnManualInput, 0, wx.HORIZONTAL | wx.ALIGN_RIGHT, border = 5)
        #-------------------------------------

        # sbSizers to main sizer widget
        mainSizer.Add(sbSizerEntered, 0, wx.ALL | wx.EXPAND)
        mainSizer.AddStretchSpacer(1)
    
        # Set sizer for panel
        self.SetSizerAndFit(mainSizer)
        self.Layout()

class Send2Pacs(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        logger.debug(f"{self.__class__.__name__} started")
                
        # sbSend ---------------------------
        self.sbSending= wx.StaticBox(self, label = load_text("txSending"))
        self.btnSend = wx.Button(self, label = load_text("btnSend"))
        #-----------------------------------

        # Widget sizers
        #|sbSizer worklist----|
        #||bSizer-------------|
        #|---------------------|


        #sbSizerSend------------------------
        sbSizerSend = wx.StaticBoxSizer(self.sbSending, wx.VERTICAL)
        bSizerSend = wx.BoxSizer(wx.VERTICAL)
        bSizerSend.Add(self.btnSend, 0, wx.ALL | wx.EXPAND, border = 5)
        sbSizerSend.Add(bSizerSend,0, wx.ALL | wx.EXPAND)
        #-----------------------------------
    
        # Set sizer for panel
        self.SetSizerAndFit(sbSizerSend)
        self.Layout()

class Files2Send(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        logger.debug(f"{self.__class__.__name__} started")
 
        # Widgets initialize
        
        #sbFiles2Upload-------------------------
        self.sbFilesToUpload = wx.StaticBox(self, label = load_text("txFilesToUpload"))
        self.lbLoadedFiles = wx.ListBox(self, style=wx.LB_SINGLE | wx.BORDER_SUNKEN, size = (0, 150))
        self.dpcSelectedFolder = wx.DirPickerCtrl(self, style = wx.DIRP_USE_TEXTCTRL)
        #---------------------------------------

        # Widget sizers
        #|sbSizer files2Up----|
        #||bSizer Listbox-----|
        #||bSizer Select fold-|
       
        #mainSizer = wx.BoxSizer(wx.VERTICAL)

        #sbSizerSelected----------------------
        self.sbSizerFiles = wx.StaticBoxSizer(self.sbFilesToUpload, wx.VERTICAL)
        bSizerLoadeFiles = wx.BoxSizer(wx.VERTICAL)
        bSizerLoadeFiles.Add(self.lbLoadedFiles, 1 , wx.ALL | wx.EXPAND, border = 5)
        bSizerLoadeFiles.Add(self.dpcSelectedFolder, 0, wx.ALL | wx.EXPAND, border = 5)
        self.sbSizerFiles.Add(bSizerLoadeFiles, 0, wx.ALL | wx.EXPAND, border = 5) 
        #-------------------------------------
    
        # Set sizer for panel
        self.SetSizerAndFit(self.sbSizerFiles)

class Preview(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        logger.debug(f"{self.__class__.__name__} started")
        
       

        # Widgets initialize
        self.imDisplay = wx.StaticBitmap(self, size=(600, 600))
        
        # StaticText for bottom-right corner
        self.stInfo = wx.StaticText(self, label=load_text("stAbout"))
        # Set text color to blue
        self.stInfo.SetForegroundColour(wx.Colour(0, 0, 255))  # RGB for blue
       
        # Widget sizers
        mainSizer = wx.BoxSizer(wx.VERTICAL)

        # sbSizerPreview
        sbSizerPreview = wx.BoxSizer(wx.HORIZONTAL)
        sbSizerPreview.Add(self.imDisplay, 0, wx.ALL | wx.CENTER, border=5)

        # Horizontal sizer for bottom-right text
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        bottomSizer.AddStretchSpacer(1)  # Pushes the StaticText to the right
        bottomSizer.Add(self.stInfo, 0, wx.ALL | wx.ALIGN_BOTTOM, 10)

        # Adding both to the mainSizer
        mainSizer.Add(sbSizerPreview, 0, wx.ALL | wx.EXPAND)
        mainSizer.Add(bottomSizer, 0, wx.ALL | wx.EXPAND)

        # Set sizer for panel
        self.SetSizerAndFit(mainSizer)
        self.Layout()

class ManualInput(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, style = wx.DEFAULT_DIALOG_STYLE | wx.FRAME_NO_TASKBAR)
        logger.debug(f"{self.__class__.__name__} started")

        if getattr(sys, 'frozen', False):
            # Aplikace je zabalená PyInstallerem
            base_path = sys._MEIPASS
        else:
            # Normální běh v Pythonu
            base_path = os.path.dirname(os.path.abspath(__file__))

        small_icon_path = os.path.join(base_path, "img", "icon-16.png")
        logger.debug(f"small_icon_path = {small_icon_path}")
        #small_icon_path = os.path.join(os.getcwd(), "src/img", "icon-16.png")
        #large_icon_path = os.path.join(os.getcwd(), "src/img", "icon-32.png")
        
        if os.path.exists(small_icon_path): 
            icon = wx.Icon(small_icon_path, wx.BITMAP_TYPE_PNG)
            self.SetIcon(icon)
        else:
            logger.warning(f"Icon cannot be loaded. Wrong path? Current path is {os.getcwd()} Icon must be in dir program_folder/src/img")

        self.SetTitle(load_text("titleManualInput"))
        
        # Widgets initialize
        
        # Dialog widgets------------------------
        self.stPatientId = wx.StaticText(self, label = load_text("txPatientId") + " * :")
        self.stFirstName = wx.StaticText(self, label = load_text("txFirstName") + " * :")
        self.stLastName = wx.StaticText(self, label = load_text("txLastName") + " * :")
        self.stAccessionNumber = wx.StaticText(self, label = load_text("txAccessionNumber") + " :")
        self.tcPatientId = wx.TextCtrl(self, size=(150, -1), style=wx.TE_PROCESS_ENTER)
        self.tcFirstName = wx.TextCtrl(self, size=(150, -1), style=wx.TE_PROCESS_ENTER)
        self.tcLastName = wx.TextCtrl(self, size=(150, -1), style=wx.TE_PROCESS_ENTER)
        self.tcAccessionNumber = wx.TextCtrl(self, size=(150, -1), style=wx.TE_PROCESS_ENTER)

        self.btnSaveInputData = wx.Button(self, label= load_text("btnSaveInputData"))
        # -------------------------------------
        
        # Widget sizers
        #|mainsizer------------|
        #||gridBagSizer--------|
        #||R0,C0|R0,C1|--------|
        #||R1,C0|R1,C1|--------|
        #||R2,C0|R2,C1|--------|
        #||R3,C0|R3,C1|--------|
        #|---------------------|

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        
        #gbSizer---------------------
        gridBagSizer = wx.GridBagSizer(hgap=5, vgap=5)
        gridBagSizer.Add(self.stPatientId, pos=(0, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gridBagSizer.Add(self.tcPatientId, pos=(0, 1), flag=wx.EXPAND)
        gridBagSizer.Add(self.stFirstName, pos=(1, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gridBagSizer.Add(self.tcFirstName, pos=(1, 1), flag=wx.EXPAND)
        gridBagSizer.Add(self.stLastName, pos=(2, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gridBagSizer.Add(self.tcLastName, pos=(2, 1), flag=wx.EXPAND)
        gridBagSizer.Add(self.stAccessionNumber, pos=(3, 0), flag=wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        gridBagSizer.Add(self.tcAccessionNumber, pos=(3, 1), flag=wx.EXPAND)
        # ---------------------------

        # Ensure columns expand properly
        gridBagSizer.AddGrowableCol(1, 1)  # Allow second column to expand horizontally

        mainSizer.Add(gridBagSizer, 0, wx.EXPAND | wx.ALL, 10)
        mainSizer.Add(self.btnSaveInputData, 0, wx.ALL | wx.ALIGN_RIGHT, 10)
        # Set sizer for panel
        self.SetSizerAndFit(mainSizer)
        self.Layout()
    
    