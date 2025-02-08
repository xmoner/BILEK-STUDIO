import flet as ft
import platform
import os
import database
# import asyncio
#from zoneinfo import ZoneInfo  # Add timezone support
import datetime

# Set timezone to Jordan/Amman
#TIMEZONE = ZoneInfo("Asia/Amman")


# poetry run flet run -d

# Request Android permissions if needed
def request_android_permissions(page: ft.Page):
    if platform.system() == 'Android':
        # Request storage permissions
        page.client_storage.set("android_storage_permission", "true")
        # Create POS directory in external storage
        pos_dir = '/storage/emulated/0/POS'
        os.makedirs(pos_dir, exist_ok=True)
class User:
    def __init__(self, user_id=None, username=None,is_admin=None, nickname=None):
        self.user_id = user_id
        self.username = username
        self.is_admin=is_admin
        self.nickname=nickname

current_user = User()


def main(page: ft.Page):
    # Request permissions at app startup
    request_android_permissions(page)
    page.window.width=400
    page.title = "Ahoy"
    page.window.always_on_top = True



    # page.add(ft.TextField(label="Username", width=300))
    # page.add(ft.TextField(label="Password", password=True, width=300))
    # page.add(ft.TextField(label="Confirm Password", password=True, width=300))
    # page.update()

    # def create_home_view():
    #     database.init_db()
    #
    #     menu_items = database.get_menu_items()
    #
    #     total_cost = ft.Ref[float]()
    #     total_cost.current = 0.0
    #
    #     # Create a reference to the date_time_label
    #     date_time_label = ft.Text(
    #         f"Date & time: {datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')}",
    #         size=18,
    #         color=ft.Colors.WHITE,
    #         bgcolor=ft.Colors.GREEN_500,
    #         text_align=ft.TextAlign.CENTER
    #     )
    #
    #     # Async function to update time continuously
    #     async def update_time_task():
    #         while True:
    #             # Update the label with current time
    #             date_time_label.value = f"Date & time: {datetime.datetime.now(TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')}"
    #             page.update()
    #
    #             # Wait for 1 second before next update
    #             await asyncio.sleep(1)
    #
    #     # Start the time update task
    #     page.run_task(update_time_task)



    def create_register_view():
        # A page for registration
        #username_field = ft.TextField(label="Username", width=300)
        email_field = ft.TextField(label="Email", width=300)
        password_info = ft.Text("Minimum 6 characters for the Password.")
        password_field = ft.TextField(label="Password", password=True, width=300, can_reveal_password=True)
        confirm_password = ft.TextField(label="Confirm Password", password=True, width=300, can_reveal_password=True, )
        error_text = ft.Text("", color=ft.Colors.RED_300)

        def try_register(e):
            if password_field.value != confirm_password.value:
                error_text.value = 'Password does not match!\nPlease try it again!'
                error_text.color = ft.Colors.RED_300
                page.update()
                return

            elif not password_field.value or not confirm_password.value:
                error_text.value = 'Password is empty!\nPlease add a password!'
                error_text.color = ft.Colors.RED_300
                page.update()
                return

            elif not email_field.value or '@' not in email_field.value:
                error_text.value = 'Email is empty!\nPlease add it!'
                error_text.color = ft.Colors.RED_300
                page.update()
                return

            if len(password_field.value) < 6:
                error_text.value = "Your password is too short!"
                error_text.color = ft.Colors.RED_300
                page.update()
                return

            # if passwords match,change text to green colour
            # elif password_field.value == confirm_password.value:
            #     error_text.value = 'Passwords match!'
            #     error_text.color = ft.Colors.GREEN
            #     page.update()
            #     return

            # {'username': 'test',
            #          'password': 'aaa',
            #          'is_admin': True,
            #          'email': 'lucas.bilek@gmail.com',
            #          'user_id_auth':user.session.user.id}

            reg_result = database.register_user( # username=username_field.value,
                                      users_password=password_field.value,
                                      users_email=email_field.value)
            result = reg_result
            print('result', result)
            if result[0]:
                print('true',True)
                print('reg_result[1]',reg_result[1])
                error_text.value = reg_result[1]
                error_text.color = ft.Colors.GREEN_300

                page.update()

                #page.go("/login")
            else:
                error_text.value = reg_result[1]
                print('false', False)
                page.update()
                return

        def go_to_login(e):
            page.go('/login')

        register_view = ft.View("/register",
                             [
                                 ft.Column(
                                     [
                                         ft.Text("Register a New User", size=15, weight=ft.FontWeight.BOLD),
                                         #username_field,
                                         email_field,
                                         password_info,
                                         password_field,
                                         confirm_password,
                                         error_text,
                                         ft.Row(
                                             [
                                                 ft.ElevatedButton("Register", on_click=try_register,
                                                                   bgcolor=ft.Colors.GREEN),
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

    def handle_keyboard_event(event):
        if event.key == 'go_back' or event.key == 'Escape':
            if page.route != "/":
                page.go("/")

    def create_home_view():
        """
        Create the home view
        Returns:

        """



        return ft.View(
            "/",
            [
                ft.Column(
                    [
                        ft.Text("Welcome to Ahoy!", size=30, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Hello, {current_user.nickname}!", size=20),
                        # ft.Text(f"Hello, {current_user.nickname}!", size=20),
                        # ft.Text(f"Hello, {current_user.is_admin}!", size=20),
                        # ft.Text("This is the home page", size=20),
                        # ft.Text("You can add more views to this page to create your app"),

                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                )],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            vertical_alignment=ft.MainAxisAlignment.CENTER
        )



    def create_nickname_view():
        # A page for registration

        text = ft.Text("Add a nick name.\nGreen colour means it is valid.", color=ft.Colors.GREEN)

        exists_nick_name = False

        def on_nick_name_change(e):
            print('e.control.value', e.control.value)
            response=database.check_nick_name(e.control.value)
            if response:
                # Change text color to red if the password is invalid
                e.control.color = ft.Colors.RED
                e.control.border_color = ft.Colors.RED  # Change border color to green
                e.control.update()
                return False
            else:
                # Change text color to green if the password is valid
                e.control.color = ft.Colors.GREEN
                e.control.border_color = ft.Colors.GREEN
                e.control.update()
                return e.control.value
        nickname = ft.TextField(label="Nickname", width=300,
                                 on_change=on_nick_name_change)

        def try_register_nickname(e):
            if nickname:
                reg_nickname=database.register_nickname(nickname.value, current_user.user_id)
                print('nickname.value:', nickname.value)
                if reg_nickname:
                    # Go back to the login page after choosing a nickname
                    page.go("/login")
                    page.update()

        def go_to_home(e):
            page.go('/')

        home_view = ft.View("/nickname",
                            [
                                ft.Column(
                                    [
                                        ft.Text("Please fill Nickname: ", size=15, weight=ft.FontWeight.BOLD),
                                        # username_field,
                                        text,
                                        nickname,
                                        ft.Row([ft.ElevatedButton("Save", on_click=try_register_nickname,
                                                          bgcolor=ft.Colors.GREEN),
                                                # ft.ElevatedButton("Skip it", on_click=go_to_home,
                                                #                    bgcolor=ft.Colors.RED)
                                               ],alignment=ft.MainAxisAlignment.CENTER)],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                )
                            ],
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            vertical_alignment=ft.MainAxisAlignment.CENTER
                            )
        return home_view

        # Login Screen
    def create_login_view():
        email_field = ft.TextField(
            label="email",
            width=300,
            value='lucas.bilek.work@gmail.com' # Temporary value for testing
        )
        password_field = ft.TextField(
            label="Password",
            password=True,  # Specify this only once
            width=300,
            can_reveal_password=True,
            value='aaaaaa' # Temporary value for testing
        )
        error_text = ft.Text("", color=ft.Colors.RED)

        def try_login(e):
            # Check if user exists in the database
            user = database.check_login(email_field.value, password_field.value)
            print('try_login - user:', user)
            if user:
                current_user.user_id = user[0]['user_id']
                print('current_user.user_id:', current_user.user_id)
                current_user.username = user[0]['username']
                print('current_user.username:', current_user.username)
                current_user.is_admin = user[0]['is_admin']
                print('current_user.is_admin:', current_user.is_admin)
                current_user.nickname = user[0]['nickname']
                print('current_user.nickname:', current_user.nickname)

                if current_user.nickname != 'None':
                    page.go("/")
                    page.update()
                else:
                    page.go("/nickname")  # Navigate to the nickname page
                    page.update()
            else:
                error_text.value = "Invalid username or password"
                page.update()
            #
            # # Verify login credentials
            # user = database.verify_login(email_field.value, password_field.value, is_admin)
            #
            # if user:
            #     current_user.user_id = user['user_id']
            #     current_user.username = user['username']
            #     current_user.is_admin = user['is_admin']
            #     page.go("/")  # Navigate to the home page
            # else:
            #     error_text.value = "Invalid username or password"
            #     page.update()
        def reset_password(e):
            reset_result=database.reset_password(email_field.value)
            error_text.value = reset_result
            error_text.color = ft.Colors.YELLOW
            page.update()
            return
        def go_to_register(e):
            page.go("/register")

        login_view = ft.View(
            "/login",
            [
                ft.Column(
                    [
                        ft.Text("Login", size=15, weight=ft.FontWeight.BOLD),
                        email_field,
                        password_field,
                        # ft.Row(
                        #     [admin_checkbox],
                        #     alignment=ft.MainAxisAlignment.CENTER
                        # ),
                        error_text,
                        ft.ElevatedButton("Reset Password", on_click=reset_password),
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

    def route_change(route):
        page.views.clear()

        if page.route == "/login" or not page.route:
             page.views.append(create_login_view())

        elif page.route == "/":
            page.views.append(create_home_view()) # page.views.append(create_home_view()) #

        elif page.route == "/nickname":
            page.views.append(create_nickname_view())
        # elif page.route == "/reports":
        #     page.views.append(create_home_view(current_user.is_admin))
        #     page.views.append(create_reports_view())
        #
        # elif page.route == "/deletion_history":
        #     page.views.append(create_home_view(current_user.is_admin))
        #     page.views.append(create_deletion_history_view())
        #
        # elif page.route == "/items":
        #     page.views.append(create_home_view(current_user.is_admin))
        #     page.views.append(create_items_view())

        elif page.route == "/register":
            page.views.append(create_register_view())

        # elif page.route == "/users":
        #     page.views.append(create_home_view(current_user.is_admin))
        #     page.views.append(create_user_management_view())

        page.update()


    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
        print("top_view", top_view, top_view.route)


    # Set up event handlers
    page.on_keyboard_event = handle_keyboard_event
    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # Start with login route
    page.go("/login")
    #     page.go("/register")
    """
    def try_register(e):
        if password_field.value != confirm_password.value:
            error_text.value = "Passwords do not match"
            page.update()
            return

        # if database.register_user(username_field.value, password_field.value):
        #     page.go("/login")
        # else:
        #     error_text.value = "Username already exists"
        #     page.update()

    def go_to_login(e):
        page.go("/login")

    ft.View(
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
    """

ft.app(main)