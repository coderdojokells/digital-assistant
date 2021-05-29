import sqlite3
from sqlite3 import Error

def main():
    print("Welcome, please enter your name: ")
    userName = input()
    existingUser = selectUser(userName)
    existingUser = existingUser[0]
    
    if userName == existingUser:
        print("Welcome back " + existingUser)
        
    print("Thank you " + userName + ". What is your age?")
    userAge = input()
    print("Thank you " + userName + ". What is your job?")
    userJob = input()    
    saveUser(userName, userAge, userJob)
    

def saveUser(name, age, job):
    # link to the database file or creates one if it does not exist
    database = r"db\assistant.db"
    sql_create_user_table = """ CREATE TABLE IF NOT EXISTS user (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        age integer NOT NULL
                                        job text NOT NULL
    
                                   ); """
    
    # create connection to database
    conn = createConn(database)
    
    if conn is not None:
        # create user table if one does not exist already 
        createTable(conn, sql_create_user_table)      
    else:
        print('Error! cannot create the database connection')


    with conn:
        user = (name, age, job)
        userID = insertUser(conn, user)
        #print(reminderID)     
    conn.close()


# this function is used select a single reminder from the database for a given time
def selectUser(name):
    database = r"db\assistant.db"
    # create connection to database
    conn = createConn(database)
    
    cur = conn.cursor()
    cur.execute("SELECT name FROM user WHERE name=? LIMIT 1", (name,))

    user = cur.fetchone()
    return user


# this function retrieves all stored users 
def getUsers():
    database = r"db\assistant.db"
    # create connection to database
    conn = createConn(database)
    
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")

    rows = cur.fetchall()
    for row in rows:
        print(row)


# writes the user details to the database
def insertUser(conn, user):
    sql = ''' INSERT INTO user(name ,age, job)
              VALUES(?,?,?)
    
            '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid


# creates a connection to the database 
def createConn(dbFile):
    conn = 'None'
    try:
        conn = sqlite3.connect(dbFile)
        return conn
        #print(sqlite3.version)
    except Error as e:
        print('DB connection error: ', e)


# this function creates a table from the connection string or details and the sql script that are provided.
def createTable(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print('create table error: ', e)


if __name__ == '__main__':
    main() 
        
