if False:
    import sip
    sip.settracemask(0x3f)

import random, time
import sys
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *
import numpy as np
from PyQt4 import QtCore, QtGui #p/ ciencAberta

class SimplePlot(Qwt.QwtPlot):
    def __init__(self, *args):

        #'white':3,'black':2,'red':7,'darkRed':13,'green':8,'darkGreen':14,'blue':9,'darkBlue':15,'cyan':10,'darkCyan':16,'magenta':11,'darkMagenta':17,'yellow':12,'darkYellow':18,'gray':5,'darkGray':4,'lightGray':6
        colors = [Qt.Qt.red,Qt.Qt.darkRed,Qt.Qt.green,Qt.Qt.darkGreen,Qt.Qt.blue,
                  Qt.Qt.darkBlue,Qt.Qt.cyan,Qt.Qt.darkCyan,Qt.Qt.magenta,
                  Qt.Qt.darkMagenta,Qt.Qt.yellow,Qt.Qt.darkYellow,Qt.Qt.gray,
                  Qt.Qt.darkGray,Qt.Qt.lightGray,Qt.Qt.black]
        Qwt.QwtPlot.__init__(self, *args)

        self.setCanvasBackground(Qt.Qt.white)
##        self.plotLayout().setAlignCanvasToScales(True)
        self.alignScales()

        #grid
        self.grid = Qwt.QwtPlotGrid()
        self.grid.attach(self)
        self.grid.setPen(Qt.QPen(Qt.Qt.black, 0, Qt.Qt.DotLine))

        
        # set titles
        self.setTitle("Gráfico")        
        self.setAxisTitle(Qwt.QwtPlot.xBottom, 'Tempo [hh:mm:ss] -->')
        self.setAxisTitle(Qwt.QwtPlot.yLeft, 'Nível [mm] -->')

        """Habilita e denomina eixo Y2"""
        self.enableAxis(Qwt.QwtPlot.yRight)
        self.setAxisTitle(Qwt.QwtPlot.yRight, '<-- Temp. [ºC]')

        self.nplots = 16
        self.Plots = np.array([])
        self.Data = np.array([])

        for i in range(self.nplots):
            self.Plots = np.append(self.Plots,Qwt.QwtPlotCurve())
##            self.Plots[i].setPen(Qt.QPen(colors[random.randint(0,15)]))
            self.Plots[i].setPen(Qt.QPen(colors[i]))
            self.Plots[i].attach(self)
            """define como valor plotado será escrito no eixo x"""
            self.setAxisScaleDraw(Qwt.QwtPlot.xBottom, TimeScaleDraw())
            self.Data = np.append(self.Data,dataclass())
            """Os índices pares se referem à plots no eixo Y1,
            e os índices ímpares são ligados ao eixo Y2"""
            if divmod(i,2)[1] == 1:          
                self.Plots[i].setYAxis(Qwt.QwtPlot.yRight)
            self.Plots[i].setData(self.Data[i].x,self.Data[i].y)

        #legend
        self.legend = Qwt.QwtLegend()
        self.legend.setFrameStyle(Qt.QFrame.Box)
        self.insertLegend(self.legend, Qwt.QwtPlot.BottomLegend)
        
        # replot
        self.replot()
        
        # zoom
        self.zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom,
                                        Qwt.QwtPlot.yLeft,
                                        Qwt.QwtPicker.DragSelection,
                                        Qwt.QwtPicker.AlwaysOn,
                                        self.canvas())
        #self.zoomer = Qwt.QwtPlotZoomer(self.canvas())

        self.zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.green))

        self.startTimer(50)

    def alignScales(self):
        self.canvas().setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Plain)
        self.canvas().setLineWidth(1)
        for i in range(Qwt.QwtPlot.axisCnt):
            scaleWidget = self.axisWidget(i)
            if scaleWidget:
                scaleWidget.setMargin(0)
            scaleDraw = self.axisScaleDraw(i)
            if scaleDraw:
                scaleDraw.enableComponent(Qwt.QwtAbstractScaleDraw.Backbone, False)
                
    def timerEvent(self,e):
        try:
            for i in range(self.nplots):
                self.Plots[i].setData(self.Data[i].x,self.Data[i].y)
