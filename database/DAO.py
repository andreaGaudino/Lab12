from database.DB_connect import DBConnect
from model.retailer import Retailer


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNazioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct(Country)
                    from go_retailers
                    order by Country"""

        cursor.execute(query, ())

        for row in cursor:
            result.append(row["Country"])

        cursor.close()
        conn.close()
        return result
    @staticmethod
    def getAllRetailers(nazione):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select *
                    from go_retailers g
                    where g.Country = %s
                    order by g.Retailer_code"""

        cursor.execute(query, (nazione,))

        for row in cursor:
            result.append(Retailer(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi(r1, anno, country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select gds.Retailer_code , count(distinct(gds.Product_number)) as conteggio
from go_sales.go_daily_sales gds , go_sales.go_daily_sales gds2, go_sales.go_retailers gr
where year(gds2.`Date`) = %s and year(gds.`Date`) = %s and gds2.Retailer_code = %s and gds.Retailer_code!= %s and gds2.Product_number = gds.Product_number and gr.Retailer_code  = gds.Retailer_code and gr.Country = %s
group by gds.Retailer_code 

                """

        cursor.execute(query, (anno, anno, r1, r1,   country))

        for row in cursor:
            result.append((row["Retailer_code"],row["conteggio"]))

        cursor.close()
        conn.close()
        return result
