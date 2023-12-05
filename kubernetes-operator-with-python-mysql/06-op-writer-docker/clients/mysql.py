import mysql.connector
import logging
from mysql.connector import Error


class MysqlClient:
    def __init__(self, host, username, password, db):
        self.host = host
        self.username = username
        self.__password = password
        self.db = db
        self.__connection = None

    def connect_if_not_connected(self):
        if self.__connection is None or not self.__connection.is_connected():
            return self._try_connect()

        return True

    def _try_connect(self):
        try:
            self.__connection = mysql.connector.connect(
                host=self.host,
                database=self.db,
                user=self.username,
                password=self.__password,
            )
            logging.info("Database connection is established.")
            return True
        except Error as e:
            logging.error(f"Database connection is not established: {e}")
            return False

    def get_connection(self):
        return self.__connection

    def insert_row(self, table, primary_id, name, age, country):
        logging.info(f"insert_row: {primary_id}")
        if self.connect_if_not_connected():
            db_connection = self.get_connection()
            insert_query = (
                f"INSERT INTO {table} (id, name, age, country) "
                f"VALUES ('{primary_id}', '{name}', {age}, '{country}')"
            )

            try:
                with db_connection.cursor() as cursor:
                    cursor.execute(insert_query)
                    db_connection.commit()
            except Error as e:
                logging.error(f"Error during insertion: {e}")
            finally:
                if db_connection.is_connected():
                    db_connection.close()

    def delete_row(self, table, primary_id):
        success_status = False
        if self.connect_if_not_connected():
            db_connection = self.get_connection()
            delete_query = """DELETE FROM {table_name} WHERE id='{id}'""".format(
                table_name=table, id=primary_id
            )
            logging.info(f"delete_query: {delete_query}")

            try:
                with db_connection.cursor() as cursor:
                    cursor.execute(delete_query)
                    db_connection.commit()
                    success_status = True
            except Error as e:
                logging.error(f"Error during deletion: {e}")
            finally:
                if db_connection.is_connected():
                    db_connection.close()

        return success_status
