from flask import Flask, jsonify, request, send_file,request
from rtree import index
from flask_cors import CORS
import face_recognition
from PIL import Image
import os

idx = index.Index()

##def init_rtree():
   ##
    
    
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
        }
    }
)
''' Correrlo una vez
def get_face_embedding(img_path):
        a = face_recognition.load_image_file(img_path)
        messi_encoding = face_recognition.face_encodings(a)
        found = len(messi_encoding) > 0
        return messi_encoding, found

def add_to_train_set(train_path, train_set_file, person_name):
        person_path = train_path + "/" + person_name + "/"
        imgs_names = os.listdir(person_path)
        for img_name in imgs_names:
                face_embedding , found = get_face_embedding(person_path + "/" + img_name)
                if found:
                    train_set_file.write(person_name)
                    for x in face_embedding[0]:
                            train_set_file.write("," + str(x))
                    train_set_file.write("/n")

def create_train_set(train_path):
        persons_names = os.listdir(train_path)
        with open("train_set.txt", "w") as train_set_file:
                for person_name in persons_names:
                        add_to_train_set(train_path, train_set_file, person_name)

create_train_set("./lfw")
'''

#def RTree()
#indexar vectores de imagenes del dataset
#def KNN_RTree(vector_carac, k)

#def KNN(vector_carac, k)

#def Range_Search(vector_carac, r)

@app.route('/',methods=['GET'])
def home():
    return ('API BD2PR')

@app.route('/', methods=['POST'])##Recibe input y lo mete al r tree y devuelve el más parecido
def insert_image():
    uploaded_file = request.files['file']
    known_image = face_recognition.load_image_file("messi.jpg")
    Image_From_Frontend = face_recognition.load_image_file(uploaded_file)

    messi_encoding = face_recognition.face_encodings(known_image)[0]##Extrae vector caracteristico

    try:
        #unknown_encoding = face_recognition.face_encodings(Image_From_Frontend)[0]
        face_locations = face_recognition.face_locations(Image_From_Frontend)
        face_image = {}
        for face_location in face_locations:
            top, right, bottom, left = face_location
            face_image = Image_From_Frontend[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)
            pil_image.show()

        unknown_encoding = face_recognition.face_encodings(face_image)[0]   
    except IndexError :
        Rpta = "No se detecto cara"

    else:
        results = face_recognition.compare_faces([messi_encoding], unknown_encoding)
        Rpta = bool(results[0])

    return jsonify(Rpta)
    #debe retornar imagen 
    
if __name__ == '__main__':
    app.run(debug=True,port=5000)
