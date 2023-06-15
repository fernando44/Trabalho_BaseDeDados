import uuid
from flask import Blueprint, jsonify, request
import flask
import jwt
from componentes.baseDeDados import conectar,secret_key

Musicas = Blueprint('Musicas',__name__)
"""
    "nome": "musica1",
    "dataDePublicacao": "22/03/99",
    "artista": "id",
    "outrosArtistas": "id1,id2,id3"
"""
# Adicionar musica
@Musicas.route('/dbproj/song', methods=['POST'])#adicionar musica a base de dados
def addMusic():
    jwtToken = request.headers.get('results')
    if jwtToken:#USUARIO POSSUI TOKEN
        
        payload = jwt.decode(jwtToken, secret_key, algorithms=['HS256'])
        conn = conectar()
        cur = conn.cursor()

        statement = "SELECT * FROM artist WHERE usuario_id = %s"
        values = (payload["id"])#verificar se é um artista
        #Executar a consulta
        cur.execute(statement,(values,))

        row = cur.fetchone()

        if row is not None:#se for artista
            info = flask.request.get_json()
            print(info)
            # Gera um UUID aleatório
            id = uuid.uuid4()
            # Obtém a representação inteira do UUID
            idStr = str(id)
            statement = "INSERT INTO songs (ismn,nome,duracao,datapublicacao,outrosartistas,artist_usuario_id) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (idStr, info['nome'], info['duracao'], info['dataDePublicacao'], info['artista'], info['outrosArtistas'])
            cur.execute(statement,values)
            conn.commit()
            resposta = jsonify(
                {
                    'mensagem':'Operacao realizada com sucesso',
                }
            )
            return resposta,200

        else:#nao é artista
           return jsonify({"erro": "Artista não encontrado"}),404

    else:#NAO POSSUI TOKEN
        print("vazio")

    

"""
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
"""   