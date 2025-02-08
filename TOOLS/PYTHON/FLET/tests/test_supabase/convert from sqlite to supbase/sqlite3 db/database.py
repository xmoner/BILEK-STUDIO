import sqlite3 
import datetime
from zoneinfo import ZoneInfo
import os
import sys
import flet as ft

# Set timezone to Jordan/Amman
TIMEZONE = ZoneInfo("Asia/Amman")

def get_db_path():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, 'pos.db')

def get_connection():
    db_path = get_db_path()
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    return sqlite3.connect(db_path)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    # Step 1: Create the 'category' table if it doesn't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS category (
        id_category INTEGER PRIMARY KEY AUTOINCREMENT,
        name_category TEXT NOT NULL
    )
''')    
    cursor.execute('''
    INSERT OR IGNORE INTO category (id_category, name_category)
    VALUES (1, 'drinks'), (2, 'food')
''')

    # Create items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        id_category INTEGER,
        FOREIGN KEY (id_category) REFERENCES category(id_category)
    )
''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0
        )
    ''')
    
    # Create transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_amount REAL,
            FOREIGN KEY (user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Create transaction_items table for individual items in each transaction
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transaction_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER,
            item_name TEXT,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
        )
    ''')
    
    # Create deleted_transactions_history table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS deleted_transactions_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id INTEGER NOT NULL,
            transaction_date TEXT NOT NULL,
            transaction_user_id INTEGER NOT NULL,
            transaction_amount REAL NOT NULL,
            transaction_items TEXT,
            deleted_by_user_id INTEGER NOT NULL,
            deleted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (transaction_user_id) REFERENCES users(user_id),
            FOREIGN KEY (deleted_by_user_id) REFERENCES users(user_id)
        )
    ''')
    
    # Check if items table is empty
    cursor.execute('SELECT COUNT(*) FROM items')
    if cursor.fetchone()[0] == 0:
        # Insert initial menu items
        items = [
    ("swissroll-50gm", 5.00, 2),  # Food
    ("swissroll-150gm", 9.00, 2),
    ("lemon juice", 5.50, 2)  # drink
]
    cursor.execute('SELECT COUNT(*) FROM items')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO items (name, price, id_category) VALUES (?, ?, ?)', items)
    
    # Add admin user if not exists
    cursor.execute("INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, ?)", 
             ('admin', 'admin123', 1))
    
    conn.commit()
    conn.close()

def get_menu_items():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT name, price FROM items')
    items = cursor.fetchall()
    conn.close()
    return items

def add_item(name, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO items (name, price) VALUES (?, ?)', (name, price))
    conn.commit()
    conn.close()

def update_item(item_id, name, price):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE items SET name = ?, price = ? WHERE id = ?', (name, price, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM items WHERE id = ?', (item_id,))
    conn.commit()
    conn.close()

# User related functions
def register_user(username, password):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        return False  # Username already exists

def verify_login(username, password,is_admin):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id, username,is_admin FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    conn.close()
    return user  # Returns (user_id, username) if found, None if not found

