import logging
logger = logging.getLogger(__name__)

import wx
import os

import src.gui as gui
import src.settings as settings

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Initializing GUI
        self.panelFilters = gui.Filters(self)           # filtres
        self.panelWorklist = gui.Worklist(self)         # worklist
        self.panelEntered = gui.EnteredStudy(self)      # entered 
        self.panelSend = gui.Send2Pacs(self)            # send
        self.panelFiles = gui.Files2Send(self)          # files 
        self.panelPreview = gui.Preview(self)           # preview
        
        
        #self.dialogManualInput = gui.ManualInput(self)      # manual input
        
        # Main sizer
        #   __________________________________
        #  |Main Sizer - HORIZONTAL           |
        #  | _______________   ____________   |
        #  | |Vert. Si 1    | |Vert. Si 2  |  |
        #  | |Filtres       | |HOT Folder  |  |
        #  | |Worklist      | |Preview     |  |
        #  | |Entered       | |------      |  |
        #  | |--------      | |            |  |
        #  | |Send          | |About       |  |
        #  | |______________| |____________|  |
        #  |__________________________________|
        
        mainSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        vertSizer1 = wx.BoxSizer(wx.VERTICAL)
        vertSizer2 = wx.BoxSizer(wx.VERTICAL)
        
        vertSizer1.Add(self.panelFilters, 0, wx.ALL | wx.EXPAND, 5)
        vertSizer1.Add(self.panelWorklist, 0, wx.ALL | wx.EXPAND, 5)
        vertSizer1.Add(self.panelEntered, 0, wx.ALL | wx.EXPAND, 5)
        vertSizer1.AddStretchSpacer(1)
        vertSizer1.Add(self.panelSend, 0, wx.ALL | wx.EXPAND, 5)
        
        vertSizer2.Add(self.panelFiles, 0, wx.ALL | wx.EXPAND, 5)
        vertSizer2.Add(self.panelPreview, 0, wx.ALL | wx.EXPAND, 5)

        mainSizer.Add(vertSizer1, 0, wx.EXPAND | wx.ALL, 5)
        mainSizer.Add(vertSizer2, 1, wx.EXPAND | wx.ALL, 5)

        # Set size for main panel
        self.SetSizer(mainSizer)
        mainSizer.Fit(self)

        # Settings program
        self.programSettings = settings.Settings(self,
                                                 self.panelFilters,
                                                 self.panelWorklist,
                                                 self.panelEntered,
                                                 self.panelSend,
                                                 self.panelFiles,
                                                 self.panelPreview,
                                                 #self.dialogManualInput
                                                 )

class RunGui:
    def __init__(self, *args, **kwargs):
        self.app = wx.App(False)
        self.frame = wx.Frame(None, wx.ID_ANY, "Photo PACS sender")  

        small_icon_path = os.path.join(os.getcwd(), "src/img", "icon-16.png")
        #large_icon_path = os.path.join(os.getcwd(), "src/img", "icon-32.png")
        
        if os.path.exists(small_icon_path): 
            icon = wx.Icon(small_icon_path, wx.BITMAP_TYPE_PNG)
            self.frame.SetIcon(icon)
        else:
            logger.warn(f"Icon cannot be loaded. Wrong path? Current path is {os.getcwd()} Icon must be in dir program_folder/src/img")
               
        self.panel = MainPanel(self.frame)
        self.panel.SetName("MainPanel")

        self.frame.Fit() 
        self.frame.Center()
        self.frame.Show(True)

        #print(f"Main window size {self.frame.GetSize()}")

    def MainLoop(self):
        self.app.MainLoop()



