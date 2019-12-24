import PostgreSQL_backend


class ModelPostgreSQL(object):
    def __init__(self,orm = True):
        self._connection = PostgreSQL_backend.connect_to_db()
        if orm:
            self._orm_session = PostgreSQL_backend.connect_to_db_orm()
        else:
            self._orm_session = None
        self._present_table_type = ''
        self._cursor = self.connection.cursor()

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor

    @property
    def orm_session(self):
        return self._orm_session

    @property
    def present_table_type(self):
        return self._present_table_type

    @present_table_type.setter
    def present_table_type(self,new_present_table_type):
        self._present_table_type = new_present_table_type

    def create_item(self,cortage):
        if self.orm_session:
            PostgreSQL_backend.insert_one_orm(self.orm_session,self.present_table_type,cortage)
        else:
            PostgreSQL_backend.insert_one(self.cursor,self.present_table_type,cortage)

    def read_items(self):
        if self.orm_session:
            return PostgreSQL_backend.select_all_orm(self.orm_session,self.present_table_type)
        else:
            return PostgreSQL_backend.select_all(self.cursor,self.present_table_type)

    def update_item(self, list):
        if self.orm_session:
            return PostgreSQL_backend.update_item_orm(self.orm_session,self.present_table_type,list)
        else:
            return PostgreSQL_backend.update_item(self.cursor, self.present_table_type, list)

    def delete_item(self,pr_key):
        if self.orm_session:
            return PostgreSQL_backend.delete_one_orm(self.orm_session,self.present_table_type,pr_key)
        else:
            return PostgreSQL_backend.delete_one(self.cursor,self.present_table_type,pr_key)

    def delete_all(self):
        if self.orm_session:
            return PostgreSQL_backend.delete_all_orm(self.orm_session,self.present_table_type)
        return PostgreSQL_backend.delete_all(self.cursor,self.present_table_type)

    def disconnect_from_db(self):
        PostgreSQL_backend.disconnect_from_db(self.connection,self.cursor)

    def search_item(self,item,pr_key_mode,not_default_table=None):
        if pr_key_mode:
            return PostgreSQL_backend.select_item(self.cursor,self.present_table_type,item,pr_key_mode)
        else:
            return PostgreSQL_backend.select_item(self.cursor,not_default_table,item,pr_key_mode)



