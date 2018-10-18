from pcaspy import SimpleServer, Driver, Alarm, Severity
from datetime import date
import random
import os
import datetime
import json
import httplib2
import time
import shutil
import threading
import epics
import numpy as np

#Define variaveis PV
prefix = 'HLS:'
pvdb = {'POT1_LEVEL' : {'prec' : 4,'scan' : 1,},'POT1_TEMP' : {'prec' : 4,'scan' : 1,},'POT1_POSX' : {'prec' : 4,'scan' : 1,},'POT1_POSY' : {'prec' : 4,'scan' : 1,},
        'POT2_LEVEL' : {'prec' : 4,'scan' : 1,},'POT2_TEMP' : {'prec' : 4,'scan' : 1,},'POT2_POSX' : {'prec' : 4,'scan' : 1,},'POT2_POSY' : {'prec' : 4,'scan' : 1,},
        'POT3_LEVEL' : {'prec' : 4,'scan' : 1,},'POT3_TEMP' : {'prec' : 4,'scan' : 1,},'POT3_POSX' : {'prec' : 4,'scan' : 1,},'POT3_POSY' : {'prec' : 4,'scan' : 1,},
        'POT4_LEVEL' : {'prec' : 4,'scan' : 1,},'POT4_TEMP' : {'prec' : 4,'scan' : 1,},'POT4_POSX' : {'prec' : 4,'scan' : 1,},'POT4_POSY' : {'prec' : 4,'scan' : 1,},
        'POT5_LEVEL' : {'prec' : 4,'scan' : 1,},'POT5_TEMP' : {'prec' : 4,'scan' : 1,},'POT5_POSX' : {'prec' : 4,'scan' : 1,},'POT5_POSY' : {'prec' : 4,'scan' : 1,},
        'POT6_LEVEL' : {'prec' : 4,'scan' : 1,},'POT6_TEMP' : {'prec' : 4,'scan' : 1,},'POT6_POSX' : {'prec' : 4,'scan' : 1,},'POT6_POSY' : {'prec' : 4,'scan' : 1,},
        'POT7_LEVEL' : {'prec' : 4,'scan' : 1,},'POT7_TEMP' : {'prec' : 4,'scan' : 1,},'POT7_POSX' : {'prec' : 4,'scan' : 1,},'POT7_POSY' : {'prec' : 4,'scan' : 1,},
        'POT8_LEVEL' : {'prec' : 4,'scan' : 1,},'POT8_TEMP' : {'prec' : 4,'scan' : 1,},'POT8_POSX' : {'prec' : 4,'scan' : 1,},'POT8_POSY' : {'prec' : 4,'scan' : 1,},
        'POT9_LEVEL' : {'prec' : 4,'scan' : 1,},'POT9_TEMP' : {'prec' : 4,'scan' : 1,},'POT9_POSX' : {'prec' : 4,'scan' : 1,},'POT9_POSY' : {'prec' : 4,'scan' : 1,},
        'POT10_LEVEL' : {'prec' : 4,'scan' : 1,},'POT10_TEMP' : {'prec' : 4,'scan' : 1,},'POT10_POSX' : {'prec' : 4,'scan' : 1,},'POT10_POSY' : {'prec' : 4,'scan' : 1,},
        'POT11_LEVEL' : {'prec' : 4,'scan' : 1,},'POT11_TEMP' : {'prec' : 4,'scan' : 1,},'POT11_POSX' : {'prec' : 4,'scan' : 1,},'POT11_POSY' : {'prec' : 4,'scan' : 1,},
        'POT12_LEVEL' : {'prec' : 4,'scan' : 1,},'POT12_TEMP' : {'prec' : 4,'scan' : 1,},'POT12_POSX' : {'prec' : 4,'scan' : 1,},'POT12_POSY' : {'prec' : 4,'scan' : 1,},
        'POT13_LEVEL' : {'prec' : 4,'scan' : 1,},'POT13_TEMP' : {'prec' : 4,'scan' : 1,},'POT13_POSX' : {'prec' : 4,'scan' : 1,},'POT13_POSY' : {'prec' : 4,'scan' : 1,},
        'POT14_LEVEL' : {'prec' : 4,'scan' : 1,},'POT14_TEMP' : {'prec' : 4,'scan' : 1,},'POT14_POSX' : {'prec' : 4,'scan' : 1,},'POT14_POSY' : {'prec' : 4,'scan' : 1,},
        'POT15_LEVEL' : {'prec' : 4,'scan' : 1,},'POT15_TEMP' : {'prec' : 4,'scan' : 1,},'POT15_POSX' : {'prec' : 4,'scan' : 1,},'POT15_POSY' : {'prec' : 4,'scan' : 1,},
        'POT16_LEVEL' : {'prec' : 4,'scan' : 1,},'POT16_TEMP' : {'prec' : 4,'scan' : 1,},'POT16_POSX' : {'prec' : 4,'scan' : 1,},'POT16_POSY' : {'prec' : 4,'scan' : 1,},
        'POT17_LEVEL' : {'prec' : 4,'scan' : 1,},'POT17_TEMP' : {'prec' : 4,'scan' : 1,},'POT17_POSX' : {'prec' : 4,'scan' : 1,},'POT17_POSY' : {'prec' : 4,'scan' : 1,},
        'POT18_LEVEL' : {'prec' : 4,'scan' : 1,},'POT18_TEMP' : {'prec' : 4,'scan' : 1,},'POT18_POSX' : {'prec' : 4,'scan' : 1,},'POT18_POSY' : {'prec' : 4,'scan' : 1,},
        'POT19_LEVEL' : {'prec' : 4,'scan' : 1,},'POT19_TEMP' : {'prec' : 4,'scan' : 1,},'POT19_POSX' : {'prec' : 4,'scan' : 1,},'POT19_POSY' : {'prec' : 4,'scan' : 1,},
        'POT20_LEVEL' : {'prec' : 4,'scan' : 1,},'POT20_TEMP' : {'prec' : 4,'scan' : 1,},'POT20_POSX' : {'prec' : 4,'scan' : 1,},'POT20_POSY' : {'prec' : 4,'scan' : 1,},
}


