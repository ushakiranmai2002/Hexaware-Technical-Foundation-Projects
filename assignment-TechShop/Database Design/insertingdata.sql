
use techShop;
-- Insert 15 sample records into Customers table
INSERT INTO Customers (FirstName, LastName, Email, Phone, Address)
VALUES
    ('John', 'Doe', 'john.doe@example.com', '123-456-7890', '123 Main St, Anytown, USA'),
    ('Jane', 'Smith', 'jane.smith@example.com', '456-789-0123', '456 Elm St, Anycity, USA'),
    ('Michael', 'Johnson', 'michael.johnson@example.com', '789-012-3456', '789 Oak St, Anystate, USA'),
    ('Emily', 'Brown', 'emily.brown@example.com', '321-654-9870', '321 Maple St, Anyvillage, USA'),
    ('Daniel', 'Martinez', 'daniel.martinez@example.com', '654-987-0123', '654 Cedar St, Anysuburb, USA'),
    ('Sarah', 'Wilson', 'sarah.wilson@example.com', '987-012-3456', '987 Pine St, Anyhamlet, USA'),
    ('David', 'Taylor', 'david.taylor@example.com', '111-222-3333', '111 Oak St, Anycity, USA'),
    ('Olivia', 'Anderson', 'olivia.anderson@example.com', '444-555-6666', '444 Elm St, Anystate, USA'),
    ('James', 'Hernandez', 'james.hernandez@example.com', '777-888-9999', '777 Maple St, Anytown, USA'),
    ('Emma', 'Garcia', 'emma.garcia@example.com', '000-111-2222', '000 Cedar St, Anyvillage, USA'),
    ('Ava', 'Lopez', 'ava.lopez@example.com', '333-444-5555', '333 Pine St, Anysuburb, USA'),
    ('Alexander', 'Martinez', 'alexander.martinez@example.com', '666-777-8888', '666 Oak St, Anyhamlet, USA'),
    ('Sophia', 'Gonzalez', 'sophia.gonzalez@example.com', '999-000-1111', '999 Elm St, Anytown, USA'),
    ('Mia', 'Perez', 'mia.perez@example.com', '222-333-4444', '222 Maple St, Anycity, USA'),
    ('Logan', 'Rodriguez', 'logan.rodriguez@example.com', '555-666-7777', '555 Cedar St, Anystate, USA');


	-- Insert 15 sample records into Products table
INSERT INTO Products (ProductID, ProductName, Description, Price)
VALUES
    (1, 'Smartphone', 'Smartphone with high-resolution camera', 599.99),
    (2, 'Laptop', 'Thin and lightweight laptop with SSD storage', 999.99),
    (3, 'Headphones', 'Wireless noise-canceling headphones', 199.99),
    (4, 'Smart Watch', 'Fitness tracker with heart rate monitor', 149.99),
    (5, 'Tablet', '10-inch tablet with retina display', 399.99),
    (6, 'Digital Camera', 'Mirrorless digital camera with 4K video recording', 799.99),
    (7, 'Gaming Console', 'Next-gen gaming console with VR support', 499.99),
    (8, 'Bluetooth Speaker', 'Portable Bluetooth speaker with long battery life', 79.99),
    (9, 'External Hard Drive', '1TB external hard drive with USB 3.0', 69.99),
    (10, 'Wireless Router', 'Dual-band wireless router for high-speed internet', 129.99),
    (11, 'Fitness Tracker', 'Waterproof fitness tracker with GPS', 129.99),
    (12, 'Smart Home Hub', 'Voice-controlled smart home hub', 149.99),
    (13, 'Wireless Earbuds', 'True wireless earbuds with touch controls', 129.99),
    (14, 'Monitor', '27-inch 4K monitor with IPS display', 399.99),
    (15, 'Printer', 'All-in-one printer with wireless connectivity', 199.99);

	INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
    (1, 1, '2024-02-01', 249.99),
    (2, 3, '2024-02-03', 799.99),
    (3, 5, '2024-02-05', 149.99),
    (4, 2, '2024-02-07', 399.99),
    (5, 4, '2024-02-10', 999.99),
    (6, 6, '2024-02-12', 79.99),
    (7, 8, '2024-02-15', 129.99),
    (8, 10, '2024-02-18', 499.99),
    (9, 12, '2024-02-20', 129.99),
    (10, 14, '2024-02-22', 69.99),
    (11, 7, '2024-02-25', 149.99),
    (12, 9, '2024-02-28', 129.99),
    (13, 11, '2024-03-01', 399.99),
    (14, 13, '2024-03-03', 199.99),
    (15, 15, '2024-03-05', 999.99);

	INSERT INTO Orders (OrderID, CustomerID, OrderDate, TotalAmount)
