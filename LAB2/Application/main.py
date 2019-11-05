
from Controller import Controller
from Model import ModelPostgreSQL
from View import View

if __name__ == '__main__':

    c = Controller(ModelPostgreSQL(),View())
    while True:
        type = c.action_type_select()
        if type == "1":
            c.table_type_select()
            c.action_select()
        elif type == "2":
            c.dynamic_search()
        else:
            c.static_search_film_and_session()
        if not c.question_about_end():
            break
    c.disconnect_from_db()



