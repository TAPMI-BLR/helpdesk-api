SELECT u.id, u.name, u.email, u.data, (s.id IS NOT NULL) AS is_team, s.is_sys_admin IS true AS is_sys_admin
FROM users u
FULL OUTER JOIN staff s on u.id = s.id
WHERE u.email = $email;
