import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dao.IOrderManagementRepository import IOrderManagementRepository

from util.DB_Util import DBUtil
from entity.model import *
from exceptions.custom_exceptions import OrderNotFound,UnauthorizedAccess
from exceptions.custom_exceptions import UserNotFound


class OrderProcessor(IOrderManagementRepository):

    
    def createOrder(self, user, order_id, product_id, quantity, order_date):
        # to create an order for the given user with the specified product
        conn = DBUtil.getDBConn()
        cursor = conn.cursor()
        try:
            # Insert into orders table
            sql_query = f"INSERT INTO orders (orderId,userId, productId, quantity, orderDate) VALUES ({order_id},'{user.getUserId()}', {product_id}, {quantity}, '{order_date}')"
            cursor.execute(sql_query)
            conn.commit()
            
        except Exception as e:
            conn.rollback()
            print("Exception occured The command is not executed and is rollbacked.")
        finally:
            cursor.close()
            conn.close()

    def cancelOrder(self, userId, orderId):
        # Cancel the order with the given orderId for the specified userId
        conn = DBUtil.getDBConn()
        cursor = conn.cursor()
        try:
            # Check if the order exists in the database
            cursor.execute("SELECT * FROM orders WHERE userId = ? AND orderId = ?", (userId, orderId))
            order_exists = cursor.fetchone()
            if order_exists is None:
                # If the order doesn't exist, raise OrderNotFound exception
                raise OrderNotFound(userId, orderId)
            else:
                # If the order exists, delete it from the database
                cursor.execute("DELETE FROM orders WHERE userId = ? AND orderId = ?", (userId, orderId))
                conn.commit()
                print("Order canceled successfully.")
        
        except Exception as e:
            print(f"Exception occurred: {e}")
            conn.rollback()
        finally:
            cursor.close()
            conn.close()

   

    def createProduct(self, user, product):
        # Implement logic to create a new product in the database
        # For example:
        # Connect to the database
        conn = DBUtil.getDBConn()
        # Create a cursor
        cursor = conn.cursor()
        try:
            # Check if the user is an admin
            if user.getRole() == "Admin":
                # If the user is an admin, insert the product into the database
                cursor.execute("INSERT INTO Product (productId, productName, description, price, quantityInStock, type) VALUES (?, ?, ?, ?, ?, ?)",
                            (product.getProductId(), product.getProductName(), product.getDescription(), product.getPrice(), product.getQuantityInStock(), product.getType()))

                # Check if the product type is Electronics
                if isinstance(product, Electronics):
                    # If the product type is Electronics, insert into Electronics table
                    cursor.execute("INSERT INTO Electronics (productId, brand, warrantyPeriod) VALUES (?, ?, ?)",
                                (product.getProductId(), product.getBrand(), product.getWarrantyPeriod()))
                elif isinstance(product, Clothing):
                    # If the product type is Clothing, insert into Clothing table
                    cursor.execute("INSERT INTO Clothing (productId, color, size) VALUES (?, ?, ?)",
                                (product.getProductId(), product.getColor(), product.getSize()))

                # Commit the transaction
                conn.commit()
                print("Product Created Successfully!!")
            else:
                # If the user is not an admin, raise an exception
                raise UnauthorizedAccess("User is not authorized to create products")
        except Exception as e:
            # Rollback the transaction in case of any error
            conn.rollback()
            # Raise an exception or handle it as appropriate
            print(str(e))
        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()


    def createUser(self, user):
        # Implement logic to create a new user in the database
        # For example:
        # Connect to the database
        conn = DBUtil.getDBConn()
        # Create a cursor
        cursor = conn.cursor()
        try:
         
            # Insert the user into the database
            cursor.execute("INSERT INTO users (userId, username, password, role) VALUES (?, ?, ?, ?)",
                        (user.getUserId(), user.getUsername(), user.getPassword(), user.getRole()))
            # Commit the transaction
            conn.commit()
            print("User Created Successfully")
        except Exception as e:
            # Rollback the transaction in case of any error
            conn.rollback()
            # Raise an exception or handle it as appropriate
            print(str(e))
        finally:
            # Close the cursor and database connection
            cursor.close()
            conn.close()


    def getAllProducts(self):
        # Implement logic to retrieve all products from the database
        # to retrieve all products from the database
        conn = DBUtil.getDBConn()
        cursor = conn.cursor()
        try:
            # Retrieve all products from the database
            cursor.execute("SELECT * FROM Product")
            products = []
            for col in cursor.fetchall():
                product = Product(col[0], col[1], col[2], col[3], col[4], col[5])
                products.append(product)
            return products
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def getOrderByUser(self, user):
         
        # to retrieve orders placed by the specified user from the database
        conn = DBUtil.getDBConn()
        cursor = conn.cursor()
        try:
            #Checking the user
            user_id=user.getUserId
            if user_id is None:
                raise UserNotFound(user_id)

            # Retrieve orders by user from the database
            cursor.execute("SELECT * FROM orders WHERE userId = ?", (user.getUserId(),))
            orders = cursor.fetchall()
            return orders
        except Exception as e:
            print("Error Occured.Check user details!!")
        finally:
            cursor.close()
            conn.close()

    def getUserByUsernameAndPassword(self, username, password):
        # to fetch user details from the database based on username and password
        conn = DBUtil.getDBConn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user_data = cursor.fetchone()
            if user_data:
                # Assuming the database schema matches the User class attributes order
                userId, username, password, role = user_data
                user = User(userId, username, password, role)
                return user
            else:
                return None
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()