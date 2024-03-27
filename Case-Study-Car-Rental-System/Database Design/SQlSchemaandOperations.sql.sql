create database challenges;
use challenges;

CREATE TABLE Vehicle (
    carID INT constraint V_PK PRIMARY KEY,
    make VARCHAR(255),
    model VARCHAR(255),
    Year INT,
    dailyRate DECIMAL(10, 2),
    available BIT,
    passengerCapacity INT,
    engineCapacity INT
);

INSERT INTO Vehicle (carID, make, model, Year, dailyRate, available, passengerCapacity, engineCapacity) 
VALUES
(1, 'Toyota', 'Camry', 2022, 50.00, 1, 4, 1450),
(2, 'Honda', 'Civic', 2023, 45.00, 1, 7, 1500),
(3, 'Ford', 'Focus', 2022, 48.00, 0, 4, 1400),
(4, 'Nissan', 'Altima', 2023, 52.00, 1, 7, 1200),
(5, 'Chevrolet', 'Malibu', 2022, 47.00, 1, 4, 1800),
(6, 'Hyundai', 'Sonata', 2023, 49.00, 0, 7, 1400),
(7, 'BMW', '3 Series', 2023, 60.00, 1, 7, 2499),
(8, 'Mercedes', 'C-Class', 2022, 58.00, 1, 8, 2599),
(9, 'Audi', 'A4', 2022, 55.00, 0, 4, 2500),
(10, 'Lexus', 'ES', 2023, 54.00, 1, 4, 2500);



CREATE TABLE Customer (
    customerID INT constraint C_PK PRIMARY KEY,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    email VARCHAR(100),
    phoneNumber VARCHAR(20)
);

INSERT INTO Customer (customerID, firstName, lastName, email, phoneNumber)
VALUES
(1, 'John', 'Doe', 'johndoe@example.com', '555-555-5555'),
(2, 'Jane', 'Smith', 'janesmith@example.com', '555-123-4567'),
(3, 'Robert', 'Johnson', 'robert@example.com', '555-789-1234'),
(4, 'Sarah', 'Brown', 'sarah@example.com', '555-456-7890'),
(5, 'David', 'Lee', 'david@example.com', '555-987-6543'),
(6, 'Laura', 'Hall', 'laura@example.com', '555-234-5678'),
(7, 'Michael', 'Davis', 'michael@example.com', '555-876-5432'),
(8, 'Emma', 'Wilson', 'emma@example.com', '555-432-1098'),
(9, 'William', 'Taylor', 'william@example.com', '555-321-6547'),
(10, 'Olivia', 'Adams', 'olivia@example.com', '555-765-4321');

Create TABLE Lease (
    leaseID INT constraint L_PK PRIMARY KEY,
    vehicleID INT constraint LV_FK FOREIGN KEY REFERENCES Vehicle(carID), 
    customerID INT  constraint LC_FK FOREIGN KEY REFERENCES Customer(customerID),
    startDate DATE,
    endDate DATE,
    type VARCHAR(20),
);

INSERT INTO Lease (leaseID, vehicleID, customerID, startDate, endDate, type)
VALUES 
(1, 1, 1, '2023-01-01', '2023-01-05', 'Daily'),
(2, 2, 2, '2023-02-15', '2023-02-28', 'Monthly'),
(3, 3, 3, '2023-03-10', '2023-03-15', 'Daily'),
(4, 4, 4, '2023-04-20', '2023-04-30', 'Monthly'),
(5, 5, 5, '2023-05-05', '2023-05-10', 'Daily'),
(6, 4, 3, '2023-06-15', '2023-06-30', 'Monthly'),
(7, 7, 7, '2023-07-01', '2023-07-10', 'Daily'),
(8, 8, 8, '2023-08-12', '2023-08-15', 'Monthly'),
(9, 3, 3, '2023-09-07', '2023-09-10', 'Daily'),
(10, 10, 10, '2023-10-10', '2023-10-31', 'Monthly');

create table Payment(
paymentID int constraint PAY_PK Primary key,
leaseID int constraint PL_FK foreign key references Lease(leaseID),
paymentDate date,
amount decimal(10,2)
);


