
import flet as ft
import datetime
import database
import asyncio
import xlsxwriter
import os
import platform
from zoneinfo import ZoneInfo  # Add timezone support


    
# Set timezone to Jordan/Amman
TIMEZONE = ZoneInfo("Asia/Amman")


# Request Android permissions if needed
def request_android_permissions(page: ft.Page): 
    if platform.system() == 'Android':
        # Request storage permissions
        page.client_storage.set("android_storage_permission", "true")
        # Create POS directory in external storage
        pos_dir = '/storage/emulated/0/POS'
        os.makedirs(pos_dir, exist_ok=True)

class User:
    def __init__(self, user_id=None, username=None,is_admin=None):
        self.user_id = user_id
        self.username = username
        self.is_admin=is_admin


current_user = User()


def main(page: ft.Page):
    page.window.width=450
    def handle_change(e):
        if e.control.selected_index == 0:  
            naser1(e)
        if e.control.selected_index == 1:  
            naser5(e)    
        elif e.control.selected_index == 2:  
            naser2(e) 
        elif e.control.selected_index == 3:  
            naser4(e)     
        elif e.control.selected_index == 4:  
            naser3(e) 
        elif e.control.selected_index == 5:  
            naser6(e)  
    def naser6(e):
            current_user.user_id = None
            current_user.username = None
            page.go("/login")                  
    def naser1(e):

        page.go("/reports")
    def naser5(e):
        page.go("/users")    
    def naser2(e):
        page.go("/items")
    def open_link(e):
        page.launch_url("https://t.me/ayamnash")
    def send_email(e):
        # Create a mailto link
        email_address = "ayamnash@gmail.com"
        subject = "Hello"
        body = "write here"
        mailto_link = f"mailto:{email_address}?subject={subject}&body={body}"
        
        # Open the mailto link to launch the default email client
        page.launch_url(mailto_link)   

    def naser3(e):
        alert_dialog  = ft.AlertDialog(
            title=ft.Row(
                controls=[
                    ft.Text( "CONTACT US", size=30, color="pink600", italic=True
                    )

                ]

            ),

            content=ft.Column(
                controls=[
                    ft.Column(
                        controls=[
                        ft.Divider(),

                            ft.ResponsiveRow(
                                controls=[
                                    
                                ft.TextButton(
                                'To contact the developer \ntelegram ',
                                on_click=open_link,icon="TELEGRAM",
                                 icon_color="green400",
                                style=ft.ButtonStyle(
            color=ft.Colors.BLUE,  # Set the text color here
        ),
                               
                            ),
                                ft.TextButton(
                                'ayamnash@gmail.com \nEmail ',
                                on_click=send_email,icon="EMAIL_OUTLINED",
                                 icon_color="green400",
                                style=ft.ButtonStyle(
            color=ft.Colors.BLUE,  # Set the text color here
        ),
                               
                            )
                                ],
                                spacing=4,
                                vertical_alignment='start',
                                alignment='start',
                                
                            ),
                            
                               
                            
                            

                            
                           
                            
                        ],
                        
                    
                        
                   )
                ],
                
                horizontal_alignment='start',
                scroll= ft.ScrollMode.ALWAYS
                
            )
        
        ,


            # actions=[ft.TextButton(text="Close", on_click=self.close_dialog)],
            # open=True,
          actions=[
                ft.ElevatedButton("OK", on_click=lambda _: close_dialog(alert_dialog))
            ],  
        )
        page.overlay.append(alert_dialog)
        alert_dialog.open = True
        page.update()
        
    def naser4(e):
        page.go("/deletion_history")


    
    # Request permissions at app startup
    request_android_permissions(page)
    
    page.title = "POS System"
    page.window.always_on_top = True
    def create_responsive_button(text, on_click, bgcolor=ft.Colors.BLUE):
        return ft.ElevatedButton(
            text,
            on_click=on_click,
            bgcolor=bgcolor,
            color=ft.Colors.WHITE,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            col={"xs": 4, "sm": 2, "md": 2},  # Set column size for responsiveness
        )
    def close_dialog(dlg):

                dlg.open = False
                page.update() 
    def handle_keyboard_event(event):
        if event.key == 'go_back' or event.key == 'Escape':
            if page.route != "/":
                page.go("/")


    # Login Screen
    def create_login_view():
        username_field = ft.TextField(label="Username", width=300)
        password_field = ft.TextField(
                    label="Password",
                    password=True,  # Specify this only once
                    width=300,
                    can_reveal_password=True
                )
        admin_checkbox = ft.Checkbox(label="Login as Admin", value=False)
        error_text = ft.Text("", color=ft.Colors.RED)

        def try_login(e):
            is_admin_selected = admin_checkbox.value
            # Check if user exists and is admin
            is_admin = database.check_admin_login(username_field.value, password_field.value)
            
            if is_admin_selected and not is_admin:
                error_text.value = "Invalid admin credentials"
                page.update()
                return
            
            if not is_admin_selected and is_admin:
                error_text.value = "Please check 'Login as Admin' for admin accounts"
                page.update()
                return
            
            # Verify login credentials
            user = database.verify_login(username_field.value, password_field.value,is_admin)
            if user:
                current_user.user_id = user[0]
                current_user.username = user[1]
                current_user.is_admin = user[2]
                page.go("/")
            else:
                error_text.value = "Invalid username or password"
                page.update()

        def go_to_register(e):
            page.go("/register")

        login_view = ft.View(
            "/login",
            [
                ft.Column(
                    [
                        ft.Text("Login\n username admin\npassword admin123", size=15, weight=ft.FontWeight.BOLD),
                        username_field,
                        password_field,
                        ft.Row(
                            [admin_checkbox],
                            alignment=ft.MainAxisAlignment.CENTER
                        ),
                        error_text,
                        ft.Row(
                            [
                                ft.ElevatedButton("Login", on_click=try_login),
                                ft.ElevatedButton("Register", on_click=go_to_register, bgcolor=ft.Colors.GREEN),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        return login_view

    # Register Screen
    def create_register_view():
        username_field = ft.TextField(label="Username", width=300)
        password_field = ft.TextField(label="Password", password=True, width=300)
        confirm_password = ft.TextField(label="Confirm Password", password=True, width=300)
        error_text = ft.Text("", color=ft.Colors.RED)

        def try_register(e):
            if password_field.value != confirm_password.value:
                error_text.value = "Passwords do not match"
                page.update()
                return
            
            if database.register_user(username_field.value, password_field.value):
                page.go("/login")
            else:
                error_text.value = "Username already exists"
                page.update()

        def go_to_login(e):
            page.go("/login")

        register_view = ft.View(
            "/register",
            [
                ft.Column(
                    [
                        ft.Text("Register", size=30, weight=ft.FontWeight.BOLD),
                        username_field,
                        password_field,
                        confirm_password,
                        error_text,
                        ft.Row(
                            [
                                ft.ElevatedButton("Register", on_click=try_register, bgcolor=ft.Colors.GREEN),
                                ft.ElevatedButton("Back to Login", on_click=go_to_login)
                            ],
                            alignment=ft.MainAxisAlignment.CENTER
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )
        return register_view

    # Item Management Screen
    def create_items_view():
        search_field = ft.TextField(
            label="Search Items",
            width=300,
            prefix_icon=ft.Icons.SEARCH,
        )
        items_list = ft.ListView(
            expand=1,
            spacing=10,
            auto_scroll=True,
        )

        def update_items_list(search_term=""):
            items_list.controls.clear()
            items = database.search_menu_items(search_term)
            for item_id, name, price in items:
                items_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                [
                                    ft.ListTile(
                                        leading=ft.Icon(ft.Icons.FASTFOOD),
                                        title=ft.Text(name, size=16),
                                        subtitle=ft.Text(f"Price: {price:.2f} JD"),
                                    ),
                                    ft.Row(
                                        [
                                            ft.IconButton(
                                                icon=ft.Icons.EDIT,
                                                icon_color=ft.Colors.BLUE,
                                                on_click=lambda e, item_id=item_id: edit_item_dialog(item_id)
                                            ),
                                            ft.IconButton(
                                                icon=ft.Icons.DELETE,
                                                icon_color=ft.Colors.RED,
                                                on_click=lambda e, item_id=item_id: delete_item_dialog(item_id)
                                            ),
                                        ],
                                        alignment=ft.MainAxisAlignment.END,
                                    ),
                                ]
                            ),
                            padding=10,
                        )
                    )
                )
            page.update()

        def add_item_dialog():
            name_field = ft.TextField(label="Item Name")
            price_field = ft.TextField(label="Price", keyboard_type=ft.KeyboardType.NUMBER)
            
            # Add category dropdown
            categories = database.get_all_categories()
            category_options = [ft.dropdown.Option(key=str(cat_id), text=cat_name) 
                               for cat_id, cat_name in categories]
            category_dropdown = ft.Dropdown(
                label="Category",
                options=category_options,
                width=200,
            )

            def save_new_item(e):
                try:
                    price = float(price_field.value)
                    category_id = int(category_dropdown.value) if category_dropdown.value else None
                    database.add_menu_item(name_field.value, price, category_id)
                    close_dialog(dia)
                    update_items_list()
                    page.update()
                except ValueError:
                    price_field.error_text = "Please enter a valid price"
                    page.update()

            dia = ft.AlertDialog(
                title=ft.Text("Add New Item"),
                content=ft.Column([name_field, price_field, category_dropdown], tight=True),
                actions=[
                    ft.TextButton("Cancel", on_click=lambda _: close_dialog(dia)),
                    ft.TextButton("Save", on_click=save_new_item),
                ],
            )
            
            page.overlay.append(dia)
            dia.open = True
            page.update()


        def edit_item_dialog(item_id):
            # Get the current item details including category
            item = database.get_menu_item(item_id)
            print(item)
            print(item)
            if item:
                name_field = ft.TextField(label="Item Name", value=item[1])
                price_field = ft.TextField(label="Price", value=str(item[2]))
                
                # Get all categories for dropdown
                categories = database.get_all_categories()
                
                # Create category dropdown

                category_dropdown = ft.Dropdown(
                    label="Category",
                    options=[
                        ft.dropdown.Option(
                            key=str(cat[0]),  # category id
                            text=cat[1]  # category name
                        ) for cat in categories
                    ],
                    value=str(item[3]) if item[3] is not None else None,  # Set current category
                    width=300
                )
                
                def save_edit(e):
                    try:
                        price = float(price_field.value)
                        # Update menu item with new category
                        if database.update_menu_item(
                            item_id, 
                            name_field.value, 
                            price, 
                            int(category_dropdown.value) if category_dropdown.value else None
                        ):
                            dia.open = False
                            update_items_list()
                            page.update()
                    except ValueError:
                        price_field.error_text = "Please enter a valid price"
                        page.update()

                dia = ft.AlertDialog(
                    title=ft.Text("Edit Item"),
                    content=ft.Column([
                        name_field, 
                        price_field, 
                        category_dropdown
                    ], tight=True),
                    actions=[
                        ft.TextButton("Cancel", on_click=lambda _: close_dialog(dia)),
                        ft.TextButton("Save", on_click=save_edit),
                    ],
                )
                page.overlay.append(dia)
                dia.open = True
                page.update()

        def delete_item_dialog(item_id):
            def confirm_delete(e):
                if database.delete_menu_item(item_id):
                    dia.open = False
                    update_items_list()
                    page.update()

            dia = ft.AlertDialog(
                title=ft.Text("Delete Item"),
                content=ft.Text("Are you sure you want to delete this item?"),
                actions=[
                    ft.TextButton("Cancel", on_click=lambda _: close_dialog(dia)),
                    ft.TextButton("Delete", on_click=confirm_delete),
                ],
            )
            page.overlay.append(dia)
            dia.open = True
            page.update()

        search_field.on_change = lambda e: update_items_list(e.control.value)
        
        # Create the management view
        management_view = ft.View(
            "/items",
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                            controls=[
                                # Left icon
                                ft.IconButton(
                                    icon=ft.Icons.ARROW_BACK,
                                    icon_color=ft.Colors.BLUE,
                                    on_click=lambda _: (page.clean(), page.go("/")),
                                ),
                                # Centered text
                                ft.Container(
                                    content=ft.Text(
                                        "Item Management",
                                        size=25 if page.width > 600 else 20,  # Adjust text size based on screen width
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    alignment=ft.alignment.center,  # Center the text
                                    expand=True,  # Expand to fill available space
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.START,  # Align the row to the start (left)
                        ),
                            search_field,
                            ft.Container(
                                content=items_list,
                                width=page.width*0.9,
                                height=page.height*0.7,
                                border=ft.border.all(1, ft.Colors.OUTLINE),
                                border_radius=10,
                                padding=10,
                            ),
                            ft.ElevatedButton(
                                "Add New Item",
                                on_click=lambda _: add_item_dialog(),
                                bgcolor=ft.Colors.GREEN,
                                color=ft.Colors.WHITE,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=10,
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.START,
        )
        
        # Initialize the items list
        update_items_list()

        return management_view

    # Reports Screen
    def create_reports_view():
        day1=datetime.date.today()
        start_date_picker = ft.DatePicker(
            on_change=lambda e: on_start_date_change(e),
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime(2100, 12, 31),
        )

        end_date_picker = ft.DatePicker(
            on_change=lambda e: on_end_date_change(e),
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime(2100, 12, 31),
        )

        start_date_field = ft.TextField(
            label="Start Date",
            read_only=True,
            hint_text="Select Start Date",
            expand=True,
            value=day1,
            on_click=lambda e: page.open(start_date_picker),

        )

        end_date_field = ft.TextField(
            label="End Date",
            read_only=True,
            hint_text="Select End Date",
            expand=True,
            value=day1,
            on_click=lambda e: page.open(end_date_picker),
        )

        def on_start_date_change(e):
            selected_date = e.control.value
            if selected_date:
                start_date_field.value = selected_date.strftime("%Y-%m-%d")
                end_date_picker.first_date = selected_date
                if end_date_picker.value and end_date_picker.value < selected_date:
                    end_date_picker.value = None
                    end_date_field.value = ""
            else:
                start_date_field.value = ""
                end_date_picker.first_date = datetime.datetime(2000, 1, 1)
            page.update()
            if start_date_field.value and end_date_field.value:
                update_date_range_report(None)
        def show_row_details(row_data):
            # Create TextFields for each column
            date_field = ft.TextField(label="Date", value=row_data[1])
            username_field = ft.TextField(label="Username", value=row_data[2])
            items_field = ft.TextField(label="Items", value=row_data[4])
            amount_field = ft.TextField(label="Amount", value=f"{row_data[3]:.2f} JD")

            

              

            def delete_row(e):
                try:
                    # Delete with current user ID for tracking
                    database.delete_transaction(row_data[0], current_user.user_id)
                    
                    
                    
                    # Trigger a refresh of the data
                    if start_date_picker.value and end_date_picker.value:
                        start_str = start_date_picker.value.strftime("%Y-%m-%d")
                        end_str = end_date_picker.value.strftime("%Y-%m-%d")
                        
                        if user_dropdown.value:
                            transactions, total = database.get_sales_by_user_and_date(
                                int(user_dropdown.value),
                                start_str,
                                end_str
                            )
                        else:
                            if current_user.is_admin:
                                transactions, total = database.get_sales_by_date_range(start_str, end_str)
                            else:
                                transactions, total = database.get_sales_by_date_range(start_str, end_str, current_user.user_id)
                        
                        # Update table
                        results_table.rows.clear()
                        for trans_id, date, username, amount, items in transactions:
                            row = ft.DataRow(
                                cells=[
                                    ft.DataCell(ft.Text(date)),
                                    ft.DataCell(ft.Text(username)),
                                    ft.DataCell(ft.Text(items or "")),
                                    ft.DataCell(ft.Text(f"{amount:.2f} JD")),
                                ],
                                on_select_changed=lambda e, row_data=(trans_id, date, username, amount, items): show_row_details(row_data)
                            )
                            results_table.rows.append(row)
                        
                        total_label.value = f"Total: {total:.2f} JD"
                    
                    page.update()

                    # Show success message
                    dia = ft.AlertDialog(
                        title=ft.Text("Success"),
                        content=ft.Text("Transaction deleted successfully"),
                        actions=[
                            ft.TextButton("OK", on_click=lambda _: close_dialog(dia))
                        ],
                    )
                    page.overlay.append(dia)
                    dia.open = True
                    page.update()
                    
                except Exception as e:
                    print(f"Error deleting row: {e}")
                    # Show error message
                    dia = ft.AlertDialog(
                        title=ft.Text("Error"),
                        content=ft.Text(f"Failed to delete transaction: {str(e)}"),
                        actions=[
                            ft.TextButton("OK", on_click=lambda _: close_dialog(dia))
                        ],
                    )
                    page.overlay.append(dia)
                    dia.open = True
                    page.update()

            dia = ft.AlertDialog(
                title=ft.Text("Row Details"),
                content=ft.Column([
                    date_field,
                    username_field,
                    items_field,
                    amount_field,
                ]),
                actions=[
                    
                    ft.TextButton("Delete", on_click=delete_row),
                    ft.TextButton("Close",on_click=lambda _: close_dialog(dia)),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.overlay.append(dia)
            dia.open = True
            page.update()

        def update_user_report(e):

            if not user_dropdown.value:
                return

            try:
                if not start_date_picker.value or not end_date_picker.value:
                    return

                start_str = start_date_picker.value.strftime("%Y-%m-%d")
                end_str = end_date_picker.value.strftime("%Y-%m-%d")

                transactions, total = database.get_sales_by_user_and_date(
                    int(user_dropdown.value),
                    start_str,
                    end_str
                )

                results_table.rows.clear()
                for trans_id, date, username, amount, items in transactions:
                    row = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(date)),
                            ft.DataCell(ft.Text(username)),
                            ft.DataCell(ft.Text(items or "")),
                            ft.DataCell(ft.Text(f"{amount:.2f} JD")),
                        ],
                        on_select_changed=lambda e, row_data=(trans_id, date, username, amount, items): show_row_details(row_data)
                    )
                    results_table.rows.append(row)

                total_label.value = f"Total: {total:.2f} JD"
                page.update()

            except ValueError as e:
                print(f"Error: {e}")
                

                

        def on_end_date_change(e):
            selected_date = e.control.value
            if selected_date:
                end_date_field.value = selected_date.strftime("%Y-%m-%d")
                if start_date_field.value and end_date_field.value:
                    update_date_range_report(None)
            else:
                end_date_field.value = ""
            page.update()

        page.overlay.extend([start_date_picker, end_date_picker])
        
        users = database.get_all_users()
        
        is_admin1=current_user.is_admin
        user_id1=current_user.user_id
        user_name=current_user.username
        

        if is_admin1 == 1:
            user_options = [ft.dropdown.Option(key=str(uid), text=uname) for uid, uname, _ in users]
            # If the user is an admin, show all users in the dropdown
            user_dropdown = ft.Dropdown(
                label="Select User",
                expand=True,
                options=user_options,
                on_change=update_user_report  # Pass the function directly
            )
        else:
            # If the user is not an admin, show only the current user's name
            user_dropdown = ft.Dropdown(
                label="Select User",
                expand=True,
                options=[ft.dropdown.Option(text=user_name, key=str(user_id1))],
                on_change=update_user_report  # Pass the function directly
            )
        
        results_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Date")),
                ft.DataColumn(ft.Text("User")),
                ft.DataColumn(ft.Text("Items")),
                ft.DataColumn(ft.Text("Total")),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
            column_spacing=10,
            heading_row_height=20,
            data_row_min_height=50,
            heading_row_color=ft.Colors.BLUE_GREY_100,
        )

        table_container = ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [results_table],
                        scroll=ft.ScrollMode.ALWAYS,
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        alignment=ft.MainAxisAlignment.START,
                    )
                ],
                scroll=ft.ScrollMode.ALWAYS,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            expand=True,
            height=400,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            padding=1,
            alignment=ft.alignment.top_left,
        )
        
        total_label = ft.Text(
            "Total: 0.00 JD",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN
        )
        
        def update_date_range_report(e):
            try:
                if not start_date_picker.value or not end_date_picker.value:
                    return

                start_str = start_date_picker.value.strftime("%Y-%m-%d")
                end_str = end_date_picker.value.strftime("%Y-%m-%d")
                is_admin1 = current_user.is_admin
                user_id1 = current_user.user_id
                user_name = current_user.username
               

                # Determine if we need to filter by user_id
                if is_admin1:
                    transactions, total = database.get_sales_by_date_range(start_str, end_str)
                else:
                    transactions, total = database.get_sales_by_date_range(start_str, end_str, user_id1)

                results_table.rows.clear()
                for trans_id, date, username, amount, items in transactions:
                    row = ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(date)),
                            ft.DataCell(ft.Text(username)),
                            ft.DataCell(ft.Text(items or "")),
                            ft.DataCell(ft.Text(f"{amount:.2f} JD")),
                        ],
                        on_select_changed=lambda e, row_data=(trans_id, date, username, amount, items): show_row_details(row_data)
                    )
                    results_table.rows.append(row)

                total_label.value = f"Total: {total:.2f} JD"
                page.update()

            except ValueError as e:
                print(f"Error: {e}")
                

        def export_to_excel(e):
            # Check if there are any rows in the table
            if len(results_table.rows) == 0:
                # Show a dialog if no data is available
                dia = ft.AlertDialog(
                    title=ft.Text("Export Error"),
                    content=ft.Text("No data available to export."),
                    actions=[
                        ft.TextButton("Close", on_click=lambda _: close_dialog(dia))
                    ]
                )
                page.overlay.append(dia)
                dia.open = True
                page.update()
                return

            # Prepare data for export
            export_data = [
                ["Date", "Username", "Items", "Amount"]  # Add headers
            ]
            for row in results_table.rows:
                # Extract cell values from the row
                row_data = [cell.content.value for cell in row.cells]
                export_data.append(row_data)

            # Create filename with current date
            filename = f"sales_report_{datetime.datetime.now().strftime('%y_%m_%d-%H-%M-%S')}.xlsx"

            async def save_file_result(e: ft.FilePickerResultEvent):
                if e.path:
                    try:
                        # Export to Excel
                        workbook = xlsxwriter.Workbook(e.path)
                        worksheet = workbook.add_worksheet()
                        
                        # Apply formatting to headers
                        header_format = workbook.add_format({
                            'bold': True, 
                            'bg_color': '#D3D3D3',  # Light gray background
                            'align': 'center'
                        })
                        
                        # Write data with headers
                        for row_index, row_data in enumerate(export_data):
                            for col_index, cell_value in enumerate(row_data):
                                if row_index == 0:
                                    # Apply header formatting
                                    worksheet.write(row_index, col_index, cell_value, header_format)
                                else:
                                    worksheet.write(row_index, col_index, cell_value)
                        
                        # Auto-adjust column widths
                        for col_index in range(len(export_data[0])):
                            worksheet.set_column(col_index, col_index, 15)
                        
                        workbook.close()

                        # Show success dialog
                        success_dialog = ft.AlertDialog(
                            title=ft.Text("Export Successful"),
                            content=ft.Text(f"Sales report exported to:\n{e.path}"),
                            actions=[ft.TextButton("OK", on_click=lambda _: close_dialog(success_dialog))],
                        )
                        
                        page.overlay.append(success_dialog)
                        success_dialog.open = True
                        page.update()

                    except Exception as ex:
                        # Show error dialog if export fails
                        error_dialog = ft.AlertDialog(
                            title=ft.Text("Export Error"),
                            content=ft.Text(f"Failed to export: {str(ex)}"),
                            actions=[ft.TextButton("OK", on_click=lambda _: close_dialog(success_dialog))],
                        )
                        page.dialog = error_dialog
                        error_dialog.open = True
                        page.update()

            # Create file picker
            file_picker = ft.FilePicker(
                on_result=save_file_result,
                # allow_multiple=False
            )
            
            # Add file picker to page
            page.overlay.append(file_picker)
            page.update()
            
            # Show save file dialog
            file_picker.save_file(
                allowed_extensions=["xlsx"],
                file_name=filename
            )

        

        reports_view = ft.View(
            "/reports",
            [
                ft.ResponsiveRow([
                    ft.Column([
                        ft.Row(
                    [
                        # Left icon
                        ft.IconButton(
                            icon=ft.Icons.ARROW_BACK,
                            icon_color=ft.Colors.BLUE,
                            on_click= lambda _: (page.clean(), page.go("/"))
                        ),
                        # Centered text
                        ft.Row(
                            [ft.Text("Sales Reports", size=30, weight=ft.FontWeight.BOLD)],
                            alignment=ft.MainAxisAlignment.CENTER,
                            expand=True
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                        
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Sales by Date Range", size=20, weight=ft.FontWeight.BOLD),
                                ft.ResponsiveRow([
                                    ft.Column([start_date_field], col={"sm": 12, "md": 6}),
                                    ft.Column([end_date_field], col={"sm": 12, "md": 6}),
                                    
                                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            ]),
                            bgcolor=ft.Colors.BLUE_50,
                            padding=5,
                            border_radius=10,
                            expand=True,
                            margin=ft.margin.only(bottom=10),
                        ),
                        ft.Container(
                            content=ft.Column([
                                ft.Text("Sales by User", size=20, weight=ft.FontWeight.BOLD),
                                ft.ResponsiveRow([
                                    ft.Column([user_dropdown], col={"sm": 12, "md": 6}),
                                ]),
                            ]),
                            bgcolor=ft.Colors.GREEN_50,
                            padding=5,
                            border_radius=10,
                            expand=True,
                            margin=ft.margin.only(bottom=10),
                        ),
                        ft.Container(
                            content=ft.Column([ft.Row([
            total_label,
            ft.ElevatedButton(
                "Export to Excel",
                on_click=export_to_excel,
                bgcolor=ft.Colors.GREEN,
                color=ft.Colors.WHITE,
            )
        ]),table_container
                            ],),
                            bgcolor=ft.Colors.GREY_50,
                            padding=0,
                            border_radius=10,
                            expand=True,
                        ),
                        
                    
                        
                        
                    ], scroll=ft.ScrollMode.ADAPTIVE, expand=True)
                ])
            ],
            padding=20,
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        
        return reports_view

    # Deletion History Screen
    def create_deletion_history_view():
        # Initialize date pickers for filtering
        start_date_picker = ft.DatePicker(
            on_change=lambda e: on_start_date_change(e),
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime(2100, 12, 31),
        )

        end_date_picker = ft.DatePicker(
            on_change=lambda e: on_end_date_change(e),
            first_date=datetime.datetime(2000, 1, 1),
            last_date=datetime.datetime(2100, 12, 31),
        )

        start_date_field = ft.TextField(
            label="Start Date",
            read_only=True,
            hint_text="Select Start Date",
            expand=True,
            on_click=lambda e: page.open(start_date_picker),
        )

        end_date_field = ft.TextField(
            label="End Date",
            read_only=True,
            hint_text="Select End Date",
            expand=True,
            on_click=lambda e: page.open(end_date_picker),
        )

        history_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Transaction ID")),
                ft.DataColumn(ft.Text("Transaction Date")),
                ft.DataColumn(ft.Text("Transaction User")),
                ft.DataColumn(ft.Text("Amount")),
                ft.DataColumn(ft.Text("Items")),
                ft.DataColumn(ft.Text("Deleted By")),
                ft.DataColumn(ft.Text("Deleted At")),
            ],
            rows=[],
            border=ft.border.all(1, ft.Colors.GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
            column_spacing=10,
            heading_row_height=20,
            data_row_min_height=50,
            heading_row_color=ft.Colors.BLUE_GREY_100,
        )


        table_container = ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [history_table],
                        scroll=ft.ScrollMode.ALWAYS,
                        expand=True,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        alignment=ft.MainAxisAlignment.START,
                    )
                ],
                scroll=ft.ScrollMode.ALWAYS,
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            expand=True,
            height=400,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            padding=1,
            alignment=ft.alignment.top_left,
        )

        total_label = ft.Text(
            "Total Deleted: 0.00 JD",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.RED
        )

        def on_start_date_change(e):
            selected_date = e.control.value
            if selected_date:
                start_date_field.value = selected_date.strftime("%Y-%m-%d")
                end_date_picker.first_date = selected_date
                if end_date_picker.value and end_date_picker.value < selected_date:
                    end_date_picker.value = None
                    end_date_field.value = ""
            else:
                start_date_field.value = ""
                end_date_picker.first_date = datetime.datetime(2000, 1, 1)
            page.update()
            if start_date_field.value and end_date_field.value:
                load_history()

        def on_end_date_change(e):
            selected_date = e.control.value
            if selected_date:
                end_date_field.value = selected_date.strftime("%Y-%m-%d")
            else:
                end_date_field.value = ""
            page.update()
            if start_date_field.value and end_date_field.value:
                load_history()

        def load_history():
            if not start_date_picker.value or not end_date_picker.value:
                return

            start_str = start_date_picker.value.strftime("%Y-%m-%d")
            end_str = end_date_picker.value.strftime("%Y-%m-%d")
            
            # Get deletion history
            history = database.get_deleted_transactions_history(start_str, end_str)
            
            # Update table
            history_table.rows.clear()
            total_deleted = 0.0
            
            for id, trans_id, trans_date, trans_user, amount, items, deleted_by, deleted_at in history:
                row = ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(trans_id))),
                        ft.DataCell(ft.Text(trans_date)),
                        ft.DataCell(ft.Text(trans_user)),
                        ft.DataCell(ft.Text(f"{amount:.2f} JD")),
                        ft.DataCell(ft.Text(items or "")),
                        ft.DataCell(ft.Text(deleted_by)),
                        ft.DataCell(ft.Text(deleted_at)),
                    ],
                )
                history_table.rows.append(row)
                total_deleted += amount
            
            total_label.value = f"Total Deleted: {total_deleted:.2f} JD"
            page.update()

        def go_back(e):
            page.go("/")

        def page_resize(e):
            history_table.width = page.window.width * 0.95
            page.update()

        page.on_resized = page_resize

        # Create the view
        history_view = ft.View(
            "/deletion_history",
            [
                ft.AppBar(
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=go_back),
                    title=ft.Text("Deletion History"),
                    center_title=False,
                ),
                ft.Container(
                    content=ft.Column([
                        ft.Row(
                            [
                                start_date_field,
                                end_date_field,
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        table_container,
                        total_label,
                    ], 
                    scroll=ft.ScrollMode.ADAPTIVE,
                    expand=True,
                    spacing=20,
                    )
                    
                )
            ],
            padding=20,
            
            scroll=ft.ScrollMode.ADAPTIVE,
        )

        return history_view

    # User Management Screen
    def create_user_management_view():
        users_list = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
        )

        def update_users_list():
            users_list.controls.clear()
            users = database.get_all_users()
            
            for user_id, username, is_admin in users:
                # Don't show toggle for current user
                if user_id == current_user.user_id:
                    continue
                    
                def create_switch(user_id, initial_state):
                    def handle_switch_change(e):
                        new_state = e.control.value
                        if database.update_user_admin_status(user_id, new_state):
                            e.control.value = new_state
                            page.show_snack_bar(
                                ft.SnackBar(content=ft.Text(f"Updated {username}'s admin status"))
                            )
                        else:
                            e.control.value = not new_state
                            page.show_snack_bar(
                                ft.SnackBar(content=ft.Text("Failed to update user status"))
                            )
                        page.update()
                    
                    return ft.Switch(
                        value=bool(initial_state),  # Convert to boolean
                        label="Admin",
                        on_change=handle_switch_change
                    )
                
                admin_switch = create_switch(user_id, is_admin)
                
                users_list.controls.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column([
                                ft.ListTile(
                                    leading=ft.Icon(ft.Icons.PERSON),
                                    title=ft.Text(username),
                                    trailing=admin_switch
                                ),
                            ]),
                            padding=10
                        )
                    )
                )
            page.update()

        view = ft.View(
            "/users",
            [
                ft.AppBar(
                    leading=ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda _: page.go("/")),
                    title=ft.Text("User Management"),
                    center_title=False,
                ),
                users_list,
            ],
            scroll=ft.ScrollMode.ADAPTIVE,
        )
        
        update_users_list()
        return view

    # Home Screen (POS)
    def create_home_view(is_admin=False):
        database.init_db()
        menu_items = database.get_menu_items()

        total_cost = ft.Ref[float]()
        total_cost.current = 0.0

        # Create a reference to the date_time_label
        date_time_label = ft.Text(
            f"Date & time: {datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')}",
            size=18,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREEN_500,
            text_align=ft.TextAlign.CENTER
        )

        # Async function to update time continuously
        async def update_time_task():
            while True:
                # Update the label with current time
                date_time_label.value = f"Date & time: {datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')}"
                page.update()
                
                # Wait for 1 second before next update
                await asyncio.sleep(1)

        # Start the time update task
        page.run_task(update_time_task)
        
        total_cost = ft.Ref[float]()
        total_cost.current = 0.0
        date_time_label = ft.Text(
        f"Date & time: {datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')}",
        size=18,
        color=ft.Colors.WHITE,
        bgcolor=ft.Colors.GREEN_500,
        text_align=ft.TextAlign.CENTER
    )

        logo = ft.Image(
            src="logo.png",
            width=30,
            height=30,
            fit=ft.ImageFit.CONTAIN
        )

        restaurant_label = ft.Text(
            "Boss Restaurant",
            size=24,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE,
            text_align=ft.TextAlign.CENTER
        )

        user_label = ft.Text(
            f"Welcome, {current_user.username}",
            size=18,
            color=ft.Colors.GREEN,
            text_align=ft.TextAlign.CENTER
        )

        date_time_label = ft.Text(
            f"Date & time: {datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')}",
            size=18,
            color=ft.Colors.WHITE,
            bgcolor=ft.Colors.GREEN_500,
            text_align=ft.TextAlign.CENTER
        )

        item_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=20,
            auto_scroll=True
        )

        total_label = ft.Text(
            "Total: 0.00 JD",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREEN_500
        )

        

        def add_item(item, price):
            
            def show_quantity_dialog(e):
                
                def handle_quantity(e):
                   

                    try:
                       
                        quantity = int(quantity_input.value)
                        if 1 <= quantity <= 100:
                            total_price = price * quantity
                            item_text = f"{item} X {quantity} = {total_price:.2f} JD"
                            for row in item_list.controls:
                                if item in row.controls[0].value:
                                    existing_quantity = int(row.controls[0].value.split('X')[1].split('=')[0].strip())
                                    new_quantity = existing_quantity + quantity
                                    new_total_price = price * new_quantity
                                    row.controls[0].value = f"{item} X {new_quantity} = {new_total_price:.2f} JD"
                                    total_cost.current += total_price
                                    total_label.value = f"Total: {total_cost.current:.2f} JD"
                                    total_label.update()
                                    item_list.update()
                                    quantity_dialog.open = False
                                    quantity_dialog.update()
                                    page.update()
                                    return
                            def delete_this_item(del_e):
                                item_list.controls.remove(item_row)
                                total_cost.current -= total_price
                                total_label.value = f"Total: {total_cost.current:.2f} JD"
                                total_label.update()
                                item_list.update()
                                page.update()

                            item_row = ft.Row([
                                ft.Text(item_text, expand=True),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color=ft.Colors.RED,
                                    on_click=delete_this_item
                                )
                            ])
                            
                            item_list.controls.append(item_row)
                            total_cost.current += total_price
                            total_label.value = f"Total: {total_cost.current:.2f} JD"
                            
                            total_label.update()
                            item_list.update()
                            quantity_dialog.open = False
                            quantity_dialog.update()
                            page.update()
                        else:
                            raise ValueError("Quantity must be between 1 and 100")
                    except ValueError:
                        quantity_input.error_text = "Invalid quantity"
                        quantity_dialog.update()

                quantity_input = ft.TextField(label="Quantity", value="1", keyboard_type=ft.KeyboardType.NUMBER)
               
                
                def handle_close(e):
                    page.close(quantity_dialog)
                def increment_quantity(e):
                    current_value = int(quantity_input.value)
                    quantity_input.value = str(current_value + 1)
                    quantity_input.update()

                # Function to handle decrementing the quantity
                def decrement_quantity(e):
                    current_value = int(quantity_input.value)
                    if current_value > 1:  # Ensure quantity doesn't go below 1
                        quantity_input.value = str(current_value - 1)
                        quantity_input.update()
               
                quantity_dialog = ft.AlertDialog(
        title=ft.Text(f"Enter quantity for {item}"),
        content=ft.Container(
            content=ft.Column(
                [
                    quantity_input,
                    ft.Row(
                        [
                            ft.IconButton(ft.Icons.REMOVE, on_click=decrement_quantity),
                            ft.IconButton(ft.Icons.ADD, on_click=increment_quantity),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=200,
            height=150,
            alignment=ft.alignment.center,
        ),
        actions=[
            ft.TextButton("OK", on_click=handle_quantity),
            ft.TextButton("Cancel", on_click=handle_close),
        ],
    )
                page.overlay.append(quantity_dialog)
                quantity_dialog.open = True
                page.update()

            return show_quantity_dialog

        def new_check(e):
            if len(item_list.controls) > 0:
                items = []
                for item_row in item_list.controls:
                    item_text = item_row.controls[0].value
                    name = item_text.split(" X ")[0]
                    quantity = int(item_text.split(" X ")[1].split(" = ")[0])
                    price = float(item_text.split(" = ")[1].replace(" JD", ""))
                    items.append({
                        "name": name,
                        "quantity": quantity,
                        "price": price
                    })
                
                transaction_id = database.create_transaction(current_user.user_id, items, total_cost.current)
                
                if transaction_id:
                    bill_summary = generate_bill_summary(items, total_cost.current, transaction_id)
                    show_bill_dialog(bill_summary)
                
                item_list.controls.clear()
                total_cost.current = 0
                total_label.value = "Total: 0.00 JD"
                total_label.update()
                item_list.update()
                page.update()
        def generate_bill_summary(items, total_amount, transaction_id):
            bill_lines = []
            bill_lines.append(f"Transaction ID: {transaction_id}")
            bill_lines.append("Items:")
            for item in items:
                bill_lines.append(f"{item['name']} X {item['quantity']} = {item['price'] * item['quantity']} JD")
            bill_lines.append(f"Total: {total_amount} JD")
            return "\n".join(bill_lines)

        def show_bill_dialog(bill_summary):
            def close_dialog(e):
                bill_dialog.open = False
                page.update()
            timestamp = datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')    
            
            bill_dialog = ft.AlertDialog(
                title=ft.Text(f"Bill Summary - {timestamp}",size=11, weight=ft.FontWeight.BOLD),
                content=ft.Text(bill_summary),
                actions=[
                    ft.TextButton("Close", on_click=close_dialog)
                ]
            )
            
            
            page.overlay.append(bill_dialog)
            bill_dialog.open = True
            page.update()
        def logout(e):
            current_user.user_id = None
            current_user.username = None
            page.go("/login")

        def go_to_reports(e):
            page.go("/reports")
        


        menu_grid = ft.GridView(
    expand=False,
    runs_count=4,
    max_extent=70,
    child_aspect_ratio=1.0,
    spacing=10,
    run_spacing=10,
)


        for item, price in menu_items:
            menu_grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(item, size=12, weight=ft.FontWeight.BOLD),
                            ft.Text(f"{price:.2f} JD", size=14),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER, 
                        spacing=5,
                    ),
                    bgcolor=ft.Colors.BLUE_100,
                    border_radius=10,
                    on_click=add_item(item, price),
               
                    ink=True,
                )
            )

        def show_db_path(e):
            db_path = database.get_db_path()
            dia = ft.AlertDialog(
                title=ft.Text("Database Location"),
                content=ft.Column([
                    ft.Text("Your database is located at:"),
                    ft.Text(db_path),  # Makes the path copyable
                    ft.Text("\nNote: You may need a file explorer app with root access to view this file."),
                ], tight=True),
                actions=[
                    ft.TextButton("OK", on_click=lambda _: close_dialog(dia)),
                ],
            )
            page.overlay.append(dia)
            dia.open = True
            page.update()
        def backup_database_dialog(e):
            def share_backup(e):
                database.backup_database(page)  # Pass the page parameter to backup_database

            dia = ft.AlertDialog(
                title=ft.Text("Backup Database"),
                content=ft.Text("Choose where to save the database backup."),
                actions=[
                    ft.TextButton("Cancel", on_click=lambda _: close_dialog(dia)),
                    ft.TextButton("Create Backup", on_click=share_backup),
                ],
            )
            page.overlay.append(dia)
            dia.open = True
            page.update()
    

        if is_admin:
           
            admin_buttons = ft.Row(
                [
                    ft.ElevatedButton(
                        "Manage Items",
                        on_click=lambda _: page.go("/items"),
                        bgcolor=ft.Colors.ORANGE,
                        color=ft.Colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        "Deletion History",
                        on_click=lambda _: page.go("/deletion_history"),
                        bgcolor=ft.Colors.RED,
                        color=ft.Colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        "User-Admin",
                        on_click=lambda _: page.go("/users"),
                        bgcolor=ft.Colors.PURPLE,
                        color=ft.Colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        "Show DB Path",
                        on_click=show_db_path,
                        bgcolor=ft.Colors.TEAL,
                        color=ft.Colors.WHITE,
                    ),
                    ft.ElevatedButton(
                        "Backup Database",
                        on_click=backup_database_dialog,
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            page.add(admin_buttons)

        # Create category grid
        category_grid = ft.GridView(
            expand=False,
            runs_count=4,
            max_extent=70,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
        )

        # Create menu grid (your existing grid)
        # menu_grid = ft.GridView(
        #     expand=1,
        #     runs_count=5,
        #     max_extent=70,
        #     child_aspect_ratio=1.0,
        #     spacing=10,
        #     run_spacing=10,
        # )

        # Function to update menu items based on category
        def on_category_click(e, category_id):
            menu_grid.controls.clear()
            items = database.fetch_items_by_category(category_id)

            # Update menu grid with filtered items
            for item_name, item_price in items:
                print(type(item_price))
                menu_grid.controls.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(item_name, size=16, weight=ft.FontWeight.BOLD),

                                ft.Text(f"{item_price:.2f} JD", size=14),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        width=150,
                        height=150,
                        bgcolor=ft.Colors.BLUE_100,
                        border_radius=10,
                        ink=True,
                        on_click=add_item(item_name, item_price),
                    )
                )
            menu_grid.update()

        # Populate category grid
        categories = database.fetch_all_categories()
        
        for cat_id, cat_name in categories:
            category_grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(cat_name, 
                                   size=16, 
                                   weight=ft.FontWeight.BOLD,
                                   text_align=ft.TextAlign.CENTER),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    width=150,
                    height=150,
                    bgcolor=ft.Colors.ORANGE_100,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e, cid=cat_id: on_category_click(e, cid),
                )
            )

        
        home_view = ft.View(
    "/",drawer= ft.NavigationDrawer(on_change=handle_change,controls=[
            ft.Container(height=12),
            ft.Row(
        controls=[ft.ElevatedButton(
        content=ft.Text("P.O.S ", size=15, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
        style=ft.ButtonStyle(
            shape=ft.CircleBorder(),
            padding=5,
            bgcolor=ft.Colors.BLUE,
        ),
       on_click=lambda _: page.go("/")),], alignment=ft.MainAxisAlignment.CENTER,
    ),
            ft.NavigationDrawerDestination(
                label="Reports",
                icon=ft.Icons.ASSESSMENT,
                selected_icon_content=ft.Icon(ft.Icons.ASSESSMENT, color=ft.Colors.BLUE),

            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                label="User Management",
                icon=ft.Icons.PERSON,
                selected_icon_content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE),

            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                
                icon_content=ft.Icon(ft.Icons.INVENTORY, color=ft.Colors.BLUE),
                label="Manage Items",
                selected_icon=ft.Icons.INVENTORY
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
    
                icon_content=ft.Icon(ft.Icons.DELETE, color=ft.Colors.BLUE),
                label="Deletion History",
                selected_icon=ft.Icons.DELETE
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.Icons.TELEGRAM, color=ft.Colors.BLUE),
                label="Contact Us",
                selected_icon=ft.Icons.TELEGRAM,
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.BLUE),
                label="Logout",
                selected_icon=ft.Icons.TELEGRAM,
            )
        ]),controls=[*([ft.AppBar(title = ft.Row(controls = [ft.Text("Ideal Body Weighe (IBW)",
                    size=15,color=ft.Colors.WHITE,expand = True,),])
                ,bgcolor = ft.Colors.BLUE_800,)]if is_admin
                                            else [])
    
        ,ft.Column(
            [
                # ResponsiveRow for restaurant_label, logo, user_label
                ft.ResponsiveRow(
                    controls=[
                        ft.Container(content=restaurant_label, col={"xs": 12, "sm": 4, "md": 4}),
                        ft.Container(content=logo, col={"xs": 12, "sm": 4, "md": 4}),
                        ft.Container(content=user_label, col={"xs": 8, "sm": 2, "md": 2}),
                    ],
                    alignment="center",
                    vertical_alignment="center",
                ),
                # Other elements in the screen
                date_time_label,

                category_grid,
                menu_grid,
                ft.Column(
                    [
                        item_list,
                        total_label,
                        ft.ResponsiveRow(
                            controls=[
                                create_responsive_button("New Check", new_check),
                                create_responsive_button("Reports", go_to_reports, ft.Colors.BLUE),
                               
                                # Conditionally add Manage Items and Deletion History buttons
                                
                            ],
                            alignment="center",  # Center align buttons
                        ),
                    ],
                    expand=True,
                ),
            ],
            expand=True,  # Expand the column to fill available space
            spacing=10,   # Add spacing between elements
        )
    ],
    scroll=ft.ScrollMode.ADAPTIVE,  # Enable scrolling for the view
)

 
        return home_view

    def route_change(route):
        page.views.clear()
        
        if page.route == "/login" or not page.route:
            page.views.append(create_login_view())
            
        elif page.route == "/":
            page.views.append(create_home_view(current_user.is_admin))
            
        elif page.route == "/reports":
            page.views.append(create_home_view(current_user.is_admin))
            page.views.append(create_reports_view())
            
        elif page.route == "/deletion_history":
            page.views.append(create_home_view(current_user.is_admin))
            page.views.append(create_deletion_history_view())
            
        elif page.route == "/items":
            page.views.append(create_home_view(current_user.is_admin))
            page.views.append(create_items_view())
            
        elif page.route == "/register":
            page.views.append(create_register_view())
            
        elif page.route == "/users":
            page.views.append(create_home_view(current_user.is_admin))
            page.views.append(create_user_management_view())
            
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    # Set up event handlers
    page.on_keyboard_event = handle_keyboard_event
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Start with login route
    page.go("/login")

ft.app(target=main)