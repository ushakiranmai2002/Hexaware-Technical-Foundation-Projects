class CarNotFoundException(Exception):
    def __init__(self, car_id):
        super().__init__(f"Car with ID {car_id} not found in the database.")
        self.car_id = car_id

class LeaseNotFoundException(Exception):
    def __init__(self, lease_id):
        super().__init__(f"Lease with ID {lease_id} not found in the database.")
        self.lease_id = lease_id

class CustomerNotFoundException(Exception):
    def __init__(self, customer_id):
        super().__init__(f"Customer with ID {customer_id} not found in the database.")
        self.customer_id = customer_id