insert into Payment (paymentID,leaseID,paymentDate,amount)
values
(1, 1, '2023-01-03', 200.00),
(2, 2, '2023-02-20', 1000.00),
(3, 3, '2023-03-12', 75.00),
(4, 4, '2023-04-25', 900.00),
(5, 5, '2023-05-07', 60.00),
(6, 6, '2023-06-18', 1200.00),
(7, 7, '2023-07-03', 40.00),
(8, 8, '2023-08-14', 1100.00),
(9, 9, '2023-09-09', 80.00),
(10, 10, '2023-10-25', 1500.00);

/*1. Update the daily rate for a Mercedes car to 68*/
update Vehicle
set dailyRate=68.00
where make='Mercedes';
SELECT * FROM VEHICLE;
/*2. Delete a specific customer and all associated leases and payments*/
declare @custId int=3
delete from Payment where leaseID in(select leaseId from lease where customerID=@custId);
delete  from lease where customerID=@custId;
delete from customer where customerID=@custId;

/*3.Rename the "paymentDate" column in the Payment table to "transactionDate"*/
exec sp_rename 'Payment.paymentDate','TransactionDate','column';

/*4. Find a specific customer by email*/
select concat(firstName,' ',lastName) as FUllName from Customer where email='johndoe@example.com';

/*5. Get active leases for a specific customer.*/
select * from lease where customerID=4;

/*6. Find all payments made by a customer with a specific phone number*/
select amount from payment where leaseId=(select leaseId from Lease where customerID=(select customerID from Customer where phoneNumber='555-555-5555'));

/*7. Calculate the average daily rate of all available cars.*/

select round(avg(dailyrate),2) as avgDailyRate from vehicle where available=1;

/*8. Find the car with the highest daily rate.*/
select CONCAT(make,'of model ',model,'has the highest daily rate') as carDetails from Vehicle where dailyRate=(select max(dailyRate) from Vehicle);

/*9. Retrieve all cars leased by a specific customer.*/
select concat(make,model) CarModel from Vehicle where carId in (select vehicleID from Lease where customerID=4);

/*10. Find the details of the most recent lease*/
select top 1 * from lease
order by startdate desc;

/*11. List all payments made in the year 2023.*/
select amount,TransactionDate from Payment where year(TransactionDate)=2023;

/*12. Retrieve customers who have not made any payments.*/
select concat(firstname,' ',lastname)as Customer from Customer where customerId not in (select customerID from lease);

/*13. Retrieve Car Details and Their Total Payments.*/
 
 SELECT
    V.carID,
    V.make,
    V.model,
    V.year,
    SUM(P.amount) AS totalPayments
FROM
    Vehicle V
LEFT JOIN
    Lease L ON V.carID = L.vehicleID
LEFT JOIN
    Payment P ON L.leaseID = P.leaseID
GROUP BY
    V.carID,
	V.make,
	V.model,
	V.year;

/*14. Calculate Total Payments for Each Customer.*/

select 
   C.FirstName,
   sum(P.amount) AS Total
   from 
   Customer C
   left join
	Lease L on C.customerID=L.customerID
  left join
   Payment P on P.leaseID=L.leaseID
   group by
   C.FirstName;

/*15. List Car Details for Each Lease.*/
select CONCAT(make,' ',model,' ',dailyRate,' ',passengerCapacity,' ',engineCapacity) as cardetails from Vehicle where carID in(select vehicleID from Lease);

select make, model, dailyRate, passengerCapacity, engineCapacity as cardetails from Vehicle where carID in(select vehicleID from Lease);

/*16. Retrieve Details of Active Leases with Customer and Car Information*/

select v.make,v.model,v.year, CONCAT(c.firstName,' ',c.lastname) as customer, c.phoneNumber
from lease l join Vehicle v on l.vehicleID=v.carID
join customer c on l.customerID=c.customerID;

/*17. Find the Customer Who Has Spent the Most on Leases.*/

select top 1 CONCAT(c.firstname,' ',c.lastname) as customer,sum(p.amount) as amountSpent from
customer c join lease l on c.customerID=l.customerID
join Payment p on p.leaseId=l.leaseID
group by c.firstName,c.lastName
order by amountSpent desc;

/*18. List All Cars with Their Current Lease Information.*/

select v.make,v.model,l.startdate,l.enddate,l.type
from vehicle v join lease l on
l.vehicleId=v.carid;
