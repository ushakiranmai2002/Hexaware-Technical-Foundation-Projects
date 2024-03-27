import sys
import os

# Add parent directory of 'dao' to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from entity.model import *
from datetime import date
from dao.ICarLeaseRepository import ICarLeaseRepository
from exceptions.custom_exceptions import * 
from util.DBConnUtil import *
from util.DBPropertyUtil import PropertyUtil

class ICarLeaseRepositoryImpl(ICarLeaseRepository):
   
   def __init__(self) -> None:
       
       self.conn=DBConnection.getConnection()
       self.cursor=self.conn.cursor()
       
   
   def add_car(self, Vehicle: Vehicle) -> None:
        

        try:
            self.cursor.execute("""
                INSERT INTO Vehicle (carID, make, model, Year, dailyRate, available, passengerCapacity, engineCapacity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (Vehicle.get_vehicle_id(), Vehicle.get_make(),Vehicle.get_model(), Vehicle.get_year(), Vehicle.get_daily_rate(), Vehicle.get_available(),Vehicle.get_passenger_capacity(), Vehicle.get_engine_capacity()))
            
            self.conn.commit()
            print("Vehicle added successfully")
        except Exception as e:
            self.conn.rollback()
            print(str(e))
            print("Some error occured and your connection is roll backed.")
        
        finally:
          
           print("Select the option from below:")
            
        
            

   def remove_car(self, vehicle_id: int) -> None:
        
        try:
            self.cursor.execute("""
                DELETE FROM Vehicle
                WHERE carID = ?
            """, (vehicle_id))

            if self.cursor.rowcount == 0:
                raise CarNotFoundException(vehicle_id)

            self.conn.commit()
            print("Vehicle removed successfully")

        except CarNotFoundException as e:
            print(e)

        except Exception as e:
            self. conn.rollback()
            print(str(e))
            print("Some error occured and your connection is roll backed.")
        finally:
          
           print("Select the option from below:")

   def list_available_cars(self) -> list[Vehicle]:
       try:
           
           self.cursor.execute("""
                    SELECT * FROM Vehicle
                    WHERE available = 1
                """)
           available_cars = []
           for row in self.cursor.fetchall():
                    vehicle_id, make, model, year, daily_rate, status, passenger_capacity, engine_capacity = row
                    vehicle = Vehicle(vehicle_id, make, model, year, daily_rate, status, passenger_capacity, engine_capacity)
                    available_cars.append(vehicle)

           return available_cars

           
       except Exception as e:
                print("Error occurred while fetching available cars.")
                print(e)  # Print the exception for debugging purposes
                return []
    
   def list_rented_cars(self) -> list[Vehicle]:
        
        try:
             self.cursor.execute("""
                    SELECT * FROM Vehicle
                    WHERE available <> 1
                """)
             rented_cars = []
             for row in self.cursor.fetchall():
                    vehicle_id, make, model, year, daily_rate, status, passenger_capacity, engine_capacity = row
                    vehicle = Vehicle(vehicle_id, make, model, year, daily_rate, status, passenger_capacity, engine_capacity)
                    rented_cars.append(vehicle)

             return rented_cars

           
        except Exception as e:
                
                print("Error occurred while fetching available cars.")
                print(e)  # Print the exception for debugging purposes
                return []
        

   def find_car_by_id(self, Vehicle_id: int) -> Vehicle:
    try:
        self.cursor.execute("""
            SELECT * FROM Vehicle
            WHERE carID = (?)
        """, (Vehicle_id,))
        
        if self.cursor.rowcount == 0:
            # No rows were returned by the query, raise CarNotFoundException
            raise CarNotFoundException(Vehicle_id)
        
        else:
            # Fetch the row and create a Vehicle object
            row = self.cursor.fetchone()
            vehicle_id, make, model, year, daily_rate, status, passenger_capacity, engine_capacity = row
            return Vehicle(vehicle_id, make, model, year, daily_rate, status, passenger_capacity, engine_capacity)
            
    except CarNotFoundException as e:
        # Handle CarNotFoundException
        print(e)
        
    except Exception as e:
        # Handle other exceptions
        print("Error occurred while fetching car details.")
        print(e)  # Print the exception for debugging purposes
        return None

             
   def add_customer(self, customer: Customer) -> None:
        try:
              self.cursor.execute("""
                    INSERT INTO Customer(customerID,firstName, lastName, email, phoneNumber)
                    VALUES (?, ?, ?, ?, ?)
                """, (customer.get_customer_id(),customer.get_first_name(),customer.get_last_name(),customer.get_email(),customer.get_phone_number()))

              self.conn.commit()
              print("Customer added successfully")
        except Exception as e:
                self.conn.rollback()
                print("Some error occurred and your connection is rolled back.")
                print(e)  # Print the exception for debugging purposes


   def remove_customer(self, customer_id: int) -> None:
        
        try:
            self.cursor.execute("""
                DELETE FROM Customer
                WHERE customerID = ?
            """, (customer_id))

            if self.cursor.rowcount == 0:
                raise CustomerNotFoundException(customer_id)

            self.conn.commit()
            print("Customer removed successfully")

        except CustomerNotFoundException as e:
            print(e)

        except Exception as e:
            self. conn.rollback()
            print(str(e))
            print("Some error occured and your connection is roll backed.")

   def list_customers(self) -> list[Customer]:

        try:
            self.cursor.execute("""
                    SELECT * FROM Customer
                """)

            customers = []
            for row in self.cursor.fetchall():
                    customer_id, first_name, last_name, email, phone_number = row
                    customer = Customer(customer_id, first_name, last_name, email, phone_number)
                    customers.append(customer)

            return customers
        except Exception as e:
                print("Error occurred while fetching customer details.")
                print(e)  # Print the exception for debugging purposes
                return []
        
   def find_customer_by_id(self, customer_id: int) -> Customer:
        
        try:
            self.cursor.execute("""
                    SELECT * FROM customer
                    WHERE customerID = ?
                """, (customer_id))
                
            if self.cursor.rowcount == 0:
                raise CustomerNotFoundException(customer_id)
            
            else:

                row = self.cursor.fetchone()
                customer_id, first_name, last_name, email, phone_number = row
                return Customer(customer_id, first_name, last_name, email, phone_number)
                
        except CustomerNotFoundException as e:
            print(e)

        except Exception as e:
                print("Error occurred while fetching car details.")
                print(e)  # Print the exception for debugging purposes
                return None
             
   def create_lease(self, lease:Lease) -> Lease:
        try:
            self.cursor.execute("""
                    INSERT INTO Lease (leaseID, vehicleID, customerID, startDate, endDate,type)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (lease.get_lease_id(),lease.get_vehicle_id(),lease.get_customer_id(),lease.get_start_date(),lease.get_end_date(),lease.get_type()))

            self.conn.commit()
            print("Lease created successfully")
        except Exception as e:
            self.conn.rollback()
            print("Some error occurred and your connection is rolled back.")
            print(e)  # Print the exception for debugging purposes

   def return_car(self, lease_id: int) -> Lease:
        try:
            self.cursor.execute("""
                SELECT * FROM Lease
                WHERE leaseID = ?
            """, (lease_id,))
            
            row = self.cursor.fetchone()
            
            if row is None:
                raise LeaseNotFoundException(lease_id)
            
            return row

        except LeaseNotFoundException as e:
            print(e)

        except Exception as e:
            self.conn.rollback()
            print("Error occurred while fetching Lease details.")
            print(e)  # Print the exception for debugging purposes
            return None
             
   def list_active_leases(self) -> list[Lease]:
        try:
             today = date.today()
                # Execute SQL query to fetch active leases
             self.cursor.execute("""
                    SELECT * FROM Lease
                    WHERE startDate = ? 
                """, ("2023-04-01"))
             row=self.cursor.fetchall()
             return row
        except Exception as e:
            self.conn.rollback()
            print("Some error occurred and your connection is rolled back.")
            print(e)
             
   def list_lease_history(self) -> list[Lease]:
        try:
            # Execute SQL query to fetch lease history
            self.cursor.execute("""
                    SELECT * FROM Lease
                """) 
            rows = self.cursor.fetchall()
            return rows
        except Exception as e:
            self.conn.rollback()
            print("Some error occurred and your connection is rolled back.")
            print(e)

   def record_payment(self, payment:Payment) -> None:
        try:
            # Execute SQL query to insert payment details into the database
            self.cursor.execute("""
                    INSERT INTO Payment (paymentID, leaseID, TransactionDate, amount)
                    VALUES (?, ?, ?, ?)
                """, (payment.get_payment_id(),payment.get_lease_id(),payment.get_payment_date(),payment.get_amount()))

                # Commit the transaction
            self.conn.commit()

            print("Payment recorded successfully.")

        except Exception as e:
                # Rollback the transaction in case of any error
                self.conn.rollback()
                print("Error occurred while recording payment.")
                print(e)  # Print the exception for debugging purposes

             
   def closeconn(self):
        if hasattr(self,'cursor'):
             self.cursor.close()
        if hasattr(self,'conn'):
             self.conn.close()
        print("Connection closed...")


