UPDATE
    tickets
SET
    assignee_id = $assignee_id
WHERE
    id = $ticket_id;
