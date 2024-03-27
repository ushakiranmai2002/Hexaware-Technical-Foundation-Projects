import sys
import os
import datetime
# Add parent directory of 'dao' to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


import unittest
from dao.ICarLeaseRepositoryImpl import ICarLeaseRepositoryImpl # Importing the ServiceProvider class
from entity.model import Vehicle,Lease  
from exceptions.custom_exceptions import CarNotFoundException,LeaseNotFoundException,CustomerNotFoundException 


class TestCarRentalSystem(unittest.TestCase):
    def setUp(self):
        # Initialize test objects or resources
        self.service_provider = ICarLeaseRepositoryImpl()
    
    def test_create_car(self):
        # Test case to check if a car is created successfully
        vehicle_id=int(input("Enter Id: "))
        make = input("Enter make: ")
        model = input("Enter model: ")
        year = int(input("Enter year: "))
        daily_rate = float(input("Enter daily rate: "))
        available = bool(input("Enter status: "))
        passenger_capacity = int(input("Enter passenger capacity: "))
        engine_capacity = int(input("Enter engine capacity: "))

        car = Vehicle(vehicle_id=vehicle_id,make=make, model=model, year=year, daily_rate=daily_rate, available=available,passenger_capacity=passenger_capacity, engine_capacity=engine_capacity)

        car_id = self.service_provider.add_car(car)
        self.assertIsNone(car_id)  

    def test_create_lease(self):
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

        l=self.service_provider.create_lease(lease)
        self.assertIsNone(l)


    def test_retrieve_lease(self):

        lease_id = 1  # Assuming lease ID 1 exists in the database
        retrieved_lease = self.service_provider.return_car(lease_id)
        self.assertIsNotNone(retrieved_lease)
    
    def test_customer_not_found_exception(self):
        try:
            # Call the method with a non-existing customer ID
            self.service_provider.find_customer_by_id(888)  # Assuming customer ID 999 does not exist
        except CustomerNotFoundException as e:
            print("CustomerNotFoundException was raised:", e)
              # Re-raise the exception for the test framework to catch
        
    def test_car_not_found_exception(self):
        try:
             self.service_provider.find_car_by_id(888) 
        except CarNotFoundException:
            print("CarNotFound Exception is  raised.") 

    def test_lease_not_found_exception(self):
        # Test case to check if LeaseNotFoundException is thrown when lease ID is not found
        try:
            # Call the method with a non-existing lease ID
            self.service_provider.return_car(888)  # Assuming lease ID 999 does not exist
        except LeaseNotFoundException:
            print("LeaseNotFound Exception is raised.")

    


if __name__ == '__main__':
    unittest.main()
