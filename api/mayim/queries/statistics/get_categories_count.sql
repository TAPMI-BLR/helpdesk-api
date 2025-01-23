SELECT c.name as title, COUNT(*) AS count
FROM tickets t
JOIN subcategories s on t.subcategory_id = s.id
JOIN categories c ON s.category_id = c.id
GROUP BY c.id
ORDER BY count DESC;
