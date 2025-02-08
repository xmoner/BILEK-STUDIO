import gotrue.errors
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


# def init_db():
#     # Check if items table is empty
#     response = supabase.table('items').select('*').execute()
#     if len(response.data) == 0:
#         # Insert initial menu items
#         items = [
#             {"name": "swiss roll 150gm", "price": 5.00, "id_category": 2},  # Food
#             {"name": "juice", "price": 5.50, "id_category": 2}  # drink
#         ]
#         supabase.table('items').insert(items).execute()
#         print("Initial items inserted successfully.")
#     else:
#         print(".")
#
#     # Add admin user if not exists
#     admin_check = supabase.table('users').select('*').eq('username', 'admin').execute()
#     if not admin_check.data:
#         admin_user = {
#             "username": "admin",
#             "password": "admin123",  # In production, use proper password hashing
#             "is_admin": True
#         }
#         supabase.table('users').insert(admin_user).execute()


def register_user(users_password=None, users_email=None):
    # Register a new user, but also check if already does not exist already one

    # Registration - Signing up a new user
    reg_user = supabase.auth.sign_up({"email": users_email, "password": users_password})

    # try:

        # result = None

        # data=supabase.table('anonymous').select('username','email').execute()
        # if data.data is None:
        #     return [False, 'No data in anonymous']
        # print('data', data)
        #
        # for i in data.data:
        #     if i.get('username') != username:
        #         print('This name is free to use')
        #
        #         result = [True, ('This name is free to use')]
        #     else:
        #         print('Username already exists')
        #         result = [False, 'Username already exists']
        # if not users_password:
        #     result = [False, 'Password is missing']
        # for email in data.data:
        #     if users_email == email['email']:
        #         print('The email already exist!\nYou need to create a different one!')
        #         result = [False, 'The email already exist!\nYou need to create a different one!']
        # if not result[0]:
        #     return result


    # except Exception as e:
    #     print("Error:", e)

        # supabase.postgrest.auth(reg_user.session.access_token)
        #
        # user_data = {'username': username,
        #          'is_admin': False,
        #          'email': users_email,
        #          'user_id_auth':reg_user.session.user.id}
        # supabase.table('users').insert(user_data).execute()
        #
        # admin = {'username': username,
        #          'user_id_auth': reg_user.session.user.id,
        #          'email': users_email}
        # anonym_results = supabase.table('anonymous').insert(admin).execute()
        # print('anonym_results', anonym_results)
    return [True, 'Successfully registered email.\nCheck your email to confirm registration.']
    # except :
    #     return False

    # try:
    #     supabase.auth.sign_up({"email": users_email, "password": users_password})
    #
    #
    #
    # try:
    #     # Insert the new user into the users table
    #     response = supabase.table('users').insert({
    #         "username": username,
    #         "password": password
    #     }).execute()
    #
    #     # If the insertion is successful, return True
    #     if response.data:
    #         return True
    #     else:
    #         return False
    # except Exception as e:
    #     # Handle unique constraint violation (username already exists)
    #     if "duplicate key value violates unique constraint" in str(e):
    #         return False
    #     else:
    #         raise e  # Re-raise other exception

def get_menu_items():
    response = supabase.table('items').select('*').order('name').execute()
    return response.data


def check_login(users_email, users_password):
    # Query the users table for an admin user with the given username and password
    try:
        user = supabase.auth.sign_in_with_password({"email": users_email, "password": users_password})
    except gotrue.errors.AuthApiError:
        print('Login failed')
        return False

    # Check if the user is already registered in the users table
    response = supabase.table('users').select('user_id_auth').execute()
    print('response - check_login', response)
    if not response.data:

        supabase.postgrest.auth(user.session.access_token)

        user_data = {'username': 'None',
             'is_admin': False,
             'email': users_email,
             'user_id_auth':user.session.user.id}
        supabase.table('users').insert(user_data).execute()
    elif response.data:
        supabase.postgrest.auth(user.session.access_token)
        response_user_id_auth = supabase.table('users').select('*').eq('user_id_auth', user.session.user.id).execute()
        if response_user_id_auth.data:
            print('response_user_id_auth', response_user_id_auth)

            for i in response_user_id_auth.data:
                if i.get('user_id_auth') == user.session.user.id:
                    print(f"User with user_id_auth '{user.session.user.id}' found:", response.data)
                    return response_user_id_auth.data
        else:
            user_data = {'username': 'None',
                         'is_admin': False,
                         'email': users_email,
                         'user_id_auth': user.session.user.id}
            supabase.table('users').insert(user_data).execute()
            print(f"User with user_id_auth '{user.session.user.id}' creating row in database.")

            # print(f"User with user_id_auth '{user.session.user.id}' not found.")
    # else:
    #     # Query the users table for an admin user with the given username and password
    #     response = supabase.table('users') \
    #         .select('user_id_auth') \
    #         .eq('is_admin', False).execute()  #.eq('password', password) \


    # If a matching user is found, return True; otherwise, return False
    return len(response.data) > 0

def reset_password(email):
    print('email',email)
    supabase.auth.reset_password_email(email)
    return 'Check your email for reset password (Unfinished)'

def verify_login(email, password, is_admin):
    # Query the users table for a user with the given username and password
    response = supabase.table('users').select(
        'user_id, email, is_admin'
    ).eq('email', email).eq('password', password).execute()

    # Return the first matching user if found, otherwise return None
    return response.data[0] if response.data else None

def check_username(username):
    # Query the users table for a user and nick_name table
    # If the username is already taken, return True; otherwise, return False

    print('nick_name',username)
    response = supabase.table('users').select('username').execute()
    usernames = [user['username'] for user in response.data]
    if username in usernames:
        return True
    else:
        return False

    # print('usernames:', usernames)

def register_username(username, user_id):
    # Register a username for a user
    response = supabase.table('users').select('username').eq('username', username).execute()
    if response.data:
        print('username already exists:', response.data)
        return False

    else:
        supabase.table('users').update({'username': username}).eq('user_id', user_id).execute()
        print('Username registered successfully.')
        return True