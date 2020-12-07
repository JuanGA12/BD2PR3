from flask import Flask, jsonify
from rtree import index

idx = index.Index()

def init_rtree():
   ##Si usamos db, cargar los datos de la db a idx.
    
app = Flask(__name__)

@app.route('/',methods=['GET'])
def home():
    elem1 = 'hola'
    elem2 = 5
    return jsonify(caca = g)

@app.route('/', methods=['POST'])##Recibe input y lo mete al r tree y devuelve el más parecido
def insert_image(image):
    #magia
    
if __name__ == '__main__':
    app.run(debug=True,port=5000)
