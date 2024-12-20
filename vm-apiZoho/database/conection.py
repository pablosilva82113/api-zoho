import mysql.connector
import config as config
from loguru import logger as Log


class Connection:
    def __init__(self):
        self.host = config.DB_HOST
        self.user = config.DB_USERNAME
        self.password = config.DB_PASSWORD
        self.database = config.DB_DATABASE

    def _get_connection(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                charset="utf8mb4",
                collation='utf8mb4_general_ci'
            )
        except mysql.connector.Error as error:
            Log.error("Error Initial MySQL: " + str(error))
            return None

    def exist(self, sql):
        connection = self._get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(sql)
                exists = cursor.rowcount > 0
                cursor.close()
                return exists
            except mysql.connector.Error as error:
                Log.error("Error Exists MySQL: " + str(error))
            finally:
                connection.close()
        return False

    def firstOrDefault(self, sql):
        rows = self.getData(sql)
        if len(rows) == 0:
            return None
        else:
            return rows[0]

    def getData(self, sql):
        connection = self._get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(sql)
                result = cursor.fetchall()
                columns = [column[0] for column in cursor.description]
                cursor.close()

                serialized_result = []
                for row in result:
                    serialized_row = dict(zip(columns, row))
                    serialized_result.append(serialized_row)

                return serialized_result
            except mysql.connector.Error as error:
                Log.error("sql: " + sql)
                Log.error("Error GetData MySQL: " + str(error))
            finally:
                connection.close()
        return []

    def execute(self, sql, params=[]):
        connection = self._get_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute(sql, params=params)
                connection.commit()
                try:
                    last_row_id = cursor.lastrowid
                    return last_row_id
                except Exception as error:
                    return None
                finally:
                    cursor.close()
            except mysql.connector.Error as error:
                Log.warning(sql)
                Log.warning(params)
                Log.error("Error Execute MySQL: " + str(error))
            except Exception as error:
                Log.warning(sql)
                Log.warning(params)
                Log.error("Error: " + str(error))
            finally:
                connection.close()
        return None
