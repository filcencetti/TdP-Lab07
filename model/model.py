from database.meteo_dao import MeteoDao


class Model:
    def __init__(self):
        pass

    @staticmethod
    def get_mean_humidity(month):
        return MeteoDao.get_mean_humidity(month)

    @staticmethod
    def get_15_days(month):
        return MeteoDao.get_15_day(month)