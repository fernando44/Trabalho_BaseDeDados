#########################################################
#Alunos
#########################################################
#Fernando Chiareli Ferreira - 
#Kevin dourado - 

#########################################################
#Incio das importacoes
#########################################################
import uuid
import jwt
import hashlib
from flask import Blueprint, Flask, render_template
from dateutil.relativedelta import relativedelta
from datetime import date
import os
import logging as log
from flask import Flask, request#importacao padrao para utilizacao do flask
from flask import jsonify
import flask#para formatar as informações e enviar ao navegador 
from flask_cors import CORS#importacao padrao para utilizacao do flask
import psycopg2
from componentes.musica import Musicas
from componentes.baseDeDados import conectar#importacao para conexao com base de dados postgree
from componentes.Registro import Registro
#########################################################
#fim das importacoes
#########################################################

#########################################################
#var global
#########################################################
secret_key = "chave"#chave para token

#########################################################
#inicio do programa
#########################################################
app = Flask(__name__, static_folder='staticFiles')
CORS(app,resources={r"/*":{"origins":"*"}})
os.environ['FLASK_ENV'] = 'production'

##########################################################
# Inicio das OPERAÇÕES
##########################################################
@app.route("/")#Operacao no caso / apresentar informações da versão da api
def info():
    return "Api v 1.0" #render_template('index.html')

##APAGAR?
@app.route('/example', methods=['GET'])
def example():
    response = jsonify({"message": "Exemplo de cabeçalho personalizado"})
    response.headers['Custom-Header'] = 'Custom-Value'
    return response



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
# Upgrade de usuário para premium
##########################################################
@app.route('/dbproj/subcription', methods=['POST'])  # adicionar usuario a base de dados
def upgrade():
    jwtToken = request.headers.get('results')
    if jwtToken:#USUARIO POSSUI TOKEN
        payload = jwt.decode(jwtToken, secret_key, algorithms=['HS256'])
        try:
            conn = conectar()
            cur = conn.cursor()
            statement = "SELECT * FROM usuario WHERE id = %s"
            values = (payload['id'],)
            cur.execute(statement, values)
            retorno = cur.fetchone()
            dia = date.today()
            print(retorno[7])
            if retorno[7]:
                print(retorno[0])
                statement = "SELECT * FROM subscricao WHERE id_usuario = %s"
                values = (retorno[0],)
                cur.execute(statement, values)
                retor = cur.fetchone()
                dia = retor[2]
               
            
            if float(retorno[6]) > 21 and float(retorno[6]) >= 42:
                atualiza_status(retorno[0], 42,conn)
                mes = dia + relativedelta(months=6)

            elif float(retorno[6]) > 7 and float(retorno[6]) >=21:
                atualiza_status(retorno[0], 21,conn)
                mes = dia + relativedelta(months=3)
            
            elif float(retorno[6]) >0 and float(retorno[6]) >=7:
                atualiza_status(retorno[0], 7,conn)
                mes = dia + relativedelta(months=1)

            else:
                return jsonify({'mensagem': 'sem dinheiro',})


            if retorno[7]:
                statement_subscricao = "UPDATE subscricao SET data_termino = %s WHERE id_usuario = %s"
                values = (str(mes),retorno[0])
                cur.execute(statement_subscricao, values)
                 

            else:
                statement_subscricao = "INSERT INTO subscricao (id_usuario, data_inicio, data_termino) VALUES (%s, %s, %s)"
                values = (payload['id'], str(date.today()) , str(mes))
                cur.execute(statement_subscricao, values)

            conn.commit()

            resposta = jsonify({'mensagem': 'Operacao realizada com sucesso',})

        except Exception as e:
            conn.rollback()
            resposta = jsonify({'erro': str(e)})
        finally:
            conn.close()

    else:
        return jsonify({'mensagem': 'sem token logar novamente',})

    return resposta

def atualiza_status(id_usuario, valor,conn):
    cur = conn.cursor()
    statement = "UPDATE usuario SET premium_status = True, saldofinal = saldofinal - %s WHERE id = %s"
    cur.execute(statement, (valor,id_usuario))


##########################################################
#Estrutura inicial do projeto
##########################################################
if __name__ == "__main__":#estrutura inicial do projeto
    # Configuração básica do registro
    #log.basicConfig(filename='bdLog.log', level=log.INFO,format='%(asctime)s [%(levelname)s]: %(message)s')
    host = '127.0.0.1'
    port = 5000
    #log.info(f'API v1.0 online: http://{host}:{port}')#escrever no arquivo de log
    app.register_blueprint(Registro)
    app.register_blueprint(Musicas)
    app.run(host=host, debug=True, threaded=True, port=port)#local da execucao + porta da execucao lembrando que a base de dados esta na 5432
    
