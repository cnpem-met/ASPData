#! /usr/bin/env python
# ESTA VERSÃO PLOTA GRAFICOS COM AS OPÇÕES DE REFEERNCIAS
#
import datetime, time, sys, threading
import numpy as np
import matplotlib.pyplot as plt
from qwt import QwtPlot as Qwt
from os import listdir
from Variables import var
from Plot_definitions import dataclass
from PyQt5 import QtGui, QtWidgets

class PlotOnOff:
    def __init__(self):
        self.data_ini = ""
        self.data_fim = ""
        self.data = ""
        self.flagPlot_off = False
        self.plotSet = "nivel"
        #self.plotBox_act()

    """ Define between level and temperature variable to be plotted """
    def plotBox_act(self):
        # plot level
        if var.ria.ui.plotBox_on.currentIndex() == 0:
            self.plotSet = "nivel"
            var.ria.ui.widget_on.setAxisTitle(Qwt.QwtPlot.yLeft, 'Height [mm]')
        else:
            # plot temperature
            self.plotSet = "temp"
            var.ria.ui.widget_on.setAxisTitle(Qwt.QwtPlot.yLeft, 'Temperature [ºC]')

    def plotBox_dataAct(self):
        self.currentDate = var.ria.ui.plotBox_data.currentText()

    """ generate a menu with the last 5 past days to choose plotting """
    def set_dataList(self):
        self.listData = []
        for i in range (5):
            self.listData = np.append(self.listData,
                                      time.strftime("%d/%m/%Y", time.localtime(time.mktime(time.localtime())-(i*83400))))
        var.ria.ui.plotBox_data.addItems(self.listData)

    """ defines the number of plot points """
    def set_cmp_on(self):
        var.cmp_on = var.ria.ui.cmp_on.value()

   # seta valores de referencia com botao 'Set Ref'
    def setRef_on(self):
        if(var.rack1 == 1):
            var.refD1 = var.D1[-1][1:]
            var.refSet = True
            # teste de nova referencia, em relação ao shift inicial no plot de refSensor ##
            try:
                self.shiftSensD1 = var.refD1 - self.val_ref_D
            except:
                pass
            var.ria.ui.logOutput_on.insertPlainText("Referency values: " +
                                                    str(var.refD1)+', time: ' +
                                                    time.strftime("%H:%M:%S", time.localtime(var.D1[-1][0]))+'\n')
        if(var.rack2 == 1):
            var.refD2 = var.D2[-1][1:]
            var.refSet = True
            var.ria.ui.logOutput_on.insertPlainText("Referency values: " +
                                                    str(var.refD2)+', time: ' +
                                                    time.strftime("%H:%M:%S", time.localtime(var.D1[-1][0]))+'\n')
        if(var.rack3 == 1):
            var.refD3 = var.D3[-1][1:]
            var.refSet = True
            var.ria.ui.logOutput_on.insertPlainText("Referency values: " +
                                                    str(var.refD3)+', time: ' +
                                                    time.strftime("%H:%M:%S", time.localtime(var.D1[-1][0]))+'\n')
        if(var.rack4 == 1):
            var.refD4 = var.D4[-1][1:]
            var.refSet = True
            var.ria.ui.logOutput_on.insertPlainText("Referency values: " +
                                                    str(var.refD4)+', time: ' +
                                                    time.strftime("%H:%M:%S", time.localtime(var.D1[-1][0]))+'\n')

    def set_plot_on(self, j):
        self.checkPlot_list = [var.ria.ui.checkPlot1_on, var.ria.ui.checkPlot2_on, var.ria.ui.checkPlot3_on, var.ria.ui.checkPlot4_on,
                                var.ria.ui.checkPlot5_on, var.ria.ui.checkPlot6_on, var.ria.ui.checkPlot7_on, var.ria.ui.checkPlot8_on,
                                var.ria.ui.checkPlot9_on, var.ria.ui.checkPlot10_on, var.ria.ui.checkPlot11_on, var.ria.ui.checkPlot12_on,
                                var.ria.ui.checkPlot13_on, var.ria.ui.checkPlot14_on, var.ria.ui.checkPlot15_on, var.ria.ui.checkPlot16_on]
        if(not self.checkPlot_list[j].isChecked()):
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget_on.Plots[j].setTitle("")
            var.ria.ui.widget_on.Data[j] = dataclass()
        else:
            """muda nome do plot e zera valores"""
            var.ria.ui.widget_on.Plots[j].setTitle(var.disp_sensores[int(j/8)][j%8])
            var.ria.ui.widget_on.Data[j] = dataclass()

    # def startPlot_absBoxes(self):
    #     var.plotFlag = True
    #     self.plotType_on = "absBoxes"
    #     var.ria.ui.logOutput_on.insertPlainText("Selected reference: Raw Value\n")
    #     var.ria.ui.logOutput_on.moveCursor(QTextCursor.End)
    #
    # def startPlot_abs(self):
    #     var.plotFlag = True
    #     self.plotType_on = "abs"
    #     var.ria.ui.logOutput_on.insertPlainText("Selected reference: Raw Value\n")
    #     var.ria.ui.logOutput_on.moveCursor(QTextCursor.End)
    #
    # def startPlot_refSensor(self):
    #     var.plotFlag = True
    #     self.plotType_on = "refSensor"
    #     var.ria.ui.logOutput_on.insertPlainText("Selected reference: Specific Sensor\n")
    #     var.ria.ui.logOutput_on.moveCursor(QTextCursor.End)
    #
    # def startPlot_refMediaG(self):
    #     var.plotFlag = True
    #     self.plotType_on = "refMediaG"
    #     var.ria.ui.logOutput_on.insertPlainText("Selected reference: Overall Mean\n")
    #     var.ria.ui.logOutput_on.moveCursor(QTextCursor.End)
    #
    # def startPlot_refMediaI(self):
    #     var.plotFlag = True
    #     self.plotType_on = "refMediaI"
    #     var.ria.ui.logOutput_on.insertPlainText("Selected reference: Local Mean\n")
    #     var.ria.ui.logOutput_on.moveCursor(QTextCursor.End)
    #
    # def startPlot_refFixa(self):
    #     var.plotFlag = True
    #     self.plotType_on = "refFixa"
    #     var.ria.ui.logOutput_on.insertPlainText("Selected reference: Time Fixed Data\n")
    #     var.ria.ui.logOutput_on.moveCursor(QTextCursor.End)

    def startPlot_on (self):
        if(var.ria.ui.refBox_on.currentIndex() == 0):
            var.ria.ui.logOutput_on.insertPlainText("Selected reference: Raw Value\n")
            var.ria.ui.logOutput_on.moveCursor(QtGui.QTextCursor.End)
        elif(var.ria.ui.refBox_on.currentIndex() == 2):
            var.ria.ui.logOutput_on.insertPlainText("Selected reference: Specific Sensor\n")
            var.ria.ui.logOutput_on.moveCursor(QtGui.QTextCursor.End)
        elif(var.ria.ui.refBox_on.currentIndex() == 3):
            var.ria.ui.logOutput_on.insertPlainText("Selected reference: Overall Mean\n")
            var.ria.ui.logOutput_on.moveCursor(QtGui.QTextCursor.End)
        elif(var.ria.ui.refBox_on.currentIndex() == 4):
            var.ria.ui.logOutput_on.insertPlainText("Selected reference: Local Mean\n")
            var.ria.ui.logOutput_on.moveCursor(QtGui.QTextCursor.End)
        elif(var.ria.ui.refBox_on.currentIndex() == 1 and var.refSet):
            var.ria.ui.logOutput_on.insertPlainText("Selected reference: Time Fixed Data\n")
            var.ria.ui.logOutput_on.moveCursor(QtGui.QTextCursor.End)
        else:
            QtWidgets.QMessageBox.information(var.ria, "Plot error","Error in plot. Please, push the Set time ref. button before start plot in this mode.")
            return
        var.plotFlag = True

    def stopPlot_on(self):
        var.plotFlag = False

    def plot_call(self):
        self.str_hora = time.mktime(time.localtime())
        # call function to plot raw data
        if(var.ria.ui.refBox_on.currentIndex() == 0):
            self.plot_abs(var.i)
        # call a function to plot data referenced by a specific sensor
        elif(var.ria.ui.refBox_on.currentIndex() == 1):
            self.plot_refFixa(var.i)
        # call a function to plot data referenced by the average of all sensors data
        elif(var.ria.ui.refBox_on.currentIndex() == 2):
            self.plot_refSensor(var.i)
        # call a function to plot data referenced by sensor's own data average
        elif(var.ria.ui.refBox_on.currentIndex() == 3):
            self.plot_refMediaG(var.i)
        # call a function to plot data referenced by a specific value
        elif(var.ria.ui.refBox_on.currentIndex() == 4):
            self.plot_refMediaI(var.i)
        else:
            print("erro em plotType_on")
        # else:
        # self.str_hora = time.mktime(time.localtime())
        # if(self.plotType_on == "abs"):
        #     self.plot_abs(i)
        # # call a function to plot data referenced by a specific sensor
        # elif(self.plotType_on == "refSensor"):
        #     self.plot_refSensor(i)
        # # call a function to plot data referenced by the average of all sensors data
        # elif(self.plotType_on == "refMediaG"):
        #     self.plot_refMediaG(i)
        # # call a function to plot data referenced by sensor's own data average
        # elif(self.plotType_on == "refMediaI"):
        #     self.plot_refMediaI(i)
        # # call a function to plot data referenced by a specific value
        # elif(self.plotType_on == "refFixa"):
        #     self.plot_refFixa(i)
        # else:
        #     print("erro em plotType_on")

    def plotData(self, i, D, T):
        """lista criada para checar os checkPlots"""
        self.list_check = [var.ria.ui.checkPlot1_on, var.ria.ui.checkPlot2_on, var.ria.ui.checkPlot3_on, var.ria.ui.checkPlot4_on,
                           var.ria.ui.checkPlot5_on, var.ria.ui.checkPlot6_on, var.ria.ui.checkPlot7_on, var.ria.ui.checkPlot8_on,
                           var.ria.ui.checkPlot9_on, var.ria.ui.checkPlot10_on, var.ria.ui.checkPlot11_on, var.ria.ui.checkPlot12_on,
                           var.ria.ui.checkPlot13_on, var.ria.ui.checkPlot14_on, var.ria.ui.checkPlot15_on, var.ria.ui.checkPlot16_on]
        # correcting rack number to be used properly as index above
        i = i - 1
        if(i <= 1):  # TEMPORARIO (checkPLots ainda vão só até 16)
            for j in range(8):
                if(self.list_check[(i*8)+j].isChecked()):
                    # Level plot - y axis
                    if(self.plotSet == "nivel"):
                        var.ria.ui.widget_on.Data[(i*8)+j].y = np.append(
                                    var.ria.ui.widget_on.Data[(i*8)+j].y,
                                    self.D[j+1])
                    else:
                        # Temperature plot - y axis
                        var.ria.ui.widget_on.Data[(i*8)+j].y = np.append(
                                    var.ria.ui.widget_on.Data[(i*8)+j].y,
                                    self.T[j+1])
                    # Time scale - x axis
                    var.ria.ui.widget_on.Data[(i*8)+j].x = np.append(
                                    var.ria.ui.widget_on.Data[(i*8)+j].x,
                                    self.str_hora) # self.D[0]
                    # correcting x range
                    self.menor = var.ria.ui.widget_on.Data[(i*8)+j].x[0]
                    for k in range(var.ria.ui.widget_on.nplots): #nplots = 16
                        try:
                            if(var.ria.ui.widget_on.Data[k].x[0] < self.menor):
                                self.menor = var.ria.ui.widget_on.Data[k].x[0]
                        except:
                            pass
                    try:
                        var.ria.ui.widget_on.setAxisScale(var.ria.ui.widget_on.xBottom,
                                                          self.menor, var.ria.ui.widget_on.Data[(i*8)+j].x[-1])
                    except TypeError:
                            print('erro3\n')
                    """se o comprimento do vetor de dados for maior que limite, retira o valor mais antigo"""
                    if(var.ria.ui.checkCmp_on.isChecked()):
                        try:
                            if len(var.ria.ui.widget_on.Data[(i*8)+j].x) > var.cmp_on:
                                self.dif = len(var.ria.ui.widget_on.Data[(i*8)+j].x) - var.cmp_on
                                var.ria.ui.widget_on.Data[(i*8)+j].x = var.ria.ui.widget_on.Data[(i*8)+j].x[self.dif:]
                                var.ria.ui.widget_on.Data[(i*8)+j].y = var.ria.ui.widget_on.Data[(i*8)+j].y[self.dif:]
                        except TypeError:
                            print('erro4\n')

    def plot_abs(self, i):
        if(i == 1):
            self.D = var.D1[-1]
            self.T = var.T1[-1]
        elif(i == 2):
            self.D = var.D2[-1]
            self.T = var.T2[-1]
        elif(i == 3):
            self.D = var.D3[-1]
            self.T = var.T3[-1]
        elif(i == 4):
            self.D = var.D4[-1]
            self.T = var.T4[-1]
        self.plotData(i, self.D, self.T)

    def plot_refSensor(self, i):
        ## acquiring reference sensor's read data ##
        self.ref_sensor = var.ria.ui.plotBoxSens_on.currentText()
        # sweeping racks
        for k in range(4):
            # sweeping sensors
            for j in range(8):
                if(self.ref_sensor == var.disp_sensores[k][j]):
                    # getting ref sensor's index
                    self.num_rack_ref_sensor = k+1
                    self.indice_ref_sensor = j

        if(self.num_rack_ref_sensor == i):
            # ref sensor is loccated at the same rack i which is currently being ploted
            if(i == 1):
                self.val_ref_D = var.D1[-1][1+self.indice_ref_sensor]
                self.val_ref_T = var.T1[-1][1+self.indice_ref_sensor]
            elif(i == 2):
                self.val_ref_D = var.D2[-1][1+self.indice_ref_sensor]
                self.val_ref_T = var.T2[-1][1+self.indice_ref_sensor]
            elif(i == 3):
                self.val_ref_D = var.D3[-1][1+self.indice_ref_sensor]
                self.val_ref_T = var.T3[-1][1+self.indice_ref_sensor]
            elif(i == 4):
                self.val_ref_D = var.D4[-1][1+self.indice_ref_sensor]
                self.val_ref_T = var.T4[-1][1+self.indice_ref_sensor]
        else:
            # ref sensor isn't loccated at the same rack i
            self.date = time.strftime("%Y_%m_%d", time.localtime())
            p = open('../data/rack'+str(self.num_rack_ref_sensor)+'_'+str(self.date)+'.dat', 'r')
            self.lines = p.readlines()
            self.values = self.lines[-1].split()
            self.val_ref_D = self.values[2+self.indice_ref_sensor]
            self.val_ref_T = self.values[10+self.indice_ref_sensor]
            p.close()

        if(i == 1):
            self.D = var.D1[-1]
            self.T = var.T1[-1]
        elif(i == 2):
            self.D = var.D2[-1]
            self.T = var.T2[-1]
        elif(i == 3):
            self.D = var.D3[-1]
            self.T = var.T3[-1]
        elif(i == 4):
            self.D = var.D4[-1]
            self.T = var.T4[-1]

        self.D[1:] = np.subtract(self.D[1:], float(self.val_ref_D))
        self.T[1:] = np.subtract(self.T[1:], float(self.val_ref_T))

        self.plotData(i, self.D, self.T)

    def plot_refMediaG(self, i):
        ## getting the general data average ##
        self.date = time.strftime("%Y_%m_%d", time.localtime())
        self.sumD = 0
        self.sumT = 0
        self.total = 0
        active_racks = [var.rack1, var.rack2, var.rack3, var.rack4]
        for k in range (4):
            if (active_racks[k] == True and k == 1):
                arq = '../data/rack1_'+str(self.date)+'.dat'
            elif (active_racks[k] == True and k == 2):
                arq = '../data/rack2_'+str(self.date)+'.dat'
            elif (active_racks[k] == True and k == 3):
                arq = '../data/rack3_'+str(self.date)+'.dat'
            elif (active_racks[k] == True and k == 4):
                arq = '../data/rack4_'+str(self.date)+'.dat'
            try:
                p = open(arq, 'r')
                self.lines = p.readlines()
                self.values = self.lines[-1].split()
                p.close()

                for j in range(8):
                    if(float(self.values[2+j]) > 5 and float(self.values[2+j]) < 10):
                        self.sumD = self.sumD + float(self.values[2+j])
                        self.sumT = self.sumT + float(self.values[10+j])
                        self.total += 1
            except:
                pass

        self.meanD = self.sumD/self.tam
        self.meanT = self.sumT/self.tam

        if(i == 1):
            self.D = var.D1[-1]
            self.T = var.T1[-1]
        elif(i == 2):
            self.D = var.D2[-1]
            self.T = var.T2[-1]
        elif(i == 3):
            self.D = var.D3[-1]
            self.T = var.T3[-1]
        elif(i == 4):
            self.D = var.D4[-1]
            self.T = var.T4[-1]

        self.D[1:] = np.subtract(self.D[1:], self.meanD)
        self.T[1:] = np.subtract(self.T[1:], self.meanT)

        self.plotData(i, self.D, self.T)

    def plot_refDeltaCG(self, i):
        if(i == 1):
            self.D = var.D1[-1]
            self.D[1:] = np.subtract(self.D[1:], var.refD1)
            self.T = var.T1[-1][1:]
        elif(i == 2):
            self.D = var.D2[-1]
            self.D[1:] = np.subtract(self.D[1:], var.refD2)
            self.T = var.T2[-1][1:]
        elif(i == 3):
            self.D = var.D3[-1]
            self.D[1:] = np.subtract(self.D[1:], var.refD3)
            self.T = var.T3[-1][1:]
        elif(i == 4):
            self.D = var.D4[-1]
            self.D[1:] = np.subtract(self.D[1:], var.refD4)
            self.T = var.T4[-1][1:]
        self.tanAng = (self.D[8]-self.D[1])/(var.posSens[7]-var.posSens[0])
        self.posCG = (var.posSens[0]+var.posSens[1]+var.posSens[2]+var.posSens[3]+var.posSens[4]+var.posSens[5]+var.posSens[6]+var.posSens[7])/8
        self.deltaCG = self.posCG*self.tanAng
        self.D[1:] = np.add(self.D[1:], self.deltaCG)

        self.plotData(i, self.D, self.T)

    def plot_refMediaI(self, i):
        self.date = time.strftime("%Y_%m_%d", time.localtime())
        if(var.rack1 == 1):
            p = open('../data/rack1_'+str(self.date)+'.dat', 'r')
            self.lines = p.readlines()
            self.values = self.lines[-1].split()
            p.close()
            for j in range(8):
                var.sumD1[j] = var.sumD1[j] + float(self.values[2+j])
                var.sumT1[j] = var.sumT1[j] + float(self.values[10+j])
            var.sumD1[8] += 1  # total number of items to get the average
            var.sumT1[8] += 1
        if(var.rack2 == 1):
            p = open('../data/rack2_'+str(self.date)+'.dat', 'r')
            self.lines = p.readlines()
            self.values = self.lines[-1].split()
            p.close()
            for j in range(8):
                var.sumD2[j] = var.sumD2[j] + float(self.values[2+j])
                var.sumT2[j] = var.sumT2[j] + float(self.values[10+j])
            var.sumD2[8] += 1
            var.sumT2[8] += 1
        if(var.rack3 == 1):
            p = open('../data/rack3_'+str(self.date)+'.dat', 'r')
            self.lines = p.readlines()
            self.values = self.lines[-1].split()
            p.close()
            for j in range(8):
                var.sumD3[j] = var.sumD3[j] + float(self.values[2+j])
                var.sumT3[j] = var.sumT3[j] + float(self.values[10+j])
            var.sumD3[8] += 1
            var.sumT3[8] += 1
        if(var.rack4 == 1):
            p = open('../data/rack4_'+str(self.date)+'.dat', 'r')
            self.lines = p.readlines()
            self.values = self.lines[-1].split()
            p.close()
            for j in range(8):
                var.sumD4[j] = var.sumD4[j] + float(self.values[2+j])
                var.sumT4[j] = var.sumT4[j] + float(self.values[10+j])
            var.sumD4[8] += 1
            var.sumT4[8] += 1

        if(var.rack1):
            self.meanD1 = np.divide(var.sumD1, var.sumD1[8])
            self.meanT1 = np.divide(var.sumT1, var.sumT1[8])
        if(var.rack2):
            self.meanD2 = np.divide(var.sumD2, var.sumD2[8])
            self.meanT2 = np.divide(var.sumT2, var.sumT2[8])
        if(var.rack3):
            self.meanD3 = np.divide(var.sumD3, var.sumD3[8])
            self.meanT3 = np.divide(var.sumT3, var.sumT3[8])
        if(var.rack4):
            self.meanD4 = np.divide(var.sumD4, var.sumD4[8])
            self.meanT4 = np.divide(var.sumT4, var.sumT4[8])

        self.D = np.array([])
        self.T = np.array([])
        for k in range(8):
            if(i == 0):
                self.D = var.D1[-1]
                self.T = var.T1[-1]
                self.D[1:] = np.subtract(self.D[1:], self.meanD1)
                self.T[1:] = np.subtract(self.T[1:], self.meanT1)
            if(i == 1):
                self.D = var.D2[-1]
                self.T = var.T2[-1]
                self.D[1:] = np.subtract(self.D[1:], self.meanD2)
                self.T[1:] = np.subtract(self.T[1:], self.meanT2)
            if(i == 2):
                self.D = var.D3[-1]
                self.T = var.T3[-1]
                self.D[1:] = np.subtract(self.D[1:], self.meanD3)
                self.T[1:] = np.subtract(self.T[1:], self.meanT3)
            if(i == 3):
                self.D = var.D4[-1]
                self.T = var.T4[-1]
                self.D[1:] = np.subtract(self.D[1:], self.meanD4)
                self.T[1:] = np.subtract(self.T[1:], self.meanT4)

        self.plotData(i, self.D, self.T)

    def plot_refMMQ(self, i):
        if(i == 1):
            self.D = var.D1[-1]
            self.T = var.T1[-1]
        elif(i == 2):
            self.D = var.D2[-1]
            self.T = var.T2[-1]
        elif(i == 3):
            self.D = var.D3[-1]
            self.T = var.T3[-1]
        elif(i == 4):
            self.D = var.D4[-1]
            self.T = var.T4[-1]
        self.N = len(self.D) - 1
        self.x = []
        self.xy = []
        self.x2 = []
        self.sum_x = 0
        self.sum_xy = 0
        self.sum_x2 = 0
        self.sum_D = 0
        for k in range(8):
            self.x = np.append(self.x, k)
            self.xy = np.append(self.xy, self.x[k]*self.D[k+1])
            self.x2 = np.append(self.x2, self.x[k]**2)
        for k in range(8):
            self.sum_x += self.x[k]
            self.sum_xy += self.xy[k]
            self.sum_x2 += self.x2[k]
            self.sum_D += self.D[k+1]

        self.a = (self.sum_xy - (self.sum_x*(self.sum_D/self.N)))/(self.sum_x2-(self.sum_x*(self.sum_x/self.N)))
        self.b = (self.sum_D/self.N)-(self.sum_x/self.N)*self.a
        self.y_line = self.a*self.x+self.b

        self.plot_data_D = np.subtract(self.D[1:], self.y_line)
        self.plotData(i, self.plot_data_D, self.T)

    def plot_refFixa(self, i):
        if(i == 1):
            self.D = var.D1[-1]
            self.D[1:] = np.subtract(self.D[1:], var.refD1)
            self.T = var.T1[-1]
            self.T[1:] = np.subtract(self.T[1:], var.refT1)
        elif(i == 2):
            self.D = var.D2[-1]
            self.D[1:] = np.subtract(self.D[1:], var.refD2)
            self.T = var.T2[-1]
            self.T[1:] = np.subtract(self.T[1:], var.refT2)
        elif(i == 3):
            self.D = var.D3[-1]
            self.D[1:] = np.subtract(self.D[1:], var.refD3)
            self.T = var.T3[-1]
            self.T[1:] = np.subtract(self.T[1:], var.refT3)
        elif(i == 4):
            self.D = var.D4[-1]
            self.D[1:] = np.subtract(self.D[1:], var.refD4)
            self.T = var.T4[-1]
            self.T[1:] = np.subtract(self.T[1:], var.refT4)

        self.plotData(i, self.D, self.T)

    def setScalePlot(self):

        var.scaleMinY = var.ria.ui.logMinY.textCursor()
        var.scaleMinY = var.ria.ui.logMinY.toPlainText()
        var.scaleMaxY = var.ria.ui.logMaxY.textCursor()
        var.scaleMaxY = var.ria.ui.logMaxY.toPlainText()
        var.scaleMinX = var.ria.ui.logMinX.textCursor()
        var.scaleMinX = var.ria.ui.logMinX.toPlainText()
        var.scaleMaxX = var.ria.ui.logMaxX.textCursor()
        var.scaleMaxX = var.ria.ui.logMaxX.toPlainText()

        self.str_horaMin = var.ria.ui.plotBox_data.currentText()+' '+var.scaleMinX

        a = time.strptime(self.str_horaMin, "%d/%m/%Y %H:%M:%S")
        self.flt_horaMin = time.mktime(a)
        self.str_horaMax = var.ria.ui.plotBox_data.currentText()+' '+var.scaleMaxX
        a = time.strptime(self.str_horaMax, "%d/%m/%Y %H:%M:%S")
        self.flt_horaMax = time.mktime(a)

        var.ria.ui.widget_on.setAxisScale(0, float(var.scaleMinY), float(var.scaleMaxY))
        var.ria.ui.widget_on.setAxisScale(2, self.flt_horaMin, self.flt_horaMax)
        #var.ria.ui.widget_on.zoomer.setZoomBase()

    def setAutoScalePlot(self):
        var.ria.ui.widget_on.setAxisAutoScale(0)
        var.ria.ui.widget_on.setAxisAutoScale(2)
        #var.ria.ui.widget_on.zoomer.setZoomBase()

    # converte mes no formato de 3 caracteres para numero
    def ReturnMonth(self, string):
        if string == 'jan':
            return '01'
        elif string == 'fev':
            return '02'
        elif string == 'mar':
            return '03'
        elif string == 'abr':
            return '04'
        elif string == 'mai':
            return '05'
        elif string == 'jun':
            return '06'
        elif string == 'jul':
            return '07'
        elif string == 'ago':
            return '08'
        elif string == 'set':
            return '09'
        elif string == 'out':
            return '10'
        elif string == 'nov':
            return '11'
        elif string == 'dez':
            return '12'

    def startPlot_abs_off(self):
        self.plotType_off = "abs"
        var.ria.ui.logOutput_off.insertPlainText("Referência selecionada: ABSOLUTA\n")
        var.ria.ui.logOutput_off.moveCursor(QtGui.QTextCursor.End)

    def startPlot_refSensor_off(self):
        self.plotType_off = "refSens"
        var.ria.ui.logOutput_off.insertPlainText("Referência selecionada: SENSOR\n")
        var.ria.ui.logOutput_off.moveCursor(QtGui.QTextCursor.End)

    def startPlot_refMediaG_off(self):
        self.plotType_off = "refMediaG"
        var.ria.ui.logOutput_off.insertPlainText("Referência selecionada: MÉDIA\n")
        var.ria.ui.logOutput_off.moveCursor(QtGui.QTextCursor.End)

    def startPlot_refFixa_off(self):
        self.plotType_off = "refFixa"
        var.ria.ui.logOutput_off.insertPlainText("Referência selecionada: VALOR FIXO\n")
        var.ria.ui.logOutput_off.moveCursor(QtGui.QTextCursor.End)

    def startPlot_off(self):
        if(self.data_ini > self.data_fim and self.data_fim != ""):
            var.ria.ui.logOutput_off.insertPlainText("Erro: período inválido\n")
            var.ria.ui.logOutput_off.moveCursor(QtGui.QTextCursor.End)
            return
        elif (self.data_ini == ""):
            var.ria.ui.logOutput_off.insertPlainText("Erro: data inicial não selecionada\n")
            var.ria.ui.logOutput_off.moveCursor(QtGui.QTextCursor.End)
            return
        elif (self.data_fim == ""):
            var.ria.ui.logOutput_off.insertPlainText("Erro: data final não selecionada\n")
            var.ria.ui.logOutput_off.moveCursor(QtGui.QTextCursor.End)
            return
        else:
            onlyfiles = listdir('../data/')
            self.flag_dados = False
            self.flag_control_racks = 0 # 'flag' que indicará em quais racks constam dados
            var.ria.ui.logOutput_off.insertPlainText("Iniciando plot...\n")
            for i in range (1, 5):
                self.arq_ini = "rack"+str(i)+"_"+self.data_ini+".dat"
                self.arq_fim = "rack"+str(i)+"_"+self.data_fim+".dat"
                self.valores = []
                self.val_D = []
                self.val_T = []
                prim_arquivo = True
                #cont = 0
                for j in onlyfiles:
                    if(j >= self.arq_ini and j <= self.arq_fim):
                        var.flag_freeToPlot_off = True #habilita plot
                        self.flag_control_racks = i
                        f = open('../data/'+j, "r")
                        self.lines = f.readlines()

                        ### caso opção de shift esteja setada, definir time shift ###
                        if(var.ria.ui.checkShift_off.isChecked()):
                            self.aux = []
                            for w in range(1, 3):
                                self.aux = np.append(self.aux, self.lines[w].split())
                            self.aux = np.reshape(self.aux, (2, int(len(self.aux)/2)))
                            shift = self.defineTimeShift_off(self.aux)
                        else:
                            shift = 1

                        aux1 = []
                        if (prim_arquivo):  # operação para pegar legenda apenas no primeiro arquivo
                            p = 0
                        else:
                            p = 1
                        for k in range(p, int(len(self.lines)/shift)):
                            prim_arquivo = False
                            try:
                                self.values = self.lines[k*shift].split()
                                self.val_D = np.append(self.val_D, self.values[:10])
                                aux1 = np.append(self.values[:2], self.values[10:18])
                                self.val_T = np.append(self.val_T, aux1) #pegar a data, hora e as temperaturas
                            except:
                                pass
                            aux1 = []
                        f.close()
                if(i == 1):
                    self.rack1_val_D = self.val_D
                    self.rack1_val_T = self.val_T
                elif(i == 2):
                    self.rack2_val_D = self.val_D
                    self.rack2_val_T = self.val_T
                elif(i == 3):
                    self.rack3_val_D = self.val_D
                    self.rack3_val_T = self.val_T
                elif(i == 4):
                    self.rack4_val_D = self.val_D
                    self.rack4_val_T = self.val_T

            # deixa no formato D = [[data hora x x x x x x x],[data hora x x x x x x x x],...]
            try:
                self.rack1_val_D = np.reshape(self.rack1_val_D, (int(len(self.rack1_val_D)/10), 10))
                self.rack1_val_T = np.reshape(self.rack1_val_T, (int(len(self.rack1_val_T)/10), 10))
                self.rack2_val_D = np.reshape(self.rack2_val_D, (int(len(self.rack2_val_D)/10), 10))
                self.rack2_val_T = np.reshape(self.rack2_val_T, (int(len(self.rack2_val_T)/10), 10))
                self.rack3_val_D = np.reshape(self.rack3_val_D, (int(len(self.rack3_val_D)/10), 10))
                self.rack3_val_T = np.reshape(self.rack3_val_T, (int(len(self.rack3_val_T)/10), 10))
                self.rack4_val_D = np.reshape(self.rack4_val_D, (int(len(self.rack4_val_D)/10), 10))
                self.rack4_val_T = np.reshape(self.rack4_val_T, (int(len(self.rack4_val_T)/10), 10))
            except:
                pass
            if(self.flag_control_racks == 1):
                self.D = self.rack1_val_D
                self.T = self.rack1_val_T
            elif(self.flag_control_racks == 2):
                self.D = []
                self.T = []
                for i in range(len(self.rack1_val_D)):
                    self.D = np.append(self.D, self.rack1_val_D[i])
                    self.D = np.append(self.D, self.rack2_val_D[i][2:])
                    self.T = np.append(self.T, self.rack1_val_T[i])
                    self.T = np.append(self.T, self.rack2_val_T[i][2:])
                self.D = np.reshape(self.D, (int(len(self.D)/18), 18))
                self.T = np.reshape(self.T, (int(len(self.T)/18), 18))
            elif(self.flag_control_racks == 3):
                self.D = []
                self.T = []
                for i in range(len(self.rack1_val_D)):
                    self.D = np.append(self.D, self.rack1_val_D[i])
                    self.D = np.append(self.D, self.rack2_val_D[i][2:])
                    self.D = np.append(self.D, self.rack3_val_D[i][2:])
                    self.T = np.append(self.T, self.rack1_val_T[i])
                    self.T = np.append(self.T, self.rack2_val_T[i][2:])
                    self.T = np.append(self.T, self.rack3_val_T[i][2:])
                self.D = np.reshape(self.D, (int(len(self.D)/26), 26))
                self.T = np.reshape(self.T, (int(len(self.T)/26), 26))
            elif(self.flag_control_racks == 3):
                self.D = []
                self.T = []
                for i in range(len(self.rack1_val_D)):
                    self.D = np.append(self.D, self.rack1_val_D[i])
                    self.D = np.append(self.D, self.rack2_val_D[i][2:])
                    self.D = np.append(self.D, self.rack3_val_D[i][2:])
                    self.D = np.append(self.D, self.rack4_val_D[i][2:])
                    self.T = np.append(self.T, self.rack1_val_T[i])
                    self.T = np.append(self.T, self.rack2_val_T[i][2:])
                    self.T = np.append(self.T, self.rack3_val_T[i][2:])
                    self.T = np.append(self.T, self.rack4_val_T[i][2:])
                self.D = np.reshape(self.D, (int(len(self.D)/34), 34))
                self.T = np.reshape(self.T, (int(len(self.T)/34), 34))

            self.D = np.transpose(self.D)
            self.T = np.transpose(self.T)

            if(var.flag_freeToPlot_off):
                if(self.plotType_off == "abs"):
                    self.plot_abs_off()
                elif(self.plotType_off == "refSensor"):
                    self.plot_refSensor_off()
                elif(self.plotType_off == "mediaG"):
                    self.plot_refMediaG_off()
                elif(self.plotType_off == "refFixa"):
                    self.plot_refFixa_off()
            else:  # nao achou arquivos
                var.ria.ui.logOutput.insertPlainText("Erro: arquivo de dados não encontrado" + '\n')
                return
            var.ria.ui.logOutput_off.moveCursor(QtGui.QTextCursor.End)

    def onpick(self,event):
        # on the pick event, find the orig line corresponding to the
        # legend proxy line, and toggle the visibility
        self.legline = event.artist
        self.origline = self.lined[self.legline]
        vis = not self.origline.get_visible()
        self.origline.set_visible(vis)
        # Change the alpha on the line in the legend so we can see what lines
        # have been toggled
        if vis:
            self.legline.set_alpha(1.0)
        else:
            self.legline.set_alpha(0.2)
        self.fig.canvas.draw()

    def plot_off(self, x, y):
        self.fig = plt.figure(num=None, figsize=(14, 7.5), dpi=80, facecolor='w', edgecolor='k')
        ax = self.fig.add_subplot(111)

        self.n = []
        # legendas #
        for k in range(2,len(self.D)):
            self.n = np.append(self.n, self.D[k][0])
        ## ARRUMAR DEPOIS
        """n = [var.disp_sensores[0][0], var.disp_sensores[0][1], var.disp_sensores[0][2], var.disp_sensores[0][3],
             var.disp_sensores[0][4], var.disp_sensores[0][5], var.disp_sensores[0][6], var.disp_sensores[0][7],
             'H7DC_036', 'H7DC_044', 'H7DC_042', 'H7DC_056', 'H7DC_045', 'H7DC_038', 'H7DC_032', 'H7DC_055'] #esta linha para testes!
        #n=["H7DC-33","H7DC-32","H7DC-40","H7DC-59","H7DC-47","H7DC-46","H7DC-39","H7DC-52","H7DC-57","H7DC-36","H7DC-44","H7DC-42","H7DC-56","H7DC-45","H7DC-38","H7DC-55"]"""

        # plot das curvas#
        self.lines = []
        for j in range (len(self.y)):
            """for k in range(shift)): #implementação do SHIFT
                plotY = np.append(plotY, self.y["""
            self.lines = np.append(self.lines, ax.plot(x, y[j], label=self.n[j]))#append para existir vetor com as curvas
                                                                                      #para usar na legenda interativa
        #definições da interface do plot
        self.fig.suptitle("Variação Absoluta de Altura", fontsize=16)
        ax.set_ylabel('Height [mm]', labelpad=10, fontsize=14)
        ax.set_xlabel('Time [day hh:mm]', labelpad=20, fontsize=14)
        plt.grid(True)
        plt.gcf().autofmt_xdate()

        #implementação da legenda interativa#
        leg = ax.legend(loc='upper right', bbox_to_anchor=(1.135, 1))
        leg.get_frame().set_alpha(0.4)
        self.lined = dict()
        for self.legline, self.origline in zip(leg.get_lines(), self.lines):
            self.legline.set_picker(5)  # 5 pts tolerance
            self.lined[self.legline] = self.origline
        self.fig.canvas.mpl_connect('pick_event', self.onpick)

        show()

    def plot_abs_off(self):

        self.x = []
        self.y = []

        for i in range(2, len(self.D)):
            for w in range(1, len(self.D[i])):
                self.y = np.append(self.y, self.D[i][w])
        tam = len(self.D)-2
        # ajusting y format
        self.y = np.reshape(self.y, (tam, int(len(self.y)/tam)))

        for i in range(1,len(self.D[0])):
            self.current_datetime = self.D[0][i]+' '+self.D[1][i]
            self.x = np.append(self.x, datetime.datetime.strptime(self.current_datetime, "%Y/%m/%d %H:%M:%S"))

        self.plot_off(self.x, self.y)

    def plot_refSensor_off(self):
        # valores da abscissa x e ordenada y #
        self.x = []
        self.y = []

        achou_sensor = False
        self.refSensor_off = var.ria.ui.plotBoxSens_off.currentText()
        for j in range(2, len(self.D)):  # Achar sensor de referencia
            sensor = self.D[j][0]
            sensor = sensor[:7]
            if(self.refSensor_off == sensor):
                self.indice_ref_sensor = j
                self.val_ref_off = self.D[j][1:]
                achou_sensor = True
        if(not achou_sensor):
            var.ria.ui.logOutput_off.insertPlainText("Erro: sensor de referência não encontrado" + '\n')
            var.ria.ui.logOutput_off.moveCursor(QtGui.QTextCursor.End)
            return

        val = []
        for i in range(2, len(self.D)):
            for k in range(1, int(len(self.D[i]))):
                val = np.append(val, float(self.D[i][k]) - float(self.val_ref_off[(k-1)]))
            self.y = np.append(self.y, val)
            val = []
        tam = len(self.D)-2
        self.y = np.reshape(self.y, (tam, int(len(self.y)/tam)))

        for i in range(1, len(self.D[0])):
            current_datetime = self.D[0][i]+' '+self.D[1][i]
            self.x = np.append(self.x, datetime.datetime.strptime(current_datetime, "%Y/%m/%d %H:%M:%S"))

        self.plot_off(self.x, self.y)

    def plot_refMediaG_off(self):
        # valores da abscissa x e ordenada y #
        self.x = []
        self.y = []

        self.mediaG = 0
        val = []
        for i in range(2, len(self.D)):
            for k in range(1, len(self.D[i])):
                for j in range(2, len(self.D)):  # para calculo da média neste instante de tempo
                    self.mediaG += float(self.D[j][k])
                self.mediaG = self.mediaG/(len(self.D)-2)
                val = np.append(val, float(self.D[i][k]) - self.mediaG)
                self.mediaG = 0
            self.y = np.append(self.y, val)
            val = []
        tam = len(self.D)-2
        self.y = np.reshape(self.y, (tam, int(len(self.y)/tam)))  # ajustar formato da matriz de dados y

        for i in range(1, len(self.D[0])):
            current_datetime = self.D[0][i]+' '+self.D[1][i]
            self.x = np.append(self.x, datetime.datetime.strptime(current_datetime, "%Y/%m/%d %H:%M:%S"))

        self.plot_off(self.x, self.y)

    def plot_refFixa_off(self):
        # valores da abscissa x e ordenada y #
        self.x = []
        self.y = []

        val = []
        for i in range(2, len(self.D)):
            for k in range(1, len(self.D[i])):
                val = np.append(val, float(self.D[i][k]) - float(self.refValoresD_off[i-2]))
            self.y = np.append(self.y, val)
            val = []
        tam = len(self.D)-2
        self.y = np.reshape(self.y, (tam, int(len(self.y)/tam)))  # ajustar formato dos dados de y

        for i in range(1, len(self.D[0])):
            current_datetime = self.D[0][i]+' '+self.D[1][i]
            self.x = np.append(self.x, datetime.datetime.strptime(current_datetime, "%Y/%m/%d %H:%M:%S"))

        self.plot_off(self.x, self.y)

    def setRef_off(self):
        refDateTime = var.ria.ui.logDateTime_off.textCursor()
        refDateTime = var.ria.ui.logDateTime_off.toPlainText()
        self.refTime = refDateTime[:8]
        self.refDate = refDateTime[15:19]+'_'+refDateTime[12:14]+'_'+refDateTime[9:11]

        mypath="Data/"
        onlyfiles = listdir(mypath)
        self.refValoresD_off = []
        self.refValoresT_off = []
        for i in onlyfiles:
            # if file 'rackX_AAAA/MM/DD' has the taggered reference Value
            if (i[6:16] == self.refDate):
                f = open("Data/"+i)
                self.lines = f.readlines()
                for j in range(len(self.lines)):
                    values = self.lines[j].split()
                    # if date is equal, data must get stored
                    if(values[1] == self.refTime):
                        # storing reference values
                        self.refValoresD_off = np.append(self.refValoresD_off, values[2:10])
                        self.refValoresT_off = np.append(self.refValoresT_off, values[10:])

    def defineTimeShift_off(self, aux):
        self.timeDate1 = aux[0][0]+' '+aux[0][1]
        self.timeDate2 = aux[1][0]+' '+aux[1][1]

        self.timeDate1 = time.mktime(time.strptime(self.timeDate1, '%Y/%m/%d %H:%M:%S'))
        self.timeDate2 = time.mktime(time.strptime(self.timeDate2, '%Y/%m/%d %H:%M:%S'))

        # current shift, in seconds
        self.shiftAtual = self.timeDate2-self.timeDate1

        # shift recebe quantidade total de segundos que há no arquivo
        # divido pelo shift de segundos estipulado na interface,
        # resultando na quantidade de amostras que serão colhidas do arquivo
        self.shift = int(var.ria.ui.plotBoxShift_off.value()/self.shiftAtual)
        return self.shift

    def getDate_ini(self):
        mes_ini = self.ReturnMonth(self.data[4:7])
        aux_dia_ini = int(self.data[8:10])
        if(aux_dia_ini < 10):
            dia_ini = "0"+str(aux_dia_ini)
        else:
            dia_ini = str(aux_dia_ini)
        ano_ini = self.data[(len(self.data)-4):len(self.data)]
        self.data_ini = ano_ini+"_"+mes_ini+"_"+dia_ini
        var.ria.ui.logOutput_off.insertPlainText("Data Inicial: " + str(dia_ini)+'/'+str(mes_ini)+'/'+str(ano_ini)+'\n')

    def getDate_fim(self):
        mes_fim = self.ReturnMonth(self.data[4:7])
        aux_dia_fim = int(self.data[8:10])
        if(aux_dia_fim < 10):
            dia_fim = "0"+str(aux_dia_fim)
        else:
            dia_fim = str(aux_dia_fim)
        ano_fim = self.data[(len(self.data)-4):len(self.data)]
        self.data_fim = ano_fim+"_"+mes_fim+"_"+dia_fim
        var.ria.ui.logOutput_off.insertPlainText("Data Final: " + str(dia_fim)+'/'+str(mes_fim)+'/'+str(ano_fim)+'\n')

    def showDate(self, date):
        aux = date.toString()
        print ("\ndata:", aux)
        self.data = aux


plot = PlotOnOff()
