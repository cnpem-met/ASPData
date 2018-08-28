import numpy as np
import threading

class Var(object):
    def __init__(self):
        ####Inicio da Declaração de variáveis globais####

        """Variável para alocar a interface gráfica"""
        self.ria = None

        """lock para gerenciamento de threads"""
        self.lock = threading.RLock()

        """lista de sensores que é mostrada no 'plot options'"""
        self.sensor_list = ["H7DC_32", "H7DC_33", "H7DC_34", "H7DC_35", "H7DC_36",
                       "H7DC_37", "H7DC_38", "H7DC_39", "H7DC_40", "H7DC_41",
                       "H7DC_42", "H7DC_43", "H7DC_44", "H7DC_45", "H7DC_46",
                       "H7DC_47", "H7DC_48", "H7DC_49", "H7DC_50", "H7DC_51",
                       "H7DC_52", "H7DC_53", "H7DC_54", "H7DC_55", "H7DC_56",
                       "H7DC_57", "H7DC_58", "H7DC_59", "H7DC_60", "H7DC_61"]

        """lista de referencia da disposicao dos sensores"""
        self.disp_sensores =  [["H7DC_51", "H7DC_49", "H7DC_35", "H7DC_34",
                               "H7DC_48", "H7DC_50", "H7DC_41", "H7DC_54"],
                               ["N/C", "N/C", "N/C", "N/C",  
                                "N/C", "N/C", "N/C", "N/C"], 
                               ["N/C", "N/C", "N/C", "N/C",  
                                "N/C", "N/C", "N/C", "N/C"], 
                               ["N/C", "N/C", "N/C", "N/C",  
                                "N/C", "N/C", "N/C", "N/C"]]


        """variáveis para peso na média caminhante; a soma das duas deve ser 1"""
        self.wlast = 0.9
        self.wcurr = 0.1
        
        """cada elemento do vetor v possui dados sobre as 16 tensões lidas
        e o tempo no qual as medidas foram tomadas, os índices"""
        self.v1 = []
        self.v2 = []
        self.v3 = []
        self.v4 = []

        self.D = np.array([[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],
                           [0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]], float)
        
        self.D1 = np.array([])
        self.D2 = np.array([])
        self.D3 = np.array([])
        self.D4 = np.array([])

        self.T1 = np.array([])
        self.T2 = np.array([])
        self.T3 = np.array([])
        self.T4 = np.array([])

        self.mediaD = 0
        self.tam = 0
        self.somaD = 0
        self.mediaT = 0

        """Declaração das flags"""
        self.rack_status = [False, False, False, False]
        self.serialFlag = False

        ###Início das configurações salvas em arquivos###
        """intervalo de aquisição de dados em segundos"""
        self.t_aq = 5
        
        """número de medidas salvas na memória disponíveis para gráfico"""
        self.cmp = 1000
        self.cmp_on = 1000 #novo
        """Declaração das flags de habilitação dos Racks"""
        self.rack1 = False
        self.rack2 = False
        self.rack3 = False
        self.rack4 = False

        """Valores de referência para nível e temperatura"""
        self.Do = np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]], float)
        self.To = np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]], float)
        
        """Valores médios de nível e temperatura (média total)"""
        self.Davg = np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]], float)
        self.Tavg = np.array([[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],
                            [0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]], float)        
        ###Fim das configurações salvas em arquivos###

        
        ###Declaração dos comandos###
        """os dados são enviados na forma EECCDDSS, onde:
        EE = endereço do rack com 2 caracteres de hexa;
        CC = comando com 2 caracteres de hexa;
        DD = dados do comando, podendo ter 0 caracteres;
        SS = checksum com 2 caracteres de hexa"""
        
        """comando F0, rack reset"""
        self.data10 = '01F00F'
        self.data20 = '02F00E'
        self.data30 = '03F00D'
        self.data40 = '04F00C' 

        """comando F1, rack connect"""
        self.data11 = '01F10E'
        self.data21 = '02F10D'
        self.data31 = '03F10C'
        self.data41 = '04F10B'

        """comando F2, rack disconnect"""
        self.data12 = '01F20D'
        self.data22 = '02F20C' 
        self.data32 = '03F20B'
        self.data42 = '04F20A' 

        """comando 30, acquisition of values"""
        self.data13 = '013008C7'
        self.data23 = '023008C6'
        self.data33 = '033008C5'
        self.data43 = '043008C4'

        """comando 31, initialization of acquisition parameters"""
        self.data14 = '01311E00020005A9'
        self.data24 = '02311E00020005A8'
        self.data34 = '03311E00020005A7'
        self.data44 = '04311E00020005A6'

        """comando F6, read status"""
        self.data15 = '01F609'
        self.data25 = '01F608'
        self.data35 = '01F607'
        self.data45 = '01F606'

        """para mais informações sobre os comandos descritos, além de outros
        que não são utilizados aqui, checar documentação da fogale"""
        self.pol_T = np.poly1d([5.00352, -0.4045])

        ###Declaração dos polinômios para conversão tensão-nível###
        self.H7DC_032 = np.poly1d([1.473e-4, -2.382e-3, 5.0951e-1, 5.0000])  #
        self.H7DC_033 = np.poly1d([1.486e-4, -2.447e-3, 5.0950e-1, 4.9993])  #
        self.H7DC_034 = np.poly1d([1.469e-4, -2.416e-3, 5.1002e-1, 4.9994])  #
        self.H7DC_035 = np.poly1d([1.479e-4, -2.445e-3, 5.0971e-1, 4.9993])  #
        self.H7DC_036 = np.poly1d([1.444e-4, -2.387e-3, 5.0941e-1, 4.9992])  #
        self.H7DC_037 = np.poly1d([1.522e-4, -2.419e-3, 5.0900e-1, 4.9990])  #
        self.H7DC_038 = np.poly1d([1.472e-4, -2.378e-3, 5.0913e-1, 4.9995])  #
        self.H7DC_039 = np.poly1d([1.452e-4, -2.331e-3, 5.0884e-1, 4.9994])  #
        self.H7DC_040 = np.poly1d([1.433e-4, -2.366e-3, 5.0923e-1, 4.9993])  #
        self.H7DC_041 = np.poly1d([1.478e-4, -2.335e-3, 5.0846e-1, 4.9995])  #
        self.H7DC_042 = np.poly1d([1.437e-4, -2.321e-3, 5.0883e-1, 4.9993])  #
        self.H7DC_043 = np.poly1d([1.417e-4, -2.278e-3, 5.0844e-1, 4.9995])  #
        self.H7DC_044 = np.poly1d([1.451e-4, -2.422e-3, 5.0961e-1, 4.9994])  #
        self.H7DC_045 = np.poly1d([1.470e-4, -2.350e-3, 5.0884e-1, 5.0001])  #
        self.H7DC_046 = np.poly1d([1.517e-4, -2.379e-3, 5.0852e-1, 4.9992])  #
        self.H7DC_047 = np.poly1d([1.464e-4, -2.290e-3, 5.0862e-1, 4.9996])  #
        self.H7DC_048 = np.poly1d([1.532e-4, -2.401e-3, 5.0866e-1, 4.9997])  #
        self.H7DC_049 = np.poly1d([1.445e-4, -2.365e-3, 5.0896e-1, 4.9999])  #
        self.H7DC_050 = np.poly1d([1.439e-4, -2.334e-3, 5.0876e-1, 4.9995])  #
        self.H7DC_051 = np.poly1d([1.450e-4, -2.307e-3, 5.0841e-1, 4.9995])  #
        self.H7DC_052 = np.poly1d([1.466e-4, -2.277e-3, 5.0724e-1, 4.9994])  #
        self.H7DC_053 = np.poly1d([1.451e-4, -2.330e-3, 5.0857e-1, 4.9999])  #
        self.H7DC_054 = np.poly1d([1.501e-4, -2.309e-3, 5.0791e-1, 4.9996])  #
        self.H7DC_055 = np.poly1d([1.384e-4, -2.282e-3, 5.0877e-1, 4.9992])  #
        self.H7DC_056 = np.poly1d([1.401e-4, -2.256e-3, 5.0810e-1, 4.9998])  #
        self.H7DC_057 = np.poly1d([1.493e-4, -2.378e-3, 5.0835e-1, 4.9995])  #
        self.H7DC_058 = np.poly1d([1.464e-4, -2.325e-3, 5.0915e-1, 4.9994])  #
        self.H7DC_059 = np.poly1d([1.469e-4, -2.411e-3, 5.0952e-1, 4.9992])  #
        self.H7DC_060 = np.poly1d([1.480e-4, -2.283e-3, 5.0728e-1, 4.9995])  #
        self.H7DC_061 = np.poly1d([1.453e-4, -2.317e-3, 5.0852e-1, 5.0001])  #
        self.H7DC_062 = np.poly1d([0.000000, 0.0000000, 0.0000000, 0.0000])  #
        self.H7DC_063 = np.poly1d([0.000000, 0.0000000, 0.0000000, 0.0000])  #
        
        """self.D_Rack é uma matriz 2x2 contendo os polinomios de conversão de cada sensor,
        onde o elemento i+1 (linha) é o índice do Rack e o elemento j (coluna) é o sensor"""
                    ###Configuração na ordem padrão dos sensores###
        #=============================================================================#
        #self.D_Rack = [[self.H7DC_032, self.H7DC_033, self.H7DC_034, self.H7DC_035,  #
        #                self.H7DC_036, self.H7DC_037, self.H7DC_038, self.H7DC_039], #
        #               [self.H7DC_040, self.H7DC_041, self.H7DC_042, self.H7DC_043,  #
        #                self.H7DC_044, self.H7DC_045, self.H7DC_046, self.H7DC_047], #
        #               [self.H7DC_048, self.H7DC_049, self.H7DC_050, self.H7DC_051,  #
        #                self.H7DC_052, self.H7DC_053, self.H7DC_054, self.H7DC_055], #
        #               [self.H7DC_056, self.H7DC_057, self.H7DC_058, self.H7DC_059,  #
        #                self.H7DC_060, self.H7DC_061, self.H7DC_062, self.H7DC_063]] #
        #=============================================================================#

                    ### Configuração da atual disposição dos sensores na bancada METRO (SÓ UM RACK) ###
        self.D_Rack = [[self.H7DC_051, self.H7DC_049, self.H7DC_035, self.H7DC_034,  
                        self.H7DC_048, self.H7DC_050, self.H7DC_041, self.H7DC_054], 
                       [self.H7DC_036, self.H7DC_044, self.H7DC_042, self.H7DC_056,  
                        self.H7DC_045, self.H7DC_038, self.H7DC_032, self.H7DC_055], 
                       [self.H7DC_062, self.H7DC_062, self.H7DC_062, self.H7DC_062,  
                        self.H7DC_062, self.H7DC_053, self.H7DC_062, self.H7DC_062], 
                       [self.H7DC_037, self.H7DC_062, self.H7DC_058, self.H7DC_043,  
                        self.H7DC_060, self.H7DC_061, self.H7DC_062, self.H7DC_063]]
                    ### ideia: implementar isso automaticamente, junto a 'sensor_list' ###


        ###Correção térmica do nível###
        """correção de dilatação termica da água:"""
        self.T = 0
        self.Tref = 20 #ºC
        self.F = np.poly1d([-0.0036023, 0.75406167, -5.2344, 8.4976])
        self.Cag = (self.F(self.T) - self.F(self.Tref))/(1e5-self.F(self.T))

        """Correção de dilatação térmica do recipiente:"""
        self.Hdiff = 54 #mm
        self.Cdil_vessel = 17 #ppm/ºC
        self.Pt = 11 #mm; Ponto de equilíbrio da água
        self.Cm = self.Hdiff*self.Cdil_vessel*1e-6*(self.T-self.Tref)
        ###Fim da declaração de váriáveis globais####


var = Var()
