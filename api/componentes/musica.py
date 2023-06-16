import uuid
from flask import Blueprint, jsonify, request
import flask
import jwt
import psycopg2
from componentes.baseDeDados import conectar,secret_key

Musicas = Blueprint('Musicas',__name__)

#escutar musica
@Musicas.route('/dbproj/<songID>', methods=['PUT'])
def escutarMusica(songID):
    jwtToken = request.headers.get('results')
    if jwtToken:#USUARIO POSSUI TOKEN
        statement = "SELECT * FROM songs WHERE ismn = %s"
        values = (songID)#verificar musica
        conn = conectar()
        cur = conn.cursor()
        cur.execute(statement,(values,))

        row = cur.fetchone()

        if row is not None:#se for artista
            return jsonify({"Status: 200 ok  "+"Musica": row[1]+"  tocando"}),200
        
        else:
            return jsonify({"erro": "Musica não encontrada"}),404

    else:
        return jsonify({"erro": "Logar novamente"}),404


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

            #verificar se existe todos os artistas
            verificar = verificarArtistas(info)
            if verificar is 'erro':
                return jsonify({"erro": "Outros artistas não encontrado"}),404
            
            aux1 = info["outrosArtistas"]
            statement = "INSERT INTO songs (ismn,nome,duracao,datapublicacao,outrosartistas,artist_usuario_id) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (idStr, info['nome'], info['duracao'], info['dataDePublicacao'], aux1, info['artista'])
            cur.execute(statement,values)
            conn.commit()
            resposta = jsonify(
            {
                'mensagem': 'Operacao realizada com sucesso /\ Songid:{}'.format(idStr),
            }
            )
            
            return resposta,200

        else:#nao é artista
           return jsonify({"erro": "Artista não encontrado"}),404

    else:#NAO POSSUI TOKEN
        return jsonify({"erro": "Logar novamente"}),404


def verificarArtistas(aux):
    conn = conectar()
    cur = conn.cursor()
    aux1 = aux["outrosArtistas"]
    indice = 0

    while indice < len(aux1)    :
        statement = "SELECT * FROM artist WHERE usuario_id = %s"
        values = (aux1[indice])#verificar se é um artista
        #Executar a consulta
        cur.execute(statement,(values,))
        row = cur.fetchone()
        if row is None:#se for artista
            return 'erro'
        indice += 1

# Adicionar album
@Musicas.route('/dbproj/album', methods=['POST'])#adicionar album a base de dados
def addAlbum():
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

            #verificar se existe todos os artistas
            #verificar = verificarArtistas(info)
            #if verificar is 'erro':
            #    return jsonify({"erro": "Outros artistas não encontrado"}),404
           
            aux1 = info["musicas"]
            print(aux1)
            statement = "INSERT INTO album (id,nome,datapublicacao,ismn, artist_usuario_id) VALUES (%s, %s, %s, %s, %s)"
            values = (idStr, info['nome'], info['dataDePublicacao'], aux1, info['artista'])
            cur.execute(statement,values)
            conn.commit()
            resposta = jsonify(
            {
                'mensagem': 'Operacao realizada com sucesso /\ albumId:{}'.format(idStr),
            }
            )
            
            return resposta,200

        else:#nao é artista
           return jsonify({"erro": "Artista não encontrado"}),404

    else:#NAO POSSUI TOKEN
        print("vazio")


@Musicas.route('/dbproj/song', methods=['GET'])
def search_song():
    keyword = request.args.get('keyword')
    conn = conectar()
    cur = conn.cursor()
    statement = "SELECT * FROM songs WHERE nome LIKE '%' || '"+keyword+"' || '%'"
    
    cur.execute(statement)
    results = cur.fetchall()

    # Fecha a conexão com o banco de dados
    cur.close()
    conn.close()
    
    return jsonify(results),200



@Musicas.route('/dbproj/artist_info/<artist_id>', methods=['GET'])#informações do artista
def artistInfo(artist_id):
    conn = conectar()
    cur = conn.cursor()

    # Consulta SQL para obter as informações do artista, músicas, álbuns e listas de reprodução
    statement = '''
    SELECT a.nomeartistico, s.nome AS song_name, al.nome AS album_name, p.nome AS playlist_name
    FROM artist a
    LEFT JOIN songs s ON a.usuario_id = s.artist_usuario_id
    LEFT JOIN album al ON s.ismn = al.ismn
    LEFT JOIN usuario_playlist up ON a.usuario_id = up.usuario_id
    LEFT JOIN playlist p ON up.playlist_id = p.id
    WHERE a.usuario_id = %s
    '''

    cur.execute(statement, (artist_id,))
    rows = cur.fetchall()
    print(rows)
    #Formata os resultados em um dicionário
    artist_info = {
        'artist_name': rows[0][0],
        'songs': [],
        'albums': [],
        'playlists': []
    }

    for row in rows:
        if row[1]:
            artist_info['songs'].append(row[1])
        if row[2]:
            artist_info['albums'].append(row[2])
        if row[3]:
            artist_info['playlists'].append(row[3])

    #Fecha a conexão com o banco de dados
    conn.close()

    return jsonify(artist_info)


##########################################################
# Procurar musica
##########################################################
@Musicas.route('/dbproj/song/<ismn>', methods=['GET'])
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

