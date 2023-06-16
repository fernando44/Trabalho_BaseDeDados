import hashlib
import uuid
from flask import Flask, Blueprint, jsonify
import flask
import jwt
from componentes.baseDeDados import conectar,secret_key

Registro = Blueprint('Registro',__name__)

@Registro.route('/dbproj/user', methods=['POST'])#adicionar usuario
def adicionar():
    users = flask.request.get_json()
    try:#criar
            # Gera um UUID aleatório
            id = uuid.uuid4()
            # Obtém a representação inteira do UUID
            idStr = str(id)

            conn = conectar()
            cur = conn.cursor()
            # Gerar um hash da senha
            hash_senha = hashlib.sha256(users['password'].encode('utf-8')).hexdigest()
            hash_senha = str(hash_senha)
            print(users)
            statement = "INSERT INTO usuario (id, nome, idade, sexo, address, number, senha) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (idStr, users['username'], users['idade'], users['sexo'], users['address'], users['number'],  hash_senha)
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

@Registro.route('/dbproj/user', methods=['PUT'])#Logar
def logar():
    users = flask.request.get_json()
    try:#login
            conn = conectar()
            cur = conn.cursor()

            statement = "SELECT * FROM usuario WHERE nome = %s"
            values = (users['username'],)

            # Executar a consulta
            cur.execute(statement, values)

            # Obter os resultados da consulta
            result = cur.fetchone()

            if hashlib.sha256(users['password'].encode('utf-8')).hexdigest() == result[8]:
                payload = {'id': result[0], 'nome': result[1]}#informacoes do token
                jwtToken = jwt.encode(payload, secret_key, algorithm='HS256')#gerar o token
                response = jsonify({"message": "Login successful"})#enviar mensagem
                response.headers["status"] = "200"#envia o status
                response.headers["results"] = f"{jwtToken}"#enviar o token

            else:
                return jsonify({"message": "Login error login/senha não encontrado"})#enviar mensagem

    except Exception as e:
        conn.rollback()
        response = jsonify({'erro' : str(e)})
    finally:
        conn.close()
    return response