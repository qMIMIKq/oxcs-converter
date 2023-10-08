import os

config = {
    "app_addr": os.getenv("APP_ADDR"),
    "main_app_port": os.getenv('MAIN_APP_PORT'),
    "main_app_host": os.getenv('MAIN_APP_HOST'),
}
