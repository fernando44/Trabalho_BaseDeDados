#Incio das importacoes
from flask import Flask#importacao padrao para utilizacao do flask
from flask import jsonify#para formatar as informações e enviar ao navegador 
from flask_cors import CORS#importacao padrao para utilizacao do flask
import psycopg2#importacao para conexao com base de dados postgree
#fim das importacoes

#inicio do programa
app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})

def conectar():# Funcao para se conectar ao banco de dados
     return psycopg2.connect("dbname=streaming user=postgres password=admin")#estrutura de conexao simples pasando a base de dados o usuario e a senha 

#
# Inicio das OPERAÇÕES
#
@app.route("/")#Operacao no caso / apresentar informações da versão da api
def info():
    return "API v.1.0"

@app.route("/teste", methods=['GET'])#Operacao /teste metodo GET select na tabela administrador  
def teste():
        clientes = []
        try:
            conn = conectar()#conecta ao banco de dados
            cur = conn.cursor()#utiliza o cur para executar comando no banco 
            cur.execute("SELECT * FROM administrador")#utiliza o cur.execute para solicitar a execucao de comandos no banco 

            for i in cur.fetchall():#A variavel i contem as informacoes do banco em forma de conjunto de elementos 
                cliente ={}
                print(i)#verificacao retirar depois
                cliente["nome"] = str(i["nome"])
                cliente["usuario_person_id"] = str(i["usuario_person_id"])
               
                clientes.append(clientes)#add a estutura para printar depois

        except Exception as e:
             print(e)#caso de erro
             clientes=[]
        
        return jsonify(clientes)#joga as informacoes na tela

#Estrutura inicial do projeto
if __name__ == "__main__":#estrutura inicial do projeto
    app.run(debug=True,host="localhost", port=5000)#local da execucao + porta da execucao lembrando que a base de dados esta na 5432
