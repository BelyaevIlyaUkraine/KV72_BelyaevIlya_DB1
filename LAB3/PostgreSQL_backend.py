from Models import *
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

    else:
        cursor.execute("""INSERT INTO "Cinema-Session" ("CinemaID","SessionID") 
            VALUES ('{}', '{}')""".format(list[0], list[1]))


def insert_one_orm(Session,list):

    session = Session()
    film = Film(Name = list[0], Genre = list[1], Year = list[2], Budget = list[3], Country = list[4], Duration = list[5]
                ,Oscar = list[6])
    session.add(film)
    session.commit()
    session.close()


def select_all(cursor, table_name):
    table_name = scrub(table_name)

    cursor.execute(""" SELECT * FROM "{}" """.format(table_name))

    return cursor


def select_all_orm(Session):
    session = Session()
    films = session.query(Film).all()
    session.close()

    return films


def delete_one(cursor, table_name, pr_key):
    table_name = scrub(table_name)

    def delete_one_network():
        cursor.execute("""DELETE FROM "Network" WHERE "Name" = '{}' """.format(pr_key))

    def delete_one_cinema():
        cursor.execute("""DELETE FROM "Cinema" WHERE  "Address" = '{}' """.format(pr_key))

    def delete_one_session():
        cursor.execute("""DELETE FROM "Session" WHERE "ID" = '{}' """.format(pr_key))

    def delete_one_cinema_session():
        cursor.execute("""DELETE FROM "Cinema-Session" WHERE "ID" = '{}' """.format(pr_key))

    if table_name == "Network":
        delete_one_network()
    elif table_name == "Cinema":
        delete_one_cinema()
    elif table_name == "Session":
        delete_one_session()
    elif table_name == "Cinema-Session":
        delete_one_cinema_session()

    return cursor.rowcount


def delete_one_orm(Session,pr_key):
    session = Session()
    film = session.query(Film).filter(Film.ID == pr_key).first()
    session.delete(film)
    session.commit()
    session.close()

def delete_all(cursor,table_name):
    cursor.execute("""DELETE FROM "{}" """.format(table_name))
    return cursor.rowcount

def delete_all_orm(Session):
    session = Session()
    films = session.query(Film).all()
    session.delete(films)
    session.commit()
    session.close()

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


def update_item_orm(Session,list):
    session = Session()
    film = session.query(Film).filter(Film.ID == list[0]).first()
    film.Name,film.Genre,film.Year,film.Budget,film.Country,film.Duration = list[1],list[2],list[3],list[4],list[5],\
                                                                            list[6]
    session.commit()
    session.close()


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






