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
        for n in list(self.grafo.nodes):
            self.ricorsione(n, nMax, [n])
        print(self.solBest)


    def ricorsione(self, nodo, nMax, parziale):

        if len(parziale) == nMax+1 :
            somma = 0
            for i in range(len(parziale)-1):
                somma += self.grafo[parziale[i]][parziale[i+1]]["weight"]
            if somma > self.sommaArchi:
                self.sommaArchi = somma
                self.solBest = parziale



        else:
            vicini = list(nx.neighbors(self.grafo, nodo))
            for v in vicini:
                parziale.append(v)
                if self.vincoli(parziale, nMax):
                    self.ricorsione(v, nMax, parziale)
                parziale.pop()

    def vincoli(self, parziale, nMax):
        if len(parziale) < nMax +1 :
            return True
        elif len(parziale) == nMax + 1 and parziale[0] == parziale[-1]:
            return True
        return False


