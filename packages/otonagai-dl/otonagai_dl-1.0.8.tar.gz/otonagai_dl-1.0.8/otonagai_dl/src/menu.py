from InquirerPy import inquirer
from .controller import search_table_navigation, log_table_navigation
import sys
from .hobby_link_jp_scraper.hlj_ui import HLJ_scraper_ui
from .model import gunpla_log_db, gunpla_search_db, web_to_db_bridge
from .view import Search_Table_View, Log_Table_View
from .utils import (
    use_edit_file,
    add_to_search_db,
    extract_urls_from_file,
    get_product_info_from_urls
)
from rich.console import Console
from .log_system import log_msg
import os


def menu():

    # create the data folder to contain the db

    # create objects for the search database and log database
    search_db = gunpla_search_db()
    log_db = gunpla_log_db()
    console = Console()

    while True:

        os.system("cls" if os.name == "nt" else "clear")
        menu_choice = inquirer.select(
            message="Welcome to Otonagai. \n\n Please select any option to proceed",
            choices=[
                "Merchandise Database",
                "Merchandise Log",
                "Extract Merch info",
                "URLs to download",
                "Exit",
            ],
            vi_mode=True,
        ).execute()

        log_msg(f'Selected "{menu_choice}"')

        if menu_choice == "Merchandise Database":

            os.system("cls" if os.name == "nt" else "clear")

            # Open up the search database
            search_view = Search_Table_View(search_db.view_table())
            search_table_navigation(
                console=console, model=search_db, view=search_view
            ).navigate_table()

        elif menu_choice == "Merchandise Log":

            os.system("cls" if os.name == "nt" else "clear")

            # Open up the log database
            log_view = Log_Table_View(log_db.view_table())
            log_table_navigation(
                model=log_db, view=log_view, console=console
            ).navigate_table()

        elif menu_choice == "URLs to download":
            os.system("cls" if os.name == "nt" else "clear")
            # open the file that contains the urls
            use_edit_file(inquirer)

        elif menu_choice == "Exit":

            sys.exit()

        # Extract the product info from the product urls
        elif menu_choice == "Extract Merch info":
            os.system("cls" if os.name == "nt" else "clear")

            text_urls = extract_urls_from_file()
            full_urls = get_product_info_from_urls(text_urls)

            # add all the product information to the search database
            add_to_search_db(
                extracted_urls=full_urls,
                scraper_ui=HLJ_scraper_ui(),
                search_db_conn=web_to_db_bridge(),
            )
