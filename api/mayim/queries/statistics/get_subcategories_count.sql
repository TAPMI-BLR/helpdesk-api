SELECT s.name as title, COUNT(*) AS count
FROM tickets t
JOIN subcategories s on t.subcategory_id = s.id
WHERE s.category_id = $parent_id
GROUP BY s.id
ORDER BY count DESC;
