from database.DB_connect import DBConnect
from model.contiguity import Contiguity
from model.country import Country


class DAO():
    def __init__(self):
        pass
    @staticmethod
    def get_edges(year):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary = True)
        query = """
                select *
                from contiguity c 
                where `year` <= %s and conttype = 1
                """
        cursor.execute(query, (year, ))

        for row in cursor:
            result.append(Contiguity(**row))


        cursor.close()
        conn.close()
        return result


    @staticmethod
    def get_nodi(year):
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select distinct c.CCode ,  c.StateAbb , c.StateNme
                from country c, contiguity c2 
                where c.CCode = c2.state1no and c2.year <= %s
                """
        cursor.execute(query, (year, ))

        for row in cursor:
            result.append(Country(**row))


        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_all_countries():
        conn = DBConnect.get_connection()
        result = []

        cursor = conn.cursor(dictionary=True)
        query = """
                select *
                from country c
                        """
        cursor.execute(query)

        for row in cursor:
            result.append(Country(**row))

        cursor.close()
        conn.close()
        return result


if __name__ == "__main__":
    d = DAO()
    d.get_borders_year(2000)
    d.get_all_countries()