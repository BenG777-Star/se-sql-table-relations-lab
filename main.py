import sqlite3
import pandas as pd

conn = sqlite3.connect('data.sqlite')

# ==========================================
# Part 1: Join and Filter
# ==========================================

# Question 1
q1 = """
SELECT e.firstName, e.lastName, e.jobTitle
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
WHERE o.city = 'Boston';
"""
print("--- Question 1 ---")
print(pd.read_sql(q1, conn))

# Question 2
q2 = """
SELECT o.officeCode, o.city
FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode
WHERE e.employeeNumber IS NULL;
"""
print("\n--- Question 2 ---")
print(pd.read_sql(q2, conn))


# ==========================================
# Part 2: Type of Join
# ==========================================

# Question 3
q3 = """
SELECT e.firstName, e.lastName, o.city, o.state
FROM employees e
LEFT JOIN offices o ON e.officeCode = o.officeCode
ORDER BY e.firstName ASC, e.lastName ASC;
"""
print("\n--- Question 3 ---")
print(pd.read_sql(q3, conn))

# Question 4
q4 = """
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName ASC;
"""
print("\n--- Question 4 ---")
print(pd.read_sql(q4, conn))


# ==========================================
# Part 3: Built-In Function
# ==========================================

# Question 5
q5 = """
SELECT c.contactFirstName, c.contactLastName, p.amount, p.paymentDate
FROM customers c
JOIN payments p ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC;
"""
print("\n--- Question 5 ---")
print(pd.read_sql(q5, conn))


# ==========================================
# Part 4: Joining and Grouping
# ==========================================

# Question 6
q6 = """
SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS num_customers
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
HAVING AVG(c.creditLimit) > 90000
ORDER BY num_customers DESC;
"""
print("\n--- Question 6 ---")
print(pd.read_sql(q6, conn))

# Question 7
q7 = """
SELECT p.productName, 
       COUNT(od.orderNumber) AS numorders, 
       SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
GROUP BY p.productCode, p.productName
ORDER BY totalunits DESC;
"""
print("\n--- Question 7 ---")
print(pd.read_sql(q7, conn))


# ==========================================
# Part 5: Multiple Joins
# ==========================================

# Question 8
q8 = """
SELECT p.productName, p.productCode, COUNT(DISTINCT o.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY numpurchasers DESC;
"""
print("\n--- Question 8 ---")
print(pd.read_sql(q8, conn))

# Question 9
q9 = """
SELECT o.officeCode, o.city, COUNT(c.customerNumber) AS n_customers
FROM offices o
JOIN employees e ON o.officeCode = e.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city;
"""
print("\n--- Question 9 ---")
print(pd.read_sql(q9, conn))


# ==========================================
# Part 6: Subquery
# ==========================================

# Question 10
q10 = """
SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord ON c.customerNumber = ord.customerNumber
JOIN orderdetails od ON ord.orderNumber = od.orderNumber
WHERE od.productCode IN (
    SELECT od2.productCode
    FROM orderdetails od2
    JOIN orders o2 ON od2.orderNumber = o2.orderNumber
    GROUP BY od2.productCode
    HAVING COUNT(DISTINCT o2.customerNumber) < 20
);
"""
print("\n--- Question 10 ---")
print(pd.read_sql(q10, conn))
