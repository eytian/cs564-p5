SELECT COUNT(*) FROM (SELECT * FROM Items i, item_categories c WHERE i.item_id = c.item_id 
GROUP BY c.item_id HAVING COUNT(*) = 4);