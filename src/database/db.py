import sqlite3


class BotDB:
    def __init__(self, db_file: str) -> None:
        self.conn = sqlite3.connect(database=db_file)
        self.cursor = self.conn.cursor()

    # check if user exist
    def user_exists(self, unique_id: int) -> bool:
        query = self.cursor.execute(
            """
            SELECT 
              unique_id
            FROM 
              users
            WHERE 
              unique_id = ?
            """,
            (unique_id,)
        )

        return bool(len(query.fetchall()))

    # adding user
    def add_user(self, user: dict) -> None:
        self.cursor.execute(
            """
            INSERT INTO 
              users (unique_id, username, registration_date, balance)
            VALUES 
              (?, ?, ?, ?)
            """,
            (user['unique_id'], user['username'], user['registration_date'], user['balance'])
        )

        return self.conn.commit()

    # adding order
    def add_order(self, order: dict) -> None:
        # order types: item purchase, deposit wallet

        self.cursor.execute(
            """
            INSERT INTO 
              orders (type, unique_id, item_name, order_date, price)
            VALUES 
              (?, ?, ?, ?, ?)
            """,
            (order['type'], order['unique_id'], order['item_name'], order['order_date'], order['price'])
        )

        return self.conn.commit()

    # get user info
    def get_user_info(self, unique_id: int) -> dict:
        query = self.cursor.execute(
            """
            SELECT 
              unique_id, 
              registration_date, 
              balance
            FROM 
              users
            WHERE 
              unique_id = ?
            """,
            (unique_id,)
        )

        keys = ['unique_id', 'registration_date', 'balance']
        user = {k: v for k, v in zip(keys, query.fetchone())}

        return user

    # get categories
    def get_categories(self) -> dict:
        query = self.cursor.execute(
            """
            SELECT
              category_id,
              category_name
            FROM 
              categories
            """
        )

        categories = {k: v for v, k in list(query.fetchall())}

        return categories

    # get items by category
    def get_items_by_category(self, category_id: int) -> list:
        query = self.conn.execute(
            """
            SELECT
              item_name,
              item_price,
              item_amount,
              category_name,
              description
            FROM
              items
            INNER JOIN categories
              ON items.category_id == categories.category_id
            WHERE
              items.category_id = ?
            ORDER BY
              item_price
            """,
            (category_id,)
        )

        keys = ['name', 'price', 'amount', 'category', 'description']
        items = [{k: v for k, v in zip(keys, i)} for i in list(query.fetchall())]

        return items

    # get purchaces history
    def get_purchaces_history(self, unique_id: int) -> list:
        query = self.cursor.execute(
            """
            SELECT 
              order_date, 
              item_name, 
              price
            FROM 
              orders
            WHERE 
              unique_id = ?
            ORDER BY 
              order_date
            """,
            (unique_id,)
        )

        return list(query.fetchall())

    # update table by column in row
    def update(self, table: str, column: str, value: any, where_column: str, row: int) -> None:
        self.cursor.execute(
            f"""
            UPDATE
              {table}
            SET
              {column} = ?
            WHERE
              {where_column} = ?
            """,
            (value, row)
        )

        return self.conn.commit()

    # close connection
    def close(self):
        self.conn.close()
