from supabase import create_client, Client
import datetime

from zoneinfo import ZoneInfo
import os
import sys
import json

# Set timezone to Jordan/Amman
TIMEZONE = ZoneInfo("Asia/Amman")

# Supabase configuration
SUPABASE_URL ="https://rjxzzfnwyanwxbgjkpbh.supabase.co" #'imput your url'
SUPABASE_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJqeHp6Zm53eWFud3hiZ2prcGJoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgxMzkxNTcsImV4cCI6MjA1MzcxNTE1N30.hRlxp4vXkSWNaaGM47SKTZZLMDDp1p6bpwMb7cpNLxU'

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase():
    return supabase


def init_db():
    
    # Check if items table is empty
    response = supabase.table('items').select('*').execute()
    if len(response.data) == 0:
        # Insert initial menu items
        items = [
        {"name": "swiss roll 150gm", "price": 5.00, "id_category": 2},  # Food
        {"name": "juice", "price": 5.50, "id_category": 2}  # drink
    ]
        supabase.table('items').insert(items).execute()
        # print("Initial items inserted successfully.")
    else:
        print(".")
    
    # Add admin user if not exists
    admin_check = supabase.table('users').select('*').eq('username', 'admin').execute()
    if not admin_check.data:
        admin_user = {
            "username": "admin",
            "password": "admin123",  # In production, use proper password hashing
            "is_admin": True
        }
        supabase.table('users').insert(admin_user).execute()
def verify_login(username, password, is_admin):
    # Query the users table for a user with the given username and password
    response = supabase.table('users').select(
        'user_id, username, is_admin'
    ).eq('username', username).eq('password', password).execute()
    
    # Return the first matching user if found, otherwise return None
    return response.data[0] if response.data else None
def check_admin_login(username, password):
    # Query the users table for an admin user with the given username and password
    response = supabase.table('users') \
        .select('user_id') \
        .eq('username', username) \
        .eq('password', password) \
        .eq('is_admin', True) \
        .execute()
    
    # If a matching user is found, return True; otherwise, return False
    return len(response.data) > 0        
def get_menu_item(item_id):
    """Get a specific menu item by ID using Supabase"""
    try:
        # Query the 'items' table for the specific item
        response = supabase.table('items') \
            .select('id, name, price, id_category') \
            .eq('id', item_id) \
            .execute()
        
        # Check if the item was found
        if response.data and len(response.data) > 0:
            return response.data[0]  # Return the first (and only) matching item
        else:
            return None  # Item not found
    except Exception as e:
        print(f"Error fetching menu item: {e}")
        return None
def get_menu_items():
    response = supabase.table('items').select('*').order('name').execute()
    return response.data

def add_item(name, price):
    response = supabase.table('items').insert({"name": name, "price": price}).execute()
    return response.data[0] if response.data else None
def update_menu_item(item_id, name, price, id_category=None):
    """
    Update an existing menu item using Supabase

    :param item_id: ID of the item to update
    :param name: New name for the item
    :param price: New price for the item
    :param id_category: Optional category ID for the item
    :return: True if update was successful, False otherwise
    """
    try:
        # Prepare the data to update
        update_data = {
            'name': name,
            'price': price
        }
        
        # Include category ID if provided
        if id_category is not None:
            update_data['id_category'] = id_category
        
        # Update the item in the 'items' table
        response = supabase.table('items') \
            .update(update_data) \
            .eq('id', item_id) \
            .execute()
        
        # Check if the update was successful
        if response.data and len(response.data) > 0:
            return True  # Update successful
        else:
            return False  # No rows updated
    except Exception as e:
        print(f"Error updating menu item: {e}")
        return False

def update_item(item_id, name, price):
    response = supabase.table('items').update({
        "name": name,
        "price": price
    }).eq('id', item_id).execute()
    return response.data[0] if response.data else None

def delete_item(item_id):
    response = supabase.table('items').delete().eq('id', item_id).execute()
    return True if response.data else False

def get_item_by_name(name):
    response = supabase.table('items').select('*').eq('name', name).execute()
    return response.data[0] if response.data else None

