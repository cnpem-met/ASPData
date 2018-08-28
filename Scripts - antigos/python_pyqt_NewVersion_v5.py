#! /usr/bin/env python
# ESTA VERSÃO PLOTA GRAFICOS COM AS OPÇÕES DE REFEERNCIAS
#
#from calendar1 import monthrange


#   IDEIAS A SEREM IMPLEMENTADAS
#   - plot com x indefinido (default online)
#   - curva de média
#   - aumentar area lateral para click nas checkPlots

#   CONSERTAR
#   - plot com 2 racks ta zuado
#   

import serial, time, sys, os, threading
import numpy as np
from PyQt4 import QtGui
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
import os
from PyQt4 import QtGui, QtCore
import PyQt4.Qwt5 as Qwt
from time import strftime
from multiprocessing import Process
import time
import threading
from HLS_plot_v1 import HLS_plot1
from HLS_plot_v2 import HLS_plot2
from HLS_plot_v3 import HLS_plot3
from HLS_plot_v4 import HLS_plot4
from os import listdir
from os.path import isfile, join
from Fogale_UI import Ui_MainWindow
from PlotGUI_Qwt_Multi import dataclass
from PlotGUI_Qwt_Multi import SimplePlot

sys.path.insert(0, "C:/users/rodrigo.neto/desktop/HLS-BancadaMETRO")

#from Variaveis import var
from Variaveis_v2 import var
from Auxiliar import aux


