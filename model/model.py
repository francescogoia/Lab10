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
        source = self._idMap[int_source]
        conn_comp = self.get_comp_connessa(source)
        print(conn_comp)
        #return conn_comp
        # modo 2 ricorsione
        source = self._idMap[int_source]
        self._raggiungibili.append(source)
        successori = list(self._grafo[source])
        self.ricorsione_raggiungibili(source, [], successori)
        print(self._raggiungibili)

    def ricorsione_raggiungibili(self, source, parziale, successori):
        # caso banale
        banale = False
        for i in successori:
            if i in parziale:
                banale = True

        if banale and len(parziale) != 0:              # tutti i successori sono già in parziale
            self._raggiungibili.append(parziale)

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
