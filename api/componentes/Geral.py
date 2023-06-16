from datetime import date
import uuid
from dateutil.relativedelta import relativedelta
from datetime import date
from flask import Blueprint, jsonify, request
import flask
import jwt
from componentes.baseDeDados import conectar,secret_key
from flask import Blueprint

valor = 0

Geral = Blueprint('Geral',__name__)

##########################################################
# Upgrade de usuário para premium
##########################################################
@Geral.route('/dbproj/subcription', methods=['POST'])  # adicionar usuario a base de dados
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
                statement = "SELECT * FROM subscricao WHERE usuario_id = %s"
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
                statement_subscricao = "INSERT INTO subscricao (usuario_id, data_inicio, data_termino) VALUES (%s, %s, %s)"
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
    statement = "UPDATE usuario SET premiumstatus = True, saldofinal = saldofinal - %s WHERE id = %s"
    cur.execute(statement, (valor,id_usuario))

@Geral.route('/dbproj/playlist', methods=['POST'])#Crirar playlist
def createPlaylist():
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
            print(retorno[7])
            
            
            if retorno[7] == True:#se for premium
                statement = "SELECT * FROM subscricao WHERE usuario_id = %s"
                values = (retorno[0],)
                cur.execute(statement, values)
                retor = cur.fetchone()
                album = flask.request.get_json()
                print(album)

                # Gera um UUID aleatório
                id = uuid.uuid4()
                # Obtém a representação inteira do UUID
                idStr = str(id)
                
                musicas = album["songs"]
                
                if verificarMusicas(musicas) == 1:
                    return jsonify({'erro' : "ismn invalido"}), 400


                if album["visibility"].lower() == "public":
                    album["visibility"] = True
                
                elif album["visibility"].lower() == "private":
                    album["visibility"] = False

                else:
                    return "erro: visibility invalido", 400
                
                
                statement = "INSERT INTO playlist (id, nome, musicas, privatestatus) VALUES (%s, %s, %s, %s)"
                values = (idStr, album['name'], musicas, album["visibility"])
                cur.execute(statement, values)
     
                conn.commit()

                resposta = jsonify({'mensagem': 'Operacao realizada com sucesso',})

            else:
                return jsonify({'erro' : "user não é premium"}), 400

        except Exception as e:
            conn.rollback()
            resposta = jsonify({'erro': str(e)})
        finally:
            conn.close()

    else:
        return jsonify({'mensagem': 'sem token logar novamente',}), 400

    return resposta



def verificarMusicas(aux):
    conn = conectar()
    cur = conn.cursor()
    
    indice = 0

    while indice < len(aux)    :
        statement = "SELECT * FROM songs WHERE ismn = %s"
        values = (aux[indice])#verificar se existe
        #Executar a consulta
        cur.execute(statement,(values,))
        row = cur.fetchone()
        if row is None:#se for artista
            return 1
        indice += 1




@Geral.route('/dbproj/card', methods=['POST'])#Crirar cartão
def criarCartao():
    jwtToken = request.headers.get('results')
    if jwtToken:  # USUARIO POSSUI TOKEN
        payload = jwt.decode(jwtToken, secret_key, algorithms=['HS256'])
        try:
            conn = conectar()
            cur = conn.cursor()
            statement = "SELECT * FROM administrador WHERE usuario_id = %s"
            values = (payload['id'],)
            cur.execute(statement, values)
            retorno = cur.fetchone()
            
            if retorno is not None and retorno[0]:  # se houver um retorno válido
                info = flask.request.get_json()

                if int(info["number_cards"]) < 0:#cartões negativos
                    return jsonify({'erro': "valor de cartões invalido"}), 400

                if float(info["card_price"]) != 10 and float(info["card_price"])  != 20 and float(info["card_price"])  != 30:#valor errado
                    return jsonify({'erro': "valor do cartão invalido"}), 400
                
                indice = 0
                cartoes = []
                info["number_cards"] = int(info["number_cards"])
                while indice < info["number_cards"]    :
                    id = uuid.uuid4()
                    idStr = str(id)

                    statement = "INSERT INTO pre_paid_cards (id_card,valor) VALUES (%s, %s)"
                    values = (idStr,float(info["card_price"]))
                    
                    cur.execute(statement,(values))
                    cartoes.append(idStr)
                    indice += 1
                    
                    
                conn.commit()
                return jsonify(
                {
                    'mensagem': 'Operacao realizada com sucesso /\ cartões:{}'.format(cartoes),
                }
                )
            
            else:
                return jsonify({'erro': "admin invalido"}), 400

        except Exception as e:
            return jsonify({'erro': str(e)})
        finally:
            conn.close()

    else:
        return jsonify({'erro': "Logar novamente"}), 400



@Geral.route('/dbproj/comments/<songID>', methods=['POST'])#relatório mensal
def generate_monthly_report(songID):
    jwtToken = request.headers.get('results')
    try:
        if jwtToken:  # USUARIO POSSUI TOKEN
            info = flask.request.get_json()
            payload = jwt.decode(jwtToken, secret_key, algorithms=['HS256'])
            conn = conectar()
            cur = conn.cursor()
            
            statement = "SELECT * FROM songs WHERE ismn = %s"
            cur.execute(statement, (songID,))
            musica = cur.fetchone()

            if musica:
                statement = "SELECT * FROM usuario WHERE id = %s"
                cur.execute(statement, (payload["id"],))
                user = cur.fetchone()

                if user:
                    adicionarComent(info["comment"],payload["id"], songID,0)
                
                else:
                    return jsonify({"erro": "usuario não encontrado"}), 404
                

            else:
                return jsonify({"erro": "Música não encontrada"}), 404
        

        else:
            return jsonify({'erro': "Logar novamente"}), 400

    except Exception as e:
            return jsonify({'erro': str(e)})
    
    finally:
        conn.close()

def adicionarComent(comentario, idUser, idMudica, idAnterior):
    conn = conectar()
    cur = conn.cursor()
    id = uuid.uuid4()
    

    # Obtém a representação inteira do UUID
    idStr = str(id)
    statement_subscricao = "INSERT INTO comentario (id, data, comentario, comentario_id, songs_ismn, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (idStr, str(date.today()) , comentario, idAnterior, idMudica,idUser)
    cur.execute(statement_subscricao, values)
    if not cur.fetchone():
        statement_subscricao = "INSERT INTO comentario (id, data, comentario, comentario_id, songs_ismn, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)"
        values = (0, str(date.today()) , 0, idAnterior, idMudica,idUser)
        cur.execute(statement_subscricao, values)
        conn.commit()

    statement_subscricao = "INSERT INTO comentario (id, data, comentario, comentario_id, songs_ismn, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (idStr, str(date.today()) , comentario, idAnterior, idMudica,idUser)
    cur.execute(statement_subscricao, values)
    conn.commit()
    