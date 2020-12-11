from flask import Flask, jsonify, request
from rtree import index
from flask_cors import CORS

idx = index.Index()

##def init_rtree():
   ##Si usamos db, cargar los datos de la db a idx.
    
    
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
        }
    })


@app.route('/',methods=['GET'])
def home():
    elem1 = 'hola'
    elem2 = 5
    return jsonify(elem1=elem2)

@app.route('/', methods=['POST'])##Recibe input y lo mete al r tree y devuelve el más parecido
def insert_image():
     file = request.files.get("image")
     return jsonify("hola ")
    #magia
    
if __name__ == '__main__':
    app.run(debug=True,port=5000)
