import sys
import os

# Add parent directory of 'dao' to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from datetime import datetime
from entity.model import Vehicle, Customer, Lease, Payment
from dao import ICarLeaseRepositoryImpl
from exceptions.custom_exceptions import CarNotFoundException, CustomerNotFoundException, LeaseNotFoundException


class CarLeaseMenu:
    def __init__(self):
        self.repoimpl = ICarLeaseRepositoryImpl.ICarLeaseRepositoryImpl()

    def display_menu(self):
        print("Car Lease System Menu:")
        print("1. Add a new car")
        print("2. Remove a car")
        print("3. List available cars")
        print("4. List rented cars")
        print("5. Find car by ID")
        print("6. Add a new customer")
        print("7. Remove a customer")
        print("8. List customers")
        print("9. Find customer by ID")
        print("10. Create a lease")
        print("11. Return a leased car")
        print("12. List active leases")
        print("13. List lease history")
        print("14. Record payment")
        print("15. Exit")

    def run(self):
        while True:
            self.display_menu()
            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_car()
            elif choice == '2':
                self.remove_car()
            elif choice == '3':
                self.list_available_cars()
            elif choice == '4':
                self.list_rented_cars()
            elif choice == '5':
                self.find_car_by_id()
            elif choice == '6':
                self.add_customer()
            elif choice == '7':
                self.remove_customer()
            elif choice == '8':
                self.list_customers()
            elif choice == '9':
                self.find_customer_by_id()
            elif choice == '10':
                self.create_lease()
            elif choice == '11':
                self.return_car()
            elif choice == '12':
                self.list_active_leases()
            elif choice == '13':
                self.list_lease_history()
            elif choice == '14':
                self.record_payment()
            elif choice == '15':
                print("Exiting...")
                self.repoimpl.closeconn()
                break
            else:
                print("Invalid choice. Please try again.")

    def add_car(self):
        vehicle_id=int(input("Enter Id: "))
        make = input("Enter make: ")
        model = input("Enter model: ")
        year = int(input("Enter year: "))
        daily_rate = float(input("Enter daily rate: "))
        available = bool(input("Enter status: "))
        passenger_capacity = int(input("Enter passenger capacity: "))
        engine_capacity = int(input("Enter engine capacity: "))

        vehicle = Vehicle(vehicle_id=vehicle_id,make=make, model=model, year=year, daily_rate=daily_rate, available=available,passenger_capacity=passenger_capacity, engine_capacity=engine_capacity)

        self.repoimpl.add_car(vehicle)

    def remove_car(self):
        Vehicle_id=int(input("Enter Car_id: "))

        self.repoimpl.remove_car(Vehicle_id)

    def list_available_cars(self):
       
       available_cars= self.repoimpl.list_available_cars()
       for car in available_cars:
           
            print("Vehicle ID:", car.get_vehicle_id())
            print("Make:", car.get_make())
            print("Model:", car.get_model())
            print("Year:", car.get_year())
            print("Daily Rate:", car.get_daily_rate())
            print("Available:", car.get_available())
            print("Passenger Capacity:", car.get_passenger_capacity())
            print("Engine Capacity:", car.get_engine_capacity())
            print() 
        

    def list_rented_cars(self):

        rented_cars= self.repoimpl.list_rented_cars()
        for car in rented_cars:
           
            print("Vehicle ID:", car.get_vehicle_id())
            print("Make:", car.get_make())
            print("Model:", car.get_model())
            print("Year:", car.get_year())
            print("Daily Rate:", car.get_daily_rate())
            print("Available:", car.get_available())
            print("Passenger Capacity:", car.get_passenger_capacity())
            print("Engine Capacity:", car.get_engine_capacity())
            print() 
        

    def find_car_by_id(self):
        vehicle_id=int(input("Enter Vehicle_id: "))
        car=self.repoimpl.find_car_by_id(vehicle_id)
        if car:
            print("Vehicle ID:", car.get_vehicle_id())
            print("Make:", car.get_make())
            print("Model:", car.get_model())
            print("Year:", car.get_year())
            print("Daily Rate:", car.get_daily_rate())
            print("Available:", car.get_available())
            print("Passenger Capacity:", car.get_passenger_capacity())
            print("Engine Capacity:", car.get_engine_capacity())
            print()
        

    def add_customer(self):

        customerID=int(input("Enter Customer ID:"))
        fname=input("Enter First Name: ")
        lname=input("Enter Last Name: ")
        email=input("Enter Email: ")
        phn=input("Enter Phone number: ")

        customer=Customer(customerID,fname,lname,email,phn)
        self.repoimpl.add_customer(customer)

    def remove_customer(self):
        customer_id=int(input("Enter Customer_id: "))

        self.repoimpl.remove_customer(customer_id)
        

    def list_customers(self):
        customers = self.repoimpl.list_customers()

        if customers:
            print("List of Customers:")
            for customer in customers:
                print("Customer ID:", customer.get_customer_id())
                print("First Name:", customer.get_first_name())
                print("Last Name:", customer.get_last_name())
                print("Email:", customer.get_email())
                print("Phone Number:", customer.get_phone_number())
                print()  # Add a blank line between each customer
        else:
            print("No customers found.")

    def find_customer_by_id(self):
        customer_id = int(input("Enter the customer ID to find: "))
        customer = self.repoimpl.find_customer_by_id(customer_id)

        if customer:
            print("Customer Found:")
            print("Customer ID:", customer.get_customer_id())
            print("First Name:", customer.get_first_name())
            print("Last Name:", customer.get_last_name())
            print("Email:", customer.get_email())
            print("Phone Number:", customer.get_phone_number())
        

    def create_lease(self):
            lease_id = int(input("Enter lease ID: "))
            customer_id = int(input("Enter customer ID: "))
            vehicle_id = int(input("Enter vehicle ID: "))
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            type=input("Enter Type(Daily/Monthly): ")

            # Convert start_date and end_date strings to datetime objects
            #start_date = datetime.strptime(start_date, "%Y-%m-%d")
            #end_date = datetime.strptime(end_date, "%Y-%m-%d")

            lease=Lease(lease_id,customer_id,vehicle_id,start_date,end_date,type)
            self.repoimpl.create_lease(lease)


    def return_car(self):
        lease_id = int(input("Enter the lease ID to find: "))
        lease = self.repoimpl.return_car(lease_id)

        if lease:
              
            print()
            print("Lease ID:", lease[0])
            print("Customer ID:", lease[1])
            print("Vehicle ID:", lease[2])
            print("Start Date:", lease[3])  # Use strftime to format date
            print("End Date:", lease[4]) 
            print("Type:",lease[5])
            print()
        else:
            print("No lease Found.")

    def list_active_leases(self):
        lease=self.repoimpl.list_active_leases()

        print()
    
        if lease:
           for i in lease:
                      
                print("Lease ID:", i[0])
                print("Customer ID:",i[1])
                print("Vehicle ID:", i[2])
                print("Start Date:", i[3])  
                print("End Date:", i[4])
                print("Type:", i[5])
                print()
            
        else:
            print("No lease Found...")
        

    def list_lease_history(self):
        lease=self.repoimpl.list_lease_history()

        print()
    
        if lease:
           for i in lease:
                      
                print("Lease ID:", i[0])
                print("Customer ID:",i[1])
                print("Vehicle ID:", i[2])
                print("Start Date:", i[3])  
                print("End Date:", i[4])
                print("Type:", i[5])
                print()
            
        else:
            print("No lease Found...")

    def record_payment(self):
           try:
                payment_id = int(input("Enter Payment ID: "))
                lease_id = int(input("Enter Lease ID: "))
                transaction_date = input("Enter Transaction Date (YYYY-MM-DD): ")
                amount = float(input("Enter Payment Amount: "))

                

                # Check if the lease exists in the database
                lease = self.repoimpl.return_car(lease_id)
                if lease:
                    # If lease exists, create payment
                    p=Payment(payment_id, lease_id, transaction_date, amount)
                    # Process payment (insert into database or perform any other necessary action)
                    self.repoimpl.record_payment(p)
                    
                else:
                    # If lease does not exist, print error message
                    print("Invalid Lease ID.")

           except ValueError:
                print("Please enter valid input for Payment ID, Lease ID, and Amount.")
           except Exception as e:
                print("Failed to record payment.")
                print(e) 
            

# Example usage:
if __name__ == "__main__":
    # Assuming repository is an instance of a class implementing ICarLeaseRepository
    menu = CarLeaseMenu()
    menu.run()
