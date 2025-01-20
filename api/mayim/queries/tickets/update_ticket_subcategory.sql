UPDATE
    tickets
SET
    subcategory_id = $subcategory_id
WHERE
    id = $ticket_id;
