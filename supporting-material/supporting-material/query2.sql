SELECT COUNT(*) FROM (SELECT * FROM Sellers WHERE Sellers.Location = "New York" UNION SELECT * FROM Bidders WHERE Bidders.Location = "New York");