class PlotOnOff:

    #muda numero de pontos no gráfico
    def set_cmp_on(self):
        var.cmp_on = var.ria.ui.cmp_on.value()

    def set_checkCmp_on(self):
        if var.ria.ui.checkCmp_on.isChecked():
            aux.flagCmp = True
        else:
            aux.flagCmp = False
        
    def setRef_on(self):
        if(aux.rack1_enable == 1):
            #aux.refD1 = var.D1[-1][1:]
            aux.refD1 = [7.654, 6.1231, 8.123, 5.98, 6.123, 8.12312, 7.432, 9.1321]
            var.ria.ui.logOutput_on.insertPlainText("Referency values: "+str(aux.refD1)+'\n')
        if(aux.rack2_enable == 1):
            aux.refD2 = var.D2[-1][1:]
        if(aux.rack3_enable == 1):
            aux.refD3 = var.D3[-1][1:]
        if(aux.rack4_enable == 1):
            aux.refD4 = var.D4[-1][1:]
    
    #inicializa Plot1
    def set_plot1_on(self):
        if not var.ria.ui.checkPlot1_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[0].setTitle("")
            var.ria.ui.widget_on.Plots[1].setTitle("")
            var.ria.ui.widget_on.Data[0] = dataclass()
            var.ria.ui.widget_on.Data[1] = dataclass()
        else:
            """muda nome do plot e zera valores"""
            var.ria.ui.widget_on.Plots[0].setTitle(var.disp_sensores[0][0])
            var.ria.ui.widget_on.Plots[1].setTitle(var.disp_sensores[0][0])
            var.ria.ui.widget_on.Data[0] = dataclass()
            var.ria.ui.widget_on.Data[1] = dataclass()

    #inicializa Plot2
    def set_plot2_on(self):
        if not var.ria.ui.checkPlot2_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[2].setTitle("")
            var.ria.ui.widget_on.Plots[3].setTitle("")
            var.ria.ui.widget_on.Data[2] = dataclass()
            var.ria.ui.widget_on.Data[3] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget_on.Plots[2].setTitle(var.disp_sensores[0][1])
            var.ria.ui.widget_on.Plots[3].setTitle(var.disp_sensores[0][1])
            var.ria.ui.widget_on.Data[2] = dataclass()
            var.ria.ui.widget_on.Data[3] = dataclass()
            
    #inicializa Plot3
    def set_plot3_on(self):
        if not var.ria.ui.checkPlot3_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[4].setTitle("")
            var.ria.ui.widget_on.Plots[5].setTitle("")
            var.ria.ui.widget_on.Data[4] = dataclass()
            var.ria.ui.widget_on.Data[5] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget_on.Plots[4].setTitle(var.disp_sensores[0][2])
            var.ria.ui.widget_on.Plots[5].setTitle(var.disp_sensores[0][2])
            var.ria.ui.widget_on.Data[4] = dataclass()
            var.ria.ui.widget_on.Data[5] = dataclass()

    #inicializa Plot4
    def set_plot4_on(self):
        if not var.ria.ui.checkPlot4_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[6].setTitle("")
            var.ria.ui.widget_on.Plots[7].setTitle("")
            var.ria.ui.widget_on.Data[6] = dataclass()
            var.ria.ui.widget_on.Data[7] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget_on.Plots[6].setTitle(var.disp_sensores[0][3])
            var.ria.ui.widget_on.Plots[7].setTitle(var.disp_sensores[0][3])
            var.ria.ui.widget_on.Data[6] = dataclass()
            var.ria.ui.widget_on.Data[7] = dataclass()

    #inicializa Plot5
    def set_plot5_on(self):
        if not var.ria.ui.checkPlot5_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[8].setTitle("")
            var.ria.ui.widget_on.Plots[9].setTitle("")
            var.ria.ui.widget_on.Data[8] = dataclass()
            var.ria.ui.widget_on.Data[9] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget_on.Plots[8].setTitle(var.disp_sensores[0][4])
            var.ria.ui.widget_on.Plots[9].setTitle(var.disp_sensores[0][4])
            var.ria.ui.widget_on.Data[8] = dataclass()
            var.ria.ui.widget_on.Data[9] = dataclass()

    #inicializa Plot6
    def set_plot6_on(self):
        if not var.ria.ui.checkPlot6_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[10].setTitle("")
            var.ria.ui.widget_on.Plots[11].setTitle("")
            var.ria.ui.widget_on.Data[10] = dataclass()
            var.ria.ui.widget_on.Data[11] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget_on.Plots[10].setTitle(var.disp_sensores[0][5])
            var.ria.ui.widget_on.Plots[11].setTitle(var.disp_sensores[0][5])
            var.ria.ui.widget_on.Data[10] = dataclass()
            var.ria.ui.widget_on.Data[11] = dataclass()

    #inicializa Plot7
    def set_plot7_on(self):
        if not var.ria.ui.checkPlot7_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[12].setTitle("")
            var.ria.ui.widget_on.Plots[13].setTitle("")
            var.ria.ui.widget_on.Data[12] = dataclass()
            var.ria.ui.widget_on.Data[13] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget_on.Plots[12].setTitle(var.disp_sensores[0][6])
            var.ria.ui.widget_on.Plots[13].setTitle(var.disp_sensores[0][6])
            var.ria.ui.widget_on.Data[12] = dataclass()
            var.ria.ui.widget_on.Data[13] = dataclass()

    #inicializa Plot8
    def set_plot8_on(self):
        if not var.ria.ui.checkPlot8_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[14].setTitle("")
            var.ria.ui.widget_on.Plots[15].setTitle("")
            var.ria.ui.widget_on.Data[14] = dataclass()
            var.ria.ui.widget_on.Data[15] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget_on.Plots[14].setTitle(var.disp_sensores[0][7])
            var.ria.ui.widget_on.Plots[15].setTitle(var.disp_sensores[0][7])
            var.ria.ui.widget_on.Data[14] = dataclass()
            var.ria.ui.widget_on.Data[15] = dataclass()
            
    #inicializa Plot9
    def set_plot9_on(self):
        if not var.ria.ui.checkPlot9_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[16].setTitle("")
            var.ria.ui.widget_on.Plots[17].setTitle("")
            var.ria.ui.widget_on.Data[16] = dataclass()
            var.ria.ui.widget_on.Data[17] = dataclass()
        else:
            """muda nome do plot e zera valores"""
            var.ria.ui.widget_on.Plots[16].setTitle(var.disp_sensores[1][0])
            var.ria.ui.widget_on.Plots[17].setTitle(var.disp_sensores[1][0])
            var.ria.ui.widget_on.Data[16] = dataclass()
            var.ria.ui.widget_on.Data[17] = dataclass()

    #inicializa Plot10
    def set_plot10_on(self):
        if not var.ria.ui.checkPlot10_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[18].setTitle("")
            var.ria.ui.widget_on.Plots[19].setTitle("")
            var.ria.ui.widget_on.Data[18] = dataclass()
            var.ria.ui.widget_on.Data[19] = dataclass()
        else:
            """muda nome do plot e zera valores"""
            var.ria.ui.widget_on.Plots[18].setTitle(var.disp_sensores[1][1])
            var.ria.ui.widget_on.Plots[19].setTitle(var.disp_sensores[1][1])
            var.ria.ui.widget_on.Data[18] = dataclass()
            var.ria.ui.widget_on.Data[19] = dataclass()

    #inicializa Plot11
    def set_plot11_on(self):
        if not var.ria.ui.checkPlot11_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[20].setTitle("")
            var.ria.ui.widget_on.Plots[21].setTitle("")
            var.ria.ui.widget_on.Data[20] = dataclass()
            var.ria.ui.widget_on.Data[21] = dataclass()
        else:
            """muda nome do plot e zera valores"""
            var.ria.ui.widget_on.Plots[20].setTitle(var.disp_sensores[1][2])
            var.ria.ui.widget_on.Plots[21].setTitle(var.disp_sensores[1][2])
            var.ria.ui.widget_on.Data[20] = dataclass()
            var.ria.ui.widget_on.Data[21] = dataclass()

    #inicializa Plot12
    def set_plot12_on(self):
        if not var.ria.ui.checkPlot12_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[22].setTitle("")
            var.ria.ui.widget_on.Plots[23].setTitle("")
            var.ria.ui.widget_on.Data[22] = dataclass()
            var.ria.ui.widget_on.Data[23] = dataclass()
        else:
            """muda nome do plot e zera valores"""
            var.ria.ui.widget_on.Plots[22].setTitle(var.disp_sensores[1][3])
            var.ria.ui.widget_on.Plots[23].setTitle(var.disp_sensores[1][3])
            var.ria.ui.widget_on.Data[22] = dataclass()
            var.ria.ui.widget_on.Data[23] = dataclass()

    #inicializa Plot13
    def set_plot13_on(self):
        if not var.ria.ui.checkPlot13_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[24].setTitle("")
            var.ria.ui.widget_on.Plots[25].setTitle("")
            var.ria.ui.widget_on.Data[24] = dataclass()
            var.ria.ui.widget_on.Data[25] = dataclass()
        else:
            """muda nome do plot e zera valores"""
            var.ria.ui.widget_on.Plots[24].setTitle(var.disp_sensores[1][4])
            var.ria.ui.widget_on.Plots[25].setTitle(var.disp_sensores[1][4])
            var.ria.ui.widget_on.Data[24] = dataclass()
            var.ria.ui.widget_on.Data[25] = dataclass()

    #inicializa Plot14
    def set_plot14_on(self):
        if not var.ria.ui.checkPlot14_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[26].setTitle("")
            var.ria.ui.widget_on.Plots[27].setTitle("")
            var.ria.ui.widget_on.Data[26] = dataclass()
            var.ria.ui.widget_on.Data[27] = dataclass()
        else:
            """muda nome do plot e zera valores"""
            var.ria.ui.widget_on.Plots[26].setTitle(var.disp_sensores[1][5])
            var.ria.ui.widget_on.Plots[27].setTitle(var.disp_sensores[1][5])
            var.ria.ui.widget_on.Data[26] = dataclass()
            var.ria.ui.widget_on.Data[27] = dataclass()

    #inicializa Plot15
    def set_plot15_on(self):
        if not var.ria.ui.checkPlot15_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[28].setTitle("")
            var.ria.ui.widget_on.Plots[29].setTitle("")
            var.ria.ui.widget_on.Data[28] = dataclass()
            var.ria.ui.widget_on.Data[29] = dataclass()
        else:
            """muda nome do plot e zera valores"""
            var.ria.ui.widget_on.Plots[28].setTitle(var.disp_sensores[1][6])
            var.ria.ui.widget_on.Plots[29].setTitle(var.disp_sensores[1][6])
            var.ria.ui.widget_on.Data[28] = dataclass()
            var.ria.ui.widget_on.Data[29] = dataclass()

    #inicializa Plot16
    def set_plot16_on(self):
        if not var.ria.ui.checkPlot16_on.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[30].setTitle("")
            var.ria.ui.widget_on.Plots[31].setTitle("")
            var.ria.ui.widget_on.Data[30] = dataclass()
            var.ria.ui.widget_on.Data[31] = dataclass()
        else:
            """muda nome do plot e zera valores"""
            var.ria.ui.widget_on.Plots[30].setTitle(var.disp_sensores[1][7])
            var.ria.ui.widget_on.Plots[31].setTitle(var.disp_sensores[1][7])
            var.ria.ui.widget_on.Data[30] = dataclass()
            var.ria.ui.widget_on.Data[31] = dataclass()

    def plotBox_act(self):
        if var.ria.ui.plotBox_on.currentIndex() == 0: #Plotar valores do nível
            aux.plotSet = "nivel"
        else: #Plotar valores de temperatura
            aux.plotSet = "temp"

    
    def startPlot_absBoxes(self):
        aux.plotFlag = True
        aux.plotFlag1 = True
        aux.plotFlag2 = False
        aux.plotFlag3 = False
        aux.plotFlag4 = False
        aux.plotFlag5 = False
        aux.plotFlag6 = False
        var.ria.ui.logOutput_on.insertPlainText("Selected Plot: ABSOLUT\n")
        Plot_thread = Plot()
    def startPlot_abs(self):
        aux.plotFlag = True
        aux.plotFlag2 = True
        aux.plotFlag1 = False
        aux.plotFlag3 = False
        aux.plotFlag4 = False
        aux.plotFlag5 = False
        aux.plotFlag6 = False
        var.ria.ui.logOutput_on.insertPlainText("Selected Plot: ABSOLUT\n")
        var.ria.ui.logOutput_on.moveCursor(QTextCursor.End)
        Plot_thread = Plot()
    def startPlot_refSensor(self):
        aux.plotFlag = True
        aux.plotFlag3 = True
        aux.plotFlag2 = False
        aux.plotFlag1 = False
        aux.plotFlag4 = False
        aux.plotFlag5 = False
        aux.plotFlag6 = False
        var.ria.ui.logOutput_on.insertPlainText("Selected Plot: SENSOR REFERENCY\n")
        var.ria.ui.logOutput_on.moveCursor(QTextCursor.End)
        Plot_thread = Plot()
    def startPlot_refMediaG(self):
        aux.plotFlag = True
        aux.plotFlag4 = True
        aux.plotFlag2 = False
        aux.plotFlag3 = False
        aux.plotFlag1 = False
        aux.plotFlag5 = False
        aux.plotFlag6 = False
        var.ria.ui.logOutput_on.insertPlainText("Selected Plot: OVERALL MEAN\n")
        var.ria.ui.logOutput_on.moveCursor(QTextCursor.End)
        Plot_thread = Plot()
    def startPlot_refMediaI(self):
        aux.plotFlag = True
        aux.plotFlag5 = True
        aux.plotFlag2 = False
        aux.plotFlag3 = False
        aux.plotFlag4 = False
        aux.plotFlag1 = False
        aux.plotFlag6 = False
        var.ria.ui.logOutput_on.insertPlainText("Selected Plot: LOCAL MEAN\n")
        var.ria.ui.logOutput_on.moveCursor(QTextCursor.End)
        Plot_thread = Plot()
    def startPlot_refFixa(self):
        aux.plotFlag = True
        aux.plotFlag6 = True
        aux.plotFlag2 = False
        aux.plotFlag3 = False
        aux.plotFlag4 = False
        aux.plotFlag5 = False
        var.ria.ui.logOutput_on.insertPlainText("Selected Plot: FIXED VALUE REFERENCY"+"\n")
        var.ria.ui.logOutput_on.moveCursor(QTextCursor.End)
        aux.plotFlag1 = False
        Plot_thread = Plot()

    def stopPlot(self):
        aux.plotFlag = False

    def plot_call(self):
        #while(1):
        global tam_D1
        global tam_D2
        global tam_D3
        global tam_D4
        if(len(var.D1) != 0):
            if(len(var.D1) != tam_D1 and aux.plotFlagRIAcom == True):
                aux.rack1 = 1
                tam_D1 = len(var.D1)
            else:
                aux.rack1 = 0
        if(len(var.D2) != 0):
            if(len(var.D2) != tam_D2 and aux.plotFlagRIAcom == True):
                aux.rack2 = 1
                tam_D2 = len(var.D2)
            else:
                aux.rack2 = 0
        if(len(var.D3) != 0):
            if(len(var.D3) != tam_D3 and aux.plotFlagRIAcom == True):
                aux.rack3 = 1
                tam_D3 = len(var.D3)
            else:
                aux.rack3 = 0
        if(len(var.D4) != 0):
            if(len(var.D4) != tam_D4 and aux.plotFlagRIAcom == True):
                aux.rack4 = 1
                tam_D4 = len(var.D4)
            else:
                aux.rack4 = 0

        if(aux.plotFlag2):
            if(aux.rack1 == 1):
                self.plot_abs(1)
            if(aux.rack2 == 1):
                self.plot_abs(2)
            if(aux.rack3 == 1):
                self.plot_abs(3)
            if(aux.rack4 == 1):
                self.plot_abs(4)
        if(aux.plotFlag3):
            if(aux.rack1 == 1):
                self.plot_refSensor(1)
            if(aux.rack2 == 1):
                self.plot_refSensor(2)
            if(aux.rack3 == 1):
                self.plot_refSensor(3)
            if(aux.rack4 == 1):
                self.plot_refSensor(4)
        if(aux.plotFlag4):
            if(aux.rack1 == 1):
                self.plot_refMediaG(1)
            if(aux.rack2 == 1):
                self.plot_refMediaG(2)
            if(aux.rack3 == 1):
                self.plot_refMediaG(3)
            if(aux.rack4 == 1):
                self.plot_refMediaG(4)
        if(aux.plotFlag5):
            if(aux.rack1 == 1):
                self.plot_refMediaI(1)
            if(aux.rack2 == 1):
                self.plot_refMediaI(2)
            if(aux.rack3 == 1):
                self.plot_refMediaI(3)
            if(aux.rack4 == 1):
                self.plot_refMediaI(4)
        if(aux.plotFlag6):
            if(aux.rack1 == 1):
                self.plot_refFixa(1)
            if(aux.rack2 == 1):
                self.plot_refFixa(2)
            if(aux.rack3 == 1):
                self.plot_refFixa(3)
            if(aux.rack4 == 1):
                self.plot_refFixa(4)


    def plot_abs(self, i):
        self.date = time.strftime("%Y_%m_%d", time.localtime()) #adquire data
        self.a = time.localtime()
        self.str_hora = time.mktime(self.a) 
        try:
            self.D = []
            self.T = []
            if(i==1):
                self.D = var.D1[-1]
                self.T = var.T1[-1]
            elif(i==2):
                self.D = var.D2[-1]
                self.T = var.T2[-1]
            elif(i==3):
                self.D = var.D3[-1]
                self.T = var.T3[-1]
            elif(i==4):
                self.D = var.D4[-1]
                self.T = var.T4[-1]
            """for k in range (8):
                self.D = np.append(self.D, float(self.valores[2+k]))
                self.T = np.append(self.T, float(self.valores[10+k]))"""
            #print('D:', self.D, '\nT', self.T)
        except:
            pass
        """lista criada para checar os checkPlots"""
        self.list_check = [var.ria.ui.checkPlot1_on, var.ria.ui.checkPlot2_on,var.ria.ui.checkPlot3_on,var.ria.ui.checkPlot4_on,
                           var.ria.ui.checkPlot5_on,var.ria.ui.checkPlot6_on,var.ria.ui.checkPlot7_on,var.ria.ui.checkPlot8_on,
                           var.ria.ui.checkPlot9_on, var.ria.ui.checkPlot10_on,var.ria.ui.checkPlot11_on,var.ria.ui.checkPlot12_on,
                           var.ria.ui.checkPlot13_on,var.ria.ui.checkPlot14_on,var.ria.ui.checkPlot15_on,var.ria.ui.checkPlot16_on]
        i = i - 1 #CORREÇÃO PARA USO NO INDICE DOS VETORES DE DADOS DO PLOT
        print("RACK"+str(i)+":"+str(self.str_hora))
        for j in range (8):
            if(self.list_check[(i*8)+j].isChecked()):
                if(aux.plotSet == "nivel"): #PLOT DE NIVEL
                    """Plota nivel"""
                    var.ria.ui.widget_on.Data[(i*16)+2*j].x = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+2*j].x,
                                self.str_hora)
                    var.ria.ui.widget_on.Data[(i*16)+2*j].y = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+2*j].y,
                                self.D[j+1])
                    """muda escala do eixo x"""
                    #print(var.ria.ui.widget_on.Data[i*(2*j)].x[-1])
                    self.menor = var.ria.ui.widget_on.Data[(i*16)+2*j].x[0]
                    for k in range(64):
                        try:
                            if(var.ria.ui.widget_on.Data[k].x[0] < self.menor):
                                self.menor = var.ria.ui.widget_on.Data[k].x[0]
                        except:
                            pass
                        
                    var.ria.ui.widget_on.setAxisScale(var.ria.ui.widget_on.xBottom,
                                                   self.menor,
                                                   var.ria.ui.widget_on.Data[(i*16)+2*j].x[-1])
                else: #PLOT DE TEMPERATURA
                    """Plota temperatura"""
                    #print(var.ria.ui.widget_on.Data[i*(2*j)].x[-1])
                    self.menor = var.ria.ui.widget_on.Data[(i*16)+2*j].x[0]
                    for k in range(64):
                        try:
                            if(var.ria.ui.widget_on.Data[k].x[0] < self.menor):
                                self.menor = var.ria.ui.widget_on.Data[k].x[0]
                        except:
                            pass
                        
                    var.ria.ui.widget_on.setAxisScale(var.ria.ui.widget_on.xBottom,
                                                   self.menor,
                                                   var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x[-1])
                """se o comprimento do vetor de dados for maior que limite, retira o valor mais antigo"""
                if(aux.flagCmp):
                    try:
                        if aux.plotSet == "nivel" and len(var.ria.ui.widget_on.Data[(i*16)+2*j].x) > var.cmp_on:
                            self.dif = len(var.ria.ui.widget_on.Data[(i*16)+2*j].x) - var.cmp_on
                            var.ria.ui.widget_on.Data[(i*16)+2*j].x = var.ria.ui.widget_on.Data[(i*16)+2*j].x[self.dif:]
                            var.ria.ui.widget_on.Data[(i*16)+2*j].y = var.ria.ui.widget_on.Data[(i*16)+2*j].y[self.dif:]
                        elif aux.plotSet == "temp" and len(var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x) > var.cmp_on:
                            self.dif = len(var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x) - var.cmp_on
                            var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x = var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x[self.dif:]
                            var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y = var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y[self.dif:]
                    except TypeError:
                        pass

    def plot_refSensor(self, i):
        self.date = time.strftime("%Y_%m_%d", time.localtime()) #adquire data
        #try:
        f = open('C:/users/rodrigo.neto/desktop/Software/rack'+str(i)+'_'+str(self.date)+'.dat', 'r')
        self.lines = f.readlines()
        self.valores = []
        self.valores = np.append(self.valores, self.lines[-1].split())
        f.close()
            #print(self.valores)
        """adquire hora certa"""
        self.a = time.localtime()
        self.str_hora = time.mktime(self.a)
        #self.hora = self.valores[1]
        #self.str_hora = self.date+' '+self.hora
        #a = time.strptime(self.str_hora, "%Y_%m_%d %H:%M:%S")
        #self.D[0] = time.mktime(a)
            
        """adquire leitura do sensor de referencia"""
        self.sensor_ref = var.ria.ui.plotBoxSens_on.currentText()
        for k in range(4):#Racks
            for j in range(8):#Sensores
                if(self.sensor_ref == var.disp_sensores[k][j]):
                    self.num_rack_sensor_ref = k+1
                    self.indice_sensor_ref = j
        if(self.num_rack_sensor_ref == i):
            if(i == 1):
                self.val_ref_D = var.D1[-1][1+self.indice_sensor_ref]
                self.val_ref_T = var.T1[-1][1+self.indice_sensor_ref]
            elif(i == 2):
                self.val_ref_D = var.D2[-1][1+self.indice_sensor_ref]
                self.val_ref_T = var.T2[-1][1+self.indice_sensor_ref]
            elif(i == 3):
                self.val_ref_D = var.D3[-1][1+self.indice_sensor_ref]
                self.val_ref_T = var.T3[-1][1+self.indice_sensor_ref]
            elif(i == 4):
                self.val_ref_D = var.D4[-1][1+self.indice_sensor_ref]
                self.val_ref_T = var.T4[-1][1+self.indice_sensor_ref]
        else:
            p = open('C:/users/rodrigo.neto/desktop/Software/rack'+str(self.num_rack_sensor_ref)+'_'+str(self.date)+'.dat', 'r')
            self.lines2 = p.readlines()
            self.valores2 = []
            self.valores2 = np.append(self.valores2, self.lines2[-1].split())
            #if(aux.plotSet == "nivel"):
            self.val_ref_D = self.valores2[2+self.indice_sensor_ref] #valor de referencia de nivel adquirido
            #else:
            self.val_ref_T = self.valores2[10+self.indice_sensor_ref] #valor de referencia de nivel adquirido
            p.close()
            
        #print(self.sensor_ref)
        #print(self.val_ref)
        self.D = []
        self.T = []
        if(i==1):
            #self.D = np.append(self.D, var.D1[-1])
            self.D = var.D1[-1]
            self.D[1:] = float(self.val_ref_D) - self.D[1:]
            self.T = var.T1[-1]
            self.T[1:] = float(self.val_ref_T) - var.T1[-1][1:]
        elif(i==2):
            self.D = var.D2[-1]
            self.D[1:] = float(self.val_ref_D) - var.D2[-1][1:]
            self.T = var.T2[-1]
            self.T[1:] = float(self.val_ref_T) - var.T2[-1][1:]
        elif(i==3):
            self.D = var.D3[-1]
            self.D[1:] = float(self.val_ref_D) - var.D3[-1][1:]
            self.T = var.T3[-1]
            self.T[1:] = float(self.val_ref_T) - var.T3[-1][1:]
        elif(i==4):
            self.D = var.D4[-1]
            self.D[1:] = float(self.val_ref_D) - var.D4[-1][1:]
            self.T = var.T4[-1]
            self.T[1:] = float(self.val_ref_T) - var.T4[-1][1:]
        """for k in range (8):
            if(aux.plotSet == "nivel"):
                self.D = np.append(self.D, abs(float(self.valores[2+k])-float(self.val_ref_D)))
            else:
                self.T = np.append(self.T, abs(float(self.valores[10+k])-float(self.val_ref_T)))"""
        print('D:', self.D, '\nT', self.T)
        #except:
            #pass
        """lista criada para checar os checkPlots"""
        self.list_check = [var.ria.ui.checkPlot1_on, var.ria.ui.checkPlot2_on,var.ria.ui.checkPlot3_on,var.ria.ui.checkPlot4_on,
                           var.ria.ui.checkPlot5_on,var.ria.ui.checkPlot6_on,var.ria.ui.checkPlot7_on,var.ria.ui.checkPlot8_on,
                           var.ria.ui.checkPlot9_on, var.ria.ui.checkPlot10_on,var.ria.ui.checkPlot11_on,var.ria.ui.checkPlot12_on,
                           var.ria.ui.checkPlot13_on,var.ria.ui.checkPlot14_on,var.ria.ui.checkPlot15_on,var.ria.ui.checkPlot16_on]
        i = i - 1 #correção para indices
        for j in range (8):
            if(self.list_check[(i*8)+j].isChecked()):
                if(aux.plotSet == "nivel"): #PLOT DE NIVEL
                    """Plota nivel"""
                    var.ria.ui.widget_on.Data[(i*16)+2*j].x = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+2*j].x,
                                self.str_hora)
                    var.ria.ui.widget_on.Data[(i*16)+2*j].y = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+2*j].y,
                                self.D[j+1])
                    """muda escala do eixo x"""
                    #print(var.ria.ui.widget_on.Data[i*(2*j)].x[-1])
                    self.menor = var.ria.ui.widget_on.Data[(i*16)+2*j].x[0]
                    for k in range(64):
                        try:
                            if(var.ria.ui.widget_on.Data[k].x[0] < self.menor):
                                self.menor = var.ria.ui.widget_on.Data[k].x[0]
                        except:
                            pass
                        
                    var.ria.ui.widget_on.setAxisScale(var.ria.ui.widget_on.xBottom,
                                                   self.menor,
                                                   var.ria.ui.widget_on.Data[(i*16)+2*j].x[-1])
                else: #PLOT DE TEMPERATURA
                    """Plota temperatura"""
                    var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x,
                                self.str_hora)
                    var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y,
                                self.T[j+1])
                    """muda escala do eixo x"""
                    #print(var.ria.ui.widget_on.Data[i*(2*j)].x[-1])
                    self.menor = var.ria.ui.widget_on.Data[(i*16)+2*j].x[0]
                    for k in range(64):
                        try:
                            if(var.ria.ui.widget_on.Data[k].x[0] < self.menor):
                                self.menor = var.ria.ui.widget_on.Data[k].x[0]
                        except:
                            pass
                        
                    var.ria.ui.widget_on.setAxisScale(var.ria.ui.widget_on.xBottom,
                                                   self.menor,
                                                   var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x[-1])
                """se o comprimento do vetor de dados for maior que limite, retira o valor mais antigo"""
                if(aux.flagCmp):
                    try:
                        if aux.plotSet == "nivel" and len(var.ria.ui.widget_on.Data[(i*16)+2*j].x) > var.cmp:
                            var.ria.ui.widget_on.Data[(i*16)+2*j].x = var.ria.ui.widget_on.Data[(i*16)+2*j].x[1:]
                            var.ria.ui.widget_on.Data[(i*16)+2*j].y = var.ria.ui.widget_on.Data[(i*16)+2*j].y[1:]
                        elif aux.plotSet == "temp" and len(var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x) > var.cmp:
                            var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x = var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x[1:]
                            var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y = var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y[1:]
                    except TypeError:
                        pass

    def plot_refMediaG(self, i):
        self.date = time.strftime("%Y_%m_%d", time.localtime()) #adquire data
        #try:
        f = open('C:/users/rodrigo.neto/desktop/Software/rack'+str(i)+'_'+str(self.date)+'.dat', 'r')
        self.lines = f.readlines()
        self.valores = []
        self.valores = np.append(self.valores, self.lines[-1].split())
        f.close()
            #print(self.valores)
        """adquire hora certa"""
        self.a = time.localtime()
        self.str_hora = time.mktime(self.a)
        #self.hora = self.valores[1]
        #self.str_hora = self.date+' '+self.hora
        #a = time.strptime(self.str_hora, "%Y_%m_%d %H:%M:%S")
        #self.D[0] = time.mktime(a)

        """adquire valor da média geral"""
        self.somaD = 0
        self.somaT = 0
        self.tam = 0
        if(aux.rack1_enable == 1):
            p = open('C:/users/rodrigo.neto/desktop/Software/rack1_'+str(self.date)+'.dat', 'r')
            self.lines2 = p.readlines()
            self.valores2 = []
            self.valores2 = np.append(self.valores2, self.lines2[-1].split())
            p.close()
            
            for j in range (8):
                if(aux.plotSet == "nivel"):
                    self.somaD = self.somaD + float(self.valores2[2+j])
                else:
                    self.somaT = self.somaT + float(self.valores2[10+j])
            self.tam = self.tam + 8
        if(aux.rack2_enable == 1):
            p = open('C:/users/rodrigo.neto/desktop/Software/rack2_'+str(self.date)+'.dat', 'r')
            self.lines2 = p.readlines()
            self.valores2 = []
            self.valores2 = np.append(self.valores2, self.lines2[-1].split())
            p.close()
            for j in range (8):
                if(aux.plotSet == "nivel"):
                    self.somaD = self.somaD + float(self.valores2[2+j])
                else:
                    self.somaT = self.somaT + float(self.valores2[10+j])
            self.tam = self.tam + 8
        if(aux.rack3_enable == 1):
            p = open('C:/users/rodrigo.neto/desktop/Software/rack3_'+str(self.date)+'.dat', 'r')
            self.lines2 = p.readlines()
            self.valores2 = []
            self.valores2 = np.append(self.valores2, self.lines2[-1].split())
            p.close()
            for j in range (8):
                if(aux.plotSet == "nivel"):
                    self.somaD = self.somaD + float(self.valores2[2+j])
                else:
                    self.somaT = self.somaT + float(self.valores2[10+j])
            self.tam = self.tam + 8
        if(aux.rack4_enable == 1):
            p = open('C:/users/rodrigo.neto/desktop/Software/rack4_'+str(self.date)+'.dat', 'r')
            self.lines2 = p.readlines()
            self.valores2 = []
            self.valores2 = np.append(self.valores2, self.lines2[-1].split())
            p.close()
            for j in range (8):
                if(aux.plotSet == "nivel"):
                    self.somaD = self.somaD + float(self.valores2[2+j])
                else:
                    self.somaT = self.somaT + float(self.valores2[10+j])
            self.tam = self.tam + 8

        self.mediaD = self.somaD/self.tam #MEDIA GERAL DE NIVEL OBTIDA
        self.mediaT = self.somaT/self.tam #MEDIA GERAL DE TERMPERATURA OBTIDA
        
        #print(self.sensor_ref)
        #print(self.val_ref)
        self.D = []
        self.T = []
        if(i==1):
            self.D = var.D1[-1]
            self.D[1:] = self.mediaD - self.D[1:]
            self.T = var.T1[-1]
            self.T[1:] = self.mediaT - self.T[1:]
        elif(i==2):
            self.D = var.D2[-1]
            self.D[1:] = self.mediaD - self.D[1:]
            self.T = var.T2[-1]
            self.T[1:] = self.mediaT - self.T[1:]
        elif(i==3):
            self.D = var.D3[-1]
            self.D[1:] = self.mediaD - self.D[1:]
            self.T = var.T3[-1]
            self.T[1:] = self.mediaT - self.T[1:]
        elif(i==4):
            self.D = var.D4[-1]
            self.D[1:] = self.mediaD - self.D[1:]
            self.T = var.T4[-1]
            self.T[1:] = self.mediaT - self.T[1:]
        """for k in range (8):
            self.D = np.append(self.D, abs(float(self.valores[2+k])-float(self.mediaD)))
            self.T = np.append(self.T, abs(float(self.valores[10+k])-float(self.mediaT)))"""
        print('D:', self.D, '\nT', self.T)
        #except:
            #pass
        """lista criada para checar os checkPlots"""
        self.list_check = [var.ria.ui.checkPlot1_on, var.ria.ui.checkPlot2_on,var.ria.ui.checkPlot3_on,var.ria.ui.checkPlot4_on,
                           var.ria.ui.checkPlot5_on,var.ria.ui.checkPlot6_on,var.ria.ui.checkPlot7_on,var.ria.ui.checkPlot8_on,
                           var.ria.ui.checkPlot9_on, var.ria.ui.checkPlot10_on,var.ria.ui.checkPlot11_on,var.ria.ui.checkPlot12_on,
                           var.ria.ui.checkPlot13_on,var.ria.ui.checkPlot14_on,var.ria.ui.checkPlot15_on,var.ria.ui.checkPlot16_on]
        i = i - 1 #adequação do numero do rack para facilitar na indexação dos valores na lista Data, do plot
        for j in range (8):
            if(self.list_check[(i*8)+j].isChecked()):
                if(aux.plotSet == "nivel"): #PLOT DE NIVEL
                    """Plota nivel"""
                    var.ria.ui.widget_on.Data[(i*16)+2*j].x = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+2*j].x,
                                self.str_hora)
                    var.ria.ui.widget_on.Data[(i*16)+2*j].y = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+2*j].y,
                                self.D[j+1])
                    """muda escala do eixo x"""
                    #print(var.ria.ui.widget_on.Data[i*(2*j)].x[-1])
                    self.menor = var.ria.ui.widget_on.Data[(i*16)+2*j].x[0]
                    for k in range(64):
                        try:
                            if(var.ria.ui.widget_on.Data[k].x[0] < self.menor):
                                self.menor = var.ria.ui.widget_on.Data[k].x[0]
                        except:
                            pass
                        
                    var.ria.ui.widget_on.setAxisScale(var.ria.ui.widget_on.xBottom,
                                                   self.menor,
                                                   var.ria.ui.widget_on.Data[(i*16)+2*j].x[-1])
                else: #PLOT DE TEMPERATURA
                    """Plota temperatura"""
                    var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x,
                                self.str_hora)
                    var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y,
                                self.T[j+1])
                    """muda escala do eixo x"""
                    #print(var.ria.ui.widget_on.Data[i*(2*j)].x[-1])
                    self.menor = var.ria.ui.widget_on.Data[(i*16)+2*j].x[0]
                    for k in range(64):
                        try:
                            if(var.ria.ui.widget_on.Data[k].x[0] < self.menor):
                                self.menor = var.ria.ui.widget_on.Data[k].x[0]
                        except:
                            pass
                        
                    var.ria.ui.widget_on.setAxisScale(var.ria.ui.widget_on.xBottom,
                                                   self.menor,
                                                   var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x[-1])
                """se o comprimento do vetor de dados for maior que limite, retira o valor mais antigo"""
                if(aux.flagCmp):
                    try:
                        if aux.plotSet == "nivel" and len(var.ria.ui.widget_on.Data[(i*16)+2*j].x) > var.cmp:
                            var.ria.ui.widget_on._onData[(i*16)+2*j].x = var.ria.ui.widget_on.Data[(i*16)+2*j].x[1:]
                            var.ria.ui.widget_on.Data[(i*16)+2*j].y = var.ria.ui.widget_on.Data[(i*16)+2*j].y[1:]
                        elif aux.plotSet == "temp" and len(var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x) > var.cmp:
                            var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x = var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x[1:]
                            var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y = var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y[1:]
                    except TypeError:
                        pass

    def plot_refMediaI(self, i):
        self.date = time.strftime("%Y_%m_%d", time.localtime()) #adquire data
        #try:
        f = open('C:/users/rodrigo.neto/desktop/Software/rack'+str(i)+'_'+str(self.date)+'.dat', 'r')
        self.lines = f.readlines()
        self.valores = []
        self.valores = np.append(self.valores, self.lines[-1].split())
        f.close()
            #print(self.valores)
        """adquire hora certa"""
        self.a = time.localtime()
        self.str_hora = time.mktime(self.a)
        #self.hora = self.valores[1]
        #self.str_hora = self.date+' '+self.hora
        #a = time.strptime(self.str_hora, "%Y_%m_%d %H:%M:%S")
        #self.D[0] = time.mktime(a)

        i = i - 1 #adequação do numero do rack para facilitar na indexação dos valores na lista Data, do plot
        """adquire valor da média individual"""
        #self.somaD = 0
        #self.somaT = 0
        if(aux.rack1_enable == 1):
            p = open('C:/users/rodrigo.neto/desktop/Software/rack1_'+str(self.date)+'.dat', 'r')
            self.lines2 = p.readlines()
            self.valores2 = []
            self.valores2 = np.append(self.valores2, self.lines2[-1].split())
            p.close()
            for j in range (8):
                if(aux.plotSet == "nivel"):
                    aux.somaD1[j] = aux.somaD1[j] + float(self.valores2[2+j])
                else:
                    aux.somaT1[j] = aux.somaT1[j] + float(self.valores2[10+j])
            aux.somaD1[8] += 1 #soma de valores indivuais que ja foram computados
            aux.somaT1[8] += 1 #soma de valores indivuais que ja foram computados
        if(aux.rack2_enable == 1):
            p = open('C:/users/rodrigo.neto/desktop/Software/rack2_'+str(self.date)+'.dat', 'r')
            self.lines2 = p.readlines()
            self.valores2 = []
            self.valores2 = np.append(self.valores2, self.lines2[-1].split())
            p.close()
            for j in range (8):
                if(aux.plotSet == "nivel"):
                    aux.somaD2[j] = aux.somaD2[j] + float(self.valores2[2+j])
                else:
                    aux.somaT2[j] = aux.somaT2[j] + float(self.valores2[10+j])
            aux.somaD2[8] += 1 #soma de valores indivuais que ja foram computados
            aux.somaT2[8] += 1 #soma de valores indivuais que ja foram computados
        if(aux.rack3_enable == 1):
            p = open('C:/users/rodrigo.neto/desktop/Software/rack3_'+str(self.date)+'.dat', 'r')
            self.lines2 = p.readlines()
            self.valores2 = []
            self.valores2 = np.append(self.valores2, self.lines2[-1].split())
            p.close()
            for j in range (8):
                if(aux.plotSet == "nivel"):
                    aux.somaD3[j] = aux.somaD3[j] + float(self.valores2[2+j])
                else:
                    aux.somaT3[j] = aux.somaT3[j] + float(self.valores2[10+j])
            aux.somaD3[8] += 1 #soma de valores indivuais que ja foram computados
            aux.somaT3[8] += 1 #soma de valores indivuais que ja foram computados
        if(aux.rack4_enable == 1):
            p = open('C:/users/rodrigo.neto/desktop/Software/rack1_'+str(self.date)+'.dat', 'r')
            self.lines2 = p.readlines()
            self.valores2 = []
            self.valores2 = np.append(self.valores2, self.lines2[-1].split())
            p.close()
            for j in range (8):
                if(aux.plotSet == "nivel"):
                    aux.somaD4[j] = aux.somaD4[j] + float(self.valores2[2+j])
                else:
                    aux.somaT4[j] = aux.somaT4[j] + float(self.valores2[10+j])
            aux.somaD4[8] += 1 #soma de valores indivuais que ja foram computados
            aux.somaT4[8] += 1 #soma de valores indivuais que ja foram computados

        self.mediaD1 = []
        self.mediaT1 = []
        self.mediaD2 = []
        self.mediaT2 = []
        self.mediaD3 = []
        self.mediaT3 = []
        self.mediaD4 = []
        self.mediaT4 = []
        for k  in range (8):
            if(aux.rack1_enable == 1):
                self.mediaD1 = np.append(self.mediaD1, aux.somaD1[k]/aux.somaD1[8])#MEDIAS INDIVIDUAIS DE NIVEL OBTIDAS (EM RELAÇÃO A CADA RACK)
                self.mediaT1 = np.append(self.mediaT1, aux.somaT1[k]/aux.somaT1[8])#MEDIAS INDIVIDUAIS DE TEMP OBTIDAS (EM RELAÇÃO A CADA RACK)
            if(aux.rack2_enable == 1):
                self.mediaD2 = np.append(self.mediaD2, aux.somaD2[k]/aux.somaD2[8])
                self.mediaT2 = np.append(self.mediaT2, aux.somaT2[k]/aux.somaT2[8])
            if(aux.rack3_enable == 1):
                self.mediaD3 = np.append(self.mediaD3, aux.somaD3[k]/aux.somaD3[8])
                self.mediaT3 = np.append(self.mediaT3, aux.somaT3[k]/aux.somaT3[8])
            if(aux.rack4_enable == 1):
                self.mediaD4 = np.append(self.mediaD4, aux.somaD4[k]/aux.somaD4[8])
                self.mediaT4 = np.append(self.mediaT4, aux.somaT4[k]/aux.somaT4[8])
            
        #self.mediaD = self.somaD/self.tam #MEDIA GERAL DE NIVEL OBTIDA
        #self.mediaT = self.somaT/self.tam #MEDIA GERAL DE TERMPERATURA OBTIDA
        
        #print(self.sensor_ref)
        #print(self.val_ref)
        self.D = []
        self.T = []
        for k in range (8):
            if(i==0):#Se Rack1
                self.D = np.append(self.D, float(self.mediaD1[k])-float(var.D1[-1][k]))
                self.T = np.append(self.T, float(self.mediaT1[k])-float(var.T1[-1][k]))
                #self.D = np.append(self.D, abs(float(self.valores[2+k])-float(self.mediaD1[k])))
                #self.T = np.append(self.T, abs(float(self.valores[10+k])-float(self.mediaT1[k])))
            if(i==1):#Se Rack2
                self.D = np.append(self.D, float(self.mediaD2[k])-float(var.D2[-1][k]))
                self.T = np.append(self.T, float(self.mediaT2[k])-float(var.T2[-1][k]))
            if(i==2):#Se Rack3
                self.D = np.append(self.D, float(self.mediaD3[k])-float(var.D3[-1][k]))
                self.T = np.append(self.T, float(self.mediaT3[k])-float(var.T3[-1][k]))
            if(i==3):#Se Rack4
                self.D = np.append(self.D, float(self.mediaD4[k])-float(var.D4[-1][k]))
                self.T = np.append(self.T, float(self.mediaT4[k])-float(var.T4[-1][k]))
        print('D:', self.D, '\nT', self.T)
        #except:
            #pass
        """lista criada para checar os checkPlots"""
        self.list_check = [var.ria.ui.checkPlot1_on, var.ria.ui.checkPlot2_on,var.ria.ui.checkPlot3_on,var.ria.ui.checkPlot4_on,
                           var.ria.ui.checkPlot5_on,var.ria.ui.checkPlot6_on,var.ria.ui.checkPlot7_on,var.ria.ui.checkPlot8_on,
                           var.ria.ui.checkPlot9_on, var.ria.ui.checkPlot10_on,var.ria.ui.checkPlot11_on,var.ria.ui.checkPlot12_on,
                           var.ria.ui.checkPlot13_on,var.ria.ui.checkPlot14_on,var.ria.ui.checkPlot15_on,var.ria.ui.checkPlot16_on]
        for j in range (8):
            if(self.list_check[(i*8)+j].isChecked()):
                if(aux.plotSet == "nivel"): #PLOT DE NIVEL
                    """Plota nivel"""
                    var.ria.ui.widget_on.Data[(i*16)+2*j].x = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+2*j].x,
                                self.str_hora)
                    var.ria.ui.widget_on.Data[(i*16)+2*j].y = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+2*j].y,
                                self.D[j+1])
                    """muda escala do eixo x"""
                    #print(var.ria.ui.widget_on.Data[i*(2*j)].x[-1])
                    self.menor = var.ria.ui.widget_on.Data[(i*16)+2*j].x[0]
                    for k in range(64):
                        try:
                            if(var.ria.ui.widget_on.Data[k].x[0] < self.menor):
                                self.menor = var.ria.ui.widget_on.Data[k].x[0]
                        except:
                            pass
                        
                    var.ria.ui.widget_on.setAxisScale(var.ria.ui.widget_on.xBottom,
                                                   self.menor,
                                                   var.ria.ui.widget_on.Data[(i*16)+2*j].x[-1])
                else: #PLOT DE TEMPERATURA
                    """Plota temperatura"""
                    var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x,
                                self.str_hora)
                    var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y,
                                self.T[j+1])
                    """muda escala do eixo x"""
                    #print(var.ria.ui.widget_on.Data[i*(2*j)].x[-1])
                    self.menor = var.ria.ui.widget_on.Data[(i*16)+2*j].x[0]
                    for k in range(64):
                        try:
                            if(var.ria.ui.widget_on.Data[k].x[0] < self.menor):
                                self.menor = var.ria.ui.widget_on.Data[k].x[0]
                        except:
                            pass
                        
                    var.ria.ui.widget_on.setAxisScale(var.ria.ui.widget_on.xBottom,
                                                   self.menor,
                                                   var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x[-1])
                """se o comprimento do vetor de dados for maior que limite, retira o valor mais antigo"""
                if(aux.flagCmp):
                    try:
                        if aux.plotSet == "nivel" and len(var.ria.ui.widget_on.Data[(i*16)+2*j].x) > var.cmp:
                            var.ria.ui.widget_on.Data[(i*16)+2*j].x = var.ria.ui.widget_on.Data[(i*16)+2*j].x[1:]
                            var.ria.ui.widget_on.Data[(i*16)+2*j].y = var.ria.ui.widget_on.Data[(i*16)+2*j].y[1:]
                        elif aux.plotSet == "temp" and len(var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x) > var.cmp:
                            var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x = var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x[1:]
                            var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y = var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y[1:]
                    except TypeError:
                        pass


    def plot_refFixa(self, i):
        """self.date = time.strftime("%Y_%m_%d", time.localtime()) #adquire data
        #try:
        f = open('C:/users/rodrigo.neto/desktop/Software/rack'+str(i)+'_'+str(self.date)+'.dat', 'r')
        self.lines = f.readlines()
        self.valores = []
        self.valores = np.append(self.valores, self.lines[-1].split())
        f.close()"""
            #print(self.valores)
        """adquire hora atual"""
        self.a = time.localtime()
        self.str_hora = time.mktime(self.a)

        #print(self.sensor_ref)
        #print(self.val_ref)
        self.D = []
        self.T = []
        if(i==1):
            #self.D = np.append(self.D, var.D1[-1])
            self.D = np.append(self.D, var.D1[-1][0])
            self.D = np.append(self.D, aux.refD1 - var.D1[-1][1:])
           # self.T[0] = var.T1[-1][0]
           # self.T[1:] = aux.refT1 - var.T1[-1][1:]
        elif(i==2):
            self.D[0] = var.D2[-1][0]
            self.D[1:] = aux.refD2 - var.D2[-1][1:]
            self.T[0] = var.T2[-1][0]
            self.T[1:] = aux.refT2 - var.T2[-1][1:]
        elif(i==3):
            self.D[0] = var.D3[-1][0]
            self.D[1:] = aux.refD3 - var.D3[-1][1:]
            self.T[0] = var.T3[-1][0]
            self.T[1:] = aux.refT3 - var.T3[-1][1:]
        elif(i==4):
            self.D[0] = var.D4[-1][0]
            self.D[1:] = aux.refD4 - var.D4[-1][1:]
            self.T[0] = var.T4[-1][0]
            self.T[1:] = aux.refT4 - var.T4[-1][1:]
        """for k in range (8):
            if(aux.plotSet == "nivel"):
                self.D = np.append(self.D, abs(float(self.valores[2+k])-float(self.val_ref_D)))
            else:
                self.T = np.append(self.T, abs(float(self.valores[10+k])-float(self.val_ref_T)))"""
        print('D:', self.D, '\nT', self.T)
        #except:
            #pass
        """lista criada para checar os checkPlots"""
        self.list_check = [var.ria.ui.checkPlot1_on, var.ria.ui.checkPlot2_on,var.ria.ui.checkPlot3_on,var.ria.ui.checkPlot4_on,
                           var.ria.ui.checkPlot5_on,var.ria.ui.checkPlot6_on,var.ria.ui.checkPlot7_on,var.ria.ui.checkPlot8_on,
                           var.ria.ui.checkPlot9_on, var.ria.ui.checkPlot10_on,var.ria.ui.checkPlot11_on,var.ria.ui.checkPlot12_on,
                           var.ria.ui.checkPlot13_on,var.ria.ui.checkPlot14_on,var.ria.ui.checkPlot15_on,var.ria.ui.checkPlot16_on]
        i = i - 1 #correção para indices
        for j in range (8):
            if(self.list_check[(i*8)+j].isChecked()):
                if(aux.plotSet == "nivel"): #PLOT DE NIVEL
                    """Plota nivel"""
                    var.ria.ui.widget_on.Data[(i*16)+2*j].x = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+2*j].x,
                                self.str_hora)
                    var.ria.ui.widget_on.Data[(i*16)+2*j].y = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+2*j].y,
                                self.D[j+1])
                    """muda escala do eixo x"""
                    #print(var.ria.ui.widget_on.Data[i*(2*j)].x[-1])
                    self.menor = var.ria.ui.widget_on.Data[(i*16)+2*j].x[0]
                    for k in range(64):
                        try:
                            if(var.ria.ui.widget_on.Data[k].x[0] < self.menor):
                                self.menor = var.ria.ui.widget_on.Data[k].x[0]
                        except:
                            pass
                        
                    var.ria.ui.widget_on.setAxisScale(var.ria.ui.widget_on.xBottom,
                                                   self.menor,
                                                   var.ria.ui.widget_on.Data[(i*16)+2*j].x[-1])
                else: #PLOT DE TEMPERATURA
                    """Plota temperatura"""
                    var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x,
                                self.str_hora)
                    var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y = np.append(
                                var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y,
                                self.T[j+1])
                    """muda escala do eixo x"""
                    #print(var.ria.ui.widget_on.Data[i*(2*j)].x[-1])
                    self.menor = var.ria.ui.widget_on.Data[(i*16)+2*j].x[0]
                    for k in range(64):
                        try:
                            if(var.ria.ui.widget_on.Data[k].x[0] < self.menor):
                                self.menor = var.ria.ui.widget_on.Data[k].x[0]
                        except:
                            pass
                        
                    var.ria.ui.widget_on.setAxisScale(var.ria.ui.widget_on.xBottom,
                                                   self.menor,
                                                   var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x[-1])
                """se o comprimento do vetor de dados for maior que limite, retira o valor mais antigo"""
                if(aux.flagCmp):
                    try:
                        if aux.plotSet == "nivel" and len(var.ria.ui.widget_on.Data[(i*16)+2*j].x) > var.cmp:
                            var.ria.ui.widget_on.Data[(i*16)+2*j].x = var.ria.ui.widget_on.Data[(i*16)+2*j].x[1:]
                            var.ria.ui.widget_on.Data[(i*16)+2*j].y = var.ria.ui.widget_on.Data[(i*16)+2*j].y[1:]
                        elif aux.plotSet == "temp" and len(var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x) > var.cmp:
                            var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x = var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].x[1:]
                            var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y = var.ria.ui.widget_on.Data[(i*16)+(2*j+1)].y[1:]
                    except TypeError:
                        pass
