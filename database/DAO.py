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
    def getArchi(anno, country):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select gr.Retailer_code as r1, gr2.Retailer_code as r2, count(distinct gds.Product_number) as weight
                    from go_retailers gr , go_retailers gr2 , go_daily_sales gds , go_daily_sales gds2 
                    where gr2.Country = %s
                    and gr.Country = gr2.Country 
                    and gr2.Retailer_code < gr.Retailer_code
                    and gds2.Retailer_code = gr2.Retailer_code 
                    and gds.Retailer_code = gr.Retailer_code
                    and year (gds2.`Date` ) = %s
                    and year (gds.`Date` ) = year (gds2.`Date` )
                    and gds2.Product_number = gds.Product_number 
                    group by gr.Retailer_code, gr2.Retailer_code 
                """

        cursor.execute(query, (country, anno))

        for row in cursor:
            result.append((row["r1"],row["r2"], row["weight"]))

        cursor.close()
        conn.close()
        return result