##                self.setAxisScale(var.ria.ui.widget.xBottom,
##                                               var.ria.ui.widget.Data[i].x[0],
##                                               var.ria.ui.widget.Data[i].x[-1])

            self.replot()
        except:
            pass


###NOVO###
class SimplePlot_on(Qwt.QwtPlot):
    def __init__(self, *args):

        #'white':3,'black':2,'red':7,'darkRed':13,'green':8,'darkGreen':14,'blue':9,'darkBlue':15,'cyan':10,'darkCyan':16,'magenta':11,'darkMagenta':17,'yellow':12,'darkYellow':18,'gray':5,'darkGray':4,'lightGray':6
        """colors = [Qt.Qt.red,Qt.Qt.darkRed,Qt.Qt.green,Qt.Qt.darkGreen,Qt.Qt.blue,
                  Qt.Qt.darkBlue,Qt.Qt.cyan,Qt.Qt.darkCyan,Qt.Qt.magenta,
                  Qt.Qt.darkMagenta,Qt.Qt.yellow,Qt.Qt.darkYellow,Qt.Qt.gray,
                  Qt.Qt.darkGray,Qt.Qt.lightGray,Qt.Qt.black]"""
        colors = [Qt.Qt.red, Qt.Qt.yellow, Qt.Qt.green, Qt.Qt.blue,Qt.Qt.cyan,Qt.Qt.magenta,Qt.Qt.gray, Qt.Qt.white,
                  Qt.Qt.darkRed,Qt.Qt.darkYellow,Qt.Qt.darkGreen,Qt.Qt.darkBlue,Qt.Qt.darkCyan,
                  Qt.Qt.darkMagenta,Qt.Qt.lightGray, Qt.Qt.darkGray]
        Qwt.QwtPlot.__init__(self, *args)

        self.setCanvasBackground(Qt.Qt.black)
##        self.plotLayout().setAlignCanvasToScales(True)
        self.alignScales()

        #grid
        self.grid = Qwt.QwtPlotGrid()
        self.grid.attach(self)
        self.grid.setPen(Qt.QPen(Qt.Qt.white, 0, Qt.Qt.DotLine))

        
        # set titles
        #self.setTitle("HLS")        
        self.setAxisTitle(Qwt.QwtPlot.xBottom, 'Time [hh:mm:ss]')
        self.setAxisTitle(Qwt.QwtPlot.yLeft, 'Height [mm]')

        """Habilita e denomina eixo Y2"""
        #self.enableAxis(Qwt.QwtPlot.yRight)
        #self.setAxisTitle(Qwt.QwtPlot.yRight, 'Temperature [ºC]')

        self.nplots = 16 #por enquanto. ideia: nplots = 16 (16 D ou 16 T)
        self.Plots = np.array([])
        self.Data = np.array([])

        for i in range(self.nplots):
            self.Plots = np.append(self.Plots,Qwt.QwtPlotCurve())
##            self.Plots[i].setPen(Qt.QPen(colors[random.randint(0,15)]))
            self.Plots[i].setPen(Qt.QPen(colors[i]))
            self.Plots[i].attach(self)
            """define como valor plotado será escrito no eixo x"""
            self.setAxisScaleDraw(Qwt.QwtPlot.xBottom, TimeScaleDraw())
            self.Data = np.append(self.Data,dataclass())
            """Os índices pares se referem à plots no eixo Y1,
            e os índices ímpares são ligados ao eixo Y2"""
            #if divmod(i,2)[1] == 1:          
                #self.Plots[i].setYAxis(Qwt.QwtPlot.yRight)
            self.Plots[i].setData(self.Data[i].x,self.Data[i].y)

        #legend
        self.legend = Qwt.QwtLegend()
        self.legend.setFrameStyle(Qt.QFrame.Box)
        self.insertLegend(self.legend, Qwt.QwtPlot.BottomLegend)
        
        # replot
        self.replot()
        
        # zoom
        self.zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom,
                                        Qwt.QwtPlot.yLeft,
                                        Qwt.QwtPicker.DragSelection,
                                        Qwt.QwtPicker.AlwaysOn,
                                        self.canvas())
        #self.zoomer = Qwt.QwtPlotZoomer(self.canvas())
        
        self.zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.green))

        self.startTimer(50)
        

