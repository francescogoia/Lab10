from time import time

import networkx as nx

from database.DAO import DAO


class Model:

    def __init__(self):
        self._countriesList = []
        self._grafo = nx.Graph()
        self._idMap = {}
        all_countries = DAO.get_all_countries()
        for c in all_countries:
            self._idMap[c.CCode] = c
        self._raggiungibili = set()
        self.nRicorsioni = 0

    def handle_calcola_confini(self, year):
        self.build_graph(year)
        result = []
        result.append(self.get_num_connected_components())
        for c in self._countriesList:
            result.append((c, self.get_len_comp_connessa(c)))
        return result

    def build_graph(self, year):
        self._grafo.clear()
        self._countriesList = DAO.get_nodi(year)
        all_coonfini_anno = DAO.get_edges(year)
        self._grafo.add_nodes_from(self._countriesList)
        for conf in all_coonfini_anno:
            u = self._idMap[conf.state1no]
            v = self._idMap[conf.state2no]
            self._grafo.add_edge(u, v)

    def handle_raggiungibili(self, int_source):
        # modo 1: metodo di NX
        start = time()
        source = self._idMap[int_source]
        conn_comp = self.get_comp_connessa(source)
        end = time()
        print(f"Tempo metodo di nX: {end - start}\n",conn_comp)
        #return conn_comp
        # modo 2 ricorsione
        start = time()
        source = self._idMap[int_source]
        self._raggiungibili.add(source)
        successori = list(self._grafo[source])
        self.ricorsione_raggiungibili(source, [], successori)
        end = time()
        print(f"Tempo metodo ricorsivo: {end - start}\n", self._raggiungibili)
        print(f"Ricorsioni: {self.nRicorsioni}")
        return self._raggiungibili


    def ricorsione_raggiungibili(self, source, parziale, successori):
        self.nRicorsioni += 1
        # caso banale
        contatore = 0
        for s in successori:
            if s in parziale:
                contatore += 1

        if contatore == len(successori):                    # tutti i successori sono già in parziale
            for p in parziale:
                self._raggiungibili.add(p)
        else:
            nodi = self._grafo[source]
            for nodo in nodi:
                if nodo not in parziale and (x not in parziale for x in successori):
                    parziale.append(nodo)
                    # aggiorno i successori
                    nuovi_successori = list(self._grafo[nodo])
                    self.ricorsione_raggiungibili(nodo, parziale, nuovi_successori)
                    parziale.pop()




    def get_comp_connessa(self, source):
        conn_comp = nx.node_connected_component(self._grafo, source)
        return conn_comp

    def get_len_comp_connessa(self, source):
        conn_comp = nx.descendants_at_distance(self._grafo, source, 1)
        return len(conn_comp)

    def get_num_connected_components(self):
        return nx.number_connected_components(self._grafo)
