SELECT
    c.*,
    (
        SELECT json_agg(subcategories)
        FROM subcategories
        WHERE subcategories.category_id = c.id
    ) AS subcategories
FROM categories c;
