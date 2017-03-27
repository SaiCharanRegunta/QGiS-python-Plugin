import os
import re

from PyQt4 import QtGui, uic
from PyQt4.QtCore import *
from qgis.core import *
from qgis.gui import *
from LatLon import LatLon

import mgrs

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ui/zoomToLatLon.ui'))


class ZoomToLatLon(QtGui.QDockWidget, FORM_CLASS):

    closingPlugin = pyqtSignal()

    def __init__(self, lltools, iface, parent,lat,lon):
        super(ZoomToLatLon, self).__init__(parent)
        self.setupUi(self)
        self.lltools = lltools

        self.lltools.zoomToLatLon(lat,lon)
	#self.settings = lltools.settingsDialog        
	#self.iface = iface
        #self.coordTxt.returnPressed.connect(self.zoomToPressed)
        #self.configure()

    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()
        
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False
    
    def configure(self):
        self.coordTxt.setText("")
        
        if self.settings.zoomToCoordType == 1:
            # This is an MGRS coordinate
            self.label.setText("Enter MGRS Coordinate")
        else:
            if self.settings.zoomToCoordOrder == 0:
                self.label.setText("Enter 'Latitude, Longitude'")
            else:
                self.label.setText("Enter 'Longitude, Latitude'")

    def zoomToPressed(self):
        self.lltools.zoomToLatLon(0,0)
