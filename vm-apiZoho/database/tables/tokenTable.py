from .baseTable import BaseTable
from database.conection import Connection
import json


class Token(BaseTable):
    def __init__(self):
        self.tableName = "tokens"
        self.context = Connection()

    def Add(self, model):
        sql = "INSERT INTO tokens(new_token) "
        sql += "VALUES(%s,)"
        contactId = self.context.execute(
            sql, (model)
        )
        return contactId
    
    def Update(self, set, where, params):
        sql = f"UPDATE {self.tableName} SET {set}, time = now() WHERE {where}"
        self.context.execute(sql, params)


    def GetDetail(self, contact_id):
        sql = f"SELECT * FROM contact_custom_detail where contact_id = {contact_id} limit 1"
        contactDetail = self.context.firstOrDefault(sql)
        if contactDetail is None:
            return None
        else:
            return json.loads(contactDetail["detail"])


