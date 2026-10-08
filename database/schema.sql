CREATE DATABASE IF NOT EXISTS pay_pal;
USE pay_pal;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS policies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    autonomous_limit DECIMAL(10,2) DEFAULT 100.00,
    daily_limit DECIMAL(10,2) DEFAULT 500.00,
    monthly_limit DECIMAL(10,2) DEFAULT 2000.00,
    new_merchant_approval BOOLEAN DEFAULT TRUE,
    high_risk_block BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    merchant VARCHAR(255) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    currency VARCHAR(3) DEFAULT 'USD',
    category VARCHAR(100),
    description TEXT,
    risk_score INT,
    risk_level VARCHAR(20),
    decision VARCHAR(50),
    paypal_order_id VARCHAR(100),
    paypal_capture_id VARCHAR(100),
    status VARCHAR(50) DEFAULT 'ANALYZING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS risk_factors (
    id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_id INT NOT NULL,
    factor_type VARCHAR(50),
    severity VARCHAR(20),
    description TEXT,
    FOREIGN KEY (transaction_id) REFERENCES transactions(id)
);

-- Insert dummy user for testing
INSERT IGNORE INTO users (id, name, email) VALUES (1, 'Demo User', 'demo@payguard.ai');
INSERT IGNORE INTO policies (user_id, autonomous_limit, daily_limit, monthly_limit) VALUES (1, 100.00, 500.00, 2000.00);
