import time
from qwt.qt.QtCore import Qt, QObject
from qwt.qt.QtGui import (QPen, QFrame)
from qwt import QwtPlot, QwtPlotCurve, QwtScaleDraw, QwtPlotGrid, QwtAbstractScaleDraw, QwtText, QwtLegend
import numpy as np

class SimplePlot(QwtPlot):
    def __init__(self, *args):

        colors = [Qt.red, Qt.darkRed, Qt.green, Qt.darkGreen, Qt.blue,
                  Qt.darkBlue, Qt.cyan, Qt.darkCyan, Qt.magenta,
                  Qt.darkMagenta, Qt.yellow, Qt.darkYellow, Qt.gray,
                  Qt.darkGray, Qt.lightGray, Qt.black]
        QwtPlot.__init__(self, *args)

        self.setCanvasBackground(Qt.white)
        self.alignScales()

        # grid
        self.grid = QwtPlotGrid()
        self.grid.attach(self)
        self.grid.setPen(QPen(Qt.black, 0, Qt.DotLine))

        # set titles
        self.setTitle("Gráfico")
        self.setAxisTitle(QwtPlot.xBottom, 'Tempo [hh:mm:ss] -->')
        self.setAxisTitle(QwtPlot.yLeft, 'Nível [mm] -->')

        """Habilita e denomina eixo Y2"""
        self.enableAxis(QwtPlot.yRight)
        self.setAxisTitle(QwtPlot.yRight, '<-- Temp. [ºC]')

        self.nplots = 16
        self.Plots = np.array([])
        self.Data = np.array([])

        for i in range(self.nplots):
            self.Plots = np.append(self.Plots, QwtPlotCurve())
            self.Plots[i].setPen(QPen(colors[i]))
            self.Plots[i].attach(self)
            """define como valor plotado será escrito no eixo x"""
            self.setAxisScaleDraw(QwtPlot.xBottom, TimeScaleDraw())
            self.Data = np.append(self.Data, dataclass())
            """Os índices pares se referem à plots no eixo Y1,
            e os índices ímpares são ligados ao eixo Y2"""
            if divmod(i, 2)[1] == 1:
                self.Plots[i].setYAxis(QwtPlot.yRight)
            self.Plots[i].setData(self.Data[i].x, self.Data[i].y)

        # legend
        #self.legend = QwtLegend
        #QwtLegend().setFrameStyle(QFrame.Box)
        #self.insertLegend(QwtLegend().setFrameStyle(QFrame.Box), QwtPlot.BottomLegend)
        self.insertLegend(QwtLegend(), QwtPlot.BottomLegend)

        # replot
        self.replot()

        # zoom
        # self.zoomer = QwtPlotZoomer(QwtPlot.xBottom,
        #                                 QwtPlot.yLeft,
        #                                 QwtPicker.DragSelection,
        #                                 QwtPicker.AlwaysOn,
        #                                 self.canvas())
        #
        # self.zoomer.setRubberBandPen(QPen(Qt.green))
        self.startTimer(50)

    def alignScales(self):
        self.canvas().setFrameStyle(QFrame.Box | QFrame.Plain)
        self.canvas().setLineWidth(1)
        for i in range(QwtPlot.axisCnt):
            scaleWidget = self.axisWidget(i)
            if scaleWidget:
                scaleWidget.setMargin(0)
            scaleDraw = self.axisScaleDraw(i)
            if scaleDraw:
                scaleDraw.enableComponent(QwtAbstractScaleDraw.Backbone, False)

    def timerEvent(self, e):
        try:
            for i in range(self.nplots):
                self.Plots[i].setData(self.Data[i].x, self.Data[i].y)
            self.replot()
        except:
            pass


class SimplePlot_on(QwtPlot):
    def __init__(self, *args):
        # colors = [Qt.Qt.red, Qt.Qt.yellow, Qt.Qt.green, Qt.Qt.blue, Qt.Qt.cyan, Qt.Qt.magenta, Qt.Qt.gray, Qt.Qt.white,
        #           Qt.Qt.darkRed, Qt.Qt.darkYellow, Qt.Qt.darkGreen, Qt.Qt.darkBlue, Qt.Qt.darkCyan,
        #           Qt.Qt.darkMagenta, Qt.Qt.lightGray, Qt.Qt.darkGray]
        colors = [Qt.red, Qt.darkRed, Qt.green, Qt.darkGreen, Qt.blue,
                  Qt.darkBlue, Qt.cyan, Qt.darkCyan, Qt.magenta,
                  Qt.darkMagenta, Qt.yellow, Qt.darkYellow, Qt.gray,
                  Qt.darkGray, Qt.lightGray, Qt.black]
        QwtPlot.__init__(self, *args)

        self.setCanvasBackground(Qt.black)
        self.alignScales()

        # grid
        self.grid = QwtPlotGrid()
        self.grid.attach(self)
        self.grid.setPen(QPen(Qt.white, 0, Qt.DotLine))

        # setting axis title. The yLeft axis title can chance to 'Temperature', depending on plot preferences
        self.setAxisTitle(QwtPlot.xBottom, 'Time [hh:mm:ss]')
        self.setAxisTitle(QwtPlot.yLeft, 'Height [mm]')

        self.nplots = 16
        self.Plots = np.array([])
        self.Data = np.array([])

        for i in range(self.nplots):
            self.Plots = np.append(self.Plots,QwtPlotCurve())
            self.Plots[i].setPen(QPen(colors[i]))
            self.Plots[i].attach(self)
            """define como valor plotado será escrito no eixo x"""
            self.setAxisScaleDraw(QwtPlot.xBottom, TimeScaleDraw())
            self.Data = np.append(self.Data,dataclass())
            # define a tupple that will contain plot data, expressed in cartesian coordinates
            self.Plots[i].setData(self.Data[i].x,self.Data[i].y)

        # legend
        # self.legend = QwtLegend()
        # self.legend.setFrameStyle(QFrame.Box)
        self.insertLegend(QwtLegend(), QwtPlot.BottomLegend)

        # replot
        self.replot()

        # zoom
        # self.zoomer = QwtPlotZoomer(QwtPlot.xBottom,
        #                                 QwtPlot.yLeft,
        #                                 QwtPicker.DragSelection,
        #                                 QwtPicker.AlwaysOn,
        #                                 self.canvas())
        #
        # self.zoomer.setRubberBandPen(QPen(Qt.green))
        self.startTimer(50)

    def alignScales(self):
        self.canvas().setFrameStyle(QFrame.Box | QFrame.Plain)
        self.canvas().setLineWidth(1)
        for i in range(QwtPlot.axisCnt):
            scaleWidget = self.axisWidget(i)
            if scaleWidget:
                scaleWidget.setMargin(0)
            scaleDraw = self.axisScaleDraw(i)
            if scaleDraw:
                scaleDraw.enableComponent(QwtAbstractScaleDraw.Backbone, False)

    def timerEvent(self, e):
        try:
            for i in range(self.nplots):
                self.Plots[i].setData(self.Data[i].x, self.Data[i].y)
            self.replot()
        except:
            pass


class dataclass(object):
    def __init__(self):
        self.x = np.array([])
        self.y = np.array([])


class TimeScaleDraw(QwtScaleDraw):
    def __init__(self):
        QwtScaleDraw.__init__(self)

    def label(self, value):
        """value é o valor x do ponto a ser plotado"""
        return QwtText(time.ctime(value)[11:19])