def create_transaction(user_id, items, total_amount):
    current_time = datetime.datetime.now(TIMEZONE).isoformat()
    
    transaction_data = {
        "user_id": user_id,
        "date_time": current_time,
        "total_amount": total_amount
    }
    
    try:
        transaction_response = supabase.table('transactions').insert(transaction_data).execute()
        transaction_id = transaction_response.data[0]['transaction_id']
        
        transaction_items = [{
            "transaction_id": transaction_id,
            "item_name": item['name'],
            "quantity": item['quantity'],
            "price": item['price']
        } for item in items]
        
        supabase.table('transaction_items').insert(transaction_items).execute()
        return transaction_id
    
    except Exception as e:
        print(f"Error adding transaction: {e}")
        return False

def get_transactions(start_date=None, end_date=None):
    query = supabase.table('transactions').select(
        'transaction_id, date_time, total_amount, users(username)'
    ).order('date_time', desc=True)
    
    if start_date:
        query = query.gte('date_time', start_date)
    if end_date:
        query = query.lte('date_time', end_date)
    
    response = query.execute()
    return response.data

def get_transaction_items(transaction_id):
    response = supabase.table('transaction_items').select(
        'item_name, quantity'
    ).eq('transaction_id', transaction_id).execute()
    return response.data


def format_transaction_items(items):
    # Format the items as "item_name xquantity" separated by commas
    return ', '.join(f"{item['item_name']} x{item['quantity']}" for item in items)


def delete_transaction(transaction_id, deleted_by_user_id):
    try:
        # Get transaction details before deletion
        transaction = supabase.table('transactions').select(
            '*'
        ).eq('transaction_id', transaction_id).single().execute()
        
        if not transaction.data:
            return False
        
        # Get transaction items
        items = get_transaction_items(transaction_id)
        formatted_items = format_transaction_items(items)  # Format the items

        # Store in deleted_transactions_history
        history_data = {
            "transaction_id": transaction_id,
            "transaction_date": transaction.data['date_time'],
            "transaction_user_id": transaction.data['user_id'],
            "transaction_amount": transaction.data['total_amount'],
            "transaction_items": formatted_items,  # Store formatted string
            "deleted_by_user_id": deleted_by_user_id
        }
        
        # Insert into history
        supabase.table('deleted_transactions_history').insert(history_data).execute()
        
        # Delete transaction items
        supabase.table('transaction_items').delete().eq('transaction_id', transaction_id).execute()
        
        # Delete transaction
        supabase.table('transactions').delete().eq('transaction_id', transaction_id).execute()
        
        return True
    
    except Exception as e:
        print(f"Error deleting transaction: {e}")
        return False

def get_sales_by_date_range(start_date, end_date, user_id=None):
    # print("Fetching sales data...")
    # Step 1: Get transactions
    query = supabase.table('transactions') \
        .select('transaction_id, date_time, total_amount, user_id') \
        .gte('date_time', f"{start_date} 00:00:00") \
        .lte('date_time', f"{end_date} 23:59:59") \
        .order('date_time', desc=True)

    if user_id is not None:
        query = query.eq('user_id', user_id)

    transactions_response = query.execute()
    transactions = transactions_response.data
    # print("Transactions Response:", transactions)

    if not transactions:
        print("No transactions found.")
        return [], 0.0

    # Step 2: Fetch usernames
    user_ids = list(set(transaction['user_id'] for transaction in transactions))
    # print("Fetching usernames for User IDs:", user_ids)
    users_response = supabase.table('users') \
        .select('user_id, username') \
        .in_('user_id', user_ids) \
        .execute()
    users = {user['user_id']: user['username'] for user in users_response.data}
    # print("Users Response:", users)

    # Step 3: Fetch items for each transaction
    for transaction in transactions:
        items_response = supabase.table('transaction_items') \
            .select('item_name, quantity') \
            .eq('transaction_id', transaction['transaction_id']) \
            .execute()
        # print(f"Items Response for Transaction {transaction['transaction_id']}:", items_response.data)
        items = [f"{item['item_name']} x{item['quantity']}" for item in items_response.data]
        transaction['items'] = ', '.join(items)

    # Step 4: Calculate total sum
    total_sum_query = supabase.table('transactions') \
        .select('total_amount') \
        .gte('date_time', f"{start_date} 00:00:00") \
        .lte('date_time', f"{end_date} 23:59:59")

    if user_id is not None:
        total_sum_query = total_sum_query.eq('user_id', user_id)

    total_sum_response = total_sum_query.execute()
    total_sum = sum(transaction['total_amount'] for transaction in total_sum_response.data)
    # print("Total Sum:", total_sum)

    # Format transactions
    formatted_transactions = [
        (
            transaction['transaction_id'],
            transaction['date_time'],
            users.get(transaction['user_id'], 'Unknown'),
            transaction['total_amount'],
            transaction['items']
        )
        for transaction in transactions
    ]

    return formatted_transactions, total_sum        
