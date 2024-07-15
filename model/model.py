import copy
import time

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
        nodi = DAO.getAllRetailers(nazione)
        for n in nodi:
            self.idMap[n.Retailer_code] = n
            self.grafo.add_node(n)
        archi = DAO.getArchi(anno, nazione)
        for a in archi:
            self.grafo.add_edge(self.idMap[a[0]], self.idMap[a[1]], weight = a[2])

    def cercaPercorso(self, nMax):
        self.solBest = []
        self.sommaArchi = 0
        soluzione = {}
        start = time.time()
        for n in list(self.grafo.nodes):
            self.ricorsione(n, nMax, [n])
        end = time.time()
        print(end-start)
        #print(self.sommaArchi)
        #print(self.solBest)
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



# select gds2.Retailer_code , gds.Retailer_code , count(distinct(gds.Product_number)) as conteggio
# from go_sales.go_daily_sales gds , go_sales.go_daily_sales gds2, go_sales.go_retailers gr, go_sales.go_retailers gr2
# where year(gds2.`Date`) = 2015
# and year(gds.`Date`) = 2015
# and gds2.Retailer_code != gds.Retailer_code
# and gds2.Product_number = gds.Product_number
# and gr.Retailer_code  = gds.Retailer_code
# and gr2.Retailer_code= gds2.Retailer_code
# and gr.Country = 'France'
# and gr2.Country = 'France'
# group by gds2.Retailer_code , gds.Retailer_code


