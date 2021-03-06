# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QGIS Full Motion Video (FMV)
                                 A QGIS plugin

 Analyze and manage georeferenced video data in your maps

                             -------------------
        begin                : 2018-03-13
        copyright            : (C) 2018 All4Gis.
        email                : franka1986@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 #   any later version.                                                    *
 *                                                                         *
 ***************************************************************************/
"""
import os.path

from PyQt5.QtCore import QSettings, QCoreApplication, QTranslator, qVersion
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from QGIS_FMV.player.QgsFmvAbout import FmvAbout
from QGIS_FMV.player.QgsManager import FmvManager
from QGIS_FMV.utils.QgsFmvLog import log
from qgis.PyQt.QtCore import Qt

try:
    from pydevd import *
except ImportError:
    None


class Fmv:
    """ Main Class """

    def __init__(self, iface):
        """ Contructor """
        self.iface = iface
        log.initLogging()

        self.plugin_dir = os.path.dirname(__file__)
        locale = QSettings().value("locale//userLocale")[0:2]
        localePath = os.path.join(
            self.plugin_dir, 'i18n', 'qgisfmv_{}.qm'.format(locale))
        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '5.9.0':
                QCoreApplication.installTranslator(self.translator)

        self._FMVManager = None

    def initGui(self):
        ''' FMV Action '''
        self.actionFMV = QAction(QIcon(":/imgFMV/images/icon.png"),
                                 u"FMV", self.iface.mainWindow(),
                                 statusTip=QCoreApplication.translate(
                                     "Fmv", "Show Video Manager"),
                                 triggered=self.run)
        self.iface.addToolBarIcon(self.actionFMV)
        self.iface.addPluginToMenu(QCoreApplication.translate(
            "Fmv", "Full Motion Video (FMV)"), self.actionFMV)

        ''' About Action '''
        self.actionAbout = QAction(QIcon(":/imgFMV/images/Information.png"), u"About", self.iface.mainWindow(),
                                   statusTip=QCoreApplication.translate(
                                       "Fmv", "Show About FMV"),
                                   triggered=self.About)

        self.iface.addPluginToMenu(QCoreApplication.translate(
            "Fmv", "Full Motion Video (FMV)"), self.actionAbout)

    def unload(self):
        ''' Unload Plugin '''
        self.iface.removePluginMenu(QCoreApplication.translate(
            "Fmv", "Full Motion Video (FMV)"), self.actionFMV)
        self.iface.removePluginMenu(QCoreApplication.translate(
            "Fmv", "Full Motion Video (FMV)"), self.actionAbout)
        self.iface.removeToolBarIcon(self.actionFMV)
        log.removeLogging()

    def About(self):
        ''' Show About Dialog '''
        self.About = FmvAbout()
        self.About.setWindowFlags(Qt.Window | Qt.WindowCloseButtonHint)
        self.About.exec_()

    def run(self):
        ''' Run method '''
        if self._FMVManager is None:
            self.CreateDockWidget()

    def CreateDockWidget(self):
        ''' Show Manager Video Dock '''
        self._FMVManager = FmvManager(self.iface)
        self.iface.addDockWidget(Qt.BottomDockWidgetArea, self._FMVManager)
