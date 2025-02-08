# Supabase configuration
#SUPABASE_URL ="https://rjxzzfnwyanwxbgjkpbh.supabase.co" #'imput your url'
#SUPABASE_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJqeHp6Zm53eWFud3hiZ2prcGJoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgxMzkxNTcsImV4cCI6MjA1MzcxNTE1N30.hRlxp4vXkSWNaaGM47SKTZZLMDDp1p6bpwMb7cpNLxU'
from gotrue.errors import AuthApiError

SUPABASE_URL = 'https://rjxzzfnwyanwxbgjkpbh.supabase.co' # /rest/v1/users?select=*
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJqeHp6Zm53eWFud3hiZ2prcGJoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgxMzkxNTcsImV4cCI6MjA1MzcxNTE1N30.hRlxp4vXkSWNaaGM47SKTZZLMDDp1p6bpwMb7cpNLxU"
# -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJqeHp6Zm53eWFud3hiZ2prcGJoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgxMzkxNTcsImV4cCI6MjA1MzcxNTE1N30.hRlxp4vXkSWNaaGM47SKTZZLMDDp1p6bpwMb7cpNLxU"

from supabase import create_client, Client

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def init_db():
    # Check if items table is empty
    # response = supabase.table('items').select('*').execute()
    # if len(response.data) == 0:
    #     # Insert initial menu items
    #     items = [
    #         {"name": "swiss roll 150gm", "price": 5.00, "id_category": 2},  # Food
    #         {"name": "juice", "price": 5.50, "id_category": 2}  # drink
    #     ]
    #     supabase.table('items').insert(items).execute()
    #     print("Initial items inserted successfully.")
    # else:
    #     print(".")

    # # Add admin user if not exists
    # admin_check = supabase.table('users').select('*').eq('username', 'is_admin').execute()
    # if not admin_check.data:
    #     admin_user = {
    #         "username": "admin",
    #         "password": "admin123",  # In production, use proper password hashing
    #         "is_admin": True
    #     }
    #     supabase.table('users').insert(admin_user).execute()

    # test
    response = supabase.table('users').select('*').execute()
    print('print response', response)

    #
    username = 'Luky'
    users_email = 'lucas.bilek@gmail.com'
    users_password = 'Sakal-sakal'
    # user_sign_up = supabase.auth.sign_up({"email": users_email, "password": users_password})
    # print(user_sign_up)
    user = None
    try:
        user = supabase.auth.sign_in_with_password({ "email": users_email, "password": users_password })
        print('sign_in', user.session.access_token)  # prints access_token
        print('id',user.session.user.id)
        # admin = {'username': 'test',
        #          'password': 'aaa',
        #          'is_admin': True,
        #          'email': 'lucas.bilek@gmail.com',
        #          'user_id_auth':user.session.user.id}
        # supabase.table('users').insert(admin).execute()



    except AuthApiError:
        print('Login failed')
    supabase.postgrest.auth(user.session.access_token)

    # admin = {'username': username,
    #          'user_id_auth': user.session.user.id}
    # anonym_results = supabase.table('anonymous').insert(admin).execute()
    # print('anonym_results', anonym_results)

    # update= (supabase.table('anonymous').update(
    #     {'email': users_email,'user_id_auth':user.session.user.id}).eq('id', 1).execute())
    # print('update',update)

    # supabase.table('users').update({'user_id_auth': user.session.user.id,
    #                                 'username':username}).eq('user_id', 11).execute()
    #
    # users_response = supabase.table('users').select('*').execute()
    # print('print users_response', users_response)
    # anonymous_response = supabase.table('anonymous').select('*').execute()
    # print('print anonymous_response', anonymous_response)
    # resp= supabase.table('users').select('username','user_id').execute()
    # print('resp', resp)
    # update = (supabase.table('anonymous').update(
    #     {'email': users_email}).eq('id', 1).execute())

    # aa=supabase.from_("anonymous").update({'user_id_auth': user.session.user.id,
    #                                        'email': users_email}).eq("id", 1).execute()
    # print(aa)

    name = supabase.table('anonymous').select('username','email').execute()
    print(name)
    # print('update', update)
    # print('users_email',users_email)
    # response = supabase.table('users').select('username','is_admin').execute()
    # print(response)
#init_db()

def initB():
    users_email = 'lucas.bilek.pipe@gmail.com'
    users_password = 'aaaaaaaaa'
    username = 'Luc'
    # reg_user = supabase.auth.sign_up({"email": users_email, "password": users_password})
    # print('access_token',reg_user.session.access_token)

    user = supabase.auth.sign_in_with_password({"email": users_email, "password": users_password})
    print('user2', user)
    supabase.postgrest.auth(user.session.access_token)

    user_data = {'username': username,
                 'is_admin': False,
                 'email': users_email,
                 'user_id_auth': user.session.user.id}
    supabase.table('users').insert(user_data).execute()

    admin = {'username': username,
             'user_id_auth': user.session.user.id,
             'email': users_email}
    anonym_results = supabase.table('anonymous').insert(admin).execute()
    print('anonym_results', anonym_results)

#initB()

a= {'a':1, "b":2}
# #print(a.get('c'))
# username = 'Luky'
# data=[{'username': 'Luky', 'email': 'lucas.bilek@gmail.com'}]
# for i in data:
#     if i.get('username') == 'Luk':
#         print(i)

data=supabase.table('anonymous').select('username','email').execute()
#print(data.data is None )

# Fetch all users
# response = supabase.auth.admin.list_users()
#
# # Print user details
# for user in response.users:
#     print(f"ID: {user.id}, Email: {user.email}, Created At: {user.created_at}")

# Registration - Signing up a new user
# try:
# reg_user = supabase.auth.sign_up({"email": 'lucas.bilek@gmail.com', "password": 'blender-blender'})
# print(reg_user)
# except AuthApiError as e:
#     print('email in the process')

user = supabase.auth.sign_in_with_password({"email":'lucas.bilek@gmail.com', "password": 'blender-blender'})
print(user.user.id)
response = supabase.table('users').select('user_id_auth').execute()
print(response)