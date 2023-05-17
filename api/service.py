from flask import Flask, Blueprint, request, jsonify
import psycopg2

service = Blueprint('service',__name__)


@service.route('/', methods=['GET'])
def teste():
    return "APIII v.1.0"

#
# RETORNAR TODOS OS CLIENTES
#
@service.route('/aue', methods=['GET'])
def get_all():
    clientes = []
    try:
        con = psycopg2.connect(
        database="streaming",
        user="postgres",
        password="admin",
        host="localhost",
        port= '5432'
        )
        cursor_obj = con.cursor()
        cursor_obj.execute("SELECT * FROM usuario")
        
    except Exception as e:
        print(e)
        clientes = []

    return jsonify(clientes)