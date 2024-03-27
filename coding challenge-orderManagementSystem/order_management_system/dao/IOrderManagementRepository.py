import sys
import os

# Add parent directory of 'dao' to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



from abc import ABC, abstractmethod
from entity.model import User, Product
from datetime import date

class IOrderManagementRepository(ABC):
    @abstractmethod
    def createOrder(self, user: User,order_id, product_id: int, quantity: int, order_date: date) -> None:
        """Create an order for a given user with a specified product."""
        pass
    
    @abstractmethod
    def cancelOrder(self, userId: int, orderId: int) -> None:
        """Cancel an order for a given user and order ID."""
        pass
    
    @abstractmethod
    def createProduct(self, user: User, product: Product) -> None:
        """Create a product for a given user."""
        pass
    
    @abstractmethod
    def createUser(self, user: User) -> None:
        """Create a new user."""
        pass
    
    @abstractmethod
    def getAllProducts(self) -> list[Product]:
        """Retrieve all products from the database."""
        pass
    
    @abstractmethod
    def getOrderByUser(self, user: User) -> list[Product]:
        """Retrieve all products ordered by a specific user."""
        pass
    
    @abstractmethod
    def getUserByUsernameAndPassword(self, username, password):
        """ Gets the user by name and password."""