VALUES
	(16, 1, '2024-03-08', 329.99),
    (17, 3, '2024-03-10', 699.99),
    (18, 5, '2024-03-12', 199.99),
    (19, 2, '2024-03-15', 449.99),
    (20, 4, '2024-03-18', 1299.99),
    (21, 6, '2024-03-20', 89.99),
    (22, 8, '2024-03-22', 149.99),
    (23, 10, '2024-03-25', 599.99),
    (24, 12, '2024-03-28', 179.99),
    (25, 14, '2024-03-30', 79.99),
    (26, 7, '2024-04-01', 199.99),
    (27, 9, '2024-04-03', 169.99),
    (28, 11, '2024-04-05', 499.99),
    (29, 13, '2024-04-08', 249.99),
    (30, 15, '2024-04-10', 1199.99),
    (31, 1, '2024-04-12', 359.99),
    (32, 3, '2024-04-15', 799.99),
    (33, 5, '2024-04-18', 249.99),
    (34, 2, '2024-04-20', 499.99),
    (35, 4, '2024-04-22', 1399.99);

-- Insert 35 sample records into OrderDetails table
INSERT INTO OrderDetails (OrderDetailID, OrderID, ProductID, Quantity) VALUES
(1, 1, 3, 2),
(2, 2, 7, 3),
(3, 3, 2, 1),
(4, 4, 10, 5),
(5, 5, 14, 2),
(6, 6, 5, 3),
(7, 7, 15, 4),
(8, 8, 8, 1),
(9, 9, 4, 3),
(10, 10, 1, 2),
(11, 11, 13, 1),
(12, 12, 9, 2),
(13, 13, 6, 3),
(14, 14, 11, 4),
(15, 15, 15, 1),
(16, 16, 3, 2),
(17, 17, 7, 3),
(18, 18, 2, 1),
(19, 19, 10, 5),
(20, 20, 14, 2),
(21, 21, 5, 3),
(22, 22, 15, 4),
(23, 23, 8, 1),
(24, 24, 4, 3),
(25, 25, 1, 2),
(26, 26, 13, 1),
(27, 27, 9, 2),
(28, 28, 6, 3),
(29, 29, 11, 4),
(30, 30, 15, 1),
(31, 31, 3, 2),
(32, 32, 7, 3),
(33, 33, 2, 1),
(34, 34, 10, 5),
(35, 35, 14, 2);


	-- Insert 15 sample records into Inventory table
INSERT INTO Inventory (InventoryID, ProductID, QuantityInStock, LastStockUpdate)
VALUES
    (1, 1, 50, '2024-02-01'),
    (2, 2, 30, '2024-02-01'),
    (3, 3, 80, '2024-02-01'),
    (4, 4, 20, '2024-02-01'),
    (5, 5, 60, '2024-02-01'),
    (6, 6, 40, '2024-02-01'),
    (7, 7, 25, '2024-02-01'),
    (8, 8, 70, '2024-02-01'),
    (9, 9, 55, '2024-02-01'),
    (10, 10, 45, '2024-02-01'),
    (11, 11, 35, '2024-02-01'),
    (12, 12, 65, '2024-02-01'),
    (13, 13, 75, '2024-02-01'),
    (14, 14, 15, '2024-02-01'),
    (15, 15, 10, '2024-02-01');



	--displaying the data

	select * from customers;
	select * from products;
	select * from orders;
	select * from orderdetails;
	select * from inventory;
	
	