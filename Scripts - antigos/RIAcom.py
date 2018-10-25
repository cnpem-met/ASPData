"""ERRROS
- 'Preferences': Botao de load e save parameters ta zoado
- 'Offline':
- 'Online':
    - o plot, depois de um longo periodo de aquisicao, fica comprometido
      no sentido de que ele nao plota mais automaticamente
    - depois de um longo tempo, vetor var.....Data[0].x e y começam a pegar muito
      mais valores em cada leitura em vez de 1 só
- ***PROGRAMA SENDO INTERROMPIDO POR ERRO DE EXECUÇÃO
    - colocar 'try' e 'except' para achar o erro
"""


import serial, time, sys, os, threading, random
import numpy as np
from Variaveis_v2 import var #novo
from Fogale_UI_v4 import Ui_MainWindow #novo
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QObject, pyqtSignal #novo
#from PyQt4.QtGui import * #NOVO
from serial.tools import list_ports
import PyQt4.Qwt5 as Qwt

from PlotGUI_Qwt_Multi_v3 import dataclass
#NOVO{
#from PlotGUI_Qwt_Multi import SimplePlot
from Auxiliar import aux
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas #NOVO
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar #NOVO
import matplotlib.pyplot as plt# NOVO
#from python_pyqt_NewVersion_v6 import * #NOVO
from python_pyqt_NewVersion_v7 import plot
#from teste import plot
#}

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

sys.stderr = open("errlog.txt", "w")
"""if ( sys.platform == 'win32' and sys.executable.split( '\\' )[-1] == 'pythonw.exe'):
    sys.stdout = open(os.devnull, 'w')
    sys.stderr = open(os.devnull, 'w')"""

"""implementar médias gerais"""
"""aplicar conversão e correção de temperatura"""


