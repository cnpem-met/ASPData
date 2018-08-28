import sys, os, threading, time
import numpy as np
from Variaveis import var
from PyQt4 import QtCore, QtGui
import PyQt4.Qwt5 as Qwt

ref_arquivo = open("arq_teste.txt", "r")
resp=[]
data=[]
hora=[]

for linha in ref_arquivo:
    valores = linha.split()
    #print('\nData:', valores[0], 'Hora:', valores[1], 'Rx:', valores[2])
    resp = np.append(resp, valores[2])
    data = np.append(data, valores[0])
    hora = np.append(hora, valores[1])
#for i in range(3):
       # print('Rx:', resp[i])
ref_arquivo.close();
#requisita e salva dados dos sensores
    #def acquire(self):

#v_converter(self.response, 1)

vtmp = np.array([])
exp = 0
mantissa = 0
output = 0
sig = ''
v = np.array([])
vout = np.array([])
timesec = time.time()
D = np.array([timesec])
T = np.array([timesec])
#for i in range(0,3):
    #D = np.append(D, [hora[i]])
    #T = np.append(T, [hora[i]])
for j in range(16):
    #for j in range(16):
    tmp0 = np.binary_repr(int(('0x'+resp[0][8*j+11]+resp[0][8*j+12]), 16), 8)
    tmp1 = np.binary_repr(int(('0x'+resp[0][8*j+9]+resp[0][8*j+10]), 16), 8)
    tmp2 = np.binary_repr(int(('0x'+resp[0][8*j+7]+resp[0][8*j+8]), 16), 8)
    tmp3 = np.binary_repr(int(('0x'+resp[0][8*j+5]+resp[0][8*j+6]), 16), 8)
    vtmp = np.append(vtmp, (tmp0 + tmp1 + tmp2 + tmp3))
    if vtmp[j][0] == '0':
        sig = ''
    else:
        sig = '-'
        #print(resp[i])
    print(vtmp)
##            self.exp = int(('0b' + self.vtmp[j][1:9]), 2) - 129
    exp = int(('0b' + vtmp[j][1:9]), 2) - 127
    mantissa = (int(('0b' + vtmp[j][9:]), 2)/2**23 + 1)
    output = float(sig+str(mantissa))*2**exp
        #print(output)
            

    if (divmod(j, 2)[1] == 0):
##                self.mantissa = (int(('0b' + self.vtmp[j][9:]), 2)/2**23 + 1)*4
##                self.output = float(self.sig+str(self.mantissa)+'e'+str(self.exp))
        output = var.D_Rack[0][int(j/2)](output)
        D = np.append(D, output)        

    else:
        output = var.pol_T(output)
        T = np.append(T,output)
    vout = np.append(vout, output)
                
v = np.reshape(vout, (8,2))
print(T[1:])
Cag = (var.F(T[1:]) - var.F(np.ones(8)*var.Tref))/(1e5-var.F(T[1:]))
Cdag = (np.ones(8)*var.Hdiff - D[1:] - np.ones(8)*var.Pt)*Cag
Cm = var.Hdiff*var.Cdil_vessel*1e-6*(T[1:] - np.ones(8)*var.Tref)
D[1:] = D[1:] + Cdag - Cm
        #self.D[10] = var.H7DC_041(self.D[10])

print('D:', D[1:])


print('v:', self.v)
try:
    var.D1 = np.row_stack([var.D1, self.D])
    var.T1 = np.row_stack([var.T1, self.T])
except ValueError:
    var.D1 = np.append(var.D1, self.D)
    var.T1 = np.append(var.T1, self.T)
if len(var.D1) > var.cmp:
    var.D1 = var.D1[1:]
    var.T1 = var.T1[1:]

print('D1', D1)
printf('T1:', T1)



