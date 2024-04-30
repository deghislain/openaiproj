import psycopg2
import os



#reading PostgresSQL credentials from environment variables

PG_USERNAME = os.getenv('PG_USERNAME')
PG_PASSWORD = os.getenv('PG_PASSWORD')

def get_user_by_username(username: str):
    global connection, cursor, user
    try:
        connection = psycopg2.connect(database='appdb',
                                      user=PG_USERNAME,
                                      password=PG_PASSWORD,
                                      host='127.0.0.1',
                                      port=5432
                                      )

        cursor = connection.cursor()
        select_query = "select *from users where username = %s"
        cursor.execute(select_query, [username,])
        user = cursor.fetchone()
        return user.__getitem__(4)
    except psycopg2.Error as error:
        print("Error while connecting to postgre", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("PostgresSQL is now closed")

#user = get_user_by_username("armelo1")

#print("List of users:", user.__getitem__(1))
