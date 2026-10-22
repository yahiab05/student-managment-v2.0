CREATE USER IF NOT EXISTS 'darcoran_app'@'{{ip}}'
IDENTIFIED BY 'StrongPassword123!';

GRANT ALL PRIVILEGES
ON darcoran.*
TO 'darcoran_app'@'{{ip}}';