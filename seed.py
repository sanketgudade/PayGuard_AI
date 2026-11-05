import os
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Extract database credentials (assuming format: mysql+pymysql://username:password@localhost/pay_pal)
db_url = os.getenv('DATABASE_URL')

if not db_url or "mysql" not in db_url:
    print("Error: DATABASE_URL not found in .env or is not a MySQL URL.")
    print("Please make sure your .env has: DATABASE_URL=mysql+pymysql://root:password@localhost/pay_pal")
    exit(1)

# Parse the URL (naive parsing for basic format)
# mysql+pymysql://root:rajkumar@123@@localhost/pay_pal
try:
    auth_part = db_url.split('://')[1].split('@localhost')[0]
    user = auth_part.split(':')[0]
    password = auth_part.split(':')[1]
except Exception as e:
    print("Could not parse database credentials from DATABASE_URL. Make sure it matches the exact format.")
    exit(1)

connection = pymysql.connect(
    host='localhost',
    user=user,
    password=password,
    database='pay_pal',
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with connection.cursor() as cursor:
        print("Connected to MySQL database...")
        
        # 1. Insert Sanket Gudade as a User
        print("Inserting user: Sanket Gudade...")
        sql_user = """
            INSERT INTO users (name, email) 
            VALUES ('Sanket Gudade', 'sanket@payguard.ai')
            ON DUPLICATE KEY UPDATE name='Sanket Gudade';
        """
        cursor.execute(sql_user)
        
        # Get Sanket's user ID
        cursor.execute("SELECT id FROM users WHERE email='sanket@payguard.ai'")
        user_id = cursor.fetchone()['id']
        
        # Insert a policy for Sanket
        sql_policy = """
            INSERT IGNORE INTO policies (user_id, autonomous_limit, daily_limit, monthly_limit)
            VALUES (%s, 500.00, 1500.00, 10000.00)
        """
        cursor.execute(sql_policy, (user_id,))
        
        # 2. Insert 10 Fake Transactions
        print("Inserting 10 dummy transactions...")
        
        transactions_data = [
            # merchant, amount, category, desc, risk_score, risk_level, decision, status
            ('TechStore', 45.00, 'Electronics', 'Mouse purchase', 12, 'LOW', 'APPROVED', 'COMPLETED'),
            ('UnknownShop', 850.00, 'Digital Goods', 'High value digital asset', 72, 'HIGH', 'BLOCKED', 'BLOCKED'),
            ('CoffeeHouse', 4.50, 'Food & Beverage', 'Morning coffee', 5, 'LOW', 'APPROVED', 'COMPLETED'),
            ('MacBook Pro Reseller', 1249.00, 'Electronics', 'Laptop purchase', 34, 'MEDIUM', 'REVIEW', 'PENDING_APPROVAL'),
            ('Amazon', 29.99, 'Books', 'AI Programming Guide', 8, 'LOW', 'APPROVED', 'COMPLETED'),
            ('Shady Crypto Exchange', 5000.00, 'Finance', 'Crypto transfer', 95, 'CRITICAL', 'BLOCKED', 'BLOCKED'),
            ('Netflix', 15.99, 'Subscriptions', 'Monthly subscription', 2, 'LOW', 'APPROVED', 'COMPLETED'),
            ('Uber', 24.50, 'Travel', 'Ride to airport', 15, 'LOW', 'APPROVED', 'COMPLETED'),
            ('New Digital Vendor', 120.00, 'Digital Goods', 'Software license', 45, 'MEDIUM', 'REVIEW', 'PENDING_APPROVAL'),
            ('Target', 85.00, 'Groceries', 'Office supplies', 10, 'LOW', 'APPROVED', 'COMPLETED')
        ]
        
        for tx in transactions_data:
            sql_tx = """
                INSERT INTO transactions 
                (user_id, merchant, amount, category, description, risk_score, risk_level, decision, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_tx, (user_id, *tx))
            
            # If it's the blocked transaction, insert a risk factor
            if tx[1] == 'UnknownShop':
                tx_id = cursor.lastrowid
                sql_rf = """
                    INSERT INTO risk_factors (transaction_id, factor_type, severity, description)
                    VALUES (%s, 'NEW_MERCHANT', 'HIGH', 'Merchant has no prior history with this agent.')
                """
                cursor.execute(sql_rf, (tx_id,))
                
                sql_rf2 = """
                    INSERT INTO risk_factors (transaction_id, factor_type, severity, description)
                    VALUES (%s, 'POLICY_VIOLATION', 'HIGH', 'Amount exceeds the autonomous limit of $500.')
                """
                cursor.execute(sql_rf2, (tx_id,))

        connection.commit()
        print("Success! Database seeded with Sanket Gudade and 10 transactions.")
        
finally:
    connection.close()
