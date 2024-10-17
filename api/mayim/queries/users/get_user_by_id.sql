SELECT u.id, u.name, u.email, u.data, (s.email IS NOT NULL) AS is_team, s.is_sys_admin IS true AS is_sys_admin
FROM users u
LEFT JOIN staff s on u.email = s.email
WHERE u.id = $user_id;
