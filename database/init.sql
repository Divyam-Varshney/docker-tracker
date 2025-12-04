-- Database create karo
CREATE DATABASE IF NOT EXISTS docker_tracker;
USE docker_tracker;

-- User create karo with privileges
CREATE USER IF NOT EXISTS 'devops_user'@'%' IDENTIFIED BY 'devops_pass';
GRANT ALL PRIVILEGES ON docker_tracker.* TO 'devops_user'@'%';
FLUSH PRIVILEGES;

-- Status logs table
CREATE TABLE IF NOT EXISTS status_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    log_type VARCHAR(50) NOT NULL,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_type (log_type),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Container logs table
CREATE TABLE IF NOT EXISTS container_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    container_name VARCHAR(255) NOT NULL,
    status VARCHAR(50),
    ports TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_container (container_name),
    INDEX idx_status (status),
    INDEX idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Sample data insert karo (testing ke liye)
INSERT INTO status_logs (log_type, message) VALUES
    ('system', 'Database initialized successfully'),
    ('system', 'Tables created');
