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
        self._raggiungibili = []

    def handle_calcola_confini(self, year):
        self.build_graph(year)
        result = []
        result.append(self.get_num_connected_components())
        for c in self._countriesList:
            result.append((c, len(self.get_comp_connessa(c))))
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
        """source = self._idMap[int_source]
        conn_comp = self.get_comp_connessa(source)
        print(conn_comp)
        return conn_comp"""
        # modo 2 ricorsione
        source = self._idMap[int_source]
        self._raggiungibili.append(source)
        self.ricorsione_raggiungibili(source, [], self._grafo)

    def ricorsione_raggiungibili(self, source, parziale, grafo):
        # caso banale
        if len(grafo[source]) == 0:
            self._raggiungibili.append(parziale)
        else:
            pass

    def get_comp_connessa(self, source):
        conn_comp = nx.descendants_at_distance(self._grafo, source, 1)
        return conn_comp

    def get_num_connected_components(self):
        return nx.number_connected_components(self._grafo)
