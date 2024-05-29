import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.grafo = nx.Graph()
        self.idMap = {}
        self.solBest = []
        self.sommaArchi = 0


    def buildGraph(self, anno, nazione):
        self.grafo.clear()
        self.grafo.add_nodes_from(DAO.getAllRetailers(nazione))
        for n in list(self.grafo.nodes):
            self.idMap[n.Retailer_code] = n

        s = 0
        for r1 in list(self.grafo.nodes):
            lista = DAO.getArchi(r1.Retailer_code, anno, nazione)
            for i in lista:
                r2 = self.idMap[i[0]]
                self.grafo.add_edge(r1, r2, weight = i[1])


    def cercaPercorso(self, nMax):
        self.solBest = []
        self.sommaArchi = 0
        soluzione = {}
        for n in list(self.grafo.nodes):
            self.ricorsione(n, nMax, [n])
        print(self.sommaArchi)
        print(self.solBest)
        for i in range(len(self.solBest)-1):
            #print(self.solBest[i], "-",self.solBest[i+1])
            soluzione[(self.solBest[i], self.solBest[i+1])] = self.grafo[self.solBest[i]][self.solBest[i+1]]["weight"]
        return self.sommaArchi, soluzione


    def ricorsione(self, nodo, nMax, parziale):

        if len(parziale) == nMax+1 :
            somma = 0
            # for i in parziale:
            #     print(i)
            # print()
            for i in range(len(parziale)-1):
                somma += self.grafo[parziale[i]][parziale[i+1]]["weight"]
            if somma > self.sommaArchi:
                self.sommaArchi = somma
                self.solBest = copy.deepcopy(parziale)
                return



        else:
            vicini = list(nx.neighbors(self.grafo, nodo))
            for v in vicini:
                if self.vincoli(v, nMax, parziale):
                    parziale.append(v)
                    self.ricorsione(v, nMax, parziale)
                    parziale.pop()

    def vincoli(self, v, nMax, parziale):
        if v not in parziale:
            if len(parziale)+1 < nMax +1 :
                return True
            # elif len(parziale)+1 == nMax + 1 and parziale[0] == v:
            #     return True
        else:
            if v == parziale[0] and len(parziale) + 1 == nMax+1:
                return True
        return False


