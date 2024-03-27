def get_all_products():
            conn = DBUtil.getDBConn()
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM Products")
                products = []
                for row in cursor.fetchall():
                    product = Products(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                    products.append(product)
                return products
            finally:
                cursor.close()
                conn.close()