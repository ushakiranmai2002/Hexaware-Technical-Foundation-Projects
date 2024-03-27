class UserNotFound(Exception):
    """Exception raised when a user is not found in the database."""

    def _init_(self):
        super()._init_(f"User  not found in the database.")
    
        


class OrderNotFound(Exception):
    def __init__(self, userId, orderId):
        super().__init__(f"Order not found for user ID {userId} and order ID {orderId}")
        self.userId = userId
        self.orderId = orderId


class UnauthorizedAccess(Exception):
    """Exception raised when user is not Authorized."""


    def _init_(self, message="Unauthorized access"):
        super()._init_(self.message)
        self.message = message
        