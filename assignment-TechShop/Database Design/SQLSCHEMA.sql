create database TechShop;
use TechShop;

/* Creating Tables*/

/*1. Customers:
• CustomerID (Primary Key)
• FirstName
• LastName
• Email
• Phone
• Address*/

create table Customers(
CustomerId int Identity constraint C_PK Primary Key,
FirstName varchar(45) not null,
LastName varchar(40),
email varchar(65) not null,
phone varchar(20),
Address varchar(80) not null);

/*. Products:
• ProductID (Primary Key)
• ProductName
• Description
• Price
*/

CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName VARCHAR(100),
    Description VARCHAR(MAX),
    Price DECIMAL(10, 2)
);

/*
Orders:
• OrderID (Primary Key)
• CustomerID (Foreign Key referencing Customers)
• OrderDate
• TotalAmount*/


CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID),
    OrderDate DATE,
    TotalAmount DECIMAL(10, 5)
);

/*OrderDetails:
• OrderDetailID (Primary Key)
• OrderID (Foreign Key referencing Orders)
• ProductID (Foreign Key referencing Products)
• Quantity*/

	CREATE TABLE OrderDetails (
    OrderDetailID INT PRIMARY KEY,
    OrderID INT,
    ProductID INT,
    Quantity INT,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);


/*Inventory
• InventoryID (Primary Key)
• ProductID (Foreign Key referencing Products)
• QuantityInStock
• LastStockUpdate*/


	CREATE TABLE Inventory (
    InventoryID INT PRIMARY KEY,
    ProductID INT,
    QuantityInStock INT,
    LastStockUpdate DATE,
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);