def get_sales_by_user_and_date(user_id, start_date, end_date):

    # Step 1: Get transactions for the specific user within the date range
    transactions_response = supabase.table('transactions') \
        .select('transaction_id, date_time, total_amount') \
        .eq('user_id', user_id) \
        .gte('date_time', f"{start_date} 00:00:00") \
        .lte('date_time', f"{end_date} 23:59:59") \
        .order('date_time', desc=True) \
        .execute()

    
    transactions = transactions_response.data
    print(transactions)
    

    # Step 2: Get the username for the user
    user_response = supabase.table('users') \
        .select('username') \
        .eq('user_id', user_id) \
        .execute()
    
    username = user_response.data[0]['username'] if user_response.data else 'Unknown'

    # Step 3: Get transaction items for each transaction
    for transaction in transactions:
        items_response = supabase.table('transaction_items') \
            .select('item_name, quantity') \
            .eq('transaction_id', transaction['transaction_id']) \
            .execute()
        
        # Format items as "item_name x quantity"
        items = [f"{item['item_name']} x{item['quantity']}" for item in items_response.data]
        transaction['items'] = ', '.join(items)

    # Step 4: Calculate the total sum for the user in this period
    total_sum_response = supabase.table('transactions') \
        .select('total_amount', count='exact') \
        .eq('user_id', user_id) \
        .gte('date_time', start_date) \
        .lte('date_time', end_date) \
        .execute()
    
    total_sum = sum(transaction['total_amount'] for transaction in total_sum_response.data)

    # Format the transactions as a list of tuples to match the original function's output
    formatted_transactions = [
        (
            transaction['transaction_id'],
            transaction['date_time'],
            username,
            transaction['total_amount'],
            transaction['items']
        )
        for transaction in transactions
    ]

    return formatted_transactions, total_sum    
def get_daily_report(date):
    start_date = f"{date}T00:00:00+03:00"
    end_date = f"{date}T23:59:59+03:00"
    
    response = supabase.table('transactions').select(
        'transaction_id, date_time, total_amount, users(username)'
    ).gte('date_time', start_date).lte('date_time', end_date).execute()
    
    return response.data

def get_monthly_report(year, month):
    start_date = f"{year}-{month:02d}-01T00:00:00+03:00"
    if month == 12:
        next_year = year + 1
        next_month = 1
    else:
        next_year = year
        next_month = month + 1
    end_date = f"{next_year}-{next_month:02d}-01T00:00:00+03:00"
    
    response = supabase.table('transactions').select(
        'transaction_id, date_time, total_amount, users(username)'
    ).gte('date_time', start_date).lt('date_time', end_date).execute()
    
    return response.data

def sfy_login(username, password, is_admin):
    response = supabase.table('users').select(
        'user_id, username, is_admin'
    ).eq('username', username).eq('password', password).execute()
    
    return response.data[0] if response.data else None

def add_user(username, password, is_admin=False):
    try:
        user_data = {
            "username": username,
            "password": password,  # In production, use proper password hashing
            "is_admin": is_admin
        }
        response = supabase.table('users').insert(user_data).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error adding user: {e}")
        return None

def get_users():
    response = supabase.table('users').select('user_id, username, is_admin').execute()
    return response.data

def delete_user(user_id):
    try:
        response = supabase.table('users').delete().eq('user_id', user_id).execute()
        return True if response.data else False
    except Exception as e:
        print(f"Error deleting user: {e}")
        return False



