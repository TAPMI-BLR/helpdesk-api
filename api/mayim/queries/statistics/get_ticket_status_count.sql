SELECT ticket_status as title,
COUNT(*) AS count
FROM tickets
GROUP BY ticket_status
ORDER BY count DESC;
