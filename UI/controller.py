import flet as ft

from UI.view import View
from model.model import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        # other attributes
        self._mese = 0

    def handle_umidita_media(self, e):
        self.mean_humiditeis = self._model.getMean(self._mese)
        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("L'umidità media nel mese selezionato è:"))
        for city in self.mean_humiditeis:
            self._view.lst_result.controls.append(ft.Text(f"{city[0]}: {city[1]}"))
        self._view.update_page()

    def handle_sequenza(self, e):
        self._model.getPath(self._mese)


    def read_mese(self, e):
        self._mese = int(e.control.value)