def check_admin_login(username, password):
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE username=? AND password=? AND is_admin=1", (username, password))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Transaction related functions
def create_transaction(user_id, items, total_amount):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get current time in Jordan timezone
    current_time = datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
    
    try:
        cursor.execute('''
            INSERT INTO transactions (date_time, user_id, total_amount)
            VALUES (?, ?, ?)
        ''', (current_time, user_id, total_amount))
        
        transaction_id = cursor.lastrowid
        
        # Add transaction items
        for item in items:
            cursor.execute('''
                INSERT INTO transaction_items (transaction_id, item_name, quantity, price)
                VALUES (?, ?, ?, ?)
            ''', (transaction_id, item['name'], item['quantity'], item['price']))
        
        conn.commit()
        return transaction_id
    except Exception as e:
        print(f"Error adding transaction: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_user_transactions(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT transaction_id, date_time, total_amount 
        FROM transactions 
        WHERE user_id = ? 
        ORDER BY date_time DESC
    ''', (user_id,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions

def update_transaction(transaction_id, date, username, amount, items):
    conn = get_connection()
    cursor = conn.cursor()

    # Update the transaction details
    cursor.execute('''
        UPDATE transactions
        SET date_time = ?, total_amount = ?
        WHERE transaction_id = ?
    ''', (date, amount, transaction_id))

    # Update the username in the users table (if needed)
    cursor.execute('''
        UPDATE users
        SET username = ?
        WHERE user_id = (SELECT user_id FROM transactions WHERE transaction_id = ?)
    ''', (username, transaction_id))

    # Update the items in the transaction_items table
    cursor.execute('''
        DELETE FROM transaction_items WHERE transaction_id = ?
    ''', (transaction_id,))

    # Parse the items string (e.g., "Item1 x2, Item2 x3")
    for item in items.split(", "):
        item_name, quantity = item.split(" x")
        cursor.execute('''
            INSERT INTO transaction_items (transaction_id, item_name, quantity)
            VALUES (?, ?, ?)
        ''', (transaction_id, item_name, int(quantity)))

    conn.commit()
    conn.close()

def delete_transaction(transaction_id, deleted_by_user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Get transaction details before deleting
        cursor.execute('''
            SELECT t.transaction_id, t.date_time, t.user_id, t.total_amount, 
                   GROUP_CONCAT(ti.item_name || ' x' || ti.quantity) as items
            FROM transactions t
            LEFT JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
            WHERE t.transaction_id = ?
            GROUP BY t.transaction_id
        ''', (transaction_id,))
        transaction = cursor.fetchone()

        if transaction:
            # Get current time in Jordan timezone
            deleted_at = datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')
            
            # Insert into deleted_transactions_history
            cursor.execute('''
                INSERT INTO deleted_transactions_history 
                (transaction_id, transaction_date, transaction_user_id, 
                 transaction_amount, transaction_items, deleted_by_user_id, deleted_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (transaction[0], transaction[1], transaction[2], 
                 transaction[3], transaction[4], deleted_by_user_id, deleted_at))

            # Delete the transaction and its items
            cursor.execute('DELETE FROM transaction_items WHERE transaction_id = ?', (transaction_id,))
            cursor.execute('DELETE FROM transactions WHERE transaction_id = ?', (transaction_id,))
            
            conn.commit()
            return True
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

def get_sales_by_date_range(start_date, end_date, user_id=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = '''
        SELECT 
            t.transaction_id,
            t.date_time,
            u.username,
            t.total_amount,
            GROUP_CONCAT(ti.item_name || ' x' || ti.quantity) as items
        FROM transactions t
        JOIN users u ON t.user_id = u.user_id
        LEFT JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
        WHERE DATE(t.date_time) BETWEEN DATE(?) AND DATE(?)
    '''
    
    params = [start_date, end_date]
    
    if user_id is not None:
        query += ' AND t.user_id = ?'
        params.append(user_id)
    
    query += ' GROUP BY t.transaction_id ORDER BY t.date_time DESC'
    
    cursor.execute(query, params)
    transactions = cursor.fetchall()
    
    # Get total sum for the period
    total_query = '''
        SELECT SUM(total_amount)
        FROM transactions
        WHERE DATE(date_time) BETWEEN DATE(?) AND DATE(?)
    '''
    
    if user_id is not None:
        total_query += ' AND user_id = ?'
    
    # Pass the full params list to the total sum query
    cursor.execute(total_query, params)
    total_sum = cursor.fetchone()[0] or 0
    
    conn.close()
    return transactions, total_sum

def get_sales_by_user_and_date(user_id, start_date, end_date):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Get transactions for specific user within date range
    cursor.execute('''
        SELECT 
            t.transaction_id,
            t.date_time,
            u.username,
            t.total_amount,
            GROUP_CONCAT(ti.item_name || ' x' || ti.quantity) as items
        FROM transactions t
        JOIN users u ON t.user_id = u.user_id
        LEFT JOIN transaction_items ti ON t.transaction_id = ti.transaction_id
        WHERE t.user_id = ? AND DATE(t.date_time) BETWEEN DATE(?) AND DATE(?)
        GROUP BY t.transaction_id
        ORDER BY t.date_time DESC
    ''', (user_id, start_date, end_date))
    
    transactions = cursor.fetchall()
    
    # Get total sum for the user in this period
    cursor.execute('''
        SELECT SUM(total_amount)
        FROM transactions
        WHERE user_id = ? AND DATE(date_time) BETWEEN DATE(?) AND DATE(?)
    ''', (user_id, start_date, end_date))
    
    total_sum = cursor.fetchone()[0] or 0
    
    conn.close()
    return transactions, total_sum

def get_all_users():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, username, CAST(is_admin AS INTEGER) FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def update_user_admin_status(user_id, is_admin):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        # Convert is_admin to integer (0 or 1)
        admin_value = 1 if is_admin else 0
        cursor.execute("UPDATE users SET is_admin = ? WHERE user_id = ?", (admin_value, user_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating user admin status: {e}")
        return False
    finally:
        conn.close()

def search_menu_items(search_term):
    """Search for menu items by name"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, price 
        FROM items 
        WHERE name LIKE ?
    """, (f'%{search_term}%',))
    items = cursor.fetchall()
    conn.close()
    return items

def add_menu_item(name, price,category_id):
    """Add a new menu item"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO items (name, price,id_category) 
            VALUES (?, ?, ?)
        """, (name, price,category_id))
        item_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return item_id
    except sqlite3.Error as e:
        print(f"Error adding menu item: {e}")
        conn.close()
        return None

def get_menu_item(item_id):
    """Get a specific menu item by ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, price, id_category
        FROM items 
        WHERE id = ?
    """, (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item

def update_menu_item(item_id, name, price, id_category=None):
    """
    Update an existing menu item
    
    :param item_id: ID of the item to update
    :param name: New name for the item
    :param price: New price for the item
    :param id_category: Optional category ID for the item
    :return: True if update was successful, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        if id_category is not None:
            # Update with category
            cursor.execute('''
                UPDATE items 
                SET name = ?, price = ?, id_category = ? 
                WHERE id = ?
            ''', (name, price, id_category, item_id))
        else:
            # Update without changing category
            cursor.execute('''
                UPDATE items 
                SET name = ?, price = ? 
                WHERE id = ?
            ''', (name, price, item_id))
        
        conn.commit()
        return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error updating menu item: {e}")
        return False
    finally:
        conn.close()

def delete_menu_item(item_id):
    """Delete a menu item"""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        return success
    except sqlite3.Error as e:
        print(f"Error deleting menu item: {e}")
        conn.close()
        return False

def get_deleted_transactions_history(start_date=None, end_date=None, user_id=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = '''
        SELECT 
            h.id,
            h.transaction_id,
            h.transaction_date,
            u1.username as transaction_user,
            h.transaction_amount,
            h.transaction_items,
            u2.username as deleted_by_user,
            h.deleted_at
        FROM deleted_transactions_history h
        JOIN users u1 ON h.transaction_user_id = u1.user_id
        JOIN users u2 ON h.deleted_by_user_id = u2.user_id
        WHERE 1=1
    '''
    params = []

    if start_date and end_date:
        query += ' AND date(h.deleted_at) BETWEEN ? AND ?'
        params.extend([start_date, end_date])

    if user_id:
        query += ' AND h.deleted_by_user_id = ?'
        params.append(user_id)

    query += ' ORDER BY h.deleted_at DESC'

    cursor.execute(query, params)
    results = cursor.fetchall()

    conn.close()
    return results

def backup_database():
    """
    Creates a copy of the database file that can be saved or shared
    Returns the path to the backup file
    """
    import shutil
    import time
    from datetime import datetime
    
    # Get original database path
    original_db = get_db_path()
    
    # Create backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f'pos_backup_{timestamp}.db'
    
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backup_path = os.path.join(script_dir, backup_filename)
    
    try:
        # Create a copy of the database
        shutil.copy2(original_db, backup_path)
        return backup_path
    except Exception as e:
        print(f"Error creating backup: {str(e)}")
        return None
def get_all_categories():
    conn = get_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM category')
    categories = c.fetchall()
    conn.close()
    return categories  
      
def fetch_items_by_category(category_id):
    conn = get_connection()
    cursor = conn.cursor()
    
    # Query items for the selected category
    cursor.execute('SELECT name, price FROM items WHERE id_category = ?', (category_id,))
    items = cursor.fetchall()
    conn.close()
    
    return items
def fetch_all_categories():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Query all categories
    cursor.execute('SELECT id_category, name_category FROM category')
    categories = cursor.fetchall()
    conn.close()
    
    return categories            

init_db()   