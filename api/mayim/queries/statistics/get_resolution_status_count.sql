SELECT resolution_status as title,
COUNT(*) AS count
FROM tickets
GROUP BY resolution_status
ORDER BY count DESC;
