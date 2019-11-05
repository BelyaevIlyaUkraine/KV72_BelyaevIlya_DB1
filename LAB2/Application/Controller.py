from mimesis import Generic
import random


class Controller(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view

    def show_items(self):
        items = self.model.read_items()
        if items.rowcount:
            self.view.table_rows_display(items)
            return
        self.view.message_print("This table was already empty\n")

    def enter_items(self, table_item_names):
        return_array = []
        for name in table_item_names:
            while True:
                self.view.enter_cortege_item_display(name)
                inp = str(input())
                if validate_input(name, inp):
                    return_array.append(inp)
                    break
                else:
                    self.view.message_print("Error:enter valid value\n")
        return return_array

    def table_type_select(self):
        self.view.table_name_select_display()
        while True:
            table_type = str(input())
            if (table_type == "Network" or table_type == "Cinema" or table_type == "Session" or table_type == "Film"
            or table_type == "Cinema-Session"):
                self.model.present_table_type = table_type
                return
            self.view.message_print("Error:enter one of suggested table names\n")

    def action_type_select(self):
        self.view.action_type_select_display()
        while True:
            action_type = str(input())
            if action_type != "1" and action_type != "2" and action_type != "3":
                self.view.message_print("Error:enter number from 1 to 3\n")
                continue
            break
        return action_type

    def action_select(self):
        self.view.action_select_display()
        while True:
            action = str(input())
            if action == "1":
                self.show_items()
            elif action == "2":
                self.update_item()
            elif action == "3":
                self.insert_item()
            elif action == "4":
                self.delete_item()
            elif action == "5":
                self.search_item()
            elif action == "6":
                self.data_random()
            elif action == "7":
                self.delete_all()
            elif action == "8":
                self.text_attribute_search()
            else:
                self.view.message_print("Error:Enter number from 1-8\n")
                continue
            break

        self.model.connection.commit()

    def question_about_end(self):
        self.view.question_about_end_display()
        while True:
            inp = str(input())
            if inp == "Y":
                return True
            elif inp == "N":
                return False
            else:
                self.view.message_print("""Error:enter "Y" or "N"\n """)

    def disconnect_from_db(self):
        self.model.disconnect_from_db()

    def insert_item(self):
        while True:
            if self.model.present_table_type == 'Network':
                list = self.enter_items(("Name", "Owner"))
            elif self.model.present_table_type == 'Cinema':
                list = self.enter_items(("Network", "Address", "NumberOfHalls", "GenNumberOfSeats"))
            elif self.model.present_table_type == 'Session':
                list = self.enter_items(("Start", "Film", "HallNumber"))
            elif self.model.present_table_type == 'Film':
                list = self.enter_items(("Name", "Genre", "Year", "Budget", "Country", "Duration","Oscar"))
            else:
                list = self.enter_items(("CinemaID", "SessionID"))
            try:
                self.model.create_item(list)
                self.view.message_print("Row was inserted successfully\n")
                break
            except Exception as error:
                print(error)
                self.model.connection.commit()
                self.view.question_about_local_end_display()
                while True:
                    answer = str(input())
                    if answer == "N":
                        return
                    elif answer == "Y":
                        break
                    else:
                        self.view.message_print("Enter Y or N \n")

    def update_item(self):
        while True:
            if self.model.present_table_type == 'Network':
                list = self.enter_items(("Name", "Owner"))
            elif self.model.present_table_type == 'Cinema':
                list = self.enter_items(("Network", "Address", "NumberOfHalls", "GenNumberOfSeats"))
            elif self.model.present_table_type == 'Session':
                list = self.enter_items(("ID", "Start", "Film", "HallNumber"))
            elif self.model.present_table_type == 'Film':
                list = self.enter_items(("ID", "Name", "Genre", "Year", "Budget", "Country", "Duration","Oscar"))
            else:
                list = self.enter_items(("ID", "CinemaID", "SessionID"))
            try:
                if self.model.update_item(list):
                    self.view.message_print("Row was updated successfully\n")
                else:
                    self.view.message_print("There isn't element with such ID in table\n")
                break
            except Exception as error:
                print(error)
                self.model.connection.commit()
                self.view.question_about_local_end_display()
                while True:
                    answer = str(input())
                    if answer == "N":
                        return
                    elif answer == "Y":
                        break
                    else:
                        self.view.message_print("Enter Y or N \n")

    def delete_item(self):
        if self.model.present_table_type == 'Network':
            list = self.enter_items(["Name"])
        elif self.model.present_table_type == 'Cinema':
            list = self.enter_items(["Address"])
        else:
            list = self.enter_items(["ID"])
        if self.model.delete_item(list[0]):
            self.view.message_print("Row was deleted successfully\n")
        else:
            self.view.message_print("There isn't row for deleting with such attribute value\n")

    def delete_all(self):
        if self.model.delete_all():
            self.view.message_print("All rows in table were deleted successfully\n")
        else:
            self.view.message_print("Table was already empty\n")

    def search_item(self):
        if self.model.present_table_type == 'Network':
            list = self.enter_items(["Name"])
        elif self.model.present_table_type == 'Cinema':
            list = self.enter_items(["Address"])
        else:
            list = self.enter_items(["ID"])

        items = self.model.search_item(list[0], True)
        if items.rowcount == 0:
            self.view.message_print("There aren't necessary rows for selecting in table\n")
        self.view.table_rows_display(items)

    def static_search_film_and_session(self):
        list = self.enter_items(("Oscar", "Start Lower Bound", "Start Upper Data Bound"))
        items = self.model.static_search_film_session(list)
        if items.rowcount == 0:
            self.view.message_print("There aren't any results matching input conditions\n")
            return
        self.view.table_rows_display(items)

    def text_attribute_search(self):
        self.view.text_search_type_select_display()
        items = None
        if self.model.present_table_type == "Network":
            pr_key = "Name"
        elif self.model.present_table_type == "Cinema":
            pr_key = "Address"
        elif self.model.present_table_type == "Cinema-Session":
            pr_key = "CinemaID"
        else:
            pr_key = "ID"
        while True:
            type = str(input())
            if type == "1":
                attribute = self.select_attribute_for_text_search()
                text_value = self.enter_items(["Phrase"])
                text_value = text_value[0]
                items = self.model.text_search_full_phrase(text_value,pr_key,attribute)
            elif type == "2":
                attribute = self.select_attribute_for_text_search()
                text_value = self.enter_items(["Words"])
                text_value = text_value[0]
                text_value = text_value.replace(",","|")
                text_value = text_value.replace(" ","<->")
                items = self.model.text_search_without_word(text_value,pr_key,attribute)
            else:
                self.view.message_print("Error:enter number of action from 1 to 2\n")
                continue
            break
        if items.rowcount == 0:
            self.view.message_print("No text parts matching input conditions\n")
            return
        self.view.table_rows_display(items)

    def select_attribute_for_text_search(self):
        if self.model.present_table_type == "Network":
            self.view.all_attributes_in_table_for_search_display(("Name", "Owner"), self.model.present_table_type)
        elif self.model.present_table_type == "Cinema":
            self.view.all_attributes_in_table_for_search_display(
                ("Network", "Address", "NumberOfHalls", "GenNumberOfSeats"),self.model.present_table_type)
        elif self.model.present_table_type == "Session":
            self.view.all_attributes_in_table_for_search_display(["HallNumber"],self.model.present_table_type)
        elif self.model.present_table_type == "Film":
            self.view.all_attributes_in_table_for_search_display(
                    ("Name", "Genre", "Year", "Budget", "Country", "Duration"),self.model.present_table_type)
        elif self.model.present_table_type == "Cinema-Session":
            self.view.all_attributes_in_table_for_search_display(["CinemaID"],self.model.present_table_type)

        while True:
            attribute_name = str(input())
            if not (attribute_name == "Name" or attribute_name == "Owner" or attribute_name == "Network"
            or attribute_name == "Address" or attribute_name == "Genre"
            or attribute_name == "Country" or attribute_name == "Year"
            or attribute_name == "Budget" or attribute_name == "Duration"
            or attribute_name == "HallNumber" or attribute_name == "NumberOfHalls"
            or attribute_name == "GenNumberOfSeats" or attribute_name == "CinemaID"):
                print("Error:enter one of suggested attribute names:\n")
                continue
            return attribute_name

    def select_attributes_for_dynamic_search(self, list_with_table_names):
        array_with_attributes = []
        for count in range(2):
            if list_with_table_names[count] == "Network":
                self.view.all_attributes_in_table_for_search_display(("Name", "Owner"), list_with_table_names[count])
            elif list_with_table_names[count] == "Cinema":
                self.view.all_attributes_in_table_for_search_display(
                    ("Network", "Address", "NumberOfHalls", "GenNumberOfSeats"), list_with_table_names[count])
            elif list_with_table_names[count] == "Session":
                self.view.all_attributes_in_table_for_search_display(("ID", "Start", "Film", "HallNumber"),
                                                                     list_with_table_names[count])
            elif list_with_table_names[count] == "Film":
                self.view.all_attributes_in_table_for_search_display(
                    ("ID", "Name", "Genre", "Year", "Budget", "Country", "Duration", "Oscar"),
                    list_with_table_names[count])

            while True:
                attribute_name = str(input())

                if (attribute_name == "Name" or attribute_name == "Owner" or attribute_name == "Network"
                        or attribute_name == "Address" or attribute_name == "Genre"
                        or attribute_name == "Country" or attribute_name == "Oscar"):
                    array_with_attributes.append(str(attribute_name))

                elif (attribute_name == "ID" or attribute_name == "Year" or attribute_name == "Budget" or
                attribute_name == "Duration" or attribute_name == "Start" or attribute_name == "HallNumber"
                or attribute_name == "Film" or attribute_name == "NumberOfHalls"
                or attribute_name == "GenNumberOfSeats"):
                    array_with_attributes.append("{} Lower Bound".format(attribute_name))
                    array_with_attributes.append("{} Upper Bound".format(attribute_name))

                else:
                    print("Error:enter one of suggested attribute names:\n")
                    continue
                break
        return array_with_attributes

    def dynamic_search(self):
        while True:
            list_with_entered_tables = self.enter_items(("First table", "Second table"))
            if not ((list_with_entered_tables[0] == "Cinema" and list_with_entered_tables[1] == "Session")or(
            list_with_entered_tables[0] == "Network" and list_with_entered_tables[1] == "Cinema")or(
            list_with_entered_tables[0] == "Film" and list_with_entered_tables[1] == "Session")or(
            list_with_entered_tables[0] == "Cinema" and list_with_entered_tables[1] == "Network")or(
            list_with_entered_tables[0] == "Session" and list_with_entered_tables[1] == "Cinema")or(
            list_with_entered_tables[0] == "Session" and list_with_entered_tables[1] == "Film")):
                self.view.message_print("Enter two tables connected directly or through intermediary table\n")
            else:
                break

        array_with_selected_attributes = self.select_attributes_for_dynamic_search(list_with_entered_tables)
        list_with_entered_attributes = self.enter_items(array_with_selected_attributes)
        items = self.model.dynamic_search(array_with_selected_attributes,list_with_entered_attributes,
                                          list_with_entered_tables)
        if items.rowcount == 0:
            self.view.message_print("There aren't any results in table matching input conditions\n")
        else:
            self.view.table_rows_display(items)

    def data_random(self):
        g = Generic('en')
        list_for_Cinema = None
        list_for_Session = None
        list_for_Cinema_Session_CinemaID = None
        list_for_Cinema_Session_SessionID = None
        count_succedded_Cinema_Session = 0
        if self.model.present_table_type == "Cinema":
            list_for_Cinema = self.model.search_item("Name", False, "Network")
            if len(list_for_Cinema) == 0:
                self.view.message_print("There aren't any Networks for random entering in table Cinema\n")
                return

        elif self.model.present_table_type == "Session":
            list_for_Session = self.model.search_item("ID", False, "Film")
            if len(list_for_Session) == 0:
                self.view.message_print("Error during random session data entering:" +
                                              "there aren't any films in table Films to set on sessions\n")
                return

        elif self.model.present_table_type == "Cinema-Session":
            list_for_Cinema_Session_CinemaID = self.model.search_item("Address", False, "Cinema")
            list_for_Cinema_Session_SessionID = self.model.search_item("ID",False,"Session")
            if len(list_for_Cinema_Session_CinemaID) == 0 or len(list_for_Cinema_Session_SessionID) == 0:
                self.view.message_print("Error:necessary table/tables for table Cinema-Session is/are empty\n")
                return

        chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'

        for k in range(10000):
            array_with_attributes = []
            count = 0
            if self.model.present_table_type == "Network":
                while True:
                    array_with_attributes = []
                    array_with_attributes.append(''.join(random.SystemRandom().choice(chars)
                                                         for i in range(random.randint(5,11))))
                    array_with_attributes.append(g.person.full_name().replace("'", ''))
                    try:
                        self.model.create_item(array_with_attributes)
                    except Exception:
                        continue
                    break

            elif self.model.present_table_type == "Cinema":
                array_with_attributes.append(g.random.choice(list_for_Cinema))
                array_with_attributes[0] = array_with_attributes[0][0].replace("'",'')
                array_with_attributes.append(g.address.city().replace("'",'') + "," +
                ''.join(random.SystemRandom().choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ")
                for i in range(random.randint(5,11))) + " " +g.address.street_suffix() + "," + ''.join(
                random.SystemRandom().choice("0123456789") for i in range(random.randint(1,4))))
                array_with_attributes.append(g.random.randint(1, 4))
                array_with_attributes.append(g.random.randint(400, 500) *
                                             array_with_attributes[len(array_with_attributes) - 1])
                while True:
                    try:
                        self.model.create_item(array_with_attributes)
                    except Exception:
                        array_with_attributes[1] = g.address.city().replace("'",'') + "," +''.join(
                        random.SystemRandom().choice( "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKMNOPQRSTUVWXYZ")
                        for i in range(random.randint(5, 11)))+ " " + g.address.street_suffix() + " " + ''.join(
                        random.SystemRandom().choice("0123456789") for i in range(random.randint(1, 4)))
                        continue
                    break

            elif self.model.present_table_type == "Session":
                array_with_attributes.append(str(g.datetime.datetime()))
                array_with_attributes.append(g.random.choice(list_for_Session))
                array_with_attributes[1] = array_with_attributes[1][0]
                array_with_attributes.append(g.random.randint(1, 4))
                self.model.create_item(array_with_attributes)

            elif self.model.present_table_type == "Film":
                array_with_attributes.append(g.business.company().replace("'", ''))
                array_with_attributes.append(g.random.choice(("Fantastical", "Western", "Thriller", "Detective", "War",
                "Sci-Fi", "Horror", "Comedy", "Historical", "Musical","Romantic", "Documentary", "Action",
                "Drama", "Family", "Sport")))
                array_with_attributes.append(g.datetime.year())
                array_with_attributes.append(str(g.random.randint(10000000, 10000000000)) + str(g.random.choice((" UAH",
                " USD"," GBP"," EUR"))))
                array_with_attributes.append(g.choice(("Ukraine", "France", "Great Britain", "Germany", "Sweden",
                                                       "Finland", "Norway", "Switzerland", "Czech Republic", "Hungary",
                                                       "Bulgaria", "Romania", "Greece", "Spain",
                                                       "Belgium", "Netherlands", "Luxemburg", "Italy", "Croatia",
                                                       "Serbia", "Montenegro", "Cyprus", "Slovakia")))
                array_with_attributes.append(str(g.random.randint(100, 200)) + " min")
                array_with_attributes.append(g.random.choice(("True", "False")))
                self.model.create_item(array_with_attributes)

            elif self.model.present_table_type == "Cinema-Session":
                while True:
                    array_with_attributes.append(g.choice(list_for_Cinema_Session_CinemaID))
                    array_with_attributes[0] = array_with_attributes[0][0]
                    array_with_attributes.append(g.choice(list_for_Cinema_Session_SessionID))
                    array_with_attributes[1] = array_with_attributes[1][0]
                    try:
                        self.model.create_item(array_with_attributes)
                        count_succedded_Cinema_Session += 1
                        break
                    except Exception:
                        if count>50:
                            count += 1
                            array_with_attributes = []
                            continue
                        self.view.message_print("There aren't enough Cinemas and Session to enter necessary "+
                        "amount of data rows in table Cinema-Session but {} rows were entered\n"
                        .format(count_succedded_Cinema_Session))
                        return

            if k % 1000 == 0:
                self.model.connection.commit()


def validate_input(attr_name, attr_value):
    bound_check = list(attr_name.split(' '))
    if len(bound_check) > 1:
        if bound_check[1] == "Lower" or bound_check[1] == "Upper":
            attr_name = bound_check[0]
    if attr_name.find("table") != -1:
        if (attr_value == "Network" or attr_value =="Cinema" or attr_value == "Session"
        or attr_value == "Cinema-Session" or  attr_value == "Film"):
            return True
        return False
    if attr_name == "ID":
        if attr_value.isdecimal():
            return True
    elif attr_name == "Year":
        if attr_value.isdecimal():
            return True
    elif attr_name == "Budget":
        li = list(attr_value.split(" "))
        if len(li) == 2:
            if li[0].isdecimal() and (li[1] == "UAH" or li[1] == "USD" or li[1] == "EUR" or li[1] == "GBP"):
                return True
    elif attr_name == "Duration":
        li = list(attr_value.split(" "))
        if len(li) == 2:
            if li[0].isdecimal() and li[1] == "min":
                return True
    elif attr_name == "Start":
        li = list(attr_value.split(" "))
        if len(li) == 2:
            li_data = list(li[0].split("-"))
            li_time = list(li[1].split(":"))
            if (li_data[0].isdecimal() and li_data[1].isdecimal and li_data[2].isdecimal() and li_time[0].isdecimal()
            and li_time[1].isdecimal() and li_time[2].isdecimal()):
                if '13' > li_data[1] and li_data[2]<'31' and li_time[0]<'24' and li_time[1]<'60' and li_time[2]<'60':
                    return True
    elif attr_name == "HallNumber":
        if attr_value.isdecimal():
            return True
    elif attr_name == "Film":
        if attr_value.isdecimal():
            return True
    elif attr_name == "NumberOfHalls":
        if attr_value.isdecimal():
            return True
    elif attr_name == "GenNumberOfSeats":
        if attr_value.isdecimal():
            return True
    elif attr_name == "Name":
        li = list(attr_value.split(" "))
        for item in li:
            if not item.isalnum():
                return False
        return True
    elif attr_name == "Owner":
        li = list(attr_value.split(" "))
        for item in li:
            if not item.isalpha() or not item[0].isupper:
                return False
        return True
    elif attr_name == "Network":
        li = list(attr_value.split(" "))
        for item in li:
            if not item.isalnum():
                return False
        return True
    elif attr_name == "Address":
        li = list(attr_value.split(","))
        if len(li) == 3:
            li0 = li[0].split(" ")
            for part in li0:
                if not part.isalpha():
                    return False
            li1 = li[1].split(" ")
            for part in li1:
                if not part.isalpha():
                    return False
            if li[2].isdecimal():
                return True
        return False
    elif attr_name == "Genre":
        if attr_value.isalpha():
            return True
    elif attr_name == "Country":
        if attr_value.isalpha():
            return True
    elif attr_name == "Oscar":
        if attr_value == "True" or attr_value == "False":
            return True
        return False
    elif attr_name == "CinemaID":
        if attr_value.isdecimal():
            return True
        return False
    elif attr_name == "SessionID":
        if attr_value.isdecimal():
            return True
        return False
    elif attr_name == "Phrase":
        return True
    elif attr_name == "Words":
        words = list(attr_value.split(","))
        for word in words:
            subwords = list(word.split(" "))
            for subword in subwords:
                if not subword.isalnum():
                    return False
        return True


