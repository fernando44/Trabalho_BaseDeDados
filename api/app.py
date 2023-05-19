#########################################################
#Alunos
#########################################################
#Fernando Chiareli Ferreira - 
#Kevin dourado - 

#########################################################
#Incio das importacoes
#########################################################
import uuid
import os
import logging as log
from flask import Flask, request#importacao padrao para utilizacao do flask
from flask import jsonify
import flask#para formatar as informações e enviar ao navegador 
from flask_cors import CORS#importacao padrao para utilizacao do flask
import psycopg2#importacao para conexao com base de dados postgree
#########################################################
#fim das importacoes
#########################################################

#########################################################
#inicio do programa
#########################################################
app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})
os.environ['FLASK_ENV'] = 'production'

##########################################################
## DATABASE ACCESS
##########################################################
def conectar():# Funcao para se conectar ao banco de dados
     return psycopg2.connect("dbname=streaming user=postgres password=admin")#estrutura de conexao simples pasando a base de dados o usuario e a senha 

##########################################################
# Inicio das OPERAÇÕES
##########################################################
@app.route("/")#Operacao no caso / apresentar informações da versão da api
def info():
    return "API v.1.0"

##########################################################
# Adicionar usuario
##########################################################
@app.route('/dbproj/user', methods=['POST'])#adicionar usuario a base de dados
def add():
    users = flask.request.get_json()
    try:
        # Gera um UUID aleatório
        id = uuid.uuid4()
        # Obtém a representação inteira do UUID
        idStr = str(id)

        conn = conectar()
        cur = conn.cursor()
        
        statement = "INSERT INTO usuario (id, username, idade, sexo, address, number, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (idStr, users['username'], users['idade'], users['sexo'], users['address'], users['number'],  users['password'])
        cur.execute(statement,values)

        conn.commit()
        resposta = jsonify(
            {
                'mensagem':'Operacao realizada com sucesso',
            }
        )
    except Exception as e:
        conn.rollback()
        resposta = jsonify({'erro' : str(e)})
    finally:
        conn.close()
    return resposta

##########################################################
# Adicionar musica
##########################################################
@app.route('/dbproj/album', methods=['POST'])#adicionar musica a base de dados
def addMusic():
    print("Verificar se é um usuario artista\nadicionar a musica")
    
    albuns = request.get_json()
    try:
        id = uuid.uuid4()
        idStr = str(id)

        conn=conectar
        cur = conn.cursor()

        statement= "INSERT INTO songs (ism, nome, duracao) VALUES (%s, %s, %s)"
        values=(idStr,albuns['nome'], albuns['duracao'])
        cur.execute(statement,values)

        conn.commit()

    except Exception as e:
        conn.rollback()
        resposta = jsonify({'erro' : str(e)})
    finally:
        conn.close()
    return resposta


##########################################################
# Procurar musica
##########################################################
@app.route('/dbproj/song/<ismn>', methods=['GET'])
def procuraMusica(ismn):
    try:
        conn = conectar()
        cur = conn.cursor()

        # Consulta SQL para buscar a música pelo ID
        statement = "SELECT * FROM songs WHERE ismn = %s"
        cur.execute(statement, (ismn,))
        musica = cur.fetchone()

        if musica:
            # Extrai os dados da música
            ismn, nome, duracao, = musica

            # Cria um dicionário com os dados da música
            musica_dict = {
                "ismn": ismn,
                "nome": nome,
                "duracao": duracao,
            }

            # Retorna a música encontrada em formato JSON
            return jsonify(musica_dict), 200
        else:
            # Retorna uma mensagem de erro se a música não for encontrada
            return jsonify({"erro": "Música não encontrada"}), 404

    except (psycopg2.Error, Exception) as error:
        # Trata possíveis erros
        return jsonify({"erro": str(error)}), 500

    finally:
        # Fecha a conexão com o banco de dados
        if conn:
            conn.close()

##########################################################
# Procurar artista (info artistas)
##########################################################
@app.route('/dbproj/artist_info/<idArtista>', methods=['GET'])#adicionar usuario a base de dados
def procuraArtista():
     print(idArtista)
     print("procurar artista pelo id")
     albuns = request.get_json()
     return 0

##########################################################
# apagar depois
##########################################################
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

##########################################################
#Estrutura inicial do projeto
##########################################################
if __name__ == "__main__":#estrutura inicial do projeto
    # Configuração básica do registro
    log.basicConfig(filename='bdLog.log', level=log.INFO,format='%(asctime)s [%(levelname)s]: %(message)s')
    host = '127.0.0.1'
    port = 5000
    log.info(f'API v1.0 online: http://{host}:{port}')#escrever no arquivo de log
    app.run(host=host, debug=False, threaded=True, port=port)#local da execucao + porta da execucao lembrando que a base de dados esta na 5432
    