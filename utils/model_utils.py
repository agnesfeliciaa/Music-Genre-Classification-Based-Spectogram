# utils/model_utils.py

from tensorflow.keras.models import load_model as keras_load_model
import numpy as np
import os
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.vgg16 import preprocess_input
from sklearn.metrics import classification_report, accuracy_score
from tensorflow.keras.preprocessing import image

# Fungsi untuk memuat model
def load_model_from_file(model_path):
    model = keras_load_model(model_path)
    return model

# Fungsi untuk memprediksi genre dengan probabilitas
def predict_genre_with_probability(image_path, model):
    # Memuat gambar
    img = image.load_img(image_path, target_size=(180, 180))  # Sesuaikan dengan ukuran input model
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)  # Menambahkan dimensi batch
    img_array = preprocess_input(img_array)  # Melakukan preprocessing sesuai dengan model

    # Melakukan prediksi
    predictions = model.predict(img_array)
    
    # Mengambil label dan probabilitas tertinggi
    predicted_class = np.argmax(predictions, axis=1)
    predicted_probability = np.max(predictions)  # Probabilitas tertinggi

    # Daftar genre berdasarkan urutan label dalam model
    genres = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal', 'pop', 'reggae', 'rock']
    
    predicted_genre = genres[predicted_class[0]]
    
    return predicted_genre, predicted_probability

def evaluate_model_on_folder(model, folder_path, class_labels):
    y_true = []
    y_pred = []

    for label in class_labels:
        class_folder = os.path.join(folder_path, label)
        if not os.path.isdir(class_folder):
            continue

        for file in os.listdir(class_folder):
            if file.endswith(".png"):
                img_path = os.path.join(class_folder, file)
                img = image.load_img(img_path, target_size=(180, 180))  # Ubah sesuai input model
                img_array = image.img_to_array(img)
                img_array = np.expand_dims(img_array, axis=0) / 255.0

                prediction = model.predict(img_array)
                predicted_index = np.argmax(prediction[0])

                y_true.append(label)
                y_pred.append(class_labels[predicted_index])

    report = classification_report(y_true, y_pred, output_dict=True, zero_division=0)
    accuracy = accuracy_score(y_true, y_pred)
    return report, accuracy


# from PIL import Image
# import tensorflow as tf
# import numpy as np

# def load_model(model_path):
#     return tf.keras.models.load_model(model_path)

# def predict_genre(image_path, model):
#     # Baca gambar PNG
#     image = Image.open(image_path).convert("RGB")
    
#     # Resize ke ukuran input model (misalnya sesuaikan dengan model kamu)
#     image = image.resize((180, 180))

    
#     # Ubah ke array dan normalisasi (0-1)
#     image_array = np.array(image) / 255.0

#     # Tambahkan dimensi batch
#     input_array = np.expand_dims(image_array, axis=0)

#     # Prediksi
#     prediction = model.predict(input_array)
#     genre_index = np.argmax(prediction)

#     # Label genre (urutan harus sama seperti saat model dilatih)
#     genre_labels = ['blues', 'classical', 'country', 'disco', 'hiphop',
#                     'jazz', 'metal', 'pop', 'reggae', 'rock']

#     return genre_labels[genre_index]