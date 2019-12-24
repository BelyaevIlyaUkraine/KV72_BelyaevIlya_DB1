from Models import *
from Models import Session as Sessn
import psycopg2
from sqlalchemy.orm import *
from sqlalchemy import create_engine


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


def insert_one_orm(Session,table_name,list):

    session = Session()

    if table_name == "Film":
        table_item = Film(Name = list[0], Genre = list[1], Year = list[2], Budget = list[3],
                          Country = list[4], Duration = list[5],Oscar = bool(list[6]))
    elif table_name == "Network":
        table_item = Network(Name = list[0],Owner = list[1])
    elif table_name == "Cinema":
        table_item = Cinema(Network = list[0],Address = list[1],NumberOfHalls = list[2], GenNumberOfSeats = list[3])
    elif table_name == "Session":
        table_item = Sessn(Start = list[0],Film = list[1],HallNumber = list[2])
    else:
        table_item = Cinema_Session(CinemaID = list[0],SessionID = list[1])
    session.add(table_item)
    session.commit()
    session.close()


def select_all(cursor, table_name):
    table_name = scrub(table_name)

    cursor.execute(""" SELECT * FROM "{}" """.format(table_name))

    return cursor


def select_all_orm(Session,table_name):
    session = Session()
    if table_name == "Network":
        table_item = session.query(Network).all()
    elif table_name == "Cinema":
        table_item = session.query(Cinema).all()
    elif table_name == "Film":
        table_item = session.query(Film).all()
    elif table_name == "Session":
        table_item = session.query(Sessn).all()
    else:
        table_item = session.query(Cinema_Session).all()
    session.close()

    return table_item


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


def delete_one_orm(Session,table_name,pr_key):
    session = Session()
    if table_name == "Network":
        table_item = session.query(Network).filter(Network.Name == pr_key).first()
    elif table_name == "Cinema":
        table_item = session.query(Cinema).filter(Cinema.Address == pr_key).first()
    elif table_name == "Session":
        table_item = session.query(Sessn).filter(Sessn.ID == pr_key).first()
    elif table_name == "Cinema-Session":
        table_item = session.query(Cinema_Session).filter(Cinema_Session.ID == pr_key).first()
    else:
        table_item = session.query(Film).filter(Film.ID == pr_key).first()
    if table_item is None:
        session.close()
        return 0

    session.delete(table_item)
    session.commit()
    session.close()

    return 1


def delete_all(cursor,table_name):
    cursor.execute("""DELETE FROM "{}" """.format(table_name))
    return cursor.rowcount


def delete_all_orm(Session,table_name):
    session = Session()
    if table_name == "Network":
        count = session.query(Network).delete()
    elif table_name == "Cinema":
        count = session.query(Cinema).delete()
    elif table_name == "Film":
        count = session.query(Film).delete()
    elif table_name == "Session":
        count = session.query(Sessn).delete()
    else:
        count = session.query(Cinema_Session).delete()
    session.commit()
    session.close()

    return count


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


def update_item_orm(Session,table_name,list):
    session = Session()

    if table_name == "Film":
        table_item = session.query(Film).filter(Film.ID == list[0]).first()
        if table_item is None:
            session.close()
            return 0
        table_item.Name,table_item.Genre,table_item.Year,table_item.Budget,table_item.Country,table_item.Duration,\
        table_item.Oscar= list[1],list[2],list[3],list[4],list[5],list[6],bool(list[7])
    elif table_name == "Network":
        table_item = session.query(Network).filter(Network.Name == list[0]).first()
        if table_item is None:
            session.close()
            return 0
        table_item.Owner = list[1]
    elif table_name == "Cinema":
        table_item = session.query(Cinema).filter(Cinema.Address == list[1]).first()
        if table_item is None:
            session.close()
            return 0
        table_item.Network,table_item.NumberOfHalls,table_item.GenNumberOfSeats = list[0],list[2],list[3]
    elif table_name == "Session":
        table_item = session.query(Sessn).filter(Sessn.ID == list[0]).first()
        if table_item is None:
            session.close()
            return 0
        table_item.Start,table_item.Film,table_item.HallNumber = list[1],list[2],list[3]
    else:
        table_item = session.query(Cinema_Session).filter(Cinema_Session.ID == list[0]).first()
        if table_item is None:
            session.close()
            return 0
        table_item.CinemaID,table_item.SessionID = list[1],list[2]
    session.commit()
    session.close()

    return 1


def connect_to_db():
    connection = psycopg2.connect(dbname="Cinema Networks", user="postgres", password="01052000x",
                                  host="127.0.0.1", port="5555")
    return connection


def connect_to_db_orm():
    engine = create_engine('postgresql+psycopg2://postgres:01052000x@127.0.0.1:5555/Cinema Networks')
    session_class = sessionmaker(bind=engine)
    return session_class


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