##    def clearZoomStack(self,i):
##        """Auto scale and clear the zoom stack
##        """
##
##        self.Plots[i].setAxisAutoScale(Qwt.QwtPlot.xBottom)
##        self.Plots[i].setAxisAutoScale(Qwt.QwtPlot.yLeft)
##        self.Plots[i].replot()
##        self.zoomer.setZoomBase()        
##
##        self.startTimer(50)
        
    def alignScales(self):
        self.canvas().setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Plain)
        self.canvas().setLineWidth(1)
        for i in range(Qwt.QwtPlot.axisCnt):
            scaleWidget = self.axisWidget(i)
            if scaleWidget:
                scaleWidget.setMargin(0)
            scaleDraw = self.axisScaleDraw(i)
            if scaleDraw:
                scaleDraw.enableComponent(Qwt.QwtAbstractScaleDraw.Backbone, False)
                
    def timerEvent(self,e):
        try:
            for i in range(self.nplots):
                self.Plots[i].setData(self.Data[i].x,self.Data[i].y)
##                self.setAxisScale(var.ria.ui.widget.xBottom,
##                                               var.ria.ui.widget.Data[i].x[0],
##                                               var.ria.ui.widget.Data[i].x[-1])

            self.replot()
        except:
            pass
        
"""CIENCIA ABERTA, EXCLUIR DEPOIS"""

class SimplePlot_cienc(Qwt.QwtPlot):
    def __init__(self, *args):
        #'white':3,'black':2,'red':7,'darkRed':13,'green':8,'darkGreen':14,'blue':9,'darkBlue':15,'cyan':10,'darkCyan':16,'magenta':11,'darkMagenta':17,'yellow':12,'darkYellow':18,'gray':5,'darkGray':4,'lightGray':6
        """colors = [Qt.Qt.red,Qt.Qt.darkRed,Qt.Qt.green,Qt.Qt.darkGreen,Qt.Qt.blue,
                  Qt.Qt.darkBlue,Qt.Qt.cyan,Qt.Qt.darkCyan,Qt.Qt.magenta,
                  Qt.Qt.darkMagenta,Qt.Qt.yellow,Qt.Qt.darkYellow,Qt.Qt.gray,
                  Qt.Qt.darkGray,Qt.Qt.lightGray,Qt.Qt.black]"""
        colors = [Qt.Qt.red, Qt.Qt.yellow, Qt.Qt.green, Qt.Qt.blue,Qt.Qt.cyan,Qt.Qt.magenta,Qt.Qt.gray, Qt.Qt.white,
                  Qt.Qt.darkRed,Qt.Qt.darkYellow,Qt.Qt.darkGreen,Qt.Qt.darkBlue,Qt.Qt.darkCyan,
                  Qt.Qt.darkMagenta,Qt.Qt.lightGray, Qt.Qt.darkGray]
        Qwt.QwtPlot.__init__(self, *args)
        self.setCanvasBackground(Qt.Qt.black)
