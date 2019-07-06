'''
Created on Mar 13, 2014

@author: chewy
'''
from Grafos.Nodo import *
import sys
from collections import deque

class Grafo(object):
    '''
    classdocs
    '''


    def __init__(self, idGrafo):
        '''
        Constructor
        '''
        self.idGrafo = idGrafo
        self.N = 0
        self.nodos = {}
        self.nodoOrigen = NADIE
        self.tiempo = 0
    
    def __str__(self):
        grafo = "IDGrafo: " +self.idGrafo + " #nodos: " + str(self.N) + " Origen: " + str(self.nodoOrigen)
        grafo += "Nodos: \n"
        for n in self.nodos.iteritems():
            grafo += str(n[1]) +"\n"
        return grafo
    
    def inicializarGrafo(self):
        print "Nombre del grafo: "
        nombreGrafo = sys.stdin.readline()
        self.idGrafo = nombreGrafo
        print "Cuantos nodos tendra el grafo: "
        n = int(sys.stdin.readline())
        print "Cuales son los nombres de los nodos: "
        nombres = sys.stdin.readline().split()
        
        
        for nombre in nombres:
            self.agregarNodo(nombre)
            print "Cuales son las transiciones del nodo: "+nombre
            transiciones = sys.stdin.readline().split()
            i=0
            for transicion in transiciones:
                t = int(transicion)
                if t > 0:
                    self.nodos[nombre].agregarTransicion(nombres[i] , t)
                i += 1     
        
        print "Cuales son los tipos de los nodos: "
        tipos = sys.stdin.readline().split()
        
        i = 0
        for tipo in tipos:
            self.nodos[nombres[i]].setTipo(int(tipo))
            i+=1
    
    
    def agregarNodo(self, idNodo):
    
        if self.nodos.has_key(idNodo) == False:
            nodo = Nodo(idNodo)
            self.nodos[idNodo] = nodo
            self.N += 1 
        else:
            print "Error: EL nodo ya existe..."
    
    def eliminarNodo(self, idNodo):
        
        if self.nodos.has_key(idNodo) == True:
            self.nodos.popitem()
            self.N -= 1
        else:
            print "Error: El nodo no existe..."
     
    def obtenerNodo(self, idNodo):
        return self.nodos[idNodo]   
        
    def bfs(self, s):
        for u in self.nodos.itervalues():
            if u.getIdNodo() != s:
                u.setColor(BLANCO)
                u.setAntecesor(NADIE)
                u.setCosto(-1)
            else:
                u.setColor(GRIS)
                u.setAntecesor(NADIE)
                u.setCosto(0)
        
        Q = deque()
        Q.append(s)
        
        while len(Q) != 0:
            nombre = Q.popleft()
            u = self.nodos[nombre]
            
            for n in u.getTransiciones().iterkeys():
                if u.getTipo() == 1:
                    if self.nodos[n].getColor() == BLANCO:
                        self.nodos[n].setColor(GRIS)
                        self.nodos[n].setCosto(u.getCosto() + 1)
                        self.nodos[n].setAntecesor(u.getIdNodo())
                        Q.append(n)
            
            u.setColor(NEGRO)
            
        
    def crearRuta(self, destino, ruta):
        
        if self.nodos[destino].getAntecesor() == NADIE:
            ruta.appendleft(self.nodos[destino].getIdNodo()) 
        
        else:
            ruta.appendleft(self.nodos[destino].getIdNodo()) 
            self.crearRuta(self.nodos[destino].getAntecesor(), ruta)
        
        
    def imprimirRuta(self, destino, ruta):    
        print "Ruta... "+ str(self.nodos[destino].getCosto())
        for e in ruta:
            print e
    
    
    def dfs(self, s):
        
        for n in self.nodos.itervalues():
            n.setColor(BLANCO)
            n.setAntecesor(NADIE)
    
        self.tiempo = 0
        self.dfs_visit(s)
        
    def dfs_visit(self, u):
    
        n = self.nodos[u]
        n.setColor(GRIS)
        n.setCosto(self.tiempo)
        self.tiempo += 1
        for v in n.getTransiciones().iterkeys():
            if n.getTipo() == 1:
                nv = self.nodos[v]
                if nv.getColor() == BLANCO:
                    nv.setAntecesor(n.getIdNodo())
                    self.dfs_visit(v)
        
        n.setColor(NEGRO)
        self.tiempo = self.tiempo + 1
        n.setCostoF(self.tiempo)
    
      
        
        
        

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        