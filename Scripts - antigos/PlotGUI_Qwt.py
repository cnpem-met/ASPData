if False:
    import sip
    sip.settracemask(0x3f)

import random
import sys
from PyQt4 import Qt
import PyQt4.Qwt5 as Qwt
from PyQt4.Qwt5.anynumpy import *
import numpy as np

class SimplePlot(Qwt.QwtPlot):
    def __init__(self, *args):
        Qwt.QwtPlot.__init__(self, *args)

        self.setCanvasBackground(Qt.Qt.white)
##        self.plotLayout().setAlignCanvasToScales(True)
        self.alignScales()
        
        # set titles
        self.setTitle("Gráfico")
        self.setAxisTitle(Qwt.QwtPlot.xBottom, 'Número de Coletas -->')
        self.setAxisTitle(Qwt.QwtPlot.yLeft, 'Leituras -->')

        # Plot1
        self.Plot1 = Qwt.QwtPlotCurve()
        self.Plot1.setPen(Qt.QPen(Qt.Qt.red))
        self.Plot1.attach(self)
        
        self.x1 = np.linspace(0,10000,10000)
        self.y1 = np.zeros(10000)
        self.Plot1.setData(self.x1,self.y1)

        # Plot2
        self.Plot2 = Qwt.QwtPlotCurve()
        self.Plot2.setPen(Qt.QPen(Qt.Qt.blue))
        self.Plot2.attach(self)
        
        self.x2 = np.linspace(0,10000,10000)
        self.y2 = np.zeros(10000)
        self.Plot2.setData(self.x2,self.y2)
        
        # replot
        self.replot()
##        
##        # zoom
##        self.zoomer = Qwt.QwtPlotZoomer(Qwt.QwtPlot.xBottom,
##                                        Qwt.QwtPlot.yLeft,
##                                        Qwt.QwtPicker.DragSelection,
##                                        Qwt.QwtPicker.AlwaysOff,
##                                        self.canvas())
##        self.zoomer.setRubberBandPen(Qt.QPen(Qt.Qt.green))

        self.startTimer(100)
        
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
            self.Plot1.setData(self.x1, self.y1)
            self.Plot2.setData(self.x2, self.y2)
            self.replot()
        except:
            pass
