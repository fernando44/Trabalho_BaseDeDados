#Alunos
#Fernando Chiareli Ferreira - 
#Kevin dourado - 

#Incio das importacoes
from flask import Flask, request#importacao padrao para utilizacao do flask
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

#
# Adicionar usuario
#
@app.route('/dbproj/user', methods=['POST'])#adicionar usuario a base de dados
def add():
    users = request.get_json()
    try:
        print( type(users['id']))#teste apagar
        conn = conectar()
        cur = conn.cursor()
        cur.execute("INSERT INTO usuario (id, nome, idade, sexo, address, number, saldofinal, premium_status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", 
                    (users['id'], users['nome'], users['idade'], users['sexo'], users['address'], users['number'], users['saldofinal'], users['premium_status']) )
        conn.commit()
        resposta = jsonify(
            {
                'mensagem':'Operacao realizada com sucesso',
                #'id' : cur.lastrowid
            }
        )
    except Exception as e:
        conn.rollback()
        resposta = jsonify({'erro' : str(e)})
    finally:
        conn.close()
    return resposta

#
# Adicionar musica
#
@app.route('/dbproj/album', methods=['POST'])#adicionar usuario a base de dados
def add():
     print("Verificar se é um usuario artista\nadicionar a musica")
     albuns = request.get_json()
     return 0

#
# Procurar musica
#
@app.route('/dbproj/song/<idMusica>', methods=['GET'])#adicionar usuario a base de dados
def add():
     print(idMusica)
     print("procurar musica pelo id")
     albuns = request.get_json()
     return 0

#
# Procurar artista (info artistas)
#
@app.route('/dbproj/artist_info/<idArtista>', methods=['GET'])#adicionar usuario a base de dados
def add():
     print(idArtista)
     print("procurar artista pelo id")
     albuns = request.get_json()
     return 0

#
# apagar depois
#
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

#
#Estrutura inicial do projeto
#
if __name__ == "__main__":#estrutura inicial do projeto
    app.run(debug=True,host="localhost", port=5000)#local da execucao + porta da execucao lembrando que a base de dados esta na 5432
