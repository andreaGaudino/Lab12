import flet as ft
import networkx as nx

from database.DAO import DAO


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDD(self):
        #riempio gli anni
        self._view.ddcountry.options = []
        anni = [2015, 2016, 2017, 2018]
        anniDD = list(map(lambda x : ft.dropdown.Option(x), anni ))
        self._view.ddyear.options = anniDD


        #riempio le nazioni
        nazioni = DAO.getNazioni()
        nazioniDD = list(map(lambda x:ft.dropdown.Option(x), nazioni))
        self._view.ddcountry.options = nazioniDD

        self._view.update_page()

    def handle_graph(self, e):
        self._view.txt_result.clean()
        self.anno = int(self._view.ddyear.value)
        self.nazione = self._view.ddcountry.value
        self._model.buildGraph(self.anno, self.nazione)

        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {len(self._model.grafo.nodes)} nodi e {len(self._model.grafo.edges)} vertici"))
        self._view.btn_volume.disabled = False
        self._view.btn_path.disabled = False
        self._view.update_page()



    def handle_volume(self, e):
        result = {}
        for r in list(self._model.grafo.nodes):
            vicini = list(nx.neighbors(self._model.grafo, r))
            somma = 0
            for v in vicini:
                somma += self._model.grafo[r][v]["weight"]
            result[r.__str__()] = somma

        ordinato = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

        self._view.txtOut2.clean()
        for i in ordinato:
            self._view.txtOut2.controls.append(ft.Text(f"{i} --> {ordinato[i]}"))
        self._view.update_page()

    def handle_path(self, e):
        nMax = int(self._view.txtN.value)

        if nMax < 2:
            self._view.txtOut3.controls.append(ft.Text(f"Numero di archi minimi inferiore a 2"))
            self._view.update_page()
            return
        self._model.cercaPercorso(nMax)