##############END-PLOTS#####################

    def setScalePlot(self):
        #SimplePlot(var.ria.ui.widget_on).__init__
        #var.ria.ui.widget_on = alignScales()
        
        aux.scaleMinY = var.ria.ui.logMinY.textCursor()
        aux.scaleMinY = var.ria.ui.logMinY.toPlainText()
        aux.scaleMaxY = var.ria.ui.logMaxY.textCursor()
        aux.scaleMaxY = var.ria.ui.logMaxY.toPlainText()
        aux.scaleMinX = var.ria.ui.logMinX.textCursor()
        aux.scaleMinX= var.ria.ui.logMinX.toPlainText()
        aux.scaleMaxX = var.ria.ui.logMaxX.textCursor()
        aux.scaleMaxX = var.ria.ui.logMaxX.toPlainText()

        #self.date = time.strftime("%Y_%m_%d", time.localtime())
        self.date = var.ria.ui.logDate.textCursor()
        self.date = var.ria.ui.logDate.toPlainText()
        self.str_horaMin = self.date+' '+aux.scaleMinX
        #a = time.strptime(self.str_horaMin, "%Y_%m_%d %H:%M:%S")
        a = time.strptime(self.str_horaMin, "%d/%m/%Y %H:%M:%S")
        self.flt_horaMin = time.mktime(a)
        self.str_horaMax = self.date+' '+aux.scaleMaxX
        a = time.strptime(self.str_horaMax, "%d/%m/%Y %H:%M:%S")
        self.flt_horaMax = time.mktime(a)
        
        #print(aux.scaleMin)
        var.ria.ui.widget_on.setAxisScale(0, float(aux.scaleMinY), float(aux.scaleMaxY))
        var.ria.ui.widget_on.setAxisScale(2, self.flt_horaMin, self.flt_horaMax)
        #var.ria.ui.widget_on.setAxisAutoScale(0)

    def setAutoScalePlot(self):
        var.ria.ui.widget_on.setAxisAutoScale(0)
        var.ria.ui.widget_on.setAxisAutoScale(2)

