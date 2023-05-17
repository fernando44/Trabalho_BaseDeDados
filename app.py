from flask import Flask
from flask import jsonify
from flask_cors import CORS
import psycopg2
#from api.service import service

app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})
#
# REGISTRAR AS ROTAS
#
#app.register_blueprint(service,url_prefix='/api/service')

def conectar():
     return psycopg2.connect("dbname=streaming user=postgres password=admin")

#
# OPERAÇÕES
#
@app.route("/")
def info():
    return "API v.1.0"

@app.route("/aue", methods=['GET'])
def teste():
        clientes = []
        try:
            conn = conectar()
            cur = conn.cursor()
            cur.execute("SELECT * FROM administrador")

            for i in cur.fetchall():
                cliente ={}
                print(i)
                cliente["nome"] = str(i["nome"])
                cliente["usuario_person_id"] = str(i["usuario_person_id"])
               
                clientes.append(clientes)

        except Exception as e:
             print(e)
             clientes=[]
        
        return jsonify(clientes)

if __name__ == "__main__":
    app.run(debug=True,host="localhost", port=5000)
