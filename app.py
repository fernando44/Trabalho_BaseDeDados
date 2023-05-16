from flask import Flask
from flask_cors import CORS
from api.service import cliente

app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})

#
# REGISTRAR AS ROTAS
#
app.register_blueprint(service,url_prefix='/api/service')

#
# OPERAÇÕES
#
@app.route("/")
def info():
    return "API v.1.0"

if __name__ == "__main__":
    app.run(debug=True,host="localhost", port=5000)