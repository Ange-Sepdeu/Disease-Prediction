import os
import sqlite3

def get_path_to_sqlite_database(file_path=__file__, relative_path_to_database="db.sqlite"):
    print(f"Calling create_db.py, the file_path is: {file_path}")
    file_directory = os.path.dirname(file_path)
    return os.path.join( file_directory, relative_path_to_database )

if __name__ == '__main__':
    # get the directory of this file (create_db.py)
    sqlite_database_path = get_path_to_sqlite_database()

    # delete the database if it already exists
    if os.path.exists(sqlite_database_path):
        os.remove(sqlite_database_path)

    connection = sqlite3.connect("db.sqlite")

    cursor = connection.cursor()

    create_students_table_query = """
    CREATE TABLE Students (
        name TEXT,
        id INTEGER PRIMARY KEY AUTOINCREMENT
    )
    """

    create_projects_table_query = """
    CREATE TABLE Projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        student INTEGER NOT NULL,
        FOREIGN KEY(student) REFERENCES Student(id)
    )
    """

    for query in [create_students_table_query, create_projects_table_query]:
        cursor.execute(query)
        connection.commit()

    cursor.close()
    connection.close()

    print("Database created successfully")