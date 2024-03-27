/*TASK-2*/

/*1.Write an SQL query to retrieve the names and emails of all customers. */
select concat(FirstName,' ',LastName) as FullName ,email from  Customers;

/*2.Write an SQL query to list all orders with their order dates and corresponding customer names.*/

select OrderId,Orderdate,CONCAT(FirstName,' ',LastName) as CustomerName from Customers,Orders where orders.CustomerID=customers.customerID; 

/*3.Write an SQL query to insert a new customer record into the "Customers" table. Include customer information such as name, email, and address*/
insert into Customers (FirstName,LastName,email,Address)
values('Usha','Kiranmai','ushakiranmai2002@example.com', '123 Main Street');
select * from Customers;

/*4.Write an SQL query to update the prices of all electronic gadgets in the "Products" table by increasing them by 10%.*/
update Products
set price=price+price*10/100;
select * from products;

/*5. Write an SQL query to delete a specific order and its associated order details from the
"Orders" and "OrderDetails" tables. Allow users to input the order ID as a parameter.*/

CREATE PROCEDURE DeleteOrderByOrderID
	@OrderID INT
AS
BEGIN 
	DELETE FROM OrderDetails
	WHERE OrderID = @OrderID
	DELETE FROM Orders
	WHERE OrderID = @OrderID
END;
EXEC DeleteOrderByOrderID @OrderID = 15;

/*6.Write an SQL query to insert a new order into the "Orders" table. Include the customer ID,
order date, and any other necessary information.*/
insert into Orders values(36,11,'2024-03-24', 1111.24000);
insert into orderdetails values(36,36,5,3);
select * from orders;

/*7. Write an SQL query to update the contact information (e.g., email and address) of a specific
customer in the "Customers" table. Allow users to input the customer ID and new contact
information.*/

CREATE PROCEDURE UpdateInfo
@CustomerID INT, @NewEmail VARCHAR(50),
@NewAddress VARCHAR(100)
AS
BEGIN
	UPDATE Customers
	SET Email = @NewEmail
	WHERE CustomerID = @CustomerID
	UPDATE Customers
	SET Address = @NewAddress
	WHERE CustomerID = @CustomerID
END;
EXEC UpdateInfo 
	@CustomerID = 16, 
	@NewEmail = 'ushakiranmai2002@gmail.com', 
	@NewAddress = 'Vijayawada, AP';
select * from Customers;

/*8. Write an SQL query to recalculate and update the total cost of each order in the "Orders"
table based on the prices and quantities in the "OrderDetails" table.*/

UPDATE Orders
SET TotalAmount = (
    SELECT (Quantity * Products.Price)
    FROM OrderDetails
    JOIN Products ON OrderDetails.ProductID = Products.ProductID
    WHERE OrderDetails.OrderID = Orders.OrderID);
select * from orders;

/*9. Write an SQL query to delete all orders and their associated order details for a specific
customer from the "Orders" and "OrderDetails" tables. Allow users to input the customer ID
as a parameter.*/

CREATE PROCEDURE DeleteOrders
@CusID INT
AS
BEGIN
	DELETE FROM OrderDetails
	WHERE OrderID IN(
		SELECT OrderID FROM Orders 
		WHERE CustomerID = @CusID)
	DELETE FROM Orders
	WHERE CustomerID = @CusID
END;
EXEC DeleteOrders @CusID = 14;


/*10. Write an SQL query to insert a new electronic gadget product into the "Products" table,
including product name, category, price, and any other relevant details.*/
insert into Products values(16,'Keyboard','Gamming Keyboard of 7 colors,wired,Circle Brand',1500.50);
select * from Products;

/*11. Write an SQL query to update the status of a specific order in the "Orders" table (e.g., from
"Pending" to "Shipped"). Allow users to input the order ID and the new status.*/

ALTER TABLE Orders
ADD Status VARCHAR(15);

UPDATE Orders
SET Status='Pending';

DECLARE @OID INT = 1
UPDATE Orders
SET Status='Shipped'
WHERE OrderID = @OID;
select * from orders;

/*12. Write an SQL query to calculate and update the number of orders placed by each customer
in the "Customers" table based on the data in the "Orders" table.*/
alter table Customers
add NoOfOrders int;
update Customers
set NoOfOrders=(
select count(ORderID)
from Orders
where ORders.CustomerID=Customers.CustomerId);
select * from Customers;