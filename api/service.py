from flask import Flask, Blueprint, request, jsonify
import psycopg2

con = psycopg2.connect(
database="principal",
user="postgres",
password="senha",
host="localhost",
port= '5432'
)
cursor_obj = con.cursor()

#
# RETORNAR TODOS OS CLIENTES
#
@service.route('/', methods=['GET'])
def get_all():
    clientes = []
    try:
        cursor_obj.execute("SELECT * FROM tabela")
        
    except Exception as e:
        print(e)
        clientes = []

    return jsonify(clientes)