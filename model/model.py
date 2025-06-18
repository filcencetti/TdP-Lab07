from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        self.mean_humidities = []
        self.best_path = []
        self.best_sol = 10000
        pass


    def getMean(self,month):
        self.mean_humidities = MeteoDao.get_mean(month)
        return self.mean_humidities

    def getPath(self,month):
        self.situations = MeteoDao.get_all_situazioni(month)
        for city in self.situations:
            parziale = [city]
            costo = 0
            self.recursion(parziale,costo,1)

    def recursion(self,parziale,costo,livello):
        if livello == 16:
            if self.best_sol > costo:
                self.best_sol = costo
                self.best_path = parziale

        if livello < 4:
            for city in self.situations:
                if city.localita == parziale[0].localita and city not in parziale:
                    parziale.append(city)
                    self.recursion(parziale, costo, livello + 1)
        else:
            for city in self.situations:
                if parziale[livello-1].localita == city.localita


