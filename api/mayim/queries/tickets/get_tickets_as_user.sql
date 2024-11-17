SELECT *
FROM tickets
WHERE user_id = $user_id
$status_filter
LIMIT $limit OFFSET $offset;
