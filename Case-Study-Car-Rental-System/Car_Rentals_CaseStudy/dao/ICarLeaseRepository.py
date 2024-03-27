import sys
import os

# Add parent directory of 'dao' to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from abc import ABC, abstractmethod
from datetime import date
from entity.model import *


class ICarLeaseRepository(ABC):
    @abstractmethod
    def add_car(self, Vehicle: Vehicle) -> None:
        """Add a new car to the repository."""


    @abstractmethod
    def remove_car(self, vehicle_id: int) -> None:
        """Remove a car from the repository."""


    @abstractmethod
    def list_available_cars(self) -> list[Vehicle]:
        """Get a list of all available cars."""


    @abstractmethod
    def list_rented_cars(self) -> list[Vehicle]:
        """Get a list of all rented cars."""


    @abstractmethod
    def find_car_by_id(self, Vehicle_id: int) -> Vehicle:
        """Find a car in the repository by its ID."""


    @abstractmethod
    def add_customer(self, customer: Customer) -> None:
        """Add a new customer to the repository."""


    @abstractmethod
    def remove_customer(self, customer_id: int) -> None:
        """Remove a customer from the repository."""


    @abstractmethod
    def list_customers(self) -> list[Customer]:
        """Get a list of all customers."""


    @abstractmethod
    def find_customer_by_id(self, customer_id: int) -> Customer:
        """Find a customer in the repository by their ID."""


    @abstractmethod
    def create_lease(self, lease:Lease) -> Lease:
        """Create a new lease for a customer with a car."""


    @abstractmethod
    def return_car(self, lease_id: int) -> Lease:
        """Return a leased car."""


    @abstractmethod
    def list_active_leases(self) -> list[Lease]:
        """Get a list of all active leases."""


    @abstractmethod
    def list_lease_history(self) -> list[Lease]:
        """Get a list of all lease history."""


    @abstractmethod
    def record_payment(self, Payment:Payment) -> None:
        """Record a payment for a lease."""
    