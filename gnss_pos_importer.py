# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ImportadorGNSS
                                 A QGIS plugin
 Importa, filtra e projeta arquivos .pos gerados por receptores GNSS/RTK
 ***************************************************************************/
"""
__author__ = 'Gabriel Aoki'
__date__ = '2026-09-09'
__copyright__ = '(C) 2026 by Gabriel Aoki'
__revision__ = '$Format:%H$'

import os
import sys
import inspect
import processing

from qgis.core import QgsProcessingAlgorithm, QgsApplication
from qgis.utils import iface
from qgis.PyQt.QtWidgets import QAction
from qgis.PyQt.QtGui import QIcon

from .gnss_pos_importer_provider import ImportadorGNSSProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]

if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

class ImportadorGNSSPlugin(object):

    def __init__(self):
        self.provider = None
        self.action = None

    def initProcessing(self):
        """Init Processing provider for QGIS >= 3.8."""
        self.provider = ImportadorGNSSProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        """Inicializa a interface gráfica, adicionando o botão na barra."""
        self.initProcessing()
        
        # Carrega o ícone SVG diretamente da pasta do plugin
        icon_path = os.path.join(cmd_folder, 'icon.png')
        self.action = QAction(QIcon(icon_path), "Importar Arquivo .pos", iface.mainWindow())
        
        # Conecta o clique do botão à função que abre a janela
        self.action.triggered.connect(self.run_dialog)
        
        # Adiciona no menu Plug-ins e na barra de ferramentas superior
        iface.addPluginToMenu("&GNSS Pos Importer", self.action)
        iface.addToolBarIcon(self.action)

    def unload(self):
        """Remove o botão e limpa o QGIS ao desinstalar o plugin."""
        QgsApplication.processingRegistry().removeProvider(self.provider)
        
        if self.action:
            iface.removePluginMenu("&GNSS Pos Importer", self.action)
            iface.removeToolBarIcon(self.action)

    def run_dialog(self):
        """Abre diretamente a janela do algoritmo quando o botão é clicado."""
        # Chama a ferramenta passando o "ID_do_Provedor : ID_do_Algoritmo"
        processing.execAlgorithmDialog('GNSS Pos Importer:importarpos_pro')