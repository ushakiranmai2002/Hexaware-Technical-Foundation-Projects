import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from dao.TechShopRepository import ITechShopRepository
from util.db_util import DBUtil
from entity.model import Products, Customers, OrderDetails, Orders
from datetime import date, datetime
from exception import custom_exceptions


class TechShopProcessor(ITechShopRepository):
    def CustomerRegistration(self, customer):
        try:
            conn = DBUtil.getDBConn()
            cursor = conn.cursor()
            if '@' not in customer.get_email():
                raise custom_exceptions.InvalidDataException('Invalid Email')
            cursor.execute("SELECT TOP 1 CustomerID FROM Customers ORDER BY CustomerID DESC")
            customer_id = cursor.fetchone()[0]+1
            cursor.execute("""INSERT INTO Customers (FirstName, LastName, Email, Phone, Address)
                           VALUES ( ?, ?, ?, ?, ?)""", ( customer.get_first_name(), 
                                                          customer.get_last_name(), customer.get_email(), 
                                                          customer.get_phone(), customer.get_address()))
            conn.commit()
            print('Customer created successfully.\n')
        except custom_exceptions.InvalidDataException as e:
            conn.rollback()
            print(e)
        finally:
            cursor.close()
            conn.close()
    
    def ProductCatalog(self, choice):
        # Your implementation for ProductCatalog
        def check_product_exists(product_id):
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                cursor.execute("""SELECT COUNT(*) FROM Products 
                               WHERE ProductID = ? """, (product_id,))
                count = cursor.fetchone()[0]
                cursor.close()
                return count>0

        def update_product_info():
                product_id = int(input('Enter product ID: '))
                if check_product_exists(product_id):
                    price = float(input('Enter New Price: '))
                    desc = input('Enter new description: ')
                    conn = DBUtil.getDBConn()
                    cursor = conn.cursor()
                    cursor.execute(""" UPDATE Products SET Price = ?, Description = ?
                                   WHERE ProductID = ?""",
                                   (price, desc, product_id))
                    conn.commit()
                    cursor.close()
                    print('Product information updated successfully')
                else:
                    print('Product Not found')
        def show_all_products():
            conn = DBUtil.getDBConn()
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT * FROM Products")
                print("Product details:")
                for row in cursor.fetchall():
                    print(row)
            finally:
                cursor.close()
                conn.close()

        def product_in_stock():
            product_id = int(input('Enter product ID: '))
            conn = DBUtil.getDBConn()
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT QuantityInStock FROM Inventory WHERE ProductID = ?", (product_id,))
                quantity = cursor.fetchone()[0]
                if quantity>0:
                    print(f'Product in stock: {quantity}')
                else:
                    print('Product not in stock')
            finally:
                cursor.close()
                conn.close()


        if choice == 1:
            update_product_info()
        elif choice == 2:
            show_all_products()
        elif choice == 3:
            product_in_stock()
        else:
            print('Invalid choice. Please Try again')

    def Orders(self, customer_id, choice):

        def CreateOrder():
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()

                product_id = int(input('Enter product ID: '))
                quantity = int(input('Enter quantity: '))
                order_date = date.today()
                if not product_id or not quantity:
                    raise custom_exceptions.IncompleteOrderException("Enter All the details")

                cursor.execute("SELECT Price FROM Products WHERE ProductID = ?", (product_id,))
                row = cursor.fetchone()
                if row:
                    price = row[0]
                    total_amount = price * quantity
                else:
                    raise custom_exceptions.ProductNotFoundException('Product Not Found')
                cursor.execute("SELECT TOP 1 OrderID FROM Orders ORDER BY OrderID DESC")
                order_id = cursor.fetchone()[0]
                order_id += 1

                cursor.execute("SELECT TOP 1 OrderDetailID FROM OrderDetails ORDER BY OrderDetailID DESC")
                order_detail_id = cursor.fetchone()[0]
                order_detail_id += 1

                #Insert order into Orders Table
                cursor.execute(""" INSERT INTO Orders(OrderID, CustomerId, OrderDate, TotalAmount, Status)
                               VALUES (?, ?, ?, ?, ?)""", (order_id, customer_id, order_date, total_amount, 'Pending'))
                # Insert order details into OrderDetails Table
                cursor.execute(""" INSERT INTO OrderDetails (OrderDetailID, OrderID, ProductID, Quantity)
                               VALUES(?, ?, ?, ?)""", (order_detail_id, order_id, product_id, quantity))
                # Update quantity in stock in Inventory Table
                cursor.execute("SELECT QuantityInStock FROM Inventory WHERE ProductID = ?",(product_id,))
                current_quantity = cursor.fetchone()[0]
                if current_quantity:
                    new_quantity = current_quantity - quantity
                    cursor.execute(""" UPDATE Inventory SET QuantityInStock = ?
                                WHERE ProductID = ?""", (new_quantity, product_id))
                    
                    conn.commit()
                    print('Order Created Successfully')
                else:
                    raise custom_exceptions.InsufficientStockException('Insufficient Stock')
            except custom_exceptions.ProductNotFoundException as e:
                print(e)
            except custom_exceptions.InsufficientStockException as e:
                print(e)
            except custom_exceptions.IncompleteOrderException as e:
                print(e)
            except Exception as e:
                conn.rollback()
                print('Error creating Order', e)
            finally:
                cursor.close()
                conn.close()

        def GetOrderDetails():
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                cursor.execute("""SELECT OD.OrderDetailID, OD.OrderID, OD.ProductID, OD.Quantity, O.OrderDate 
                               FROM OrderDetails OD
                               JOIN Orders O ON O.OrderID = OD.OrderID
                               WHERE O.CustomerID = ?""", (customer_id,))
                orders = cursor.fetchall()
                print(f"You've ordered {len(orders)} times, below are those order details:")
                for order in orders:
                    print()
                    print(f"Order Detail ID: {order[0]}")
                    print(f"Order ID: {order[1]}")
                    print(f"Product ID: {order[2]}")
                    print(f"Quantity: {order[3]}")
                    print(f"Order Date: {order[4]}")
                    print()
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()

        def CancelOrder():
            print('Here are your orders: \n')
            GetOrderDetails()
            order_id = int(input('Select an order to cancel: '))
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM OrderDetails WHERE OrderID = ?", (order_id,))
                cursor.execute("DELETE FROM Orders WHERE OrderID = ?", (order_id,))
                conn.commit()
                print('Order Canceled.')
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()

        if choice == 1:
            CreateOrder()
        elif choice == 2:
            GetOrderDetails()
        elif choice == 3:
            CancelOrder()
        else:
            print('Invalid Choice. Please Try again.')
            return

    def OrderStatus(self, order_id, choice):
        def DisplayStatus():
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                cursor.execute("SELECT Status FROM Orders WHERE OrderID = ?", (order_id,))
                status = cursor.fetchone()[0]
                print("Your order status: ", status)
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()
        def UpdateStatus():
            status = input('Enter status (Shipped/Pending): ')
            if status == 'Shipped'.lower() or 'Pending'.lower():
                try:
                    conn = DBUtil.getDBConn()
                    cursor = conn.cursor()
                    cursor.execute("UPDATE Orders SET Status = ? WHERE OrderID = ?", (status, order_id))
                    print('Status Updated\n')
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    raise e
                finally:
                    cursor.close()
                    conn.close()
            else:
                print('Enter valid status. Try again')
                return
        if choice == 1:
            DisplayStatus()
        elif choice == 2:
            UpdateStatus()
        else:
            print('Invalid choice. Please Try again')
    
    def InventoryManagement(self, choice):

        def AddProduct():
            conn = DBUtil.getDBConn()
            cursor = conn.cursor()
            cursor.execute('SELECT TOP 1 ProductID FROM Products ORDER BY ProductID DESC')
            product_id = cursor.fetchone()[0]+1
            cursor.execute('SELECT TOP 1 InventoryID FROM Inventory ORDER BY InventoryID DESC')
            inventory_id = cursor.fetchone()[0]+1
            try:
                product_name = input('Enter product name: ')
                desc = input('Enter product description: ')
                price = float(input('Enter product price: '))
                category = "Electronics"
                quantity = int(input('Enter quantity in stock: '))
                last_stock_date = date.today()
                cursor.execute("INSERT INTO Products VALUES (?,?,?,?,?)",
                               (product_id, product_name, desc, price, category))
                cursor.execute("INSERT INTO Inventory VALUES (?,?,?,?)",
                                (inventory_id, product_id, quantity, last_stock_date))
                conn.commit()
                print('Product Added Succesfully')
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()

        def UpdateProductStock():
            product_id = int(input('Enter product id: '))
            new_quantity = int(input('Enter quantity to be added: '))
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                cursor.execute("SELECT QuantityInStock FROM Inventory WHERE ProductID = ?", (product_id,))
                quantity_in_stock = cursor.fetchone()[0]
                print('Quantity in stock: ', quantity_in_stock)
                quantity = quantity_in_stock + new_quantity
                cursor.execute("UPDATE Inventory SET QuantityInStock = ? WHERE ProductID = ?", (quantity, product_id))
                print(f'Quantity updated for Product ID {product_id}: {quantity}')
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()

        def RemoveDiscontinuedItems():
            item = int(input('Enter product you want to discontinue (product ID): '))
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM Inventory WHERE ProductID = ?",(item))
                cursor.execute("DELETE FROM Products WHERE ProductID = ?",(item))
                conn.commit()
                print('Removed items successfully')
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()
        if choice == 1:
            AddProduct()
        elif choice == 2:
            UpdateProductStock()
        elif choice == 3:
            RemoveDiscontinuedItems()
        else:
            print('Invalid choice. Please Try again')

    def SalesReport(self, choice):
        def RetrieveSalesData():
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                query = """WITH ProductSales AS(
                            SELECT OD.ProductID, SUM(OD.Quantity) Quantity FROM OrderDetails OD
                            GROUP BY OD.ProductID
                        )
                        SELECT P.ProductID, P.ProductName, PS.Quantity AS TotalQuantity
                        FROM Products P
                        JOIN ProductSales PS ON PS.ProductID = P.ProductID"""
                cursor.execute(query)
                rows = cursor.fetchall()

                print("Sales Report:")
                print("Product ID | Product Name | Total Quantity Sold")
                for row in rows:
                    print(f"{row.ProductID} | {row.ProductName} | {row.TotalQuantity}")
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()

        def GenerateSalesReport():
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                query = """WITH ProductSales AS(
                            SELECT OD.ProductID, SUM(OD.Quantity) Quantity 
                            FROM OrderDetails OD
                            GROUP BY OD.ProductID
                        )
                        SELECT P.ProductID, P.ProductName, PS.Quantity AS TotalQuantity FROM Products P
                        JOIN ProductSales PS ON PS.ProductID = P.ProductID
                        WHERE PS.Quantity = (SELECT MAX(Quantity) FROM ProductSales) OR 
                        PS.Quantity = (SELECT MIN(Quantity) FROM ProductSales)
                        """
                cursor.execute(query)
                rows = cursor.fetchall()

                print("Sales Report:")
                print("Product ID | Product Name | Total Quantity Sold")
                for row in rows:
                    print(f"{row.ProductID} | {row.ProductName} | {row.TotalQuantity}")
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()

        if choice == 1:
            RetrieveSalesData()
        elif choice == 2:
            GenerateSalesReport()
        else:
            print('Invalid choice. Try again')
            return

    def CustomerUpdate(self, customer_id, choice):
        def UpdateCustomerDetails():
            email = input('Enter new email: ')
            phone = input('Enter new phone number: ')
            address = input('Enter new address: ')
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Customers WHERE CustomerID = ?", (customer_id,))
                customer_details = cursor.fetchone()
                if customer_details:
                    customer = Customers(*customer_details)  # Assuming Customers class takes the details as arguments
                    customer.set_email(email)
                    customer.set_phone(phone)
                    customer.set_address(address)
                    cursor.execute("""UPDATE Customers SET Email = ?, Phone = ?, Address = ?
                                    WHERE CustomerID = ?""",
                                (customer.get_email(), customer.get_phone(), customer.get_address(), customer_id))
                    conn.commit()
                    print("Customer details updated")
                else:
                    print("Customer not found")
            except Exception as e:
                conn.rollback()
                raise e
            finally: 
                cursor.close()
                conn.close()

            
        def GetCustomerDetails():
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Customers WHERE CustomerID = ?", (customer_id, ))
                detail = cursor.fetchone()
                print('Customer ID: ', detail[0])
                print('First Name: ', detail[1])
                print('Last Name: ', detail[2])
                print('Email: ', detail[3])
                print('Phone: ', detail[4])
                print('Address: ', detail[5])
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()
                
        
        if choice == 1:
            UpdateCustomerDetails()
        elif choice == 2:
            GetCustomerDetails()
        else:
            print("Invalid choice. Try again\n")

    def PaymentProcess(self, choice):

        def ProcessPayment():
            order_id = int(input('Enter order ID: '))
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                query = """SELECT OD.OrderID, OD.ProductID, OD.Quantity, SUM(P.Price * OD.Quantity) TotalAmount FROM OrderDetails OD
                        JOIN Products P ON P.ProductID = OD.ProductID
                        WHERE OrderID = ?
                        GROUP BY OD.OrderID, OD.ProductID, OD.Quantity"""
                cursor.execute(query, (order_id,))
                rows = cursor.fetchall()
                if not rows:
                    print("No order details found for the given order ID.")
                else:
                    print("OrderID | ProductID | Quantity | TotalAmount")
                    print("-" * 40)
                    for row in rows:
                        order_id, product_id, quantity, total_amount = row
                        print(f"{order_id:^8} | {product_id:^9} | {quantity:^8} | {total_amount:^12}")
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()

        def AddDiscount():
            order_id = int(input('Enter order id: '))
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                query = """SELECT OD.OrderID, SUM(P.Price * OD.Quantity) TotalAmount FROM OrderDetails OD
                            JOIN Products P ON P.ProductID = OD.ProductID
                            WHERE OrderID = ?
                            GROUP BY OD.OrderID"""
                cursor.execute(query, (order_id,))
                total_amount = cursor.fetchone()[1]
                print("Total Amount: $",total_amount)
                discounted_amount = total_amount - total_amount*0.10
                print("Discount of 10 percent will be added...")
                print("Total Amount: $", discounted_amount)
            except Exception as e:
                conn.commit()
                raise e
            finally:
                cursor.close()
                conn.close()
        if choice == 1:
            ProcessPayment()
        elif choice == 2:
            AddDiscount()
        else:
            print('Invalid choice. Try again')
            return

    def SearchOrRecommendProduct(self, choice):
        
        def SearchProduct():
            product_id = input('Enter a product id: ')
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM Products WHERE ProductID = ?", (product_id,))
                rows = cursor.fetchone()
                if rows:
                    print('Product Found!\n')
                    print('Product ID: ', rows[0])
                    print('Product Name: ', rows[1])
                    print('Product Description: ', rows[2])
                    print('Product Price: ', rows[3])
                    print('Product Category: ', rows[4])
                else:
                    print('Product Not Found\n')
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()
        
        def RecommendProduct():
            product_id = input('Enter a product id: ')
            try:
                conn = DBUtil.getDBConn()
                cursor = conn.cursor()
                cursor.execute("SELECT Category FROM Products WHERE ProductID = ?",(product_id,))
                category = cursor.fetchone()[0]
                cursor.execute("SELECT * FROM Products WHERE Category = ?",(category,))
                recommended_products = cursor.fetchall()

                if recommended_products:
                    print('Here are the recommeded products: \n')
                    for product in recommended_products:
                        print(product[1])
                else:
                    print('No recommendations')
            except Exception as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()
                conn.close()


        if choice == 1:
            SearchProduct()
        elif choice == 2:
            RecommendProduct()
        else:
            print('Invalid choice. try again')
            return