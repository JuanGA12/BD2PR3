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