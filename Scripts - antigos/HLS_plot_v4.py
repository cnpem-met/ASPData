#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
import sys
from PyQt4 import QtGui
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
import os
from PyQt4 import QtGui, QtCore
from time import strftime
from multiprocessing import Process
import time
import threading
from pylab import figure, axes, pie, title, show
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import matplotlib.ticker as plticker


#Método de análise: em um determinado horário (00:01) avalia a variação de cada sensor em relação à media do sistema.
#A media do sistema eh definida com as aquisições do primeiro dia
def HLS_plot4(dataIni, dataFim):
	print (dataIni)
	print (dataFim)
	mypath="C:/users/rodrigo.neto/Desktop/HLS-BancadaMETRO/dados-bancada-IMAS/"
	onlyfiles = sorted([f for f in listdir(mypath) if isfile(join(mypath, f))])
	#print onlyfiles
	lines=[]
	dias=[]
	#loop para pegar arquivos entre intervalo desejado e ler todas as linhas
	for i in range(0,len(onlyfiles)):
		filename=onlyfiles[i]
		#print filename
		if ((filename>=dataIni) and (filename<=dataFim)):
			print (filename)
			dias.append(filename)
			myfile=open(os.path.join("C:/users/rodrigo.neto/Desktop/HLS-BancadaMETRO/dados-bancada-IMAS/",filename))
			newlines=myfile.readlines()
			del myfile
			#print len(newlines)
			if (filename==dataIni):
				#no primeiro dia, armazena todas as aquisições
				lines_ini=newlines
				lines+=newlines[4:5]
			else:
				#nos dias restantes pega apenas a primeira aquisicao
				lines+=newlines[4:5]
			print (len(newlines))
			print (len(lines))
	#print len(lines)



	#armazena ID dos sensores
	sensoresID=[]
	string=lines_ini[3]
	pos=string.index('D_H7DC')
	sensoresID.append(string[pos+2:pos+10])
	while(True):
		try:
			pos=string.index('\t' + 'D_H7DC',pos)
			pos=pos+1
			print (string[pos+2:pos+10])
			sensoresID.append(string[pos+2:pos+10])
		except ValueError:
			break
	print (sensoresID)
	print (len(sensoresID))
	sensor_refID=(len(sensoresID))/2
	print (sensor_refID)
	print ((len(sensoresID))/2)


	aux_media_ini=[]
	#####################################################################
	####armazena parametros D, Drms, T e Trms obtidos no primeiro dia####
	#####################################################################
	D_ini=[]
	Drms_ini=[]
	T_ini=[]
	Trms_ini=[]
	for x in range(4,len(lines_ini)):	
		string=lines_ini[x]
		#print string
		pos=string.index('\t')
		pos=pos+1
		pos=string.index('\t',pos)
		pos=pos+1
		pos=string.index('\t',pos)
		pos=pos+2
		#print string[pos:pos+10]
		auxD=[]
		auxDrms=[]
		auxT=[]
		auxTrms=[]
		for i in range (0,len(sensoresID)*4):
			try:
				var=string[pos:string.index('\t',pos)]
				auxD.append(var)

				pos=string.index('\t',pos)+1
				var=string[pos:string.index('\t',pos)]
				auxDrms.append(var)

				pos=string.index('\t',pos)+1
				var=string[pos:string.index('\t',pos)]
				auxT.append(var)

				pos=string.index('\t',pos)+1
				var=string[pos:string.index('\t',pos)]
				auxTrms.append(var)
				pos=string.index('\t',pos)+1
			except ValueError:
				break
		auxD=auxD[0:len(auxD)-1]
		D_ini.append(auxD)
		Drms_ini.append(auxDrms)
		T_ini.append(auxT)
		Trms_ini.append(auxTrms)
	print (len(D_ini))
	print (len(Drms_ini))
	print (len(T_ini))
	print (len(Trms_ini))
	print (len(D_ini[0]))



	########################################################################
	####armazena parametros D, Drms, T e Trms obtidos nos dias seguintes####
	########################################################################
	D=[]
	Drms=[]
	T=[]
	Trms=[]
	for x in range(0,len(lines)):	
		string=lines[x]
		#print string
		pos=string.index('\t')
		pos=pos+1
		pos=string.index('\t',pos)
		pos=pos+1
		pos=string.index('\t',pos)
		pos=pos+2
		#print string[pos:pos+10]
		auxD=[]
		auxDrms=[]
		auxT=[]
		auxTrms=[]
		for i in range (0,len(sensoresID)*4):
			try:
				var=string[pos:string.index('\t',pos)]
				auxD.append(var)

				pos=string.index('\t',pos)+1
				var=string[pos:string.index('\t',pos)]
				auxDrms.append(var)

				pos=string.index('\t',pos)+1
				var=string[pos:string.index('\t',pos)]
				auxT.append(var)

				pos=string.index('\t',pos)+1
				var=string[pos:string.index('\t',pos)]
				auxTrms.append(var)
				pos=string.index('\t',pos)+1
			except ValueError:
				break
		auxD=auxD[0:len(auxD)-1]
		D.append(auxD)
		Drms.append(auxDrms)
		T.append(auxT)
		Trms.append(auxTrms)
	print (len(D))
	print (len(Drms))
	print (len(T))
	print (len(Trms))
	print (len(D[0]))


	###############################################################
	#######Armazena media obtida do dia de aquisicao inicial#######
	###############################################################
	soma=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	for i in range(0,len(D_ini[0])):
		for j in range(0,len(D_ini)):
			try:
				soma[i]=soma[i]+float(D_ini[j][i])
			except ValueError:
				pass

	print (D_ini[0])
	print ('\n')
	#a partir da soma, obtem media
	media=[]
	for i in range(0,len(soma)):
		media.append(soma[i]/len(D_ini))
	print (media)


	########################################################################
	###A partir da media obtem variação de cada sensor no dia determinado###
	########################################################################
	aux=[]
	y=[]
	for i in range(0,len(D)):
		for j in range(0,len(D[0])):
			aux.append(1000*(float(D[i][j]) - media[j]))
		y.append(aux)
		aux=[]
	print ('\n')

	for i in range(0, len(y)):
		#elimina sensores defeituosos
		y[i]=y[i][0:6]+y[i][7:14]+y[i][15:16]
		print (y[i])
		print ('\n')
	print (len(y[0]))


	######################
	#########Plot#########
	######################
	#organiza lista dos dias de aquisição
	for i in range(0,len(dias)):
		dias[i]=str(dias[i][12:14])+'/'+str(dias[i][9:11])+'/'+str(dias[i][4:8])
		'HLS_2016_07_22.TXT'

	#organiza vetor x de acordo com o numero de sensores
	x=[]
	for i in range(0,14):
		x.append(i)

	n=["H7DC-40","H7DC-59","H7DC-47","H7DC-46","H7DC-39","H7DC-52","H7DC-57","H7DC-36","H7DC-44","H7DC-42","H7DC-56","H7DC-45","H7DC-38","H7DC-55"]
	fig = figure(num=None, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
	ax = fig.add_subplot(111)
	for i in range(0,len(y)):
		ax.plot(x, y[i], label=dias[i])
		loc = plticker.MultipleLocator(base=1.0) # this locator puts ticks at regular intervals
		ax.xaxis.set_major_locator(loc)
		ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.05),
          ncol=3, fancybox=True, shadow=True)
		fig.suptitle("Variacao Diaria do sistema")
		plt.ylabel("dH [um]")
	#omite eixo x
	labels = [item.get_text() for item in ax.get_xticklabels()]
	labels = ['S1','S1','S2','S3','S4','S5','S6','S7','S8','S9','S10','S11','S12','S13','S14']
	#na linha de cima ha um pequeno bug onde o primeiro elemento eh omitido de xlabel. Por isso S1 foi usado 2x
	ax.set_xticklabels(labels)
	fig.savefig('HLS.png')
	show()


#HLS_plot4("HLS_2016_07_22.TXT","HLS_2016_08_03.TXT")


