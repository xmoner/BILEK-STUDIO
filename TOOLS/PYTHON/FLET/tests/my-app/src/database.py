import os
from supabase import create_client, Client
SUPABASE_URL= 'https://rjxzzfnwyanwxbgjkpbh.supabase.co'
SUPABASE_KEY='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJqeHp6Zm53eWFud3hiZ2prcGJoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgxMzkxNTcsImV4cCI6MjA1MzcxNTE1N30.hRlxp4vXkSWNaaGM47SKTZZLMDDp1p6bpwMb7cpNLxU'
# url: str = os.environ.get("SUPABASE_URL")
# key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase():
    return supabase

def init_db():

    # Check if item table is empty
    response = supabase.table('items').select('*').execute()
    if len(response.data) == 0:
        # insert initial menu items
        items = [
            {'name':'lukas', 'price':'22', "id_category":2}, # seznam
            {'name': 'Tomas', 'price': '30', "id_category": 2}  # seznam

        ]
        supabase.table('items').insert(items).execute()

        print("initial items inserted successfully.")