"""
class RIA(object):
    def __init__(self, parent = None):
        pass
    
    def send(self):
        self.ref_arquivo = open("arq_teste.txt", "r")
        self.response=[]
        self.data=[]
        self.hora=[]

    for linha in ref_arquivo:
        self.valores = linha.split()
    #print('\nData:', valores[0], 'Hora:', valores[1], 'Rx:', valores[2])
        self.response = np.append(self.resp, self.valores[2])
        self.data = np.append(self.data, self.valores[0])
        self.hora = np.append(self.hora, self.valores[1])
    ref_arquivo.close();
    for i in range(3):
        print('Rx:', self.response[i])

#requisita e salva dados dos sensores
    def acquire(self):
        self.v_converter(self.response, 1)
        print(self.v)
        try:
            var.D1 = np.row_stack([var.D1, self.D])
            var.T1 = np.row_stack([var.T1, self.T])
        except ValueError:
            var.D1 = np.append(var.D1, self.D)
            var.T1 = np.append(var.T1, self.T)
        if len(var.D1) > var.cmp:
            var.D1 = var.D1[1:]
            var.T1 = var.T1[1:]

    
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
            
        for j in range(16):
            converte os caracteres recebidos para bits, permitindo recuperar
            o valor de ponto flutuante da tensão
            self.tmp0 = np.binary_repr(int(('0x'+resp[8*j+11]+resp[8*j+12]), 16), 8)
            self.tmp1 = np.binary_repr(int(('0x'+resp[8*j+9]+resp[8*j+10]), 16), 8)
            self.tmp2 = np.binary_repr(int(('0x'+resp[8*j+7]+resp[8*j+8]), 16), 8)
            self.tmp3 = np.binary_repr(int(('0x'+resp[8*j+5]+resp[8*j+6]), 16), 8)
            self.vtmp = np.append(self.vtmp, (self.tmp0 + self.tmp1 + self.tmp2 +
                                                     self.tmp3))
            recupera o sinal da tensão
            if self.vtmp[j][0] == '0':
                self.sig = ''
            else:
                self.sig = '-'

            recupera o expoente da tensão
##            self.exp = int(('0b' + self.vtmp[j][1:9]), 2) - 129
            self.exp = int(('0b' + self.vtmp[j][1:9]), 2) - 127
            self.mantissa = (int(('0b' + self.vtmp[j][9:]), 2)/2**23 + 1)
            self.output = float(self.sig+str(self.mantissa))*2**self.exp
            
            Mantissa de índices pares, relativos às medidas de nível
            if divmod(j, 2)[1] == 0:
##                self.mantissa = (int(('0b' + self.vtmp[j][9:]), 2)/2**23 + 1)*4
##                self.output = float(self.sig+str(self.mantissa)+'e'+str(self.exp))
                self.output = var.D_Rack[i-1][int(j/2)](self.output)
                self.D = np.append(self.D, self.output)            
                
                Mantissa de índices ímpares, relativos à medidas de temperatura
            else:
##                self.mantissa = (int(('0b' + self.vtmp[j][9:]), 2)/2**23 + 1)*4
                multiplica tensão por 5, fator de conversão da temperatura
##                self.output = float(self.sig+str(self.mantissa)+'e'+str(self.exp))*5
##                self.output = self.output*5
                self.output = var.pol_T(self.output)
                self.T = np.append(self.T, self.output)
            self.vout = np.append(self.vout, self.output)
                
        self.v = np.reshape(self.vout, (8,2))

        correção de nível por dilatação térmica da água:
        self.Cag = (var.F(self.T[1:]) - var.F(np.ones(8)*var.Tref))/(1e5-var.F(self.T[1:]))
        self.Cdag = (np.ones(8)*var.Hdiff - self.D[1:] - np.ones(8)*var.Pt)*self.Cag
        correção de nível por dilatação térmica do recipiente:
        self.Cm = var.Hdiff*var.Cdil_vessel*1e-6*(self.T[1:] - np.ones(8)*var.Tref)
        aplicação das correções:
        self.D[1:] = self.D[1:] + self.Cdag - self.Cm
        #self.D[10] = var.H7DC_041(self.D[10])

        print(self.D[1:])
"""