def get_deleted_transactions_history(start_date, end_date):
    try:
        # Query the deleted_transactions_history table within the date range
        response = supabase.table('deleted_transactions_history').select(
            'transaction_id, transaction_date, transaction_user_id, transaction_amount, transaction_items, deleted_by_user_id, deleted_at'
        ).gte('deleted_at',  f"{start_date} 00:00:00").lte('deleted_at',f"{end_date} 23:59:59").execute()
        

        if response.data:
            history = [
                (
                    item.get('id'),  # Unique ID of the history record (if exists)
                    item.get('transaction_id'),
                    item.get('transaction_date'),
                    item.get('transaction_user_id'),
                    item.get('transaction_amount'),
                    item.get('transaction_items'),
                    item.get('deleted_by_user_id'),
                    item.get('deleted_at'),
                )
                for item in response.data
            ]
            return history
        else:
            return []
    except Exception as e:
        print(f"Error retrieving deleted transactions history: {e}")
        return []


def search_menu_items(search_term: str):
    """Search for menu items by name using Supabase"""
    # Use the Supabase client to query the 'items' table
    response = supabase.table('items') \
        .select('id, name, price') \
        .ilike('name', f'%{search_term}%') \
        .execute()
    
    # Extract the data from the response
    items = response.data
    return items  # 

def add_menu_item(name: str, price: float):
    """Add a new menu item using Supabase"""
    try:
        # Insert the new item into the 'items' table
        response = supabase.table('items') \
            .insert({"name": name, "price": price}) \
            .execute()
        
        # Extract the inserted item's ID from the response
        item_id = response.data[0]['id']  # Supabase returns the inserted row(s)
        return item_id
    except Exception as e:
        print(f"Error adding menu item: {e}")
        return None

    return items
def get_all_users():
    # Query the users table for all users
    response = supabase.table('users').select('user_id, username, is_admin').execute()
    
    # Convert the response to a list of tuples
    users = [(user['user_id'], user['username'], int(user['is_admin'])) for user in response.data]
    return users
def register_user(username, password):
    try:
        # Insert the new user into the users table
        response = supabase.table('users').insert({
            "username": username,
            "password": password
        }).execute()
        
        # If the insertion is successful, return True
        if response.data:
            return True
        else:
            return False
    except Exception as e:
        # Handle unique constraint violation (username already exists)
        if "duplicate key value violates unique constraint" in str(e):
            return False
        else:
            raise e  # Re-raise other exception

def delete_menu_item(item_id: int):
    """Delete a menu item using Supabase"""
    try:
        # Delete the item from the 'items' table
        response = supabase.table('items') \
            .delete() \
            .eq('id', item_id) \
            .execute()
        
        # Check if the deletion was successful
        success = len(response.data) > 0  # Supabase returns the deleted row(s)
        return success
    except Exception as e:
        print(f"Error deleting menu item: {e}")
        return False    

def update_user_admin_status(user_id: int, is_admin: bool) -> bool:
    try:
        # Convert is_admin to integer (1 or 0)
        admin_value = 1 if is_admin else 0
        
        # Update the user's admin status
        response = supabase.table('users').update({'is_admin': admin_value}).eq('user_id', user_id).execute()
        
        # Check if the update was successful
        if response.data and len(response.data) > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error updating user admin status: {e}")
        return False 
                       
def get_all_categories():
    # Initialize Supabase client
    

    # Fetch all categories
    response = supabase.table('category').select('*').execute()
    categories = response.data
    return categories
# def get_all_categories():
#     response = supabase.table("category").select("*").execute()
#     categories = response.data
#     return [(cat["id_category"], cat["name_category"]) for cat in categories]    
def fetch_items_by_category(category_id):
    # Fetch items for the selected category
    response = supabase.table('items') \
        .select('name, price') \
        .eq('id_category', category_id) \
        .execute()
    
    # Extract the data from the response
    items = response.data
    
    # Return the items as a list of tuples (name, price)
    return [(item['name'], item['price']) for item in items]


def fetch_all_categories():
    # Initialize Supabase client
    

    # Fetch all categories
    response = supabase.table('category').select('id_category, name_category').execute()
    categories = response.data
    return categories        
        