#Declaracao inicial das variaveis globais
    def globais(self):
        global flag_play
        flag_play=True
        global flag_ini
        flag_ini=True
        global vel_play
        vel_play=1
        global global_dia_ini
        global_dia_ini=0
        global global_mes_ini
        global_mes_ini=0
        global global_ano_ini
        global_ano_ini=0
        global global_dia_fim
        global_dia_fim=0
        global global_mes_fim
        global_mes_fim=0
        global global_ano_fim
        global_ano_fim=0
        global global_dia
        global_dia=0
        global global_mes
        global_mes=0
        global global_ano
        global_ano=0
        global flag_control
        flag_control=0
        self.D = [11.21, 6.5, 5, 7.8, 2.1, 2.2, 8.76, 7.6, 9]
        self.T = [23.00, 23, 24, 25, 26, 27, 28, 29, 30]


#funcao para renomear arquivos gerados pelo HLS no formato adequado de ordenacao
    def filesRename(self):
        #gera lista ordenada de arquivos
        mypath="C:/users/rodrigo.neto/Desktop/desktop/Software/"
        onlyfiles = sorted([f for f in listdir(mypath) if isfile(join(mypath, f))])
        os.chdir("C:/users/rodrigo.neto/Desktop/HLS-BancadaMETRO/dados-bancada-IMAS/")

        #renomeia arquivos HLS_dd_mm_aaaa.TXT para o formato HLS_aaaa_mm_dd.TXT
        for i in range(0, len(onlyfiles)):
            string=onlyfiles[i]
            if ((len(string) > 6) and (string[0:3]=="HLS") and (string[6] == '_')):
                pos=string.index('_',0)
                dia=string[(pos+1):(pos+3)]
                pos+=1
                pos=string.index('_',pos)
                mes=string[(pos+1):(pos+3)]
                pos+=1
                pos=string.index('_',pos)
                ano=string[(pos+1):(pos+5)]
                string="HLS_"+ano+"_"+mes+"_"+dia+".TXT"
                os.rename(onlyfiles[i],string)
        #os.rename(onlyfiles[0],"Teste.txt")
        os.chdir("C:/users/rodrigo.neto/Desktop/Software/")

    #converte mes no formato de 3 caracteres para numero
    def ReturnMonth(self, string):
        if string == 'jan':
            return 1
        elif string == 'fev':
            return 2
        elif string == 'mar':
            return 3
        elif string == 'abr':
            return 4
        elif string == 'mai':
            return 5
        elif string == 'jun':
            return 6
        elif string == 'jul':
            return 7
        elif string == 'ago':
            return 8
        elif string == 'set':
            return 9
        elif string == 'out':
            return 10
        elif string == 'nov':
            return 11
        elif string == 'dez':
            return 12

    #Ao clique do botao "data inicial" define ponto de partida
    def getData_ini(self):
        global global_dia_ini
        global global_mes_ini
        global global_ano_ini

        global_dia_ini=global_dia
        global_mes_ini=global_mes
        global_ano_ini=global_ano
        print (global_dia_ini)
        print (global_mes_ini)
        var.ria.ui.logOutput.insertPlainText("Data Inicial: " + str(global_dia_ini) + "\\" + str(global_mes_ini) + "\\" + str(global_ano_ini) + '\n')

    #Ao clique do botao "data final" define ponto de parada
    def getData_fim(self):
            global global_dia_fim
            global global_mes_fim
            global global_ano_fim
            global_dia_fim=global_dia
            global_mes_fim=global_mes
            global_ano_fim=global_ano
            print (global_dia_fim)
            print (global_mes_fim)
            var.ria.ui.logOutput.insertPlainText("Data Final: " + str(global_dia_fim) + "\\" + str(global_mes_fim) + "\\" + str(global_ano_fim) + '\n')

    #Funcao para tratar o comando play
    def Play(self):
        global flag_play
        global flag_ini
        global flag_control
        global global_dia_fim
        global global_mes_fim
        global global_ano_fim
        global global_dia_ini
        global global_mes_ini
        global global_ano_ini

        self.filesRename()
	#Nao inicia ateh que seja selecionado um intervalo valido
        if (global_dia_ini==0 or global_mes_ini==0 or global_ano_ini==0 or global_dia_fim==0 or global_mes_fim==0 or global_ano_fim==0):
            var.ria.ui.logOutput.insertPlainText("Selecione um intervalo valido de analise. \n")
            return
        elif ((global_mes_ini > global_mes_fim) or (global_ano_ini > global_ano_fim)):
            var.ria.ui.logOutput.insertPlainText("Selecione um intervalo valido de analise. \n")
            return
        elif (global_mes_ini == global_mes_fim):
            if (global_dia_ini > global_dia_fim):
                var.ria.ui.logOutput.insertPlainText("Selecione um intervalo valido de analise. \n")
                return

        #Primeira execucao do comando play
        if (flag_play):
            if (flag_ini):
                var.ria.ui.logOutput.insertPlainText("Iniciando Analise. Periodo entre: " + str(global_dia_ini) + "\\" + str(global_mes_ini) + "\\" + str(global_ano_ini) + " e " + str(global_dia_fim) + "\\" + str(global_mes_fim) + "\\" + str(global_ano_fim) + '\n')
                flag_ini=False

                if (global_dia_ini < 10):
                    charDiaIni="0"+str(global_dia_ini)
                else:
                    charDiaIni=str(global_dia_ini)
                    if (global_mes_ini < 10):
                        charMesIni="0"+str(global_mes_ini)
                    else:
                        charMesIni=str(global_mes_ini)

                    if (global_dia_fim < 10):
                        charDiaFim="0"+str(global_dia_ini)
                    else:
                        charDiaFim=str(global_dia_fim)
                    if (global_mes_fim < 10):
                        charMesFim="0"+str(global_mes_fim)
                    else:
                        charMesFim=str(global_mes_fim)

                fileIni="HLS_" + str(global_ano_ini) + "_" + charMesIni + "_" + charDiaIni + ".TXT"
                fileFim="HLS_" + str(global_ano_fim) + "_" + charMesFim + "_" + charDiaFim + ".TXT"
                if (var.ria.ui.Dlg[0] == "Variacao Media individual"):
                    HLS_plot2(fileIni, fileFim)
                elif (var.ria.ui.Dlg[0] == "Variacao por referencia"):
                    HLS_plot1(fileIni, fileFim, self.DlgRef[0])
                elif (var.ria.ui.Dlg[0] == "Valor Absoluto"):
                    HLS_plot3(fileIni, fileFim)
                elif (var.ria.ui.Dlg[0] == "Variacao Diaria"):
                    HLS_plot4(fileIni, fileFim)
                #time.sleep(1)
                #pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/HLS.png"))
	
                flag_control=1
                var.ria.ui.btn_play.setIcon(QtGui.QIcon('pause.jpg'))
                var.ria.ui.btn_play.setIconSize(QtCore.QSize(45,45))
        #Execussoes sucessivas do comando play
        else:
            flag_control=0
            btn_play.setIcon(QtGui.QIcon('play.jpg'))
            btn_play.setIconSize(QtCore.QSize(45,45))
        flag_play=not(flag_play)

	
    def Stop(self):
        global vel_play
        global flag_ini
        global flag_play
        global global_dia_ini
        global global_mes_ini
        global global_ano_ini
        global global_dia_fim
        global global_mes_fim
        global global_ano_fim
        global global_dia
        global global_mes
        global global_ano
        global flag_control
        var.ria.ui.logOutput.clear()
        var.ria.ui.logOutput.insertPlainText("Analise de dados - HLS Fogale" + '\n')
        var.ria.ui.logOutput.insertPlainText("Selecione no calendario o intervalo desejado para analise" + '\n')
        flag_play=True
        flag_ini=True
        vel_play=1
        global_dia_ini=0
        global_mes_ini=0
        global_ano_ini=0
        global_dia_fim=0
        global_mes_fim=0
        global_ano_fim=0
        global_dia=0
        global_mes=0
        global_ano=0
        flag_control=0
        var.ria.ui.btn_play.setIcon(QtGui.QIcon('play.jpg'))
        var.ria.ui.Dlg = QInputDialog.getItem(None,"Define Metodo","Selecione forma de analise", ["Variacao Media individual", "Variacao por referencia", "Valor Absoluto", "Variacao Diaria"])
	

    def showDate(self, date):
        global global_dia
        global global_mes
        global global_ano
#	print date
        aux=date.toString() ####pode precisar do SELF
        print (aux)
#	print aux
        global_dia=int(aux[8:10])
#	print aux[4:7]
        global_mes=self.ReturnMonth(aux[4:7])
#	print global_mes
        global_ano=aux[(len(aux)-4):len(aux)]
        print (global_ano)


class Plot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    def callback(self):
        self._stop()
    def run(self):
        global tam_D1
        global tam_D2
        global tam_D3
        global tam_D4
        tam_D1 = 0
        tam_D2 = 0
        tam_D3 = 0
        tam_D4 = 0
        param = open('C:/users/rodrigo.neto/desktop/Software/parameters.dat', 'r')
        self.lines = param.readlines()
        self.date = time.strftime("%Y_%m_%d", time.localtime()) #adquire data
        if(self.lines[3]=='True\n'):
            #self.rack1info = os.stat('C:/users/rodrigo.neto/desktop/Software/rack1_'+self.date+'.dat')
            #aux.tam_arq1_ant = self.rack1info.st_size
            aux.rack1_enable = 1
        else:
            aux.rack1_enable = 0
        if(self.lines[4]=='True\n'):
            aux.rack2_enable = 1
        else:
            aux.rack2_enable = 0
        if(self.lines[5]=='True\n'):
            aux.rack3_enable = 1
        else:
            aux.rack3_enable = 0
        if(self.lines[6]=='True\n'):
            aux.rack4_enable = 1
        else:
            aux.rack4_enable = 0
        while aux.plotFlag:
            plot.plot_call()
        
plot = PlotOnOff()

#if __name__ == "__main__":
#   telas = Screen()
