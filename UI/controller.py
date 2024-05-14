import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCalcola(self, e):
        try:
            intAnno = int(self._view._txtAnno.value)
            result = self._model.handle_calcola_confini(intAnno)
            self._view._txt_result.controls.append(ft.Text(f"Numero di nodi del grafo: {self._model._grafo.number_of_nodes()}\n"
                                                           f"Numero di archi del grafo {self._model._grafo.number_of_edges()}"))
            self._view._txt_result.controls.append(ft.Text(f"Numero di componenti connesse: {result[0]}"))
            for i in result[1 :]:
                self._view._txt_result.controls.append(ft.Text(f"{i[0]} - Numero di stati confinanti {i[1]}"))
            self._view.update_page()

            self.add_stati_Dd()
            self._view.update_page()
        except ValueError:
            print("Errore conversione anno")

    def add_stati_Dd(self):
        stati = self._model._countriesList
        for i in stati:
            self._view._DD_stati.options.append(ft.dropdown.Option(key=i.CCode, text=i.StateNme))
        self._view._btn_raggiungibili.disabled = False


    def handle_raggiungibili(self, e):
        cod_stato = int(self._view._DD_stati.value)
        print(cod_stato)
        result = self._model.handle_raggiungibili(cod_stato)
        self._view._txt_result.clean()
        self._view._txt_result.controls.append(ft.Text(f"Stati raggiungibili da {self._model._idMap[cod_stato]}"))
        for i in result:
            self._view._txt_result.controls.append(ft.Text(f"{i}"))
        self._view.update_page()
