from database.conection import Connection

class BaseTable:
    def firtsOrDefault(self, where, appendText=""):
        context = Connection()
        sql = f"SELECT * FROM {self.tableName} WHERE {where} {appendText}"
        return context.firstOrDefault(sql)