class RIA(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Fogale HLS")
##        self.ser = serial.Serial('COM7', 115200, 8, 'N', timeout = .2, stopbits = 1)

    ###início das funções relacionadas à interface###
    def ui_init(self):
        plot.set_dataList()
        self.list_ports()
        self.load_param()

        """seta valores em var para a interface"""
        var.ria.ui.cmp.setValue(var.cmp)
        var.ria.ui.t_aq.setValue(var.t_aq)

        """seta flags de habilitação dos racks em var"""
##        var.rack1 = var.ria.ui.check1.isChecked()
##        var.rack2 = var.ria.ui.check2.isChecked()
##        var.rack3 = var.ria.ui.check3.isChecked()
##        var.rack4 = var.ria.ui.check4.isChecked()
      
        
        """reduz comprimento das celulas das tabelas"""
        var.ria.ui.tableWidget.resizeColumnsToContents()
        var.ria.ui.tableWidget_2.resizeColumnsToContents()
        var.ria.ui.tableWidget_3.resizeColumnsToContents()

        """adiciona lista de sensores ao menu dos Plots"""
        var.ria.ui.PlotBox1.addItems(var.sensor_list)
        var.ria.ui.PlotBox2.addItems(var.sensor_list)
        var.ria.ui.PlotBox3.addItems(var.sensor_list)
        var.ria.ui.PlotBox4.addItems(var.sensor_list)
        var.ria.ui.PlotBox5.addItems(var.sensor_list)
        var.ria.ui.PlotBox6.addItems(var.sensor_list)
        var.ria.ui.PlotBox7.addItems(var.sensor_list)
        var.ria.ui.PlotBox8.addItems(var.sensor_list)

        """adiciona plots caso estejam habilitados"""
        if var.ria.ui.checkPlot1.isChecked():
            self.set_plot1()
        if var.ria.ui.checkPlot2.isChecked():
            self.set_plot2()
        if var.ria.ui.checkPlot3.isChecked():
            self.set_plot3()
        if var.ria.ui.checkPlot4.isChecked():
            self.set_plot4()
        if var.ria.ui.checkPlot5.isChecked():
            self.set_plot5()
        if var.ria.ui.checkPlot6.isChecked():
            self.set_plot6()
        if var.ria.ui.checkPlot7.isChecked():
            self.set_plot7()
        if var.ria.ui.checkPlot8.isChecked():
            self.set_plot8()
        

        """conecta sinais às respectivas funções"""
        QtCore.QObject.connect(var.ria.ui.ResButton, QtCore.SIGNAL("clicked()"),
                                                     self.res)
        QtCore.QObject.connect(var.ria.ui.RefButton, QtCore.SIGNAL("clicked()"),
                                                     self.set_ref)
        QtCore.QObject.connect(var.ria.ui.SaveButton, QtCore.SIGNAL("clicked()"),
                                                     self.save_param)
        QtCore.QObject.connect(var.ria.ui.LoadButton, QtCore.SIGNAL("clicked()"),
                                                     self.load_param)
        QtCore.QObject.connect(var.ria.ui.RefreshButton, QtCore.SIGNAL("clicked()"),
                                                     self.list_ports)
        QtCore.QObject.connect(var.ria.ui.OpenButton, QtCore.SIGNAL("clicked()"),
                                                     self.open_com)
        QtCore.QObject.connect(var.ria.ui.CloseButton, QtCore.SIGNAL("clicked()"),
                                                     self.close_com)
        QtCore.QObject.connect(var.ria.ui.check1, QtCore.SIGNAL("clicked()"),
                                                     self.enable_racks1)
        QtCore.QObject.connect(var.ria.ui.check2, QtCore.SIGNAL("clicked()"),
                                                     self.enable_racks1)
        QtCore.QObject.connect(var.ria.ui.check3, QtCore.SIGNAL("clicked()"),
                                                     self.enable_racks1)
        QtCore.QObject.connect(var.ria.ui.check4, QtCore.SIGNAL("clicked()"),
                                                     self.enable_racks1)
        QtCore.QObject.connect(var.ria.ui.checkPlot1, QtCore.SIGNAL("stateChanged(int)"),
                                                     self.set_plot1)
        QtCore.QObject.connect(var.ria.ui.checkPlot2, QtCore.SIGNAL("stateChanged(int)"),
                                                     self.set_plot2)
        QtCore.QObject.connect(var.ria.ui.checkPlot3, QtCore.SIGNAL("stateChanged(int)"),
                                                     self.set_plot3)
        QtCore.QObject.connect(var.ria.ui.checkPlot4, QtCore.SIGNAL("stateChanged(int)"),
                                                     self.set_plot4)
        QtCore.QObject.connect(var.ria.ui.checkPlot5, QtCore.SIGNAL("stateChanged(int)"),
                                                     self.set_plot5)
        QtCore.QObject.connect(var.ria.ui.checkPlot6, QtCore.SIGNAL("stateChanged(int)"),
                                                     self.set_plot6)
        QtCore.QObject.connect(var.ria.ui.checkPlot7, QtCore.SIGNAL("stateChanged(int)"),
                                                     self.set_plot7)
        QtCore.QObject.connect(var.ria.ui.checkPlot8, QtCore.SIGNAL("stateChanged(int)"),
                                                     self.set_plot8)
        QtCore.QObject.connect(var.ria.ui.PlotBox1, QtCore.SIGNAL("currentIndexChanged(int)"),
                                                     self.set_plot1)
        QtCore.QObject.connect(var.ria.ui.PlotBox2, QtCore.SIGNAL("currentIndexChanged(int)"),
                                                     self.set_plot2)
        QtCore.QObject.connect(var.ria.ui.PlotBox3, QtCore.SIGNAL("currentIndexChanged(int)"),
                                                     self.set_plot3)
        QtCore.QObject.connect(var.ria.ui.PlotBox4, QtCore.SIGNAL("currentIndexChanged(int)"),
                                                     self.set_plot4)
        QtCore.QObject.connect(var.ria.ui.PlotBox5, QtCore.SIGNAL("currentIndexChanged(int)"),
                                                     self.set_plot5)
        QtCore.QObject.connect(var.ria.ui.PlotBox6, QtCore.SIGNAL("currentIndexChanged(int)"),
                                                     self.set_plot6)
        QtCore.QObject.connect(var.ria.ui.PlotBox7, QtCore.SIGNAL("currentIndexChanged(int)"),
                                                     self.set_plot7)
        QtCore.QObject.connect(var.ria.ui.PlotBox8, QtCore.SIGNAL("currentIndexChanged(int)"),
                                                     self.set_plot8)
        QtCore.QObject.connect(var.ria.ui.t_aq, QtCore.SIGNAL("valueChanged (int)"),
                                                     self.set_t_aq)
        QtCore.QObject.connect(var.ria.ui.cmp, QtCore.SIGNAL("valueChanged (int)"),
                                                     self.set_cmp)

        #NOVO{
        val = ""
        self.list_val= []
        """adiciona valores D32, D33, ..., D47 ao plotBox_off da aba 'Offline'"""
        for k in range (len(var.disp_sensores)):
            val = var.disp_sensores[k]
            self.list_val = np.append(self.list_val, val)
        var.ria.ui.plotBoxSens_off.addItems(self.list_val)
        
        """adiciona lista de sensores que podem ser usados como referencia"""
        with open('parameters.dat', 'r') as f:
            lines = f.readlines()
            if lines[3] == 'True\n':
                var.ria.ui.plotBoxSens_on.addItems(var.disp_sensores[0])
            if lines[4] == 'True\n':
                var.ria.ui.plotBoxSens_on.addItems(var.disp_sensores[1])
            if lines[5] == 'True\n':
                var.ria.ui.plotBoxSens_on.addItems(var.disp_sensores[2])
            if lines[6] == 'True\n':
                var.ria.ui.plotBoxSens_on.addItems(var.disp_sensores[3])

        plot.set_plot1_on()
        plot.set_plot2_on()
        plot.set_plot3_on()
        plot.set_plot4_on()
        plot.set_plot5_on()
        plot.set_plot6_on()
        plot.set_plot7_on()
        plot.set_plot8_on()

        plot.set_plot9_on()
        plot.set_plot10_on()
        plot.set_plot11_on()
        plot.set_plot12_on()
        plot.set_plot13_on()
        plot.set_plot14_on()
        plot.set_plot15_on()
        plot.set_plot16_on()

        
        """conecta sinais às respectivas funções"""
        var.ria.ui.cal.clicked[QtCore.QDate].connect(plot.showDate)
        var.ria.ui.btn1.clicked[bool].connect(plot.getDate_ini)
        var.ria.ui.btn2.clicked[bool].connect(plot.getDate_fim)
        var.ria.ui.btn_play.clicked[bool].connect(plot.startPlot_off)
        var.ria.ui.btn_stop2.clicked[bool].connect(plot.stopPlot)
        var.ria.ui.setScaleBtn.clicked[bool].connect(plot.setScalePlot)
        var.ria.ui.setAutoScaleBtn.clicked[bool].connect(plot.setAutoScalePlot)
        var.ria.ui.plotAbsBtn_off.clicked[bool].connect(plot.startPlot_abs_off)
        var.ria.ui.plotRefSensorBtn_off.clicked[bool].connect(plot.startPlot_refSensor_off)
        var.ria.ui.plotRefFixaBtn_off.clicked[bool].connect(plot.startPlot_refFixa_off)
        var.ria.ui.plotRefMedGBtn_off.clicked[bool].connect(plot.startPlot_refMediaG_off)
        var.ria.ui.setRefBtn_off.clicked[bool].connect(plot.setRef_off)


        QtCore.QObject.connect(var.ria.ui.plotAbsBtn, QtCore.SIGNAL("clicked()"),
                                                     plot.startPlot_abs)
        QtCore.QObject.connect(var.ria.ui.plotRefSensorBtn, QtCore.SIGNAL("clicked()"),
                                                     plot.startPlot_refSensor)
        QtCore.QObject.connect(var.ria.ui.plotRefMedGBtn, QtCore.SIGNAL("clicked()"),
                                                     plot.startPlot_refMediaG)
        QtCore.QObject.connect(var.ria.ui.plotRefMedIBtn, QtCore.SIGNAL("clicked()"),
                                                     plot.startPlot_refMediaI)
        QtCore.QObject.connect(var.ria.ui.plotRefFixBtn, QtCore.SIGNAL("clicked()"),
                                                     plot.startPlot_refFixa)
        QtCore.QObject.connect(var.ria.ui.checkPlot1_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot1_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot2_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot2_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot3_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot3_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot4_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot4_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot5_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot5_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot6_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot6_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot7_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot7_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot8_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot8_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot9_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot9_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot10_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot10_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot11_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot11_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot12_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot12_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot13_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot13_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot14_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot14_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot15_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot15_on)
        QtCore.QObject.connect(var.ria.ui.checkPlot16_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_plot16_on)
        QtCore.QObject.connect(var.ria.ui.plotBox_on, QtCore.SIGNAL("currentIndexChanged(int)"),
                                                     plot.plotBox_act)
        QtCore.QObject.connect(var.ria.ui.cmp_on, QtCore.SIGNAL("valueChanged (int)"),
                                                     plot.set_cmp_on)
        QtCore.QObject.connect(var.ria.ui.setRef_onBtn, QtCore.SIGNAL("clicked()"),
                                                     plot.setRef_on)
        QtCore.QObject.connect(var.ria.ui.checkCmp_on, QtCore.SIGNAL("stateChanged(int)"),
                                                     plot.set_checkCmp_on)
        QtCore.QObject.connect(var.ria.ui.plotBox_data, QtCore.SIGNAL("currentIndexChanged(int)"),
                                                     plot.plotBox_dataAct)
        #NOVO}

    #muda valor de tempo de aquisição de dados
    def set_t_aq(self):
        var.t_aq = var.ria.ui.t_aq.value()

    #muda numero de pontos no gráfico
    def set_cmp(self):
        var.cmp = var.ria.ui.cmp.value()

    #lista portas disponíveis
    def list_ports(self):
        self.ports_list = []
        
        for i in list_ports.comports():
            self.ports_list.append(i[0])

        var.ria.ui.PortBox.clear()
        var.ria.ui.PortBox.addItems(self.ports_list)

    #abre comunicação serial
    def open_com(self):
        try:
            var.ria.ser = serial.Serial(var.ria.ports_list[var.ria.ui.PortBox.currentIndex()],
                                     115200, 8, 'N', timeout = .5)
            var.serialFlag = True
            self.Com = Communication()
        except:
            raise
            QtGui.QMessageBox.information(self, "Serial error",
             "Couldn't open communication. Please check if it's already open.")

    #fecha comunicação serial
    def close_com(self):
        try:
            self.ser.close()
            if not self.ser.isOpen():
                var.serialFlag = False
                print("Serial port is closed")
        except:
            raise

    #habilita racks
    def enable_racks1(self):
        self.enable = threading.Thread(target = self.enable_racks())
        self.enable.start()

    #Muda flag e led de status do rack
    def enable_racks(self):        
        if var.ria.ui.check1.isChecked() and var.rack1 == False:
            var.ria.ui.led1_g.show()
            var.rack1 = True
            self.init_rack([1])
        elif not var.ria.ui.check1.isChecked():
            var.ria.ui.led1_g.hide()
            var.ria.ui.led1_y.hide()
            var.rack1 = False
        if var.ria.ui.check2.isChecked() and var.rack2 == False:
            var.ria.ui.led2_g.show()
            var.rack2 = True
            self.init_rack([2])
        elif not var.ria.ui.check2.isChecked():
            var.ria.ui.led2_g.hide()
            var.ria.ui.led2_y.hide()
            var.rack2 = False
        if var.ria.ui.check3.isChecked() and var.rack3 == False:
            var.ria.ui.led3_g.show()
            var.rack3 = True
            self.init_rack([3])
        elif not var.ria.ui.check3.isChecked():
            var.ria.ui.led3_g.hide()
            var.ria.ui.led3_y.hide()
            var.rack3 = False
        if var.ria.ui.check4.isChecked() and var.rack4 == False:
            var.ria.ui.led4_g.show()
            var.rack4 = True
            self.init_rack([4])
        elif not var.ria.ui.check4.isChecked():
            var.ria.ui.led4_g.hide()
            var.ria.ui.led4_y.hide()
            var.rack4 = False

    #inicializa Plot1
    def set_plot1(self):
        if not var.ria.ui.checkPlot1.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget.Plots[0].setTitle("")
            var.ria.ui.widget.Plots[1].setTitle("")
            var.ria.ui.widget.Data[0] = dataclass()
            var.ria.ui.widget.Data[1] = dataclass()
        else:
            """muda nome do plot e zera valores"""
            var.ria.ui.widget.Plots[0].setTitle(var.sensor_list[var.ria.ui.PlotBox1.currentIndex()]+" D")
            var.ria.ui.widget.Plots[1].setTitle(var.sensor_list[var.ria.ui.PlotBox1.currentIndex()]+" T")
            var.ria.ui.widget.Data[0] = dataclass()
            var.ria.ui.widget.Data[1] = dataclass()
            """plot dados disponíveis"""
            self.index = divmod(var.ria.ui.PlotBox1.currentIndex(), 8)
            if self.index[0] == 0:
                if len(var.D1) > 2:
                    for i in var.D1:
                        var.ria.ui.widget.Data[0].x = np.append(var.ria.ui.widget.Data[0].x, i[0])
                        var.ria.ui.widget.Data[0].y = np.append(var.ria.ui.widget.Data[0].y, i[self.index[1]+1])
                    for i in var.T1:
                        var.ria.ui.widget.Data[1].x = np.append(var.ria.ui.widget.Data[1].x, i[0])
                        var.ria.ui.widget.Data[1].y = np.append(var.ria.ui.widget.Data[1].y, i[self.index[1]+1])
            if self.index[0] == 1:
                if len(var.D2) > 2:
                    for i in var.D2:
                        var.ria.ui.widget.Data[0].x = np.append(var.ria.ui.widget.Data[0].x, i[0])
                        var.ria.ui.widget.Data[0].y = np.append(var.ria.ui.widget.Data[0].y, i[self.index[1]+1])
                    for i in var.T2:
                        var.ria.ui.widget.Data[1].x = np.append(var.ria.ui.widget.Data[1].x, i[0])
                        var.ria.ui.widget.Data[1].y = np.append(var.ria.ui.widget.Data[1].y, i[self.index[1]+1])
            if self.index[0] == 2:
                if len(var.D3) > 2:
                    for i in var.D3:
                        var.ria.ui.widget.Data[0].x = np.append(var.ria.ui.widget.Data[0].x, i[0])
                        var.ria.ui.widget.Data[0].y = np.append(var.ria.ui.widget.Data[0].y, i[self.index[1]+1])
                    for i in var.T3:
                        var.ria.ui.widget.Data[1].x = np.append(var.ria.ui.widget.Data[1].x, i[0])
                        var.ria.ui.widget.Data[1].y = np.append(var.ria.ui.widget.Data[1].y, i[self.index[1]+1])
            if self.index[0] == 3:
                if len(var.D4) > 2:
                    for i in var.D4:
                        var.ria.ui.widget.Data[0].x = np.append(var.ria.ui.widget.Data[0].x, i[0])
                        var.ria.ui.widget.Data[0].y = np.append(var.ria.ui.widget.Data[0].y, i[self.index[1]+1])
                    for i in var.T4:
                        var.ria.ui.widget.Data[1].x = np.append(var.ria.ui.widget.Data[1].x, i[0])
                        var.ria.ui.widget.Data[1].y = np.append(var.ria.ui.widget.Data[1].y, i[self.index[1]+1])

    #inicializa Plot2
    def set_plot2(self):
        if not var.ria.ui.checkPlot2.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget.Plots[2].setTitle("")
            var.ria.ui.widget.Plots[3].setTitle("")
            var.ria.ui.widget.Data[2] = dataclass()
            var.ria.ui.widget.Data[3] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget.Plots[2].setTitle(var.sensor_list[var.ria.ui.PlotBox2.currentIndex()]+" D")
            var.ria.ui.widget.Plots[3].setTitle(var.sensor_list[var.ria.ui.PlotBox2.currentIndex()]+" T")
            var.ria.ui.widget.Data[2] = dataclass()
            var.ria.ui.widget.Data[3] = dataclass()
            """plot dados disponíveis"""
            self.index = divmod(var.ria.ui.PlotBox2.currentIndex(), 8)
            if self.index[0] == 0:
                if len(var.D1) > 2:
                    for i in var.D1:
                        var.ria.ui.widget.Data[2].x = np.append(var.ria.ui.widget.Data[2].x, i[0])
                        var.ria.ui.widget.Data[2].y = np.append(var.ria.ui.widget.Data[2].y, i[(self.index[1]+1)])
                    for i in var.T1:
                        var.ria.ui.widget.Data[3].x = np.append(var.ria.ui.widget.Data[3].x, i[0])
                        var.ria.ui.widget.Data[3].y = np.append(var.ria.ui.widget.Data[3].y, i[(self.index[1]+1)])
            if self.index[0] == 1:
                if len(var.D2) > 2:
                    for i in var.D2:
                        var.ria.ui.widget.Data[2].x = np.append(var.ria.ui.widget.Data[2].x, i[0])
                        var.ria.ui.widget.Data[2].y = np.append(var.ria.ui.widget.Data[2].y, i[(self.index[1]+1)])
                    for i in var.T2:
                        var.ria.ui.widget.Data[3].x = np.append(var.ria.ui.widget.Data[3].x, i[0])
                        var.ria.ui.widget.Data[3].y = np.append(var.ria.ui.widget.Data[3].y, i[(self.index[1]+1)])
            if self.index[0] == 2:
                if len(var.D3) > 2:
                    for i in var.D3:
                        var.ria.ui.widget.Data[2].x = np.append(var.ria.ui.widget.Data[2].x, i[0])
                        var.ria.ui.widget.Data[2].y = np.append(var.ria.ui.widget.Data[2].y, i[self.index[1]+1])
                    for i in var.T3:
                        var.ria.ui.widget.Data[3].x = np.append(var.ria.ui.widget.Data[3].x, i[0])
                        var.ria.ui.widget.Data[3].y = np.append(var.ria.ui.widget.Data[3].y, i[self.index[1]+1])
            if self.index[0] == 3:
                if len(var.D4) > 2:
                    for i in var.D4:
                        var.ria.ui.widget.Data[2].x = np.append(var.ria.ui.widget.Data[2].x, i[0])
                        var.ria.ui.widget.Data[2].y = np.append(var.ria.ui.widget.Data[2].y, i[self.index[1]+1])
                    for i in var.T4:
                        var.ria.ui.widget.Data[3].x = np.append(var.ria.ui.widget.Data[3].x, i[0])
                        var.ria.ui.widget.Data[3].y = np.append(var.ria.ui.widget.Data[3].y, i[self.index[1]+1])

    #inicializa Plot3
    def set_plot3(self):
        if not var.ria.ui.checkPlot3.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget.Plots[4].setTitle("")
            var.ria.ui.widget.Plots[5].setTitle("")
            var.ria.ui.widget.Data[4] = dataclass()
            var.ria.ui.widget.Data[5] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget.Plots[4].setTitle(var.sensor_list[var.ria.ui.PlotBox3.currentIndex()]+" D")
            var.ria.ui.widget.Plots[5].setTitle(var.sensor_list[var.ria.ui.PlotBox3.currentIndex()]+" T")
            var.ria.ui.widget.Data[4] = dataclass()
            var.ria.ui.widget.Data[5] = dataclass()
            """plot dados disponíveis"""
            self.index = divmod(var.ria.ui.PlotBox3.currentIndex(), 8)
            if self.index[0] == 0:
                if len(var.D1) > 2:
                    for i in var.D1:
                        var.ria.ui.widget.Data[4].x = np.append(var.ria.ui.widget.Data[4].x, i[0])
                        var.ria.ui.widget.Data[4].y = np.append(var.ria.ui.widget.Data[4].y, i[self.index[1]+1])
                    for i in var.T1:
                        var.ria.ui.widget.Data[5].x = np.append(var.ria.ui.widget.Data[5].x, i[0])
                        var.ria.ui.widget.Data[5].y = np.append(var.ria.ui.widget.Data[5].y, i[self.index[1]+1])
            if self.index[0] == 1:
                if len(var.D2) > 2:
                    for i in var.D2:
                        var.ria.ui.widget.Data[4].x = np.append(var.ria.ui.widget.Data[4].x, i[0])
                        var.ria.ui.widget.Data[4].y = np.append(var.ria.ui.widget.Data[4].y, i[self.index[1]+1])
                    for i in var.T2:
                        var.ria.ui.widget.Data[5].x = np.append(var.ria.ui.widget.Data[5].x, i[0])
                        var.ria.ui.widget.Data[5].y = np.append(var.ria.ui.widget.Data[5].y, i[self.index[1]+1])
            if self.index[0] == 2:
                if len(var.D3) > 2:
                    for i in var.D3:
                        var.ria.ui.widget.Data[4].x = np.append(var.ria.ui.widget.Data[4].x, i[0])
                        var.ria.ui.widget.Data[4].y = np.append(var.ria.ui.widget.Data[4].y, i[self.index[1]+1])
                    for i in var.T3:
                        var.ria.ui.widget.Data[5].x = np.append(var.ria.ui.widget.Data[5].x, i[0])
                        var.ria.ui.widget.Data[5].y = np.append(var.ria.ui.widget.Data[5].y, i[self.index[1]+1])
            if self.index[0] == 3:
                if len(var.D4) > 2:
                    for i in var.D4:
                        var.ria.ui.widget.Data[4].x = np.append(var.ria.ui.widget.Data[4].x, i[0])
                        var.ria.ui.widget.Data[4].y = np.append(var.ria.ui.widget.Data[4].y, i[self.index[1]+1])
                    for i in var.T4:
                        var.ria.ui.widget.Data[5].x = np.append(var.ria.ui.widget.Data[5].x, i[0])
                        var.ria.ui.widget.Data[5].y = np.append(var.ria.ui.widget.Data[5].y, i[self.index[1]+1])

    #inicializa Plot4
    def set_plot4(self):
        if not var.ria.ui.checkPlot4.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget.Plots[6].setTitle("")
            var.ria.ui.widget.Plots[7].setTitle("")
            var.ria.ui.widget.Data[6] = dataclass()
            var.ria.ui.widget.Data[7] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget.Plots[6].setTitle(var.sensor_list[var.ria.ui.PlotBox4.currentIndex()]+" D")
            var.ria.ui.widget.Plots[7].setTitle(var.sensor_list[var.ria.ui.PlotBox4.currentIndex()]+" T")
            var.ria.ui.widget.Data[6] = dataclass()
            var.ria.ui.widget.Data[7] = dataclass()
            """plot dados disponíveis"""
            self.index = divmod(var.ria.ui.PlotBox4.currentIndex(), 8)
            if self.index[0] == 0:
                if len(var.D1) > 2:
                    for i in var.D1:
                        var.ria.ui.widget.Data[6].x = np.append(var.ria.ui.widget.Data[6].x, i[0])
                        var.ria.ui.widget.Data[6].y = np.append(var.ria.ui.widget.Data[6].y, i[self.index[1]+1])
                    for i in var.T1:
                        var.ria.ui.widget.Data[7].x = np.append(var.ria.ui.widget.Data[7].x, i[0])
                        var.ria.ui.widget.Data[7].y = np.append(var.ria.ui.widget.Data[7].y, i[self.index[1]+1])
            if self.index[0] == 1:
                if len(var.D2) > 2:
                    for i in var.D2:
                        var.ria.ui.widget.Data[6].x = np.append(var.ria.ui.widget.Data[6].x, i[0])
                        var.ria.ui.widget.Data[6].y = np.append(var.ria.ui.widget.Data[6].y, i[self.index[1]+1])
                    for i in var.T2:
                        var.ria.ui.widget.Data[7].x = np.append(var.ria.ui.widget.Data[7].x, i[0])
                        var.ria.ui.widget.Data[7].y = np.append(var.ria.ui.widget.Data[7].y, i[self.index[1]+1])
            if self.index[0] == 2:
                if len(var.D3) > 2:
                    for i in var.D3:
                        var.ria.ui.widget.Data[6].x = np.append(var.ria.ui.widget.Data[6].x, i[0])
                        var.ria.ui.widget.Data[6].y = np.append(var.ria.ui.widget.Data[6].y, i[self.index[1]+1])
                    for i in var.T3:
                        var.ria.ui.widget.Data[7].x = np.append(var.ria.ui.widget.Data[7].x, i[0])
                        var.ria.ui.widget.Data[7].y = np.append(var.ria.ui.widget.Data[7].y, i[self.index[1]+1])
            if self.index[0] == 3:
                if len(var.D4) > 2:
                    for i in var.D4:
                        var.ria.ui.widget.Data[6].x = np.append(var.ria.ui.widget.Data[6].x, i[0])
                        var.ria.ui.widget.Data[6].y = np.append(var.ria.ui.widget.Data[6].y, i[self.index[1]+1])
                    for i in var.T4:
                        var.ria.ui.widget.Data[7].x = np.append(var.ria.ui.widget.Data[7].x, i[0])
                        var.ria.ui.widget.Data[7].y = np.append(var.ria.ui.widget.Data[7].y, i[self.index[1]+1])

    #inicializa Plot5
    def set_plot5(self):
        if not var.ria.ui.checkPlot5.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget.Plots[8].setTitle("")
            var.ria.ui.widget.Plots[9].setTitle("")
            var.ria.ui.widget.Data[8] = dataclass()
            var.ria.ui.widget.Data[9] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget.Plots[8].setTitle(var.sensor_list[var.ria.ui.PlotBox5.currentIndex()]+" D")
            var.ria.ui.widget.Plots[9].setTitle(var.sensor_list[var.ria.ui.PlotBox5.currentIndex()]+" T")
            var.ria.ui.widget.Data[8] = dataclass()
            var.ria.ui.widget.Data[9] = dataclass()
            """plot dados disponíveis"""
            self.index = divmod(var.ria.ui.PlotBox5.currentIndex(), 8)
            if self.index[0] == 0:
                if len(var.D1) > 2:
                    for i in var.D1:
                        var.ria.ui.widget.Data[8].x = np.append(var.ria.ui.widget.Data[8].x, i[0])
                        var.ria.ui.widget.Data[8].y = np.append(var.ria.ui.widget.Data[8].y, i[self.index[1]+1])
                    for i in var.T1:
                        var.ria.ui.widget.Data[9].x = np.append(var.ria.ui.widget.Data[9].x, i[0])
                        var.ria.ui.widget.Data[9].y = np.append(var.ria.ui.widget.Data[9].y, i[self.index[1]+1])
            if self.index[0] == 1:
                if len(var.D2) > 2:
                    for i in var.D2:
                        var.ria.ui.widget.Data[8].x = np.append(var.ria.ui.widget.Data[8].x, i[0])
                        var.ria.ui.widget.Data[8].y = np.append(var.ria.ui.widget.Data[8].y, i[self.index[1]+1])
                    for i in var.T2:
                        var.ria.ui.widget.Data[9].x = np.append(var.ria.ui.widget.Data[9].x, i[0])
                        var.ria.ui.widget.Data[9].y = np.append(var.ria.ui.widget.Data[9].y, i[self.index[1]+1])
            if self.index[0] == 2:
                if len(var.D3) > 2:
                    for i in var.D3:
                        var.ria.ui.widget.Data[8].x = np.append(var.ria.ui.widget.Data[8].x, i[0])
                        var.ria.ui.widget.Data[8].y = np.append(var.ria.ui.widget.Data[8].y, i[self.index[1]+1])
                    for i in var.T3:
                        var.ria.ui.widget.Data[9].x = np.append(var.ria.ui.widget.Data[9].x, i[0])
                        var.ria.ui.widget.Data[9].y = np.append(var.ria.ui.widget.Data[9].y, i[self.index[1]+1])
            if self.index[0] == 3:
                if len(var.D4) > 2:
                    for i in var.D4:
                        var.ria.ui.widget.Data[8].x = np.append(var.ria.ui.widget.Data[8].x, i[0])
                        var.ria.ui.widget.Data[8].y = np.append(var.ria.ui.widget.Data[8].y, i[self.index[1]+1])
                    for i in var.T4:
                        var.ria.ui.widget.Data[9].x = np.append(var.ria.ui.widget.Data[9].x, i[0])
                        var.ria.ui.widget.Data[9].y = np.append(var.ria.ui.widget.Data[9].y, i[self.index[1]+1])

    #inicializa Plot6
    def set_plot6(self):
        if not var.ria.ui.checkPlot6.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget.Plots[10].setTitle("")
            var.ria.ui.widget.Plots[11].setTitle("")
            var.ria.ui.widget.Data[10] = dataclass()
            var.ria.ui.widget.Data[11] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget.Plots[10].setTitle(var.sensor_list[var.ria.ui.PlotBox6.currentIndex()]+" D")
            var.ria.ui.widget.Plots[11].setTitle(var.sensor_list[var.ria.ui.PlotBox6.currentIndex()]+" T")
            var.ria.ui.widget.Data[10] = dataclass()
            var.ria.ui.widget.Data[11] = dataclass()
            """plot dados disponíveis"""
            self.index = divmod(var.ria.ui.PlotBox6.currentIndex(), 8)
            if self.index[0] == 0:
                if len(var.D1) > 2:
                    for i in var.D1:
                        var.ria.ui.widget.Data[10].x = np.append(var.ria.ui.widget.Data[10].x, i[0])
                        var.ria.ui.widget.Data[10].y = np.append(var.ria.ui.widget.Data[10].y, i[self.index[1]+1])
                    for i in var.T1:
                        var.ria.ui.widget.Data[11].x = np.append(var.ria.ui.widget.Data[11].x, i[0])
                        var.ria.ui.widget.Data[11].y = np.append(var.ria.ui.widget.Data[11].y, i[self.index[1]+1])
            if self.index[0] == 1:
                if len(var.D2) > 2:
                    for i in var.D2:
                        var.ria.ui.widget.Data[10].x = np.append(var.ria.ui.widget.Data[10].x, i[0])
                        var.ria.ui.widget.Data[10].y = np.append(var.ria.ui.widget.Data[10].y, i[self.index[1]+1])
                    for i in var.T2:
                        var.ria.ui.widget.Data[11].x = np.append(var.ria.ui.widget.Data[11].x, i[0])
                        var.ria.ui.widget.Data[11].y = np.append(var.ria.ui.widget.Data[11].y, i[self.index[1]+1])
            if self.index[0] == 2:
                if len(var.D3) > 2:
                    for i in var.D3:
                        var.ria.ui.widget.Data[10].x = np.append(var.ria.ui.widget.Data[10].x, i[0])
                        var.ria.ui.widget.Data[10].y = np.append(var.ria.ui.widget.Data[10].y, i[self.index[1]+1])
                    for i in var.T3:
                        var.ria.ui.widget.Data[11].x = np.append(var.ria.ui.widget.Data[11].x, i[0])
                        var.ria.ui.widget.Data[11].y = np.append(var.ria.ui.widget.Data[11].y, i[self.index[1]+1])
            if self.index[0] == 3:
                if len(var.D4) > 2:
                    for i in var.D4:
                        var.ria.ui.widget.Data[10].x = np.append(var.ria.ui.widget.Data[10].x, i[0])
                        var.ria.ui.widget.Data[10].y = np.append(var.ria.ui.widget.Data[10].y, i[self.index[1]+1])
                    for i in var.T4:
                        var.ria.ui.widget.Data[11].x = np.append(var.ria.ui.widget.Data[11].x, i[0])
                        var.ria.ui.widget.Data[11].y = np.append(var.ria.ui.widget.Data[11].y, i[self.index[1]+1])

    #inicializa Plot7
    def set_plot7(self):
        if not var.ria.ui.checkPlot7.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget.Plots[12].setTitle("")
            var.ria.ui.widget.Plots[13].setTitle("")
            var.ria.ui.widget.Data[12] = dataclass()
            var.ria.ui.widget.Data[13] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget.Plots[12].setTitle(var.sensor_list[var.ria.ui.PlotBox7.currentIndex()]+" D")
            var.ria.ui.widget.Plots[13].setTitle(var.sensor_list[var.ria.ui.PlotBox7.currentIndex()]+" T")
            var.ria.ui.widget.Data[12] = dataclass()
            var.ria.ui.widget.Data[13] = dataclass()
            """plot dados disponíveis"""
            self.index = divmod(var.ria.ui.PlotBox7.currentIndex(), 8)
            if self.index[0] == 0:
                if len(var.D1) > 2:
                    for i in var.D1:
                        var.ria.ui.widget.Data[12].x = np.append(var.ria.ui.widget.Data[12].x, i[0])
                        var.ria.ui.widget.Data[12].y = np.append(var.ria.ui.widget.Data[12].y, i[self.index[1]+1])
                    for i in var.T1:
                        var.ria.ui.widget.Data[13].x = np.append(var.ria.ui.widget.Data[13].x, i[0])
                        var.ria.ui.widget.Data[13].y = np.append(var.ria.ui.widget.Data[13].y, i[self.index[1]+1])
            if self.index[0] == 1:
                if len(var.D2) > 2:
                    for i in var.D2:
                        var.ria.ui.widget.Data[12].x = np.append(var.ria.ui.widget.Data[12].x, i[0])
                        var.ria.ui.widget.Data[12].y = np.append(var.ria.ui.widget.Data[12].y, i[self.index[1]+1])
                    for i in var.T2:
                        var.ria.ui.widget.Data[13].x = np.append(var.ria.ui.widget.Data[13].x, i[0])
                        var.ria.ui.widget.Data[13].y = np.append(var.ria.ui.widget.Data[13].y, i[self.index[1]+1])
            if self.index[0] == 2:
                if len(var.D3) > 2:
                    for i in var.D3:
                        var.ria.ui.widget.Data[12].x = np.append(var.ria.ui.widget.Data[12].x, i[0])
                        var.ria.ui.widget.Data[12].y = np.append(var.ria.ui.widget.Data[12].y, i[self.index[1]+1])
                    for i in var.T3:
                        var.ria.ui.widget.Data[13].x = np.append(var.ria.ui.widget.Data[13].x, i[0])
                        var.ria.ui.widget.Data[13].y = np.append(var.ria.ui.widget.Data[13].y, i[self.index[1]+1])
            if self.index[0] == 3:
                if len(var.D4) > 2:
                    for i in var.D4:
                        var.ria.ui.widget.Data[12].x = np.append(var.ria.ui.widget.Data[12].x, i[0])
                        var.ria.ui.widget.Data[12].y = np.append(var.ria.ui.widget.Data[12].y, i[self.index[1]+1])
                    for i in var.T4:
                        var.ria.ui.widget.Data[13].x = np.append(var.ria.ui.widget.Data[13].x, i[0])
                        var.ria.ui.widget.Data[13].y = np.append(var.ria.ui.widget.Data[13].y, i[self.index[1]+1])

    #inicializa Plot8
    def set_plot8(self):
        if not var.ria.ui.checkPlot8.isChecked():
            """apaga plot e nome caso esteja desabilitado"""
            var.ria.ui.widget.Plots[14].setTitle("")
            var.ria.ui.widget.Plots[15].setTitle("")
            var.ria.ui.widget.Data[14] = dataclass()
            var.ria.ui.widget.Data[15] = dataclass()
        else:
            """muda nome do plot"""
            var.ria.ui.widget.Plots[14].setTitle(var.sensor_list[var.ria.ui.PlotBox8.currentIndex()]+" D")
            var.ria.ui.widget.Plots[15].setTitle(var.sensor_list[var.ria.ui.PlotBox8.currentIndex()]+" T")
            var.ria.ui.widget.Data[14] = dataclass()
            var.ria.ui.widget.Data[15] = dataclass()
            """plot dados disponíveis"""
            self.index = divmod(var.ria.ui.PlotBox8.currentIndex(), 8)
            if self.index[0] == 0:
                if len(var.D1) > 2:
                    for i in var.D1:
                        var.ria.ui.widget.Data[14].x = np.append(var.ria.ui.widget.Data[14].x, i[0])
                        var.ria.ui.widget.Data[14].y = np.append(var.ria.ui.widget.Data[14].y, i[self.index[1]+1])
                    for i in var.T1:
                        var.ria.ui.widget.Data[15].x = np.append(var.ria.ui.widget.Data[15].x, i[0])
                        var.ria.ui.widget.Data[15].y = np.append(var.ria.ui.widget.Data[15].y, i[self.index[1]+1])
            if self.index[0] == 1:
                if len(var.D2) > 2:
                    for i in var.D2:
                        var.ria.ui.widget.Data[14].x = np.append(var.ria.ui.widget.Data[14].x, i[0])
                        var.ria.ui.widget.Data[14].y = np.append(var.ria.ui.widget.Data[14].y, i[self.index[1]+1])
                    for i in var.T2:
                        var.ria.ui.widget.Data[15].x = np.append(var.ria.ui.widget.Data[15].x, i[0])
                        var.ria.ui.widget.Data[15].y = np.append(var.ria.ui.widget.Data[15].y, i[self.index[1]+1])
            if self.index[0] == 2:
                if len(var.D3) > 2:
                    for i in var.D3:
                        var.ria.ui.widget.Data[14].x = np.append(var.ria.ui.widget.Data[14].x, i[0])
                        var.ria.ui.widget.Data[14].y = np.append(var.ria.ui.widget.Data[14].y, i[self.index[1]+1])
                    for i in var.T3:
                        var.ria.ui.widget.Data[15].x = np.append(var.ria.ui.widget.Data[15].x, i[0])
                        var.ria.ui.widget.Data[15].y = np.append(var.ria.ui.widget.Data[15].y, i[self.index[1]+1])
            if self.index[0] == 3:
                if len(var.D4) > 2:
                    for i in var.D4:
                        var.ria.ui.widget.Data[14].x = np.append(var.ria.ui.widget.Data[14].x, i[0])
                        var.ria.ui.widget.Data[14].y = np.append(var.ria.ui.widget.Data[14].y, i[self.index[1]+1])
                    for i in var.T4:
                        var.ria.ui.widget.Data[15].x = np.append(var.ria.ui.widget.Data[15].x, i[0])
                        var.ria.ui.widget.Data[15].y = np.append(var.ria.ui.widget.Data[15].y, i[self.index[1]+1])

    
    #atualiza tabela com os valores recebidos
    def refresh_table(self, i):
        if i == 1:
            try:
                len(var.D1[0])
                """atualiza tabela na interface"""
                for j in range(8):
                    """atualiza valores em D"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.D1[-1][(j+1)]))
                    var.ria.ui.tableWidget.setItem(0,j, self.item)
                    """atualiza valores de D-Do"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %(var.D1[-1][(j+1)] - var.Do[0][j])))        
                    var.ria.ui.tableWidget.setItem(1,j, self.item)
                    """atualiza valores em Davg"""
                    var.Davg[0][j] = var.wlast*var.Davg[0][j] + var.wcurr*var.D1[-1][(j+1)]
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Davg[0][j]))
                    var.ria.ui.tableWidget.setItem(2,j, self.item)
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Davg[0][j]))
                    var.ria.ui.tableWidget_3.setItem(0,j, self.item)
                    """atualiza valores em T"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.T1[-1][(j+1)]))
                    var.ria.ui.tableWidget.setItem(3,j, self.item)
                    """atualiza valores de T-To"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %(var.T1[-1][(j+1)] - var.To[0][j])))        
                    var.ria.ui.tableWidget.setItem(4,j, self.item)
                    """atualiza valores em Tavg"""
                    var.Tavg[0][j] = var.wlast*var.Tavg[0][j] + var.wcurr*var.T1[-1][(j+1)]
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Tavg[0][j]))
                    var.ria.ui.tableWidget.setItem(5,j, self.item)
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Tavg[0][j]))
                    var.ria.ui.tableWidget_3.setItem(1,j, self.item)
            except IndexError:
                "não atualiza caso haja apenas um conjunto de dados em D1"""
                print("erro ao atualizar rack 1")
                pass
            except TypeError:
                "não atualiza caso haja apenas um conjunto de dados em D1"""
                print("erro ao atualizar rack 1")
                pass
                
        elif i == 2:
            try:
                len(var.D2[0])
                """atualiza tabela na interface"""
                for j in range(8):
                    """atualiza valores em D"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.D2[-1][(j+1)]))
                    var.ria.ui.tableWidget.setItem(0,(j+8), self.item)
                    """atualiza valores de D-Do"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %(var.D2[-1][(j+1)] - var.Do[1][j])))        
                    var.ria.ui.tableWidget.setItem(1,(j+8), self.item)
                    """atualiza valores em Davg"""
                    var.Davg[1][j] = var.wlast*var.Davg[1][j] + var.wcurr*var.D2[-1][(j+1)]
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Davg[1][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(2,(j+8), self.item)
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Davg[1][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_3.setItem(0,(j+8), self.item)
                    """atualiza valores em T"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.T2[-1][(j+1)]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(3,(j+8), self.item)
                    """atualiza valores de T-To"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %(var.T2[-1][(j+1)] - var.To[1][j])))        
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(4,(j+8), self.item)
                    """atualiza valores em Tavg"""
                    var.Tavg[1][j] = var.wlast*var.Tavg[1][j] + var.wcurr*var.T2[-1][(j+1)]
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Tavg[1][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(5,(j+8), self.item)
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Tavg[1][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_3.setItem(1,(j+8), self.item)
            except IndexError:
                "não atualiza caso haja apenas um conjunto de dados em D2"""
                print("erro ao atualizar rack 2")
                pass
            except TypeError:
                "não atualiza caso haja apenas um conjunto de dados em D2"""
                print("erro ao atualizar rack 2")
                pass
        elif i == 3:
            try:
                len(var.D3[0])
                """atualiza tabela na interface"""
                for j in range(8):
                    """atualiza valores em D"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.D3[-1][(j+1)]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(0,(j+16), self.item)
                    """atualiza valores de D-Do"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %(var.D3[-1][(j+1)] - var.Do[2][j])))        
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(1,(j+16), self.item)
                    """atualiza valores em Davg"""
                    var.Davg[2][j] = var.wlast*var.Davg[2][j] + var.wcurr*var.D3[-1][(j+1)]
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Davg[2][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(2,(j+16), self.item)
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Davg[2][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_3.setItem(0,(j+16), self.item)
                    """atualiza valores em T"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.T3[-1][(j+1)]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(3,(j+16), self.item)
                    """atualiza valores de T-To"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %(var.T3[-1][(j+1)] - var.To[1][j])))        
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(4,(j+16), self.item)
                    """atualiza valores em Tavg"""
                    var.Tavg[2][j] = var.wlast*var.Tavg[2][j] + var.wcurr*var.T3[-1][(j+1)]
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Tavg[2][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(5,(j+16), self.item)
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Tavg[2][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_3.setItem(1,(j+16), self.item)
            except IndexError:
                "não atualiza caso haja apenas um conjunto de dados em D3"""
                print("erro ao atualizar rack 3")
                pass
            except TypeError:
                "não atualiza caso haja apenas um conjunto de dados em D3"""
                print("erro ao atualizar rack 3")
                pass
        if i == 4:
            try:
                len(var.D4[0])
                """atualiza tabela na interface"""
                for j in range(6):
                    """atualiza valores em D"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.D4[-1][(j+1)]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(0,(j+24), self.item)
                    """atualiza valores de D-Do"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %(var.D4[-1][(j+1)] - var.Do[3][j])))        
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(1,(j+24), self.item)
                    """atualiza valores em Davg"""
                    var.Davg[3][j] = var.wlast*var.Davg[3][j] + var.wcurr*var.D4[-1][(j+1)]
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Davg[3][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(2,(j+24), self.item)
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Davg[3][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_3.setItem(0,(j+24), self.item)
                    """atualiza valores em T"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.T4[-1][(j+1)]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(3,(j+24), self.item)
                    """atualiza valores de T-To"""
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %(var.T4[-1][(j+1)] - var.To[3][j])))        
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(4,(j+24), self.item)
                    """atualiza valores em Tavg"""
                    var.Tavg[3][j] = var.wlast*var.Tavg[3][j] + var.wcurr*var.T4[-1][(j+1)]
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Tavg[3][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(5,(j+24), self.item)
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Tavg[3][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_3.setItem(1,(j+24), self.item)
            except IndexError:
                "não atualiza caso haja apenas um conjunto de dados em D4"""
                print("erro ao atualizar rack 4")
                pass
            except TypeError:
                "não atualiza caso haja apenas um conjunto de dados em D4"""
                print("erro ao atualizar rack 4")
                pass

            

    ###Fim das funções diretamente relacionadas à interface

        
    #gera checksum dos dados enviados
    def checksum(self, data):
        self.sum = 0
        """soma bytes dos dados a serem enviados"""
        for i in range(len(data)):
            self.sum += ord(data[i])
        """cria representação binária da soma"""
        self.bin = np.binary_repr(self.sum, 8)
        """nega todos os bits"""
        self.neg = self.bin.translate(self.bin.maketrans("10","01"))
        """soma 1 à negação"""
        self.neg1 = np.binary_repr(int(self.neg, 2)+1)
        """toma os 8 Least Significant Bits do valor anterior: é o checksum"""
        self.csum = int(self.neg1[-8:],2)
        """converte o checksum para caractere a ser enviado via serial"""
        self.csum_data = chr(self.csum)

        return self.csum_data

    #converte dados enviados de hexa para string
    def hex_to_str(self, data):
        data = data + self.checksum(data)
        self.data_str = chr(0x02)
        for i in range(len(data)):
            self.hex = hex(ord(data[i]))
            if len(self.hex) == 4:
                self.data_str = self.data_str + self.hex[2].capitalize() + self.hex[3].capitalize()
            elif len(self.hex) == 3:
                self.data_str = self.data_str + '0' + self.hex[2]
            else:
                print('erro na conversão do valor hexadecimal para string')
        self.data_str = self.data_str + chr(0x03)

        return self.data_str
    
    #checa se checksum de resposta do rack está correto
    def check_response(self, response):
        self.sum = 0
        self.len = len(response)
        self.str = chr(0x00)
        for i in range(self.len - 1):
            if i == 0 or divmod(i, 2)[1] == 0:
                pass
            else:
                self.sum += int(('0x'+response[i:(i+2)]), 16)
                
        #se self.sum não for múltiplo de 256, erro no checksum
        if divmod(self.sum, 256)[1] != 0:
            print(hex(self.sum)[-2:-1] + " erro no checksum")
        
            
    #converte valores de tensão recebidos dos racks para nível e temperatura
    def v_converter(self, resp, i):
        self.vtmp = np.array([])
        self.exp = 0
        self.mantissa = 0
        self.output = 0
        self.sig = ''
        self.v = np.array([])
        self.vout = np.array([])
        self.timesec = time.time()
        self.D = np.array([self.timesec])
        self.T = np.array([self.timesec])
        
        if resp[4] != '0':
            """muda flag de status do rack"""
            var.rack_status[(i-1)] = False
            if i == 1:
                var.ria.ui.led1_g.hide()
                var.ria.ui.led1_y.show()
            if i == 2:
                var.ria.ui.led2_g.hide()
                var.ria.ui.led2_y.show()
            if i == 3:
                var.ria.ui.led3_g.hide()
                var.ria.ui.led3_y.show()
            if i == 4:
                var.ria.ui.led4_g.hide()
                var.ria.ui.led4_y.show()            
            """checa status em caso de flag de erro no rack"""
            self.check_status([i])
            """caso rack não retorne erros, muda flag de status"""
        elif var.rack_status[(i-1)] == False:
            var.rack_status[(i-1)] = True
            if i == 1:
                var.ria.ui.led1_g.show()
            if i == 2:
                var.ria.ui.led2_g.show()
            if i == 3:
                var.ria.ui.led3_g.show()
            if i == 4:
                var.ria.ui.led4_g.show()
            
        for j in range(16):
            """converte os caracteres recebidos para bits, permitindo recuperar
            o valor de ponto flutuante da tensão"""
            self.tmp0 = np.binary_repr(int(('0x'+resp[8*j+11]+resp[8*j+12]), 16), 8)
            self.tmp1 = np.binary_repr(int(('0x'+resp[8*j+9]+resp[8*j+10]), 16), 8)
            self.tmp2 = np.binary_repr(int(('0x'+resp[8*j+7]+resp[8*j+8]), 16), 8)
            self.tmp3 = np.binary_repr(int(('0x'+resp[8*j+5]+resp[8*j+6]), 16), 8)
            self.vtmp = np.append(self.vtmp, (self.tmp0 + self.tmp1 + self.tmp2 +
                                                     self.tmp3))
            """recupera o sinal da tensão"""
            if self.vtmp[j][0] == '0':
                self.sig = ''
            else:
                self.sig = '-'

            """recupera o expoente da tensão"""
##            self.exp = int(('0b' + self.vtmp[j][1:9]), 2) - 129
            self.exp = int(('0b' + self.vtmp[j][1:9]), 2) - 127
            self.mantissa = (int(('0b' + self.vtmp[j][9:]), 2)/2**23 + 1)
            self.output = float(self.sig+str(self.mantissa))*2**self.exp
            
            """Mantissa de índices pares, relativos às medidas de nível"""
            if divmod(j, 2)[1] == 0:
##                self.mantissa = (int(('0b' + self.vtmp[j][9:]), 2)/2**23 + 1)*4
##                self.output = float(self.sig+str(self.mantissa)+'e'+str(self.exp))
                self.output = var.D_Rack[i-1][int(j/2)](self.output)
                self.D = np.append(self.D, self.output)            
                
                """Mantissa de índices ímpares, relativos à medidas de temperatura"""
            else:
##                self.mantissa = (int(('0b' + self.vtmp[j][9:]), 2)/2**23 + 1)*4
                """multiplica tensão por 5, fator de conversão da temperatura"""
##                self.output = float(self.sig+str(self.mantissa)+'e'+str(self.exp))*5
##                self.output = self.output*5
                self.output = var.pol_T(self.output)
                self.T = np.append(self.T, self.output)
            self.vout = np.append(self.vout, self.output)
                
        self.v = np.reshape(self.vout, (8,2))

        """correção de nível por dilatação térmica da água:"""
        self.Cag = (var.F(self.T[1:]) - var.F(np.ones(8)*var.Tref))/(1e5-var.F(self.T[1:]))
        self.Cdag = (np.ones(8)*var.Hdiff - self.D[1:] - np.ones(8)*var.Pt)*self.Cag
        """correção de nível por dilatação térmica do recipiente:"""
        self.Cm = var.Hdiff*var.Cdil_vessel*1e-6*(self.T[1:] - np.ones(8)*var.Tref)
        """aplicação das correções:"""
        self.D[1:] = self.D[1:] + self.Cdag - self.Cm
        #self.D[10] = var.H7DC_041(self.D[10])
            
    
            

    #envia dados para racks
    def send(self, data):
        self.response = ""
        self.to_write = self.hex_to_str(data)
        #print('\n'+'Tx: ' + self.to_write)
        self.ser.write(self.to_write.encode("utf-8"))
        time.sleep(0.3)
        self.response = self.ser.read(200).decode("utf-8")
        #print('\n'+'Rx: ' + self.response)
        self.check_response(self.response)

    def send1(self, data):
        self.response = ""
        print('\n'+'Tx: ' + data)
        self.ser.write(data.encode("utf-8"))
        time.sleep(0.3)
        self.response = self.ser.read(200).decode("utf-8")
        print('\n'+'Rx: ' + self.response)
        self.check_response(self.response)
        
       
    #inicializa racks
    def init_rack(self, address):
        for i in address:
            if i > 0 and i < 5:    
                self.data = chr(i) + chr(0xf0)
                self.send(self.data)
                time.sleep(1.2)

                self.data = chr(i) + chr(0xf1)                
                self.send(self.data)
                time.sleep(0.1)
                if self.response == "" and i == 1:
                    var.rack_status[0] = False
                    var.ria.ui.led1_g.hide()
                    var.ria.ui.led1_y.show()
                if self.response == "" and i == 2:
                    var.rack_status[1] = False
                    var.ria.ui.led2_g.hide()
                    var.ria.ui.led2_y.show()
                if self.response == "" and i == 3:
                    var.rack_status[2] = False
                    var.ria.ui.led3_g.hide()
                    var.ria.ui.led3_y.show()
                if self.response == "" and i == 4:
                    var.rack_status[3] = False
                    var.ria.ui.led4_g.hide()
                    var.ria.ui.led4_y.show()               
            else:
                print("Rack address out of range")


    #requisita e salva dados dos sensores
    def acquire(self, address):
        for i in address:
            if i < 5 and i > 0:
                self.date = time.strftime("%d_%m_%Y", time.localtime()) #adquire data
                self.time = time.strftime("%H:%M:%S", time.localtime()) #adquire hora
                self.send(chr(i)+chr(0x30)+chr(0x08))
                if self.response == "":
                    if self.response == "" and i == 1:
                        var.rack_status[0] = False
                        var.ria.ui.led1_g.hide()
                        var.ria.ui.led1_y.show()
                    if self.response == "" and i == 2:
                        var.rack_status[1] = False
                        var.ria.ui.led2_g.hide()
                        var.ria.ui.led2_y.show()
                    if self.response == "" and i == 3:
                        var.rack_status[2] = False
                        var.ria.ui.led3_g.hide()
                        var.ria.ui.led3_y.show()
                    if self.response == "" and i == 4:
                        var.rack_status[3] = False
                        var.ria.ui.led4_g.hide()
                        var.ria.ui.led4_y.show()
                    print("Não foi possível estabelecer comunicação com o Rack %d"%i) 
                    print("\n")
                elif self.response[4] == '1':
                    print('Falha no Rack %d  \n' %i)
                    self.check_status([i])
                else:
                    try:
                        self.v_converter(self.response, i)
                    except:
                        print("erro em v_converter")
                        raise
                    #print(self.v)
                    if i == 1:
                        """atualiza D1"""
                        try:
                            var.D1 = np.row_stack([var.D1, self.D])
                            var.T1 = np.row_stack([var.T1, self.T])
                        except ValueError:
                            var.D1 = np.append(var.D1, self.D)
                            var.T1 = np.append(var.T1, self.T)
                        if len(var.D1) > var.cmp:
                            var.D1 = var.D1[1:]
                            var.T1 = var.T1[1:]
                    elif i == 2:
                        """atualiza D2"""
                        try:
                            var.D2 = np.row_stack([var.D2, self.D])
                            var.T2 = np.row_stack([var.T2, self.T])
                        except ValueError:
                            var.D2 = np.append(var.D2, self.D)
                            var.T2 = np.append(var.T2, self.T)
                        if len(var.D2) > var.cmp:
                            var.D2 = var.D2[1:]
                            var.T2 = var.T2[1:]
                    elif i == 3:
                        """atualiza D3"""
                        try:
                            var.D3 = np.row_stack([var.D3, self.D])
                            var.T3 = np.row_stack([var.T3, self.T])
                        except ValueError:
                            var.D3 = np.append(var.D3, self.D)
                            var.T3 = np.append(var.T3, self.T)
                        if len(var.D3) > var.cmp:
                            var.D3 = var.D3[1:]
                            var.T3 = var.T3[1:]
                    elif i == 4:
                        """atualiza D4"""
                        try:
                            var.D4 = np.row_stack([var.D4, self.D])
                            var.T4 = np.row_stack([var.T4, self.T])
                        except ValueError:
                            var.D4 = np.append(var.D4, self.D)
                            var.T4 = np.append(var.T4, self.T)
                        if len(var.D4) > var.cmp:
                            var.D4 = var.D4[1:]
                            var.T4 = var.T4[1:]
                self.refresh_table(i)
                try:
                    self.plot(i)
                except ValueError:
                    pass
                except IndexError:
                    pass
                except:
                    print('erro em plot line 1062')
            else:
                print('Endereço %i não existe \n' %i)

        try:
            #aux.plotFlagRIAcom = True #NOVO - Flag para liberar o plot dos racks simultaneamente no 'Online'
            self.save_log(address)
            #aux.plotFlagRIAcom = False #NOVO        
        except:
            print("Erro FlagRIAcom")
            raise
        
    #checa status do(s) rack(s)
    def check_status(self, address):
        for i in address:
            if i < 5 and i > 0:
                self.send(chr(i)+chr(0xF6))
                if self.response == "":
                    print("Não foi possível estabelecer comunicação com o Rack %d"%i) 
                    print("\n")
                elif self.response[3:5] == '00':
                    print('Rack %d ok \n' %i)
                elif self.response[3:5] == 'FF':
                    print('Sistema de segurança do Rack %d ativado \n' %i)
            else:
                print('Endereço %i não existe \n' %i)


    #salva dados dos sensores    
    def save_log(self, address):
        """adquire data e hora em que os dados foram salvos e tira a média"""
        self.date = time.strftime("%Y_%m_%d", time.localtime()) #adquire data
        self.date1 = self.date.replace('_','/')
        self.time = time.strftime("%H:%M:%S", time.localtime()) #adquire hora

        self.dir = 'Data/'
        """salva dados em arquivos nomeados por data, na forma:
        data, hora, D1, D2, D3, D4, D5, D6, D7, D8, T1, T2, T3, T4, T5, T6, T7, T8"""        
        for i in address:
            if i < 5 and i > 0:
                try:
                    """salva dados do rack 1"""
                    if i == 1:
                        len(var.D1[0])  #teste para ver se há mais de um elemento em D                  
                        try:
                            f = open(self.dir+'rack'+ str(i) + '_' + self.date + '.dat', 'r')
                            with open(self.dir+'rack'+ str(i) + '_' + self.date + '.dat', 'a') as f:
                                f.write(str(self.date1) + '\t' + str(self.time) + '\t')
                                for a in var.D1[-1][1:]:
                                    f.write(str(a)+'\t')
                                for a in var.T1[-1][1:]:
                                    f.write(str(a)+'\t')
                                f.write('\n')
                        except:
                            with open(self.dir+'rack'+ str(i) + '_' + self.date + '.dat', 'a') as f:
                                ### antiga escrita na saida com nomes genéricos ###
                                """f.write('data'+'\t'+'hora'+'\t'+'D32'+'\t'+'D33'+'\t'+'D34'+'\t'+'D35'+'\t'+'D36'+
                                        '\t'+'D37'+'\t'+'D38'+'\t'+'D39'+'\t'+'T32'+'\t'+'T33'+'\t'+'T34'+'\t'+'T35'+
                                        '\t'+'T36'+'\t'+'T37'+'\t'+'T38'+'\t'+'T39'+'\n')"""
                                ### nova escrita na saida ###
                                f.write('data'+'\t'+'hora'+'\t'+var.disp_sensores[i-1][0]+'_D'+'\t'+var.disp_sensores[i-1][1]+'_D'+'\t'+
                                        var.disp_sensores[i-1][2]+'_D'+'\t'+var.disp_sensores[i-1][3]+'_D'+'\t'+var.disp_sensores[i-1][4]+'_D'+'\t'+
                                        var.disp_sensores[i-1][5]+'_D'+'\t'+var.disp_sensores[i-1][6]+'_D''\t'+var.disp_sensores[i-1][7]+'_D'+'\t'+
                                        var.disp_sensores[i-1][0]+'_T'+'\t'+var.disp_sensores[i-1][1]+'_T'+'\t'+var.disp_sensores[i-1][2]+'_T'+'\t'+
                                        var.disp_sensores[i-1][3]+'_T'+'\t'+var.disp_sensores[i-1][4]+'_T'+'\t'+var.disp_sensores[i-1][5]+'_T'+'\t'+
                                        var.disp_sensores[i-1][6]+'_T'+'\t'+var.disp_sensores[i-1][7]+'_T'+'\n')
                                f.write(str(self.date1) + '\t' + str(self.time) + '\t')
                                for a in var.D1[-1][1:]:
                                    f.write(str(a)+'\t')
                                for a in var.T1[-1][1:]:
                                    f.write(str(a)+'\t')
                                f.write('\n')

                    """salva dados do rack 2"""
                    if i == 2:
                        len(var.D2[0])  #teste para ver se há mais de um elemento em D                
                        try:
                            f = open(self.dir+'rack'+ str(i) + '_' + self.date + '.dat', 'r')
                            with open(self.dir+'rack'+ str(i) + '_' + self.date + '.dat', 'a') as f:
                                f.write(str(self.date1) + '\t' + str(self.time) + '\t')
                                for a in var.D2[-1][1:]:
                                    f.write(str(a)+'\t')
                                for a in var.T2[-1][1:]:
                                    f.write(str(a)+'\t')
                                f.write('\n')
                        except:
                            with open(self.dir+'rack'+ str(i) + '_' + self.date + '.dat', 'a') as f:
                                """f.write('data'+'\t'+'hora'+'\t'+'D40'+'\t'+'D41'+'\t'+'D42'+'\t'+'D43'+'\t'+'D44'+
                                        '\t'+'D45'+'\t'+'D46'+'\t'+'D47'+'\t'+'T40'+'\t'+'T41'+'\t'+'T42'+'\t'+'T43'+
                                        '\t'+'T44'+'\t'+'T45'+'\t'+'T46'+'\t'+'T47'+'\n')"""
                                f.write('data'+'\t'+'hora'+'\t'+var.disp_sensores[i-1][0]+'_D'+'\t'+var.disp_sensores[i-1][1]+'_D'+'\t'+
                                        var.disp_sensores[i-1][2]+'_D'+'\t'+var.disp_sensores[i-1][3]+'_D'+'\t'+var.disp_sensores[i-1][4]+'_D'+'\t'+
                                        var.disp_sensores[i-1][5]+'_D'+'\t'+var.disp_sensores[i-1][6]+'_D''\t'+var.disp_sensores[i-1][7]+'_D'+'\t'+
                                        var.disp_sensores[i-1][0]+'_T'+'\t'+var.disp_sensores[i-1][1]+'_T'+'\t'+var.disp_sensores[i-1][2]+'_T'+'\t'+
                                        var.disp_sensores[i-1][3]+'_T'+'\t'+var.disp_sensores[i-1][4]+'_T'+'\t'+var.disp_sensores[i-1][5]+'_T'+'\t'+
                                        var.disp_sensores[i-1][6]+'_T'+'\t'+var.disp_sensores[i-1][7]+'_T'+'\n')
                                f.write(str(self.date1) + '\t' + str(self.time) + '\t')
                                for a in var.D2[-1][1:]:
                                    f.write(str(a)+'\t')
                                for a in var.T2[-1][1:]:
                                    f.write(str(a)+'\t')
                                f.write('\n')

                    """salva dados do rack 3"""
                    if i == 3:
                        len(var.D3[0])  #teste para ver se há mais de um elemento em D                   
                        try:
                            f = open(self.dir+'rack'+ str(i) + '_' + self.date + '.dat', 'r')
                            with open(self.dir+'rack'+ str(i) + '_' + self.date + '.dat', 'a') as f:
                                f.write(str(self.dateacquire1) + '\t' + str(self.time) + '\t')
                                for a in var.D3[-1][1:]:
                                    f.write(str(a)+'\t')
                                for a in var.T3[-1][1:]:
                                    f.write(str(a)+'\t')
                                f.write('\n')
                        except:
                            with open(self.dir+'rack'+ str(i) + '_' + self.date + '.dat', 'a') as f:
                                """f.write('data'+'\t'+'hora'+'\t'+'D48'+'\t'+'D49'+'\t'+'D50'+'\t'+'D51'+'\t'+'D52'+
                                        '\t'+'D53'+'\t'+'D54'+'\t'+'D55'+'\t'+'T48'+'\t'+'T49'+'\t'+'T50'+'\t'+'T51'+
                                        '\t'+'T52'+'\t'+'T53'+'\t'+'T54'+'\t'+'T55'+'\n')"""
                                f.write('data'+'\t'+'hora'+'\t'+var.disp_sensores[i-1][0]+'_D'+'\t'+var.disp_sensores[i-1][1]+'_D'+'\t'+
                                        var.disp_sensores[i-1][2]+'_D'+'\t'+var.disp_sensores[i-1][3]+'_D'+'\t'+var.disp_sensores[i-1][4]+'_D'+'\t'+
                                        var.disp_sensores[i-1][5]+'_D'+'\t'+var.disp_sensores[i-1][6]+'_D''\t'+var.disp_sensores[i-1][7]+'_D'+'\t'+
                                        var.disp_sensores[i-1][0]+'_T'+'\t'+var.disp_sensores[i-1][1]+'_T'+'\t'+var.disp_sensores[i-1][2]+'_T'+'\t'+
                                        var.disp_sensores[i-1][3]+'_T'+'\t'+var.disp_sensores[i-1][4]+'_T'+'\t'+var.disp_sensores[i-1][5]+'_T'+'\t'+
                                        var.disp_sensores[i-1][6]+'_T'+'\t'+var.disp_sensores[i-1][7]+'_T'+'\n')
                                f.write(str(self.date1) + '\t' + str(self.time) + '\t')
                                for a in var.D3[-1][1:]:
                                    f.write(str(a)+'\t')
                                for a in var.T3[-1][1:]:
                                    f.write(str(a)+'\t')
                                f.write('\n')

                    """salva dados do rack 4"""
                    if i == 4:
                        len(var.D4[0])  #teste para ver se há mais de um elemento em D                    
                        try:
                            f = open(self.dir+'rack'+ str(i) + '_' + self.date + '.dat', 'r')
                            with open(self.dir+'rack'+ str(i) + '_' + self.date + '.dat', 'a') as f:
                                f.write(str(self.date1) + '\t' + str(self.time) + '\t')
                                for a in var.D4[-1][1:]:
                                    f.write(str(a)+'\t')
                                for a in var.T4[-1][1:]:
                                    f.write(str(a)+'\t')
                                f.write('\n')
                        except:
                            with open(self.dir+'rack'+ str(i) + '_' + self.date + '.dat', 'a') as f:
                                """f.write('data'+'\t'+'hora'+'\t'+'D56'+'\t'+'D57'+'\t'+'D58'+'\t'+'D59'+'\t'+'D60'+
                                        '\t'+'D61'+'\t'+'D62'+'\t'+'D63'+'\t'+'T56'+'\t'+'T57'+'\t'+'T58'+'\t'+'T59'+
                                        '\t'+'T60'+'\t'+'T61'+'\t'+'T62'+'\t'+'T63'+'\n')"""
                                f.write('data'+'\t'+'hora'+'\t'+var.disp_sensores[i-1][0]+'_D'+'\t'+var.disp_sensores[i-1][1]+'_D'+'\t'+
                                        var.disp_sensores[i-1][2]+'_D'+'\t'+var.disp_sensores[i-1][3]+'_D'+'\t'+var.disp_sensores[i-1][4]+'_D'+'\t'+
                                        var.disp_sensores[i-1][5]+'_D'+'\t'+var.disp_sensores[i-1][6]+'_D''\t'+var.disp_sensores[i-1][7]+'_D'+'\t'+
                                        var.disp_sensores[i-1][0]+'_T'+'\t'+var.disp_sensores[i-1][1]+'_T'+'\t'+var.disp_sensores[i-1][2]+'_T'+'\t'+
                                        var.disp_sensores[i-1][3]+'_T'+'\t'+var.disp_sensores[i-1][4]+'_T'+'\t'+var.disp_sensores[i-1][5]+'_T'+'\t'+
                                        var.disp_sensores[i-1][6]+'_T'+'\t'+var.disp_sensores[i-1][7]+'_T'+'\n')
                                f.write(str(self.date1) + '\t' + str(self.time) + '\t')
                                for a in var.D4[-1][1:]:
                                    f.write(str(a)+'\t')
                                for a in var.T4[-1][1:]:
                                    f.write(str(a)+'\t')
                                f.write('\n')
                    #print('Dados do rack %d salvos.' %i)
                except TypeError:
                    """não salva nada caso haja apenas um elemento em D"""                
                    pass
                except IndexError:
                    """não salva nada caso haja apenas um elemento em D"""                
                    pass                        

            else:
                print('Endereço %i não existe \n' %i)

    

    #salva parâmetros em disco
    def save_param(self):
        with open('parameters.dat', 'w') as f:
            """salva parâmetros t_aq, t_int, cmp, rack1, rack2, rack3, rack4"""
            f.write(str(var.t_aq) + '\n' +  '\n' + str(var.cmp)
                    + '\n' + str(var.rack1) + '\n' + str(var.rack2) + '\n' +
                    str(var.rack3) + '\n' + str(var.rack4) + '\n')

            """salva Do"""
            for a in var.Do[0]:
                f.write(str(a)+'\t')
            f.write('\n')
            for a in var.Do[1]:
                f.write(str(a)+'\t')
            f.write('\n')
            for a in var.Do[2]:
                f.write(str(a)+'\t')
            f.write('\n')
            for a in var.Do[3]:
                f.write(str(a)+'\t')
            f.write('\n')

            """salva To"""
            for a in var.To[0]:
                f.write(str(a)+'\t')
            f.write('\n')
            for a in var.To[1]:
                f.write(str(a)+'\t')
            f.write('\n')
            for a in var.To[2]:
                f.write(str(a)+'\t')
            f.write('\n')
            for a in var.To[3]:
                f.write(str(a)+'\t')
            f.write('\n')

            """salva Davg"""
            for a in var.Davg[0]:
                f.write(str(a)+'\t')
            f.write('\n')
            for a in var.Davg[1]:
                f.write(str(a)+'\t')
            f.write('\n')
            for a in var.Davg[2]:
                f.write(str(a)+'\t')
            f.write('\n')
            for a in var.Davg[3]:
                f.write(str(a)+'\t')
            f.write('\n')

            """salva Tavg"""
            for a in var.Tavg[0]:
                f.write(str(a)+'\t')
            f.write('\n')
            for a in var.Tavg[1]:
                f.write(str(a)+'\t')
            f.write('\n')
            for a in var.Tavg[2]:
                f.write(str(a)+'\t')
            f.write('\n')
            for a in var.Tavg[3]:
                f.write(str(a)+'\t')
            f.write('\n')

            """Salva estado dos plots e seus respectivos índices"""
            f.write(str(var.ria.ui.checkPlot1.isChecked())+'\t'+
                    str(var.ria.ui.checkPlot2.isChecked())+'\t'+
                    str(var.ria.ui.checkPlot3.isChecked())+'\t'+
                    str(var.ria.ui.checkPlot4.isChecked())+'\t'+
                    str(var.ria.ui.checkPlot5.isChecked())+'\t'+
                    str(var.ria.ui.checkPlot6.isChecked())+'\t'+
                    str(var.ria.ui.checkPlot7.isChecked())+'\t'+
                    str(var.ria.ui.checkPlot8.isChecked())+'\n')
            f.write(str(var.ria.ui.PlotBox1.currentIndex())+'\t'+
                    str(var.ria.ui.PlotBox2.currentIndex())+'\t'+
                    str(var.ria.ui.PlotBox3.currentIndex())+'\t'+
                    str(var.ria.ui.PlotBox4.currentIndex())+'\t'+
                    str(var.ria.ui.PlotBox5.currentIndex())+'\t'+
                    str(var.ria.ui.PlotBox6.currentIndex())+'\t'+
                    str(var.ria.ui.PlotBox7.currentIndex())+'\t'+
                    str(var.ria.ui.PlotBox8.currentIndex())+'\n')

            """Salva indice da porta de comunicação"""
            f.write(str(var.ria.ui.PortBox.currentIndex())+'\n')
    

            print("Parâmetros salvos")

    #carrega parâmetros salvos em disco
    def load_param(self):
        
        with open('parameters.dat', 'r') as f:
            lines = f.readlines()
            
            var.t_aq = float(lines[0]) #ANTES ERA INT
            var.t_cmp = int(lines[2])
#            plot.set_dataList()
            
            """Carrega status do Rack 1"""
            if lines[3] == 'True\n':
                var.rack1 = True
            else:
                var.rack1 = False
            print("dddd")
            """Carrega status do Rack 2"""
            if lines[4] == 'True\n':
                var.rack2 = True
            else:
                var.rack2 = False

            """Carrega status do Rack 3"""
            if lines[5] == 'True\n':
                var.rack3 = True
            else:
                var.rack3 = False

            """Carrega status do Rack 4"""
            if lines[6] == 'True\n':
                var.rack4 = True
            else:
                var.rack4 = False

            """Carrega Do"""
            a = lines[7].split('\t')[:-1]
            for i in range(8):
                var.Do[0][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Do[0][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_2.setItem(0,(i), self.item)
            a = lines[8].split('\t')[:-1]
            for i in range(8):
                var.Do[1][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Do[1][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_2.setItem(0,(i+8), self.item)
            a = lines[9].split('\t')[:-1]
            for i in range(8):
                var.Do[2][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Do[2][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_2.setItem(0,(i+16), self.item)
            a = lines[10].split('\t')[:-1]
            for i in range(6):
                var.Do[3][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Do[3][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_2.setItem(0,(i+24), self.item)
                
            """Carrega To"""
            a = lines[11].split('\t')[:-1]
            for i in range(8):
                var.To[0][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.To[0][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_2.setItem(1,(i), self.item)
            a = lines[12].split('\t')[:-1]
            for i in range(8):
                var.To[1][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.To[1][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_2.setItem(1,(i+8), self.item)
            a = lines[13].split('\t')[:-1]
            for i in range(8):
                var.To[2][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.To[2][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_2.setItem(1,(i+16), self.item)
            a = lines[14].split('\t')[:-1]
            for i in range(6):
                var.To[3][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.To[0][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_2.setItem(1,(i+24), self.item)
                
            """Carrega Davg"""
            a = lines[15].split('\t')[:-1]
            for i in range(8):
                var.Davg[0][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Davg[0][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_3.setItem(0,(i), self.item)
            a = lines[16].split('\t')[:-1]
            for i in range(8):
                var.Davg[1][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Davg[1][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_3.setItem(0,(i+8), self.item)
            a = lines[17].split('\t')[:-1]
            for i in range(8):
                var.Davg[2][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Davg[2][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_3.setItem(0,(i+16), self.item)
            a = lines[18].split('\t')[:-1]
            for i in range(6):
                var.Davg[3][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Davg[3][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_3.setItem(0,(i+24), self.item)

            """Carrega Tavg"""
            a = lines[19].split('\t')[:-1]
            for i in range(8):
                var.Tavg[0][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Tavg[0][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_3.setItem(1,(i), self.item)
            a = lines[20].split('\t')[:-1]
            for i in range(8):
                var.Tavg[1][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Tavg[1][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_3.setItem(1,(i+8), self.item)
            a = lines[21].split('\t')[:-1]
            for i in range(8):
                var.Tavg[2][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Tavg[2][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_3.setItem(1,(i+16), self.item)
            a = lines[22].split('\t')[:-1]
            for i in range(8):
                var.Tavg[3][i] = a[i]
                self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Tavg[3][i]))
                self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                var.ria.ui.tableWidget_3.setItem(1,(i+24), self.item)

            """Carrega estado dos plots"""
            a = lines[23].split('\t')
            if a[0] == 'True':
                var.ria.ui.checkPlot1.setChecked(1)
            elif a[0] == 'False':
                var.ria.ui.checkPlot1.setChecked(0)
            if a[1] == 'True':
                var.ria.ui.checkPlot2.setChecked(1)
            elif a[1] == 'False':
                var.ria.ui.checkPlot2.setChecked(0)
            if a[2] == 'True':
                var.ria.ui.checkPlot3.setChecked(1)
            elif a[2] == 'False':
                var.ria.ui.checkPlot3.setChecked(0)
            if a[3] == 'True':
                var.ria.ui.checkPlot4.setChecked(1)
            elif a[3] == 'False':
                var.ria.ui.checkPlot4.setChecked(0)
            if a[4] == 'True':
                var.ria.ui.checkPlot5.setChecked(1)
            elif a[4] == 'False':
                var.ria.ui.checkPlot5.setChecked(0)
            if a[5] == 'True':
                var.ria.ui.checkPlot6.setChecked(1)
            elif a[5] == 'False':
                var.ria.ui.checkPlot6.setChecked(0)
            if a[6] == 'True':
                var.ria.ui.checkPlot7.setChecked(1)
            elif a[6] == 'False':
                var.ria.ui.checkPlot7.setChecked(0)
            if a[7] == 'True':
                var.ria.ui.checkPlot8.setChecked(1)
            elif a[7] == 'False':
                var.ria.ui.checkPlot8.setChecked(0)

            """Carrega indice relacionando o sensor dos plots"""
            a = lines[24].split('\t')
            var.ria.ui.PlotBox1.setCurrentIndex(int(a[0]))
            var.ria.ui.PlotBox2.setCurrentIndex(int(a[1]))
            var.ria.ui.PlotBox3.setCurrentIndex(int(a[2]))
            var.ria.ui.PlotBox4.setCurrentIndex(int(a[3]))
            var.ria.ui.PlotBox5.setCurrentIndex(int(a[4]))
            var.ria.ui.PlotBox6.setCurrentIndex(int(a[5]))
            var.ria.ui.PlotBox7.setCurrentIndex(int(a[6]))
            var.ria.ui.PlotBox8.setCurrentIndex(int(a[7]))

            """Carrega indice de porta de comunicação serial"""
            var.ria.ui.PortBox.setCurrentIndex(int(lines[25]))
            
            #NOVO{
            """Carrega estado dos plots da aba 'Online'"""
            var.ria.ui.checkPlot1_on.setChecked(0)
            var.ria.ui.checkPlot2_on.setChecked(0)
            var.ria.ui.checkPlot3_on.setChecked(0)
            var.ria.ui.checkPlot4_on.setChecked(0)
            var.ria.ui.checkPlot5_on.setChecked(0)
            var.ria.ui.checkPlot6_on.setChecked(0)
            var.ria.ui.checkPlot7_on.setChecked(0)
            var.ria.ui.checkPlot8_on.setChecked(0)
            var.ria.ui.checkPlot9_on.setChecked(0)
            var.ria.ui.checkPlot10_on.setChecked(0)
            var.ria.ui.checkPlot11_on.setChecked(0)
            var.ria.ui.checkPlot12_on.setChecked(0)
            var.ria.ui.checkPlot13_on.setChecked(0)
            var.ria.ui.checkPlot14_on.setChecked(0)
            var.ria.ui.checkPlot15_on.setChecked(0)
            var.ria.ui.checkPlot16_on.setChecked(0)
            #}
        print("Parâmetros carregados")

    #define valor atual das medidas de nivel e temperatura como referência
    def set_ref(self):
        try:
            """referencia nível"""
            try:
                var.Do[0] = var.D1[-1][1:]
                for j in range(8):
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Do[0][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_2.setItem(0,(j), self.item)
            except IndexError:
                pass
            except TypeError:
                pass
            try:
                var.Do[1] = var.D2[-1][1:]
                for j in range(8):
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Do[1][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_2.setItem(0,(j+8), self.item)
            except IndexError:
                pass
            except TypeError:
                pass
            try:
                var.Do[2] = var.D3[-1][1:]
                for j in range(8):
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Do[2][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_2.setItem(0,(j+16), self.item)
            except IndexError:
                pass
            except TypeError:
                pass
            try:
                var.Do[3] = var.D4[-1][1:]
                for j in range(6):
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Do[3][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget.setItem(0,(j+24), self.item)
            except IndexError:
                pass
            except TypeError:
                pass
            
            
            """referencia temperatura"""
            try:
                var.To[0] = var.T1[-1][1:]
                for j in range(8):
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.To[0][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_2.setItem(1,(j), self.item)
            except IndexError:
                pass
            except TypeError:
                pass
            try:
                var.To[1] = var.T2[-1][1:]
                for j in range(8):
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.To[1][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_2.setItem(1,(j+8), self.item)
            except IndexError:
                pass
            except TypeError:
                pass
            try:
                var.To[2] = var.T3[-1][1:]
                for j in range(8):
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.To[2][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_2.setItem(1,(j+16), self.item)
            except IndexError:
                pass
            except TypeError:
                pass
            try:
                var.Do[3] = var.T4[-1][1:]
                for j in range(6):
                    self.item = QtGui.QTableWidgetItem(str('%.3f' %var.Do[3][j]))
                    self.item.setFlags(QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
                    var.ria.ui.tableWidget_2.setItem(1,(j+24), self.item)
            except IndexError:
                pass
            except TypeError:
                pass            
            print("Reference set")
        except IndexError:
            pass
        except TypeError:
            pass
        except:
            print("Erro ao tomar referência, tente novamente.")
            raise

    #inicializa racks selecionados
    def rack_address(self):
        self.address = []
        if var.rack1:
            self.address.append(1)
        if var.rack2:
            self.address.append(2)
        if var.rack3:
            self.address.append(3)
        if var.rack4:
            self.address.append(4)
        return self.address

    def res(self):
        self.rack_address()
        self.rack_init(self.rack_address)
        print("Racks reiniciados")

    #Plota gráficos
    def plot(self, i):
        #Plots 0 e 1
        self.index = divmod(var.ria.ui.PlotBox1.currentIndex(), 8)
        if var.ria.ui.checkPlot1.isChecked() and i ==(self.index[0]+1):
            """Plota nivel"""
            var.ria.ui.widget.Data[0].x = np.append(
                        var.ria.ui.widget.Data[0].x,
                        var.ria.D[0])
            var.ria.ui.widget.Data[0].y = np.append(
                        var.ria.ui.widget.Data[0].y,
                        var.ria.D[self.index[1]+1])
            """Plota temperatura"""
            var.ria.ui.widget.Data[1].x = np.append(
                        var.ria.ui.widget.Data[1].x,
                        var.ria.T[0])
            var.ria.ui.widget.Data[1].y = np.append(
                        var.ria.ui.widget.Data[1].y,
                        var.ria.T[self.index[1]+1])
            """muda escala do eixo x"""
            var.ria.ui.widget.setAxisScale(var.ria.ui.widget.xBottom,
                                           var.ria.ui.widget.Data[0].x[0],
                                           var.ria.ui.widget.Data[0].x[-1])
            """se o comprimento do vetor de dados for maior que limite,
            retira o valor mais antigo"""
            try:
                if len(var.ria.ui.widget.Data[0].x) > var.cmp:
                    var.ria.ui.widget.Data[0].x = var.ria.ui.widget.Data[0].x[1:]
                    var.ria.ui.widget.Data[0].y = var.ria.ui.widget.Data[0].y[1:]
                    var.ria.ui.widget.Data[1].x = var.ria.ui.widget.Data[1].x[1:]
                    var.ria.ui.widget.Data[1].y = var.ria.ui.widget.Data[1].y[1:]
            except TypeError:
                pass
        #Plots 2 e 3
        self.index = divmod(var.ria.ui.PlotBox2.currentIndex(), 8)
        if var.ria.ui.checkPlot2.isChecked() and i ==(self.index[0]+1):
            """Plota nivel"""
            var.ria.ui.widget.Data[2].x = np.append(
                        var.ria.ui.widget.Data[2].x,
                        var.ria.D[0])
            var.ria.ui.widget.Data[2].y = np.append(
                        var.ria.ui.widget.Data[2].y,
                        var.ria.D[self.index[1]+1])
            """Plota temperatura"""
            var.ria.ui.widget.Data[3].x = np.append(
                        var.ria.ui.widget.Data[3].x,
                        var.ria.T[0])
            var.ria.ui.widget.Data[3].y = np.append(
                        var.ria.ui.widget.Data[3].y,
                        var.ria.T[self.index[1]+1])
            """muda escala do eixo x"""
            var.ria.ui.widget.setAxisScale(var.ria.ui.widget.xBottom,
                                           var.ria.ui.widget.Data[2].x[0],
                                           var.ria.ui.widget.Data[2].x[-1])
            """se o comprimento do vetor de dados for maior que limite,
            retira o valor mais antigo"""
            try:
                if len(var.ria.ui.widget.Data[2].x) > var.cmp:
                    var.ria.ui.widget.Data[2].x = var.ria.ui.widget.Data[2].x[1:]
                    var.ria.ui.widget.Data[2].y = var.ria.ui.widget.Data[2].y[1:]
                    var.ria.ui.widget.Data[3].x = var.ria.ui.widget.Data[3].x[1:]
                    var.ria.ui.widget.Data[3].y = var.ria.ui.widget.Data[3].y[1:]
            except TypeError:
                pass
        #Plots 4 e 5
        self.index = divmod(var.ria.ui.PlotBox3.currentIndex(), 8)
        if var.ria.ui.checkPlot3.isChecked() and i ==(self.index[0]+1):
            """Plota nivel"""
            var.ria.ui.widget.Data[4].x = np.append(
                        var.ria.ui.widget.Data[4].x,
                        var.ria.D[0])
            var.ria.ui.widget.Data[4].y = np.append(
                        var.ria.ui.widget.Data[4].y,
                        var.ria.D[self.index[1]+1])
            """Plota temperatura"""
            var.ria.ui.widget.Data[5].x = np.append(
                        var.ria.ui.widget.Data[5].x,
                        var.ria.T[0])
            var.ria.ui.widget.Data[5].y = np.append(
                        var.ria.ui.widget.Data[5].y,
                        var.ria.T[self.index[1]+1])
            """muda escala do eixo x"""
            var.ria.ui.widget.setAxisScale(var.ria.ui.widget.xBottom,
                                           var.ria.ui.widget.Data[4].x[0],
                                           var.ria.ui.widget.Data[4].x[-1])
            """se o comprimento do vetor de dados for maior que limite,
            retira o valor mais antigo"""
            try:
                if len(var.ria.ui.widget.Data[4].x) > var.cmp:
                    var.ria.ui.widget.Data[4].x = var.ria.ui.widget.Data[4].x[1:]
                    var.ria.ui.widget.Data[4].y = var.ria.ui.widget.Data[4].y[1:] 
                    var.ria.ui.widget.Data[5].x = var.ria.ui.widget.Data[5].x[1:]
                    var.ria.ui.widget.Data[5].y = var.ria.ui.widget.Data[5].y[1:]
            except TypeError:
                pass
        #Plots 6 e 7
        self.index = divmod(var.ria.ui.PlotBox4.currentIndex(), 8)
        if var.ria.ui.checkPlot4.isChecked() and i ==(self.index[0]+1):
            """Plota nivel"""
            var.ria.ui.widget.Data[6].x = np.append(
                        var.ria.ui.widget.Data[6].x,
                        var.ria.D[0])
            var.ria.ui.widget.Data[6].y = np.append(
                        var.ria.ui.widget.Data[6].y,
                        var.ria.D[self.index[1]+1])
            """Plota temperatura"""
            var.ria.ui.widget.Data[7].x = np.append(
                        var.ria.ui.widget.Data[7].x,
                        var.ria.T[0])
            var.ria.ui.widget.Data[7].y = np.append(
                        var.ria.ui.widget.Data[7].y,
                        var.ria.T[self.index[1]+1])
            """muda escala do eixo x"""
            var.ria.ui.widget.setAxisScale(var.ria.ui.widget.xBottom,
                                           var.ria.ui.widget.Data[6].x[0],
                                           var.ria.ui.widget.Data[6].x[-1])
            """se o comprimento do vetor de dados for maior que limite,
            retira o valor mais antigo"""
            try:
                if len(var.ria.ui.widget.Data[6].x) > var.cmp:
                    var.ria.ui.widget.Data[6].x = var.ria.ui.widget.Data[6].x[1:]
                    var.ria.ui.widget.Data[6].y = var.ria.ui.widget.Data[6].y[1:]
                    var.ria.ui.widget.Data[7].x = var.ria.ui.widget.Data[7].x[1:]
                    var.ria.ui.widget.Data[7].y = var.ria.ui.widget.Data[7].y[1:]
            except TypeError:
                pass
        #Plots 8 e 9
        self.index = divmod(var.ria.ui.PlotBox5.currentIndex(), 8)
        if var.ria.ui.checkPlot5.isChecked() and i ==(self.index[0]+1):
            """Plota nivel"""
            var.ria.ui.widget.Data[8].x = np.append(
                        var.ria.ui.widget.Data[8].x,
                        var.ria.D[0])
            var.ria.ui.widget.Data[8].y = np.append(
                        var.ria.ui.widget.Data[8].y,
                        var.ria.D[self.index[1]+1])
            """Plota temperatura"""
            var.ria.ui.widget.Data[9].x = np.append(
                        var.ria.ui.widget.Data[9].x,
                        var.ria.T[0])
            var.ria.ui.widget.Data[9].y = np.append(
                        var.ria.ui.widget.Data[9].y,
                        var.ria.T[self.index[1]+1])
            """muda escala do eixo x"""
            var.ria.ui.widget.setAxisScale(var.ria.ui.widget.xBottom,
                                           var.ria.ui.widget.Data[8].x[0],
                                           var.ria.ui.widget.Data[8].x[-1])
            """se o comprimento do vetor de dados for maior que limite,
            retira o valor mais antigo"""
            try:
                if len(var.ria.ui.widget.Data[8].x) > var.cmp:
                    var.ria.ui.widget.Data[8].x = var.ria.ui.widget.Data[8].x[1:]
                    var.ria.ui.widget.Data[8].y = var.ria.ui.widget.Data[8].y[1:]
                    var.ria.ui.widget.Data[9].x = var.ria.ui.widget.Data[9].x[1:]
                    var.ria.ui.widget.Data[9].y = var.ria.ui.widget.Data[9].y[1:]
            except TypeError:
                pass
        #Plots 10 e 11
        self.index = divmod(var.ria.ui.PlotBox6.currentIndex(), 8)
        if var.ria.ui.checkPlot6.isChecked() and i ==(self.index[0]+1):
            """Plota nivel"""
            var.ria.ui.widget.Data[10].x = np.append(
                        var.ria.ui.widget.Data[10].x,
                        var.ria.D[0])
            var.ria.ui.widget.Data[10].y = np.append(
                        var.ria.ui.widget.Data[10].y,
                        var.ria.D[self.index[1]+1])
            """Plota temperatura"""
            var.ria.ui.widget.Data[11].x = np.append(
                        var.ria.ui.widget.Data[11].x,
                        var.ria.T[0])
            var.ria.ui.widget.Data[11].y = np.append(
                        var.ria.ui.widget.Data[11].y,
                        var.ria.T[self.index[1]+1])
            """muda escala do eixo x"""
            var.ria.ui.widget.setAxisScale(var.ria.ui.widget.xBottom,
                                           var.ria.ui.widget.Data[10].x[0],
                                           var.ria.ui.widget.Data[10].x[-1])
            """se o comprimento do vetor de dados for maior que limite,
            retira o valor mais antigo"""
            try:
                if len(var.ria.ui.widget.Data[10].x) > var.cmp:
                    var.ria.ui.widget.Data[10].x = var.ria.ui.widget.Data[10].x[1:]
                    var.ria.ui.widget.Data[10].y = var.ria.ui.widget.Data[10].y[1:]
                    var.ria.ui.widget.Data[11].x = var.ria.ui.widget.Data[11].x[1:]
                    var.ria.ui.widget.Data[11].y = var.ria.ui.widget.Data[11].y[1:]
            except TypeError:
                pass
        #Plots 12 e 13
        self.index = divmod(var.ria.ui.PlotBox7.currentIndex(), 8)
        if var.ria.ui.checkPlot7.isChecked() and i ==(self.index[0]+1):
            """Plota nivel"""
            var.ria.ui.widget.Data[12].x = np.append(
                        var.ria.ui.widget.Data[12].x,
                        var.ria.D[0])
            var.ria.ui.widget.Data[12].y = np.append(
                        var.ria.ui.widget.Data[12].y,
                        var.ria.D[self.index[1]+1])
            """Plota temperatura"""
            var.ria.ui.widget.Data[13].x = np.append(
                        var.ria.ui.widget.Data[13].x,
                        var.ria.T[0])
            var.ria.ui.widget.Data[13].y = np.append(
                        var.ria.ui.widget.Data[13].y,
                        var.ria.T[self.index[1]+1])
            """muda escala do eixo x"""
            var.ria.ui.widget.setAxisScale(var.ria.ui.widget.xBottom,
                                           var.ria.ui.widget.Data[12].x[0],
                                           var.ria.ui.widget.Data[12].x[-1])
            """se o comprimento do vetor de dados for maior que limite,
            retira o valor mais antigo"""
            try:
                if len(var.ria.ui.widget.Data[12].x) > var.cmp:
                    var.ria.ui.widget.Data[12].x = var.ria.ui.widget.Data[12].x[1:]
                    var.ria.ui.widget.Data[12].y = var.ria.ui.widget.Data[12].y[1:]
                    var.ria.ui.widget.Data[13].x = var.ria.ui.widget.Data[13].x[1:]
                    var.ria.ui.widget.Data[13].y = var.ria.ui.widget.Data[13].y[1:]
            except TypeError:
                pass
        #Plots 14 e 15
        self.index = divmod(var.ria.ui.PlotBox8.currentIndex(), 8)
        if var.ria.ui.checkPlot8.isChecked() and i ==(self.index[0]+1):
            """Plota nivel"""
            var.ria.ui.widget.Data[14].x = np.append(
                        var.ria.ui.widget.Data[14].x,
                        var.ria.D[0])
            var.ria.ui.widget.Data[14].y = np.append(
                        var.ria.ui.widget.Data[14].y,
                        var.ria.D[self.index[1]+1])
            """Plota temperatura"""
            var.ria.ui.widget.Data[15].x = np.append(
                        var.ria.ui.widget.Data[15].x,
                        var.ria.T[0])
            var.ria.ui.widget.Data[15].y = np.append(
                        var.ria.ui.widget.Data[15].y,
                        var.ria.T[self.index[1]+1])
            """muda escala do eixo x"""
            var.ria.ui.widget.setAxisScale(var.ria.ui.widget.xBottom,
                                           var.ria.ui.widget.Data[14].x[0],
                                           var.ria.ui.widget.Data[14].x[-1])
            """se o comprimento do vetor de dados for maior que limite,
            retira o valor mais antigo"""
            try:
                if len(var.ria.ui.widget.Data[14].x) > var.cmp:
                    var.ria.ui.widget.Data[14].x = var.ria.ui.widget.Data[14].x[1:]
                    var.ria.ui.widget.Data[14].y = var.ria.ui.widget.Data[14].y[1:]
                    var.ria.ui.widget.Data[15].x = var.ria.ui.widget.Data[15].x[1:]
                    var.ria.ui.widget.Data[15].y = var.ria.ui.widget.Data[15].y[1:]
            except TypeError:
                pass
    
            

##ria = RIA()

#classe cria thread para interface gráfica
class Screen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    def callback(self):
        self._stop()
    def run(self):
        var.lock.acquire()
        var.lock.release()
        app = QtGui.QApplication(sys.argv)
        var.ria = RIA()
        var.ria.ui_init()
        var.ria.show()
        sys.exit(app.exec_())

#classe cria thread para controlar comunicação com racks
class Communication(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    def callback(self):
        self._stop()
    def run(self):
##        var.ria.init_rack(var.ria.rack_address())
##        var.lock.acquire()
        var.ria.enable_racks()
##        var.lock.release()
##        time.sleep(10)
        while var.serialFlag:
            try:
                var.ria.acquire(var.ria.rack_address())
                time.sleep(var.t_aq)
            except:
                raise

class Plot(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()
    def callback(self):
        self._stop()
    def run(self):
        while var.graphFlag:
            pass                    
                
               
if __name__ == "__main__":
    telas = Screen()

#from python_pyqt_NewVersion_v5 import plot
