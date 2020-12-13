from flask import Flask, jsonify, request, send_file,request
from rtree import index
from flask_cors import CORS
import face_recognition
from PIL import Image
import os
from heapq import heappop, heappush, heapify 
import math

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={
    r"/*": {
        "origins": "*"
        }
    }
)

def read_train_set():
    lines = [line.split(",") for line in open(os.listdir()[-1], "r").read().split('/n')]
    return [(line[0], [float(i) for i in line[1:]]) for line in lines[:-1]]

train_set = read_train_set()   


def create_RTree():
    idx = index.Index(properties = index.Property(dimension = 128))
    for i in range(len(train_set) - 1):
        idx.insert(i, train_set[i][1]*2)
    return idx

idx = create_RTree()

''' Correrlo una vez
def get_face_embedding(img_path):
        image = face_recognition.load_image_file(img_path)
        image_encoding = face_recognition.face_encodings(image)
        found = len(image_encoding) > 0
        return image_encoding, found

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
###Variables globales###
Algoritmo = str('')
K = int(-1)
R = int(-1)

def Range_Search_RTree(vec, r):
    lis = vec.tolist()
    c = r/4.2#Numero de la suerte
    nearest = idx.intersection([x-c for x in lis] + [x+c for x in lis])
    fr_dict = {}
    for n in nearest:
        label = train_set[n][0]
        if label in fr_dict:
            fr_dict[label] += 1
        else:
            fr_dict[label] = 1
    return sorted(fr_dict.items(), key = lambda x : x[1])[-1]

def KNN_RTree(vec, k):
    nearest = idx.nearest(vec.tolist()*2, k)
    fr_dict = {}
    for n in nearest:
        label = train_set[n][0]
        if label in fr_dict:
            fr_dict[label] += 1
        else:
            fr_dict[label] = 1
    return sorted(fr_dict.items(), key = lambda x : x[1])[-1]

def KNN_Sequential(vec, k):
    max_heap = []
    for i in range(k):
        max_heap.append((-0.55, "none"))
    for train_label, train_vec in train_set:
        distance = -((sum([(x1 - x2)**2 for x1, x2 in zip(vec, train_vec)]))**(1/2))
        if max_heap[0][0] < distance:
            heappop(max_heap)
            heappush(max_heap,(distance, train_label))
    nearest = [(distance, label) for distance, label in max_heap if label != "none"]
    fr_dict = {}
    for distance, label in nearest:
        if label in fr_dict:
            fr_dict[label][0] += 1
            if fr_dict[label][1] < distance:
                fr_dict[label][1] = distance
        else:
            fr_dict[label] = [1, distance]
    fr_list = sorted(fr_dict.items(), key = lambda x : x[1])
    return fr_list[-1][0], fr_list[-1][1][0] 

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
    
    Image_From_Frontend = face_recognition.load_image_file(IMAGE)
    face_locations = face_recognition.face_locations(Image_From_Frontend)
    face_image = {}
    rpta = []
    # images = []
    for face_location in face_locations:
        top, right, bottom, left = face_location
        face_image = Image_From_Frontend[top:bottom, left:right]
        #pil_image = Image.fromarray(face_image)
        #images.append(pil_image)
        #pil_image.show()
        vector_carac = face_recognition.face_encodings(face_image)[0]
        if Algoritmo == "KNN-Sequential":
            rpta.append(KNN_Sequential(vector_carac,int(K)))
        elif Algoritmo == "KNN-Rtree":
            rpta.append(KNN_RTree(vector_carac,int(K)))
        else:
            rpta.append(Range_Search_RTree(vector_carac,float(R)))

            '''                  
            pil_image = Image.fromarray(face_image)
            pil_image.show()
            results = face_recognition.compare_faces([messi_encoding], vector_carac)
            Rpta = bool(results[0])
            '''
            
    print(rpta)
    return jsonify(a=Algoritmo,b=K,c=R)
     
    #debe retornar imagen 
    
if __name__ == '__main__':
    app.run(debug=True,port=5000)
