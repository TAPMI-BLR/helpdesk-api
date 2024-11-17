SELECT *
FROM tickets
$status_filter
LIMIT $limit OFFSET $offset;