##        self.plotLayout().setAlignCanvasToScales(True)
        self.alignScales()

        #grid
        self.grid = Qwt.QwtPlotGrid()
        self.grid.attach(self)
        self.grid.setPen(Qt.QPen(Qt.Qt.white, 0, Qt.Qt.DotLine))

        # set titles
        #self.setTitle("HLS")        
        self.setAxisTitle(Qwt.QwtPlot.xBottom, 'Tempo [hh:mm:ss]')
        self.setAxisTitle(Qwt.QwtPlot.yLeft, 'Altura [mm]')
        self.font = QtGui.QFont("Courier", 7)
        self.setAxisFont(1, self.font)
        self.setAxisFont(2, self.font)
        """Habilita e denomina eixo Y2"""
        #self.enableAxis(Qwt.QwtPlot.yRight)
        #self.setAxisTitle(Qwt.QwtPlot.yRight, 'Temperature [ºC]')

        self.nplots = 16 #por enquanto. ideia: nplots = 16 (16 D ou 16 T)
        self.Plots = np.array([])
        self.Data = np.array([])
        for i in range(self.nplots):
            self.Plots = np.append(self.Plots,Qwt.QwtPlotCurve())
##            self.Plots[i].setPen(Qt.QPen(colors[random.randint(0,15)]))
            self.Plots[i].setPen(Qt.QPen(colors[i]))
            self.Plots[i].attach(self)
            """define como valor plotado será escrito no eixo x"""
            self.setAxisScaleDraw(Qwt.QwtPlot.xBottom, TimeScaleDraw())
            self.Data = np.append(self.Data,dataclass())
            """Os índices pares se referem à plots no eixo Y1,
            e os índices ímpares são ligados ao eixo Y2"""
            #if divmod(i,2)[1] == 1:          
                #self.Plots[i].setYAxis(Qwt.QwtPlot.yRight)
            self.Plots[i].setData(self.Data[i].x,self.Data[i].y)

        #legend
        #self.legend = Qwt.QwtLegend()
        #self.legend.setFrameStyle(Qt.QFrame.Box)
        #self.insertLegend(self.legend, Qwt.QwtPlot.BottomLegend)
        
        # replot
        self.replot()
        # zoom
        #self.zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom,
        #                                Qwt.QwtPlot.yLeft,
        #                                Qwt.QwtPicker.DragSelection,
        #                                Qwt.QwtPicker.AlwaysOn,
        #                                self.canvas())
        #self.zoomer = Qwt.QwtPlotZoomer(self.canvas())
        
        #self.zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.green))

        self.startTimer(50)

##    def clearZoomStack(self,i):
##        """Auto scale and clear the zoom stack
##        """
##
##        self.Plots[i].setAxisAutoScale(Qwt.QwtPlot.xBottom)
##        self.Plots[i].setAxisAutoScale(Qwt.QwtPlot.yLeft)
##        self.Plots[i].replot()
##        self.zoomer.setZoomBase()        
##
##        self.startTimer(50)
        
    def alignScales(self):
        self.canvas().setFrameStyle(Qt.QFrame.Box | Qt.QFrame.Plain)
        self.canvas().setLineWidth(1)
        for i in range(Qwt.QwtPlot.axisCnt):
            scaleWidget = self.axisWidget(i)
            if scaleWidget:
                scaleWidget.setMargin(0)
            scaleDraw = self.axisScaleDraw(i)
            if scaleDraw:
                scaleDraw.enableComponent(Qwt.QwtAbstractScaleDraw.Backbone, False)
                
    def timerEvent(self,e):
        try:
            for i in range(self.nplots):
                self.Plots[i].setData(self.Data[i].x,self.Data[i].y)
##                self.setAxisScale(var.ria.ui.widget.xBottom,
##                                               var.ria.ui.widget.Data[i].x[0],
##                                               var.ria.ui.widget.Data[i].x[-1])

            self.replot()
        except:
            pass
""" FIM CIENCIA ABERTA"""


class dataclass(object):
    def __init__(self):
        self.x = np.array([])
        self.y = np.array([])
        

class TimeScaleDraw(Qwt.QwtScaleDraw):
    def __init__(self):
        Qwt.QwtScaleDraw.__init__(self)
        
    def label(self, value):
        """value é o valor x do ponto a ser plotado"""
        return Qwt.QwtText(time.ctime(value)[11:19])
