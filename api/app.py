#########################################################
#Aluno
#########################################################
#Fernando Chiareli Ferreira - 2022251758

#########################################################
#Incio das importacoes
#########################################################
import uuid
import jwt
from componentes.baseDeDados import conectar,secret_key
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
from componentes.Registro import Registro
from componentes.Geral import Geral
#########################################################
#fim das importacoes
#########################################################

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

##########################################################
#Estrutura inicial do projeto
##########################################################
if __name__ == "__main__":#estrutura inicial do projeto
    #Configuração básica do registro
    #log.basicConfig(filename='bdLog.log', level=log.INFO,format='%(asctime)s [%(levelname)s]: %(message)s')
    host = '127.0.0.1'
    port = 5000
    #log.info(f'API v1.0 online: http://{host}:{port}')#escrever no arquivo de log
    app.register_blueprint(Registro)
    app.register_blueprint(Musicas)
    app.register_blueprint(Geral)
    app.run(host=host, debug=True, threaded=True, port=port)#local da execucao + porta da execucao lembrando que a base de dados esta na 5432
    
