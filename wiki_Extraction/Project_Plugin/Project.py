# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Project
                                 A QGIS plugin
 Project
                              -------------------
        begin                : 2016-10-06
        git sha              : $Format:%H$
        copyright            : (C) 2016 by Project
        email                : Project
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from geotext import GeoText
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from math import radians, cos, sin, asin, sqrt
from latlontools import latLonTools
import qgis.utils
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from Project_dialog import ProjectDialog
import re,os,sys
import os.path
class Project:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'Project_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Project')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'Project')
        self.toolbar.setObjectName(u'Project')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('Project', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        # Create the dialog (after translation) and keep reference
        self.dlg = ProjectDialog()

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = '/home/charan/.qgis2/python/plugins/Project/postal.jpg'
        self.add_action(
            icon_path,
            text=self.tr(u'Project'),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Project'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
	#layers = self.iface.legendInterface().layers()
	#layer_list = ["Town Name Search","Pincode Search"]
     	#choice=self.dlg.comboBox.addItems(layer_list)
	#print choice	
	#self.dlg.lineEdit.text()
        result = self.dlg.exec_()
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
		pass
	#index=self.dlg.comboBox.currentIndex()
	statementText=self.dlg.lineEdit.text()
	places = GeoText(statementText)
	TouristPlace=places.cities

	ToureGuide(self,TouristPlace[0])
    def test(self):
	return self.iface

def ToureGuide(self,TouristPlace):
	search=TouristPlace
	print search+": Searching...."
	link="https://en.wikipedia.org/wiki/"+ str(search).replace(" ","_")
	print "Link Generated is: "+link
	command="echo \"$(wget -O - "+ link +")\" > information.txt"
	os.system(command)
	fp=open("information.txt","r")
	HTMLwithTags=fp.read()
	HTMLwithTags=HTMLwithTags.replace("<span class=\"geo\">","<geo start>")
	HTMLwithTags=HTMLwithTags.split("<geo start>")
	Latitude= str(HTMLwithTags[1].split("</span>"))
	Latitude= re.sub("(<[^>]+>)", '', Latitude)
	speakstr=str(Latitude)
	speakstr=speakstr.split()
	PointLatitude=speakstr[0].replace("['",'').replace(";",'')
	PointLongitude=speakstr[1].replace("\',",'')
	print "Latitude: "+ speakstr[0].replace("['",'').replace(";",'')
	print "Longitude:"+ speakstr[1].replace("\',",'')
	t=Project(self.iface)                
	print TouristPlace
	latLonTools.LatLonTools(t.test(),float(PointLatitude),float(PointLongitude))
	fpInfo=open("information.txt","r")
	HTMLwithTagsInfo=fpInfo.read()
	HTMLwithTagsInfo=HTMLwithTagsInfo.replace("<p>The","<pThe>The")
	HTMLwithTagsInfo=HTMLwithTagsInfo.split("<pThe>")
	firstPara= str(HTMLwithTagsInfo[1].split("</p>"))
	firstPara= re.sub("(<[^>]+>)", '', firstPara)
	speakstr=str(firstPara)
	speakstr=speakstr.replace("(",'')
	speakstr=speakstr.replace(")",'')
	print speakstr
	os.system('espeak '+speakstr)
####################################################################
def dist_from_prom_places(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km
#####################################################################
def point_prominant_place(x1,x2):
	impPlaceFile=open("/home/charan/.qgis2/python/plugins/Project/Imp_Places_LatLon.csv","r")
	distancerange= 50  #Km
	for prominant in impPlaceFile:
		prominant=prominant.replace("\n",'').split(",")
		dist=dist_from_prom_places(x1,x2,float(prominant[2]),float(prominant[3]))
		if  dist <= distancerange:
			dist=round(dist,2)
			print "Distance from "+prominant[0]+" is: "+str(dist)+"Km"
