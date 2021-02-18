from flask import Flask, render_template, request, Response
import json
import dbcreds
import mariadb
import sys

#create a Flask object. Our entry point for the flask server
app = Flask(__name__)

#my_animals = ["Bear", "Lion", "Tiger", "Cheetah", "Wolf"]
def connection():
    return mariadb.connect(
        user = dbcreds.user,
        password = dbcreds.password,
        host = dbcreds.host,
        port = dbcreds.port,
        database = dbcreds.database   
    )

#this is called a decoration in flask. any requests to the / endpoint should call the following function   
@app.route('/animals', methods=["GET", "POST", "DELETE", "PATCH"])
def animals():
    if request.method == 'GET':
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM my_animals")
            result = cursor.fetchall()
            my_animals=[]
            for row in result:
                animal={
                    "id" : row[0], 
                    "animal_name": row[1]
                }
                my_animals.append(animal) 
        except mariadb.OperationalError:
            return Response("connection problem", mariadb.OperationalError)  
        finally:
            if(cursor != None):
                cursor.close()
            if(conn != None):
                conn.rollback()
                conn.close() 
                return Response(
                    json.dumps(my_animals, default=str),
                    mimetype="application/json",
                    status = 200
                )

    elif request.method == 'POST':
        animal_name = "Python"
        print(animal_name)
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO my_animals(animal_name) VALUES (?)",[animal_name])
            conn.commit()
        except mariadb.OperationalError:
            return Response("connection problem", mariadb.OperationalError)
        finally:
            if (cursor != None):
                cursor.close()
            if (conn != None):
                conn.rollback()
                conn.close()  
                return Response(
                    "You added an " + animal_name + "to the database.",
                     mimetype="text/html",
                     status=201
                )
    
    elif request.method == 'PATCH':
        animal_name = "Zebra"
        print(animal_name + "line 74")
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("UPDATE my_animals SET animal_name=? WHERE id=?", [animal_name, "7"])
            conn.commit()
        except mariadb.OperationalError:
            return Response("connection problem", mariadb.OperationalError)
        finally:
            if (cursor != None):
                cursor.close()
            if (cursor != None):
                conn.rollback()
                conn.close()
                return Response(
                    "You updated an " + animal_name,
                     mimetype="text/html",
                     status=201
                )    
    
    elif request.method == 'DELETE':
        animal_name = "Bear"
        try:
            conn = connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM my_animals WHERE animal_name=?", [animal_name])
            conn.commit()
        except mariadb.OperationalError:
            return Response("connection problem", mariadb.OperationalError)
        finally:
            if (cursor != None):
                cursor.close()
            if (cursor != None):
                conn.rollback()
                conn.close() 
                return Response(
                     "You deleted " + animal_name + " from the database",
                     mimetype="text/html",
                     status=201
                )                
    else:
        return Response(
            "There was an error!",
            mimetype="text/html",
            status=401
        )     

