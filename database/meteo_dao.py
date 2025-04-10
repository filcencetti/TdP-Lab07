from database.DB_connect import DBConnect
from model.situazione import Situazione


class MeteoDao():

    @staticmethod
    def get_all_situazioni():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s.Localita, s.Data, s.Umidita
                        FROM situazione s 
                        ORDER BY s.Data ASC"""
            cursor.execute(query)
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_mean_humidity(month):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT Localita, AVG(Umidita) as media
                        FROM meteo.situazione
                        WHERE MONTH(Data) = '%s'
                        GROUP BY Localita"""
            cursor.execute(query,
                           (month,))
            for row in cursor:
                result.append(f"{row["Localita"]}: {row["media"]}")
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_15_day(month):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT Localita, Data, Umidita
                            FROM situazione
                            WHERE MONTH(Data) = '%s' and DAY(Data) < '16'
                            ORDER BY s.Data ASC"""
            cursor.execute(query,
                           (month,))
            for row in cursor:
                result.append(Situazione(row["Localita"],
                                         row["Data"],
                                         row["Umidita"]))
            cursor.close()
            cnx.close()
        return result