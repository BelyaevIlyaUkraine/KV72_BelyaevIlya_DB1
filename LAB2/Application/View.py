class View(object):
    @staticmethod
    def action_type_select_display():
        print("Select action_type(number):\n")
        print("1---Definite action in definite table\n2---Dynamic search in two tables\n"
              "3---Static search on tables Film and Session\n")

    @staticmethod
    def text_search_type_select_display():
        print("Select text search type(number)\n")
        print("1---Full phrase\n2---Without definite words\n")

    @staticmethod
    def table_name_select_display():
        print("Select table name:\n")
        print("1---Network\n2---Cinema\n3---Session\n4---Film\n5---Cinema-Session\n")

    @staticmethod
    def action_select_display():
        print("Select action(number):\n")
        print("1---Show table items\n2---Update table item\n3---Create new table item\n"
        "4---Delete table item\n""5---Search table item\n6---Generate random data\n7---Delete all data from table\n"
        "8---Full text search on text attribute\n")

    @staticmethod
    def all_attributes_in_table_for_search_display(cortege_of_attributes, table_name):
        print("Select attribute of table {} \n".format(table_name))
        for count in range(len(cortege_of_attributes)):
            print("{}---{}\n".format(count, cortege_of_attributes[count]))

    @staticmethod
    def enter_cortege_item_display(item):
        print("Enter {}".format(item))

    @staticmethod
    def table_rows_display(items):
        cursor = items
        row = items.fetchone()
        while row is not None:
            print(row)
            row = cursor.fetchone()

    @staticmethod
    def question_about_end_display():
        print("Continue to work with Database?(Y/N)\n")

    @staticmethod
    def message_print(message):
        print(message)

    @staticmethod
    def question_about_local_end_display():
        print("Enter data again?(Y/N)\n")