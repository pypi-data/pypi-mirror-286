import sqlite3
from InquirerPy import inquirer
import time
from .log_system import log_msg
from .utils import DB_PATH

status_priority = """
            CASE 
            WHEN status = "Planning" THEN 1
            WHEN status = "Acquired" THEN 2
            WHEN status = "Building" THEN 3
            WHEN status = "Completed" THEN 4
            WHEN status = "On Hold" THEN 5
            WHEN status = "Dropped" THEN 6
            END ASC
"""
search_table_name = "oto_collection"
log_table_name = "oto_log"


def collect_options_from_db(choice_dict):

    category_dict = {}
    for category in choice_dict:
        if category[0] not in category_dict:
            category_dict[str(category[0])] = None

    category_dict["All"] = None
    return category_dict


def advanced_search(categories, item_types, series, manufacturer):
    search_title = inquirer.text(
        "Which product you want to search ?", mandatory=True
    ).execute()

    search_category = inquirer.text(
        message="Which category ? (Press Shift to open options)",
        completer=categories,
        mandatory=True,
    ).execute()

    search_item_type = inquirer.text(
        message="Which item type ? (Press Shift to open options)",
        completer=item_types,
        mandatory=True,
    ).execute()

    search_series = inquirer.text(
        message="From which series ? (Press Shift to open options)",
        completer=series,
        mandatory=True,
    ).execute()

    search_manufacturer = inquirer.text(
        message="From which manufacturer ? (Press Shift to open options)",
        completer=manufacturer,
        mandatory=True,
    ).execute()

    return (
        search_title,
        search_category,
        search_item_type,
        search_series,
        search_manufacturer,
    )


class web_to_db_bridge:

    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()

    def remove_any_duplicates(self, new_url):

        self.cursor.execute(f"select url from {search_table_name}")
        existing_url = {link[0].strip() for link in self.cursor.fetchall()}
        new_url = set(new_url)

        return list(new_url - existing_url)

    def insert_to_table(self, products):

        for product in products:
            log_msg(f"Inserting info for {product['URL']}")

            try:
                self.cursor.execute(
                    f"INSERT INTO {search_table_name} (title, url, code, jan_code, release_date, category, series, item_type, manufacturer, item_size_and_weight) VALUES (?,?,?,?,?,?,?,?,?,?)",
                    (
                        product["Title"],
                        product["URL"],
                        product["Code"],
                        product["JAN Code"],
                        product["Release Date"],
                        product["Category"],
                        product["Series"],
                        product["Item Type"],
                        product["Manufacturer"],
                        product["Item Size/Weight"],
                    ),
                )
                log_msg(f"Inserting {product['Title']}")
            except sqlite3.IntegrityError:
                log_msg(f'{product["URL"]} already exists in the database')
                break
            except KeyError:
                break
        time.sleep(3)
        self.connection.commit()


class gunpla_search_db:

    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {search_table_name} (title text, URL text, code text not null primary key, jan_code text, release_date date, category text, series text, item_type text, manufacturer text, item_size_and_weight text)"
        )

    def advanced_view_table(self):
        search_category = collect_options_from_db(
            self.cursor.execute(f"select category from {search_table_name}")
        )
        item_type_category = collect_options_from_db(
            self.cursor.execute(f"select item_type from {search_table_name}")
        )
        series_category = collect_options_from_db(
            self.cursor.execute(f"select series from {search_table_name}")
        )

        manufacturer_category = collect_options_from_db(
            self.cursor.execute(f"select manufacturer from {search_table_name}")
        )

        title, category, item_type, series, manufacturer = advanced_search(
            search_category, item_type_category, series_category, manufacturer_category
        )

        with self.connection:
            self.cursor.execute(
                f"SELECT code, title, series, item_type, manufacturer , release_date from {search_table_name} where title like ? and category like ? and item_type like ? and series like ?  and manufacturer like ? order by release_date desc;",
                (
                    f"%{title}%",
                    f"%{category if category != 'All' else ''}%",
                    f"%{item_type if item_type != 'All' else ''}%",
                    f"%{series if series != 'All' else ''}%",
                    f"%{manufacturer if manufacturer != 'All' else ''}%",
                ),
            )

            self.result = self.cursor.fetchall()

            return self.result

    def view_table(self):

        with self.connection:
            self.cursor.execute(
                f"SELECT code, title, series, item_type, manufacturer , release_date from {search_table_name} order by release_date desc;",
            )

            self.result = self.cursor.fetchall()

            return self.result

    def insert_to_table(self, Code, Title, item_type):
        log_state = inquirer.select(
            "Please confirm state of task",
            [
                "Planning",
                "Acquired",
                "Building",
                "Completed",
                "On Hold",
                "Dropped",
            ],
        ).execute()

        with self.connection:

            self.cursor.execute(f"select count(*) from {log_table_name}")
            count_log = self.cursor.fetchone()[0]
            log_id = count_log + 1

            self.cursor.execute(
                f"INSERT into {log_table_name} (log_id, code, title, item_type, status) VALUES (?,?,?,?,?)",
                (
                    log_id,
                    Code,
                    Title,
                    item_type,
                    log_state,
                ),
            )
            log_msg(f"Adding {Title} to log with current status {log_state}")


class gunpla_log_db:

    def __init__(self):
        self.connection = sqlite3.connect(DB_PATH)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {log_table_name} (log_id integer, code text, title text, item_type text, status text)"
        )

    def view_table(self):
        with self.connection:
            self.cursor.execute(
                f"select * from {log_table_name} order by {status_priority}"
            )
            # log_result = self.cursor.fetchall()
            return self.cursor.fetchall()

    def refresh_table_positions(self, old_placement, new_placement):
        with self.connection:
            self.cursor.execute(
                f"UPDATE {log_table_name} set log_id = ? where log_id = ?",
                (new_placement, old_placement),
            )

    def update_table(self, log_id, name):
        log_state = inquirer.select(
            message=f'Please confirm state of task for the product : "{name}"',
            choices=[
                "Planning",
                "Acquired",
                "Building",
                "Completed",
                "On Hold",
                "Dropped",
            ],
        ).execute()

        # current_status = self.cursor.execute(f"Select status from {log_table_name} where log_id = ?",log_id)

        with self.connection:
            self.cursor.execute(f"Select status from {log_table_name} where log_id = ?",
                                                 (log_id,),)
            current_status = self.cursor.fetchone()[0]

            self.cursor.execute(
                f"UPDATE {log_table_name} set status = ? where log_id = ?",
                (
                    log_state,
                    log_id,
                ),
            )
        log_msg(f"Changing status for {name} from \"{current_status}\" to \"{log_state}\"")
        return True

    def delete_from_table(self, log_id, name):
        if inquirer.confirm(
            f'Do you want to delete "{name}" from this entry ?'
        ).execute():
            with self.connection:
                self.cursor.execute(f"select count(*) from {log_table_name}")
                total_count = self.cursor.fetchone()[0]

                if log_id is not None:
                    self.cursor.execute(
                        f"DELETE from {log_table_name} where log_id = ?",
                        (log_id,),
                    )

                    for log_no in range(log_id, total_count + 1):
                        self.refresh_table_positions(log_no, log_no - 1)
                    log_msg(f"Deleted {name} from the log")

        return True
