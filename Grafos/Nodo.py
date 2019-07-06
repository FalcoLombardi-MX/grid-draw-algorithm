'''
Created on Mar 13, 2014

@author: chewy
'''

SIN_COLOR = 0
BLANCO = 1
GRIS = 2
NEGRO = 3
NADIE = None

SIN_TIPO = None
OBSTACULO = 0
CAMINO = 1
VERDE = 5

class Nodo(object):
    '''
    classdocs
    '''


    def __init__(self, idNodo):
        '''
        Constructor
        '''
        
        self.idNodo = idNodo
        self.color = SIN_COLOR
        self.d = 0
        self.f = 0
        self.pi = NADIE
        
        self.transiciones = {}
        self.tipo = SIN_TIPO
        
        
    def __str__(self):
        
        nodo = "ID: " + self.idNodo +" Color: "+ str(self.color) +" Costo: " + str(self.d) + " Antecesor: "
        nodo += str(self.pi) +" Transiciones: "
        
        for t in self.transiciones.iteritems():
            nodo += t[0] + "," +str(t[1])+"; "
        return nodo            
    
    def agregarTransicion(self, idNodoDestino, costo):
        
        if self.transiciones.has_key(idNodoDestino) == False:
            self.transiciones[idNodoDestino] = costo
        else:
            print "Error: La transicion ya existe..."
    
    def elimitarTransicion(self, idNodoDestino):
        if self.transiciones.has_key(idNodoDestino) ==True:
            self.transiciones.popitem(idNodoDestino)
        else:
            print "Error: La transicion no existe..."
    
    def getTransiciones(self):
        return self.transiciones
    
    def getIdNodo(self):
        return self.idNodo
    
    def setAntecesor(self, ant):
        self.pi = ant
    
    def getAntecesor(self):
        return self.pi
    
    def setCosto(self, costo):
        self.d = costo
    
    def getCosto(self):
        return self.d
    
    def setCostoF(self, costo):
        self.f = costo
    
    def getCostoF(self):
        return self.f
    
    def setColor(self, color):
        self.color = color
        
    def getColor(self):
        return self.color
    
    def setTipo(self, tipo):
        self.tipo = tipo
        
    def getTipo(self):
        return self.tipo
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        