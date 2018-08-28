#
# ESTE PROGRAMA PLOTA OS GRÁFICOS ONLINE, PORÉM SEM RECURSOS DE REFERÊNCIAS VARIÁVEIS 
#
import sys
from PyQt4 import QtGui
from PyQt4.QtGui import *
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
import random
import os
from PyQt4 import QtGui, QtCore
from time import strftime
from multiprocessing import Process
import time
import threading
from pylab import figure, axes, pie, title, show
from os import listdir
from os.path import isfile, join
import numpy as np


#Método de análise: plota gráficos através da variação média individual de cada sensor.
#A media eh definida nas 10 primeiras aquisições
#def HLS_plot2(dataIni, dataFim):
def HLS_plot2():
        dataIni = '2017_05_23'
        dataFim = '2017_05_24'
	print (dataIni)
	print (dataFim)
	mypath="C:/users/rodrigo.neto/Desktop/Software"
	onlyfiles = sorted([f for f in listdir(mypath) if isfile(join(mypath, f))])
	#print onlyfiles
	lines=[]
	#loop para pegar arquivos entre intervalo desejado e ler todas as linhas
	for i in range(0,len(onlyfiles)):
		filename=onlyfiles[i]
		#print filename
		if ((filename>=dataIni) and (filename<=dataFim)):
			print (filename)
			myfile=open(os.path.join("C:/users/rodrigo.neto/Desktop/Software",filename))
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
	print (len(D[0]))


	###############################################################
	###Armazena media inicial obtida das 10 primeiras aquisições###
	###############################################################
	#obtem soma do valor de cada sensor para as 10 primeiras aquisições
	soma=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	print (sensor_refID)
	for i in range(0,len(D[0])):
		for j in range(0,10):
			soma[i]=soma[i]+float(D[j][i])

	print (D[0])
	#a partir da soma, obtem media
	media=[]
	for i in range(0,len(soma)):
		media.append(soma[i]/10)
	print (media)


	###############################################################
	########Armazena delta para as demais aquisições###############
	###############################################################
	y=[]
	aux=[]
	print (D[0])
	print (D[0][0])
	print (D[0][1])
	print (D[0][2])
	n=["H7DC-40","H7DC-59","H7DC-47","H7DC-46","H7DC-39","H7DC-52","H7DC-57","H7DC-36","H7DC-44","H7DC-42","H7DC-56","H7DC-45","H7DC-38","H7DC-55"]
	for i in range(0,len(D[0])):
		for j in range(10,len(D)):
			try:
				aux.append(1000*(float(D[j][i]) - media[i]))
			except ValueError:
				pass
		y.append(aux)
		aux=[]
	print (len(y)) 	
	print (len(y[0]))
	#elimina sensores defeituosos
	y=y[0:6]+y[7:14]+y[15:16]
	
	#prepara vetor x
	x=np.array([])
	for i in range(0,len(y[0])):
		x=np.concatenate([x,[i]])
	ynp=np.array(y[0])
	print ("ref")
	print (len)
	print (len(ynp))
	print (len(y))
	print (len(onlyfiles))
	print ("ref")

	fig = figure(num=None, figsize=(14, 7.5), dpi=80, facecolor='w', edgecolor='k')
	ax = fig.add_subplot(111)
	for i in range(0,len(n)):
		x=np.array([])
		for j in range(0,len(y[i])):
			x=np.concatenate([x,[j]])
		print (len(x))
		ynp=np.array(y[i])
		ax.plot(x,ynp, label=n[i])
		ax.legend()
		fig.suptitle("Variacao Media Individual")

	#elementos do eixo x estarao relacionados com o intervalo de analise
	plt.xticks(np.arange(min(x), max(x)+1, len(x)/len(onlyfiles)))	
	plt.ylabel("dH [um]")
	labels = [item.get_text() for item in ax.get_xticklabels()]

	for i in range(0,len(onlyfiles)):
		labels[i]=onlyfiles[i][12:14]+"/"+onlyfiles[i][9:11]
	print (labels)

	ax.set_xticklabels(labels)

	fig.savefig('HLS.png')
	show()

#HLS_plot2("HLS_2016_07_22.TXT","HLS_2016_08_03.TXT")