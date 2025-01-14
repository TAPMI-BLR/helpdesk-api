SELECT u.id, u.name, u.email, u.data, (s.id IS NOT NULL) AS is_team, s.is_sys_admin IS true AS is_sys_admin, s.is_disabled
FROM users u
NATURAL JOIN Staff s