def get_file(ID, numSens):
    #le variaveis lidas do console VantagePro2
    #concatena nome e diretorio do arquivo de leitura
    #dst_dir="C:/users/rooli/desktop/ESTÁGIO/HLS/EPICs/Códigos"
    arq_DT="RACK"+str(ID)+"_EPICS.txt"
    arquivo = open(arq_DT, "r")
    string=arquivo.read()
    
    nivel = np.array([])
    temp = np.array([])
    for i in range(numSens[0],numSens[1]+1):
        #Le valor de nivel
        pos1=string.index("HLS_sensor"+str(i)+" - Nivel",0)
        pos1=string.index(":",pos1)
        pos1=pos1+2

        pos2=string.index("m",pos1)
        nivel = np.append(nivel, float(string[(pos1):(pos2-1)]))

        #Le valor de temperatura
        pos1=string.index("HLS_sensor"+str(i)+" - Temp",0)
        pos1=string.index(":",pos1)
        pos1=pos1+2

        pos2=string.index("C",pos1)
        temp = np.append(temp, float(string[(pos1):(pos2-1)]))

    arquivo.close()
    arq_XY="HLS_Posicoes_sensores.txt"
    arquivo = open(arq_XY, "r")
    string=arquivo.read()
    
    X = np.array([])
    Y = np.array([])
    for i in range(numSens[0],numSens[1]+1):
        #Le valor de nivel
        pos1=string.index("HLS_sensor"+str(i)+" - X",0)
        pos1=string.index(":",pos1)
        pos1=pos1+2

        pos2=string.index("m",pos1)
        X = np.append(X, float(string[(pos1):(pos2-1)]))

        #Le valor de temperatura
        pos1=string.index("HLS_sensor"+str(i)+" - Y",0)
        pos1=string.index(":",pos1)
        pos1=pos1+2

        pos2=string.index("m",pos1)
        Y = np.append(Y, float(string[(pos1):(pos2-1)]))

    resp = np.array([])
    for j in range(len(nivel)):
        resp = np.append(resp, nivel[j])
        resp = np.append(resp, temp[j])
        resp = np.append(resp, X[j])
        resp = np.append(resp, Y[j])
    return resp
    #return [nivel, temp]
    
#Relaciona variaveis PV com funcao criada para leitura dos dados
class myDriver(Driver):
    def __init__(self):
        super(myDriver, self).__init__()
        # criei e iniciei a thread
        self.process = threading.Thread(target = self.processThread)
        self.process.setDaemon(True)
        self.process.start()

    def processThread(self):
        while (True):
            """ O processo de captação de variáveis varre os arquivos txts com os dados dos racks
                do HLS, e são guardados na estrutura 'leitura' intercalados entre nivel e temp.
                Dados configuráveis:
                - range_sensors_txtRack1: intervalo da enumeração dos sensores que estão no arquivo RACK1_EPICS.txt
                - range_sensors_txtRack2: intervalo da enumeração dos sensores que estão no arquivo RACK2_EPICS.txt
                - range_sensors_txtRack3: intervalo da enumeração dos sensores que estão no arquivo RACK3_EPICS.txt
                - numTotal_sensors: número total de sensores sendo lidos"""
            leitura = np.array([])
            range_sensors_txtRack1 = [1,8]
            range_sensors_txtRack2 = [9,15]
            range_sensors_txtRack3 = [16,20]
            numTotal_sensors = 20
            leitura = np.append(leitura, get_file(1, range_sensors_txtRack1))
            leitura = np.append(leitura, get_file(2, range_sensors_txtRack2))
            leitura = np.append(leitura, get_file(3, range_sensors_txtRack3))
            #print(leitura)

            for i in range(int(len(leitura)/4)):
                paramD = "POT"+str(i+1)+"_LEVEL"
                paramT = "POT"+str(i+1)+"_TEMP"
                paramX = "POT"+str(i+1)+"_POSX"
                paramY = "POT"+str(i+1)+"_POSY"
                self.setParam(paramD, leitura[4*i])
                self.setParam(paramT, leitura[4*i+1])
                self.setParam(paramX, leitura[4*i+2])
                self.setParam(paramY, leitura[4*i+3])
            #leitura = get_file(2,5)
            #...
            self.updatePVs()
            time.sleep(0.5)

if __name__ == '__main__':
    #Envia para o archive
    server = SimpleServer()
    server.createPV(prefix, pvdb)
    driver = myDriver()
    #httpclient=httplib.HTTPConnection("10.2.105.191:17665")
    httpclient=httplib2.HTTPConnectionWithTimeout("10.2.105.191:17665")
    req=httpclient.request("GET","/mgmt/bpl/archivePV?pv=HLS:POSICAO1")
    # process CA transactions
    while True:
        server.process(0.1)
        
