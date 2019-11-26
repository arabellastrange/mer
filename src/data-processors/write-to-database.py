import json
import os
import mysql.connector
import pandas as pd
from pandas.io.json import json_normalize

# write acousticbrainz dataset to mySQL database
PATH_HIGH = 'I:\Science\CIS\wyb15135\datasets_unmodified\\acousticbrainz-highlevel-json-20150130\highlevel'
PATH_LOW = 'I:\Science\CIS\wyb15135\datasets_unmodified\\acousticbrainz-lowlevel-json-20150129\lowlevel'


def list_databases():
    mydb = mysql.connector.connect(
        host="devweb2019.cis.strath.ac.uk",
        user="wyb15135",
        passwd="yourpassword"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SHOW DATABASES")

    mycursor.close()
    mydb.close()


def connect_to_database(database_name):
    try:
        cnx = mysql.connector.connect(user='wyb15135', password='password',
                                      host='devweb2019.cis.strath.ac.uk',
                                      database=database_name)
        if cnx.is_connected():
            db_Info = cnx.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
    except mysql.connector.Error as error:
        print("Failed to create table in MySQL: {}".format(error))

    return cnx


def close_database_connection(connection):
    connection.close()


def write_to_database(connection):
    cursor = connection.cursor()
    cursor.execute('')
    cursor.close()


def read_json_directory(path):
    data = pd.DataFrame()
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(path):
        print('opened directory')
        for file in f:
            if '.json' in file:
                files.append(os.path.join(r, file))
            # if len(files) > 10:
            #     break

    for f in files:
        print("reading: " + f)
        with open(f) as json_file:
            j = json_normalize(json.load(json_file))
            data = data.append(j, sort=True)


def main():
    read_json_directory(PATH_HIGH)
    read_json_directory(PATH_LOW)


if __name__ == '__main__':
    main()
