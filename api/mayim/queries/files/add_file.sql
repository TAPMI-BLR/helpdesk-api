INSERT INTO files(file_name, storage_type, file_type) VALUES ($file_name, $storage_type, $file_type) RETURNING id;
