SELECT COUNT(*) FROM (SELECT * FROM Items i, Categories c WHERE i.ItemId = c.ItemId 
GROUP BY c.ItemId HAVING COUNT(*) = 4);