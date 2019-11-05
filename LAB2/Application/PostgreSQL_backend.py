import psycopg2


def scrub(input_string):
    """Clean an input string (to prevent SQL injection).

    Parameters
    ----------
    input_string : str

    Returns
    -------
    str
    """
    return ''.join(k for k in input_string if k.isalnum() or k == '-' or k == ',')


def insert_one(cursor, table_name, list):
    table_name = scrub(table_name)

    if table_name == "Network":
        cursor.execute("""INSERT INTO "Network" ("Name", "Owner") VALUES ('{}', '{}')""".format(list[0], list[1]))

    elif table_name == "Cinema":
        cursor.execute("""INSERT INTO "Cinema" ("Network","Address","NumberOfHalls",
        "GenNumberOfSeats") VALUES ('{}', '{}' , '{}', '{}')""".format(list[0], list[1], list[2], list[3]))

    elif table_name == "Session":
        cursor.execute("""INSERT INTO "Session" ("Start","Film","HallNumber") 
            VALUES ('{}', '{}', '{}')""".format (list[0], list[1], list[2]))

    elif table_name == "Film":
        cursor.execute("""INSERT INTO "Film" ("Name","Genre","Year","Budget","Country","Duration","Oscar") 
        VALUES ('{}','{}','{}','{}','{}','{}','{}')""".format(list[0], list[1], list[2],
                                                              list[3], list[4], list[5], list[6]))

    else:
        cursor.execute("""INSERT INTO "Cinema-Session" ("CinemaID","SessionID") 
            VALUES ('{}', '{}')""".format(list[0], list[1]))


def select_all(cursor, table_name):
    table_name = scrub(table_name)

    cursor.execute(""" SELECT * FROM "{}" """.format(table_name))

    return cursor


def delete_one(cursor, table_name, pr_key):
    table_name = scrub(table_name)

    def delete_one_network():
        cursor.execute("""DELETE FROM "Network" WHERE "Name" = '{}' """.format(pr_key))

    def delete_one_cinema():
        cursor.execute("""DELETE FROM "Cinema" WHERE  "Address" = '{}' """.format(pr_key))

    def delete_one_session():
        cursor.execute("""DELETE FROM "Session" WHERE "ID" = '{}' """.format(pr_key))

    def delete_one_film():
        cursor.execute("""DELETE FROM "Film" WHERE "ID" = '{}' """.format(pr_key))

    def delete_one_cinema_session():
        cursor.execute("""DELETE FROM "Cinema-Session" WHERE "ID" = '{}' """.format(pr_key))

    if table_name == "Network":
        delete_one_network()
    elif table_name == "Cinema":
        delete_one_cinema()
    elif table_name == "Session":
        delete_one_session()
    elif table_name == "Film":
        delete_one_film()
    elif table_name == "Cinema-Session":
        delete_one_cinema_session()

    return cursor.rowcount


def delete_all(cursor,table_name):
    cursor.execute("""DELETE FROM "{}" """.format(table_name))
    return cursor.rowcount


def update_item(cursor, table_name, list):
    if table_name == "Network":
        cursor.execute("""UPDATE "Network" SET "Owner" = '{}' 
        WHERE "Name" = '{}' """.format(list[1], list[0]))

    elif table_name == "Cinema":
        cursor.execute("""UPDATE "Cinema" SET "Network" = '{}',"NumberOfHalls" = '{}',"GenNumberOfSeats" = '{}' WHERE 
            "Address" = '{}' """.format(list[0], list[2], list[3], list[1]))

    elif table_name == "Session":
        cursor.execute("""UPDATE "Session" SET "Start" = '{}' ,"Film" = '{}', "HallNumber" = '{}' WHERE 
            "ID" = '{}'  """.format(list[1], list[2], list[3], list[0]))

    elif table_name == "Film":
        cursor.execute("""UPDATE "Film" SET "Name" = '{}',"Genre" = '{}',"Year" = '{}',"Budget" = '{}',
            "Country" = '{}' ,"Duration" = '{}' WHERE "ID" = '{}' """
                       .format(list[1], list[2], list[3], list[4], list[5], list[6], list[0]))

    elif table_name == "Cinema-Session":
        cursor.execute("""UPDATE "Cinema-Session" SET "CinemaID" = '{}',"SessionID" = '{}'
            WHERE "ID" = '{}' """.format(list[1], list[2], list[0]))

    return cursor.rowcount


def connect_to_db():
    connection = psycopg2.connect(dbname="Cinema Networks", user="postgres", password="01052000x",
                                  host="127.0.0.1", port="5555")
    return connection


def disconnect_from_db(connection,cursor):
    cursor.close()
    connection.close()
    print("Connection with PostgreSQL is closed")


def select_item(cursor,table_name,item,mode):
    table_name = scrub(table_name)
    if mode:
        if table_name == "Cinema":
            cursor.execute(""" SELECT * FROM "{}" WHERE "Address" = '{}' """.format(table_name, item))
        elif table_name == "Network":
            cursor.execute(""" SELECT * FROM "{}" WHERE "Name" = '{}' """.format(table_name,item))
        else:
            cursor.execute("""SELECT * FROM "{}" WHERE "ID" = '{}' """.format(table_name,item))
    else:
        cursor.execute("""SELECT "{}" FROM "{}" """.format(item,table_name))
        return cursor.fetchall()

    return cursor


def static_search_film_session(cursor, list):
    cursor.execute("""SELECT *
                      FROM "Film" INNER JOIN "Session" ON 
                      "Film"."ID" = "Session"."Film" WHERE "Film"."Oscar" = '{}' AND "Session"."Start" >= '{}' AND
                      "Session"."Start" < '{}' 
                   """.format(list[0], list[1], list[2]))

    return cursor


def text_search_full_phrase(cursor,phrase,pr_key,attribute,table_name):
    cursor.execute(""" SELECT "{}",ts_headline( "{}", q ) FROM "{}",
    phraseto_tsquery('{}') AS q
    WHERE to_tsvector("{}"."{}") @@ q""".format(pr_key,attribute,table_name,phrase,table_name,attribute))

    return cursor


def text_search_without_definite_words(cursor, phrase, pr_key, attribute, table_name):
    cursor.execute(""" SELECT "{}",ts_headline( "{}"."{}", phraseto_tsquery("{}"."{}") ) FROM "{}"
    WHERE NOT(to_tsvector("{}"."{}") @@ to_tsquery('{}'))"""
    .format(pr_key,table_name,attribute,table_name,attribute,table_name,table_name,attribute,phrase))
    return cursor


