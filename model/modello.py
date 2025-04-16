import copy

from networkx.algorithms.flow import cost_of_flow

from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.n_soluzioni = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []
    @staticmethod
    def get_mean_humidity(month):
        return MeteoDao.get_mean_humidity(month)

    # @staticmethod
    # def get_15_days(month):
    #     return MeteoDao.get_15_day(month)


    def calcola_sequenza(self,month):
        self.n_soluzioni = 0
        self.costo_ottimo = -1
        self.soluzione_ottima = []
        situazioni = MeteoDao.get_15_day(month)
        self._ricorsione([],situazioni)
        return self.soluzione_ottima,self.costo_ottimo

    def trova_possibili_step(self,parziale,lista_situazioni):
        giorno = len(parziale)+1
        candidati = []
        for situazione in lista_situazioni:
            if situazione.data.day == giorno:
                candidati.append(situazione)
        return candidati


    def is_admissible(self,candidate,parziale):
        # vincolo sui 6 giorni
        counter = 0
        for situazione in parziale:
            if situazione.localita == candidate.localita:
                counter +=1
        if counter >= 6:
            return False

        # vincolo sulla permanenza
        if len(parziale) == 0:
            return True

        # caso 1: lunghezza di parziale minore di 3
        if len(parziale) < 3:
            if candidate.localita != parziale[0].localita:
                return False

        # caso 2: le tre situazioni precedenti non sono tutte uguali
        else:
            if (parziale[-1].localita != parziale[-2].localita
                    or parziale[-1].localita != parziale[-3].localita
                    or parziale[-2].localita != parziale[-3].localita):
                if parziale[-1].localita != candidate.localita:
                    return False

        # altrimenti ok
        return True


    def _calcola_costo(self,parziale):
        costo = 0
        # 1) costo umidità
        for situazione in parziale:
            costo += situazione.umidita

        # 2) costo su spostamenti
        for i in range(len(parziale)):
            # se i due giorni precedenti non sono nella stessa città
            # pago 100
            if i>=2 and (parziale[i-1].localita != parziale[i].localita or
                           parziale[i-2].localita != parziale[i].localita):
                costo += 100

        return costo

    def _ricorsione(self,parziale,lista_situazioni):
        # condizione terminale
        if len(parziale) ==15:
            self.n_soluzioni += 1
            costo = self._calcola_costo(parziale)
            if self.costo_ottimo == -1 or self.costo_ottimo > costo:
                self.costo_ottimo = costo
                self.soluzione_ottima = copy.deepcopy(parziale)


        #condizione ricorsiva
        else:
            # cercare la città per il giorno che mi serve
            candidates = self.trova_possibili_step(parziale,lista_situazioni)
            # prova ad aggiungere una di queste città e vado avanti
            for candidate in candidates: # check per non mettere la stessa data
                # verifica vincoli
                if self.is_admissible(candidate,parziale):
                    parziale.append(candidate)
                    self._ricorsione(parziale,lista_situazioni)
                    parziale.pop()


if __name__ == '__main__':
    my_model = Model()
    print(my_model.calcola_sequenza(1))