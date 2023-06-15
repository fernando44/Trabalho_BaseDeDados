import psycopg2

#CHAVE SECRETA
secret_key = "chave"#chave para token

## DATABASE ACCESS
def conectar():# Funcao para se conectar ao banco de dados
     return psycopg2.connect("dbname=streaming user=postgres password=admin")#estrutura de conexao simples pasando a base de dados o usuario e a senha 
