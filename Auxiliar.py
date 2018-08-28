import numpy as np
import threading

class Aux(object):
    def __init__(self):

        self.plotSet = "nivel"

        self.plotFlagRIAcom = False
        
        self.plotFlag = False
        self.plotFlag1 = False
        self.plotFlag2 = False
        self.plotFlag3 = False
        self.plotFlag4 = False
        self.plotFlag5 = False
        self.plotFlag6 = False

        #self.plot_off_sel = [False, False, False]
        self.posSens = [-420,-80, 360, 750, 1100, 1450, 1880, 2260]

        
        self.flag_plotAbs_off = False
        self.flag_plotRefSensor_off = False
        self.flag_plotRefMediaG_off = False
        self.flag_plotRefFixa_off = False

        self.flag_freeToPlot_off = False
        
        self.flagCmp = False

        
        self.tam_arq1_ant = 0
        self.tam_arq2_ant = 0
        self.tam_arq3_ant = 0
        self.tam_arq4_ant = 0

        self.rack1_enable = 0
        self.rack2_enable = 0
        self.rack3_enable = 0
        self.rack4_enable = 0

        self.rack1 = 0
        self.rack2 = 0
        self.rack3 = 0
        self.rack4 = 0

        self.scaleMinY = 0
        self.scaleMaxY = 0
        self.scaleMinX = 0
        self.scaleMaxX = 0
        
        self.somaD1 = [0,0,0,0,0,0,0,0,0]
        self.somaT1 = [0,0,0,0,0,0,0,0,0]
        self.somaD2 = [0,0,0,0,0,0,0,0,0]
        self.somaT2 = [0,0,0,0,0,0,0,0,0]
        self.somaD3 = [0,0,0,0,0,0,0,0,0]
        self.somaT3 = [0,0,0,0,0,0,0,0,0]
        self.somaD4 = [0,0,0,0,0,0,0,0,0]
        self.somaT4 = [0,0,0,0,0,0,0,0,0]

        self.refD1 = [0,0,0,0,0,0,0,0]
        self.refT1 = [0,0,0,0,0,0,0,0]
        self.refD2 = [0,0,0,0,0,0,0,0]
        self.refT2 = [0,0,0,0,0,0,0,0]
        self.refD3 = [0,0,0,0,0,0,0,0]
        self.refT3 = [0,0,0,0,0,0,0,0]
        self.refD4 = [0,0,0,0,0,0,0,0]
        self.refT4 = [0,0,0,0,0,0,0,0]

aux = Aux()