def dynamic_search(cursor,array_with_selected_attributes,cortege_with_attributes,cortege_with_table_names):
    if len(cortege_with_attributes) == 3:
        if array_with_selected_attributes[0].find("Bound") == -1:
            array_with_selected_attributes[1] = array_with_selected_attributes[1].replace("Lower", "")
            array_with_selected_attributes[1] = array_with_selected_attributes[1].replace("Bound", "")
            array_with_selected_attributes[1] = array_with_selected_attributes[1].replace(" ", "")
            array_with_selected_attributes[2] = array_with_selected_attributes[2].replace("Upper", "")
            array_with_selected_attributes[2] = array_with_selected_attributes[2].replace("Bound", "")
            array_with_selected_attributes[2] = array_with_selected_attributes[2].replace(" ", "")

            if cortege_with_table_names[0] == "Cinema" and cortege_with_table_names[1] == "Session":
                cursor.execute("""SELECT * FROM "{}" INNER JOIN "{}" ON EXISTS(SELECT * FROM "Cinema-Session" WHERE 
                "Cinema-Session"."CinemaID" = "Cinema"."Address" AND 
                "Session"."ID" = "Cinema-Session"."SessionID") AND "{}"."{}" = '{}' AND "{}"."{}" >= '{}' AND 
                "{}"."{}" <= '{}' """
                .format(cortege_with_table_names[0],cortege_with_table_names[1],cortege_with_table_names[0],
                array_with_selected_attributes[0],cortege_with_attributes[0],cortege_with_table_names[1],
                array_with_selected_attributes[1],cortege_with_attributes[1],cortege_with_table_names[1],
                array_with_selected_attributes[2],cortege_with_attributes[2]))

            elif cortege_with_table_names[0] == "Network" and cortege_with_table_names[1] == "Cinema":
                cursor.execute("""SELECT * FROM "{}" INNER JOIN "{}" ON "Network"."Name" = "Cinema"."Network"
                AND "{}"."{}" = '{}' AND "{}"."{}" >= '{}' AND "{}"."{}" <= '{}' """
                .format(cortege_with_table_names[0], cortege_with_table_names[1],
                cortege_with_table_names[0],array_with_selected_attributes[0], cortege_with_attributes[0],
                cortege_with_table_names[1],array_with_selected_attributes[1], cortege_with_attributes[1],
                cortege_with_table_names[1],array_with_selected_attributes[2], cortege_with_attributes[2]))

            elif cortege_with_table_names[0] == "Film" and cortege_with_table_names[1] == "Session":
                cursor.execute("""SELECT * FROM "{}" INNER JOIN "{}" ON "Film"."ID" = "Session"."Film"
                AND "{}"."{}" = '{}' AND "{}"."{}" >= '{}' AND "{}"."{}" <= '{}' """
                .format(cortege_with_table_names[0], cortege_with_table_names[1],
                cortege_with_table_names[0],array_with_selected_attributes[0], cortege_with_attributes[0],
                cortege_with_table_names[1],array_with_selected_attributes[1], cortege_with_attributes[1],
                cortege_with_table_names[1],array_with_selected_attributes[2], cortege_with_attributes[2]))

        else:
            array_with_selected_attributes[0] = array_with_selected_attributes[0].replace("Lower", "")
            array_with_selected_attributes[0] = array_with_selected_attributes[0].replace("Bound", "")
            array_with_selected_attributes[0] = array_with_selected_attributes[0].replace(" ", "")
            array_with_selected_attributes[1] = array_with_selected_attributes[1].replace("Upper", "")
            array_with_selected_attributes[1] = array_with_selected_attributes[1].replace("Bound", "")
            array_with_selected_attributes[1] = array_with_selected_attributes[1].replace(" ", "")

            if cortege_with_table_names[0] == "Cinema" and cortege_with_table_names[1] == "Network":
                cursor.execute("""SELECT * FROM "{}" INNER JOIN "{}" ON "Cinema"."Network" = "Network"."Name"
                AND "{}"."{}" >= '{}' AND "{}"."{}" <= '{}' AND "{}"."{}" = '{}' """
                .format(cortege_with_table_names[0], cortege_with_table_names[1],
                cortege_with_table_names[0],array_with_selected_attributes[0], cortege_with_attributes[0],
                cortege_with_table_names[0],array_with_selected_attributes[1], cortege_with_attributes[1],
                cortege_with_table_names[1],array_with_selected_attributes[2], cortege_with_attributes[2]))

            elif cortege_with_table_names[0] == "Session" and cortege_with_table_names[1] == "Cinema":
                cursor.execute("""SELECT * FROM "{}" INNER JOIN "{}" ON EXISTS(SELECT * FROM "Cinema-Session" WHERE 
                "Cinema-Session"."CinemaID" = "Cinema"."Address" AND "Session"."ID" = "Cinema-Session"."SessionID") 
                AND "{}"."{}" >= '{}' AND "{}"."{}" <= '{}' AND "{}"."{}" = '{}' """
                .format(cortege_with_table_names[0], cortege_with_table_names[1],
                cortege_with_table_names[0], array_with_selected_attributes[0],cortege_with_attributes[0],
                cortege_with_table_names[0], array_with_selected_attributes[1],cortege_with_attributes[1],
                cortege_with_table_names[1], array_with_selected_attributes[2],cortege_with_attributes[2]))

            elif cortege_with_table_names[0] == "Session" and cortege_with_table_names[1] == "Film":
                cursor.execute("""SELECT * FROM "{}" INNER JOIN "{}" ON "Session"."Film" = "Film"."ID"
                AND "{}"."{}" >= '{}' AND "{}"."{}" <= '{}' AND "{}"."{}" = '{}' """
                .format(cortege_with_table_names[0], cortege_with_table_names[1],cortege_with_table_names[0],
                array_with_selected_attributes[0], cortege_with_attributes[0],cortege_with_table_names[1],
                array_with_selected_attributes[1], cortege_with_attributes[1],cortege_with_table_names[1],
                array_with_selected_attributes[2], cortege_with_attributes[2]))
    elif len(cortege_with_attributes) == 4:
        array_with_selected_attributes[0] = array_with_selected_attributes[0].replace("Lower", "")
        array_with_selected_attributes[0] = array_with_selected_attributes[0].replace("Bound", "")
        array_with_selected_attributes[0] = array_with_selected_attributes[0].replace(" ", "")
        array_with_selected_attributes[1] = array_with_selected_attributes[1].replace("Upper", "")
        array_with_selected_attributes[1] = array_with_selected_attributes[1].replace("Bound", "")
        array_with_selected_attributes[1] = array_with_selected_attributes[1].replace(" ", "")
        array_with_selected_attributes[2] = array_with_selected_attributes[2].replace("Lower", "")
        array_with_selected_attributes[2] = array_with_selected_attributes[2].replace("Bound", "")
        array_with_selected_attributes[2] = array_with_selected_attributes[2].replace(" ", "")
        array_with_selected_attributes[3] = array_with_selected_attributes[3].replace("Upper", "")
        array_with_selected_attributes[3] = array_with_selected_attributes[3].replace("Bound", "")
        array_with_selected_attributes[3] = array_with_selected_attributes[3].replace(" ", "")

        if ((cortege_with_table_names[0] == "Session" and cortege_with_table_names[1] == "Film")or
        (cortege_with_table_names[0] == "Film" and cortege_with_table_names[1] == "Session")):
            cursor.execute("""SELECT * FROM "{}" INNER JOIN "{}" ON "Session"."Film" = "Film"."ID"
            AND "{}"."{}" >= '{}' AND "{}"."{}" <= '{}'  AND "{}"."{}" >= '{}' AND "{}"."{}" <= '{}' """
            .format(cortege_with_table_names[0], cortege_with_table_names[1], cortege_with_table_names[0],
            array_with_selected_attributes[0], cortege_with_attributes[0],cortege_with_table_names[0],
            array_with_selected_attributes[1], cortege_with_attributes[1],cortege_with_table_names[1],
            array_with_selected_attributes[2], cortege_with_attributes[2],cortege_with_table_names[1],
            array_with_selected_attributes[3], cortege_with_attributes[3]))

        elif ((cortege_with_table_names[0] == "Session" and cortege_with_table_names[1] == "Cinema")or
        (cortege_with_table_names[0] == "Cinema" and cortege_with_table_names[1] == "Session")):
            cursor.execute("""SELECT * FROM "{}" INNER JOIN "{}" ON EXISTS(SELECT * FROM "Cinema-Session" WHERE 
            "Cinema-Session"."CinemaID" = "Cinema"."Address" AND "Session"."ID" = "Cinema-Session"."SessionID") 
            AND "{}"."{}" >= '{}' AND "{}"."{}" <= '{}' AND "{}"."{}" >= '{}' AND "{}"."{}" <= '{}' """
            .format(cortege_with_table_names[0], cortege_with_table_names[1], cortege_with_table_names[0],
            array_with_selected_attributes[0], cortege_with_attributes[0], cortege_with_table_names[0],
            array_with_selected_attributes[1], cortege_with_attributes[1], cortege_with_table_names[1],
            array_with_selected_attributes[2], cortege_with_attributes[2], cortege_with_table_names[1],
            array_with_selected_attributes[3], cortege_with_attributes[3]))

    elif len(cortege_with_attributes) == 2:
        if ((cortege_with_table_names[0] == "Network" and cortege_with_table_names[1] == "Cinema")or
        (cortege_with_table_names[0] == "Cinema" and cortege_with_table_names[1] == "Network")):
            cursor.execute("""SELECT * FROM "{}" INNER JOIN "{}" ON "Network"."Name" = "Cinema"."Network"
            AND "{}"."{}" = '{}' AND "{}"."{}" = '{}' """
            .format(cortege_with_table_names[0], cortege_with_table_names[1],
            cortege_with_table_names[0], array_with_selected_attributes[0],cortege_with_attributes[0],
            cortege_with_table_names[1], array_with_selected_attributes[1],cortege_with_attributes[1]))

        elif ((cortege_with_table_names[0] == "Film" and cortege_with_table_names[1] == "Session")or
        (cortege_with_table_names[0] == "Session" and cortege_with_table_names[1] == "Film")):
            cursor.execute("""SELECT * FROM "{}" INNER JOIN "{}" ON "Film"."ID" = "Session"."ID"
            AND "{}"."{}" = '{}' AND "{}"."{}" = '{}' """
            .format(cortege_with_table_names[0], cortege_with_table_names[1],
            cortege_with_table_names[0], array_with_selected_attributes[0],cortege_with_attributes[0],
            cortege_with_table_names[1], array_with_selected_attributes[1],cortege_with_attributes[1]))

        elif ((cortege_with_table_names[0] == "Cinema" and cortege_with_table_names[1] == "Session")or
        (cortege_with_table_names[0] == "Session" and cortege_with_table_names[1] == "Cinema")):
            cursor.execute("""SELECT * FROM "{}" INNER JOIN "{}" ON EXISTS(SELECT * FROM "Cinema-Session" WHERE 
            "Cinema-Session"."CinemaID" = "Cinema"."Address" AND "Session"."ID" = "Cinema-Session"."SessionID") 
            AND "{}"."{}" = '{}' AND "{}"."{}" = '{}' """
            .format(cortege_with_table_names[0], cortege_with_table_names[1],
            cortege_with_table_names[0], array_with_selected_attributes[0],cortege_with_attributes[0],
            cortege_with_table_names[1], array_with_selected_attributes[1],cortege_with_attributes[1]))

    return cursor


