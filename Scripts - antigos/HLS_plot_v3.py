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
import numpy as np

#metodo de analise: plot do valor absoluto do parametro D
def HLS_plot3(dataIni, dataFim):
	print (dataIni)
	print (dataFim)
	mypath="C:/users/rodrigo.neto/Desktop/HLS-BancadaMETRO/dados-bancada-IMAS/"
	onlyfiles = sorted([f for f in listdir(mypath) if isfile(join(mypath, f))])
	#print onlyfiles
	lines=[]
	#loop para pegar arquivos entre intervalo desejado e ler todas as linhas
	for i in range(0,len(onlyfiles)):
		filename=onlyfiles[i]
		#print filename
		if ((filename>=dataIni) and (filename<=dataFim)):
			print (filename)
			myfile=open(os.path.join("C:/users/rodrigo.neto/Desktop/HLS-BancadaMETRO/dados-bancada-IMAS/",filename))
			newlines=myfile.readlines()
			del myfile
			#print len(newlines)
			if (filename==dataIni):
				lines=newlines
			else:
				lines+=newlines[4:len(newlines)]
			print (len(newlines))
			print (len(lines))
	#print len(lines)


	#armazena ID dos sensores
	sensoresID=[]
	string=lines[3]
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
	#####################################################
	####armazena parametros D, Drms, T e Trms obtidos####
	#####################################################
	D=[]
	Drms=[]
	T=[]
	Trms=[]
	for x in range(4,len(lines)):	
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

	#########################################################################
	###########Armazena em delta o valor absoluto do parametro D#############
	#########################################################################
	#define posicao e identificacao dos sensores
	x=[-3.70, -3.27, -2.82, -2.36, -1.90, -1.44, -0.52, 0.41, 0.84, 1.31, 1.79, 2.24, 3.17]
	n=["H7DC-40","H7DC-59","H7DC-47","H7DC-46","H7DC-39","H7DC-52","H7DC-57","H7DC-44","H7DC-42","H7DC-56","H7DC-45","H7DC-38","H7DC-55"]
	#armazena variacao apresentada em cada sensor no parametro delta
	delta=[]
	delta_aux=[]
	for j in range(0,len(D[0])):
		for i in range(10,len(D)):
			try:
				delta_aux.append(float(D[i][j]))
			except ValueError:
				pass
		delta.append(delta_aux)
		delta_aux=[]
	print (len(delta))
	print (len(delta[0]))
	print ("Teste")
	delta = delta[0:6]+delta[7:14]+delta[15:16]
	print (len(delta))
	print (len(delta[0]))

	##########################################################
	###Faz o plot a partir dos valores armazenados em delta###
	##########################################################
	n=["H7DC-40","H7DC-59","H7DC-47","H7DC-46","H7DC-39","H7DC-52","H7DC-57","H7DC-36","H7DC-44","H7DC-42","H7DC-56","H7DC-45","H7DC-38","H7DC-55"]
	y=[]
	fig = figure(num=None, figsize=(14, 10), dpi=80, facecolor='w', edgecolor='k')
	ax = fig.add_subplot(111)
	for i in range(0,len(n)):
		x=np.array([])
		for j in range(0,len(delta[i])):
			x=np.concatenate([x,[j]])
		deltanp=np.array(delta[i])
		ax.plot(x,deltanp, label=n[i])
		ax.legend()

	plt.ylabel("dH [um]")
	fig.suptitle("Valor absoluto")

	#customização para exibir datas no eixo x
	plt.xticks(np.arange(min(x), max(x)+1, len(x)/len(onlyfiles)))
	labels = [item.get_text() for item in ax.get_xticklabels()]
	for i in range(0,len(onlyfiles)):
		labels[i]=onlyfiles[i][12:14]+"/"+onlyfiles[i][9:11]
	print (labels)
	ax.set_xticklabels(labels)

	fig.savefig('HLS.png')
	show()


#HLS_plot3("HLS_2016_07_22.TXT","HLS_2016_08_03.TXT")




