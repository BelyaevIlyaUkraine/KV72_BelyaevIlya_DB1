import PostgreSQL_backend


class ModelPostgreSQL(object):
    def __init__(self):
        self._connection = PostgreSQL_backend.connect_to_db()
        self._present_table_type = ''
        self._cursor = self.connection.cursor()

    @property
    def connection(self):
        return self._connection

    @property
    def cursor(self):
        return self._cursor

    @property
    def present_table_type(self):
        return self._present_table_type

    @present_table_type.setter
    def present_table_type(self,new_present_table_type):
        self._present_table_type = new_present_table_type

    def create_item(self,cortage):
        PostgreSQL_backend.insert_one(self.cursor,self.present_table_type,cortage)

    def read_items(self):
        return PostgreSQL_backend.select_all(self.cursor,self.present_table_type)

    def update_item(self, list):
        PostgreSQL_backend.update_item(self.cursor, self.present_table_type, list)

    def delete_item(self,pr_key):
        return PostgreSQL_backend.delete_one(self.cursor,self.present_table_type,pr_key)

    def delete_all(self):
        return PostgreSQL_backend.delete_all(self.cursor,self.present_table_type)

    def disconnect_from_db(self):
        PostgreSQL_backend.disconnect_from_db(self.connection,self.cursor)

    def search_item(self,item,pr_key_mode,not_default_table=None):
        if pr_key_mode:
            return PostgreSQL_backend.select_item(self.cursor,self.present_table_type,item,pr_key_mode)
        else:
            return PostgreSQL_backend.select_item(self.cursor,not_default_table,item,pr_key_mode)

    def static_search_film_session(self,cortage):
        return PostgreSQL_backend.static_search_film_session(self.cursor,cortage)

    def text_search_full_phrase(self,phrase,pr_key,attribute):
        return PostgreSQL_backend.text_search_full_phrase(self.cursor,phrase,pr_key,attribute,self.present_table_type)

    def text_search_without_word(self,phrase,pr_key,attribute):
        return PostgreSQL_backend.text_search_without_definite_words(self.cursor, phrase, pr_key,attribute,
        self.present_table_type)

    def dynamic_search(self,array_with_selected_attributes,cortege_with_attributes,cortege_with_table_names):
        return PostgreSQL_backend.dynamic_search(self.cursor,array_with_selected_attributes,cortege_with_attributes,
                                                 cortege_with_table_names)
