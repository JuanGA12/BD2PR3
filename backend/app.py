from flask import Flask, jsonify, request, send_file, request
from flask_cors import CORS
import face_recognition
from PIL import Image
import os 
import math
import base64
from classifiers import KNNClassifierSeq, KNNClassifierRTree, HyperCubeClassifierRTree
from rangecontainers import RangeContainers
from take_time import take_time


app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
        }
    }
)

def read_train_set():
    lines = [line.split(",") for line in open("train_set.txt", "r").read().split('/n')]
    return [(line[0], [float(i) for i in line[1:]]) for line in lines[:-1]]

train_set = read_train_set()
knn_s = RangeContainers(KNNClassifierSeq, train_set, [(0, 100), (0, 200), (0, 400), (0, 800), (0, 1600), (0, 3200), (0, 6400), (0, 13171)])
knn_r = RangeContainers(KNNClassifierRTree, train_set, [(0, 100), (0, 200), (0, 400), (0, 800), (0, 1600), (0, 3200), (0, 6400), (0, 13171)])
hcube_r = RangeContainers(HyperCubeClassifierRTree, train_set, [(0, 100), (0, 200), (0, 400), (0, 800), (0, 1600), (0, 3200), (0, 6400), (0, 13171)])


############################
#           FLASK          #
############################
     
@app.route('/',methods=['GET'])
def home():
    return ('API BD2PR3')

@app.route('/', methods=['POST'])
def Compare_Image():
    IMAGE = request.files['file']
    Algoritmo = request.form['Algoritmo']
    K  = request.form['K']
    R = request.form['R']
    P = request.form['P']

    Image_From_Frontend = face_recognition.load_image_file(IMAGE)
    face_locations = face_recognition.face_locations(Image_From_Frontend)
    face_image = {}
    rpta = []
    file_images = []

    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = Image_From_Frontend[top:bottom, left:right]
       
        vector_carac = face_recognition.face_encodings(face_image)[0]
        if Algoritmo == "KNN-Sequential":
            #rpta.append(KNN_Sequential(vector_carac,int(K)))
            rpta.append(take_time(lambda : knn_s.call_container((0, int(P)), lambda x : x.classify(vector_carac, int(K), 0.55))))
        elif Algoritmo == "KNN-Rtree":
            #rpta.append(KNN_RTree(vector_carac,int(K)))
            rpta.append(take_time(lambda : knn_r.call_container((0, int(P)), lambda x : x.classify(vector_carac, int(K)))))
        else:
            #rpta.append(Range_Search_RTree(vector_carac,float(R)))
            rpta.append(take_time(lambda : hcube_r.call_container((0, int(P)), lambda x : x.classify(vector_carac, float(R)/4.2))))
        file_images.append(Image.fromarray(face_image))
  
    list_images = []    
    for i in range (len(file_images)):
        file_images[i].save(str(i)+'.png')
        with open(str(i)+'.png',"rb") as tmp_file:
            encoded_image = base64.b64encode(tmp_file.read())
        list_images.append( ( rpta[i], encoded_image.decode('utf-8')) )
        os.remove(str(i)+'.png')    

    print(rpta)

    return jsonify(list_images)
    
if __name__ == '__main__':
    app.run(debug=True,port=5000)
