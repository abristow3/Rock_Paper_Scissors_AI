import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing import image
import matplotlib.image as mpimg
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import shutil

import cv2
import time
from heic2png import HEIC2PNG


class ObjectDetection:
    def __init__(self, load_model: bool = False):
        self.color_mode = "rgb"
        self.prediction = None
        self.training_data = "assets/training"

        if load_model:
            self.model = tf.keras.models.load_model('green_model.h5')
        else:
            # self.training_data = "assets/new_dataset/Rock-Paper-Scissors/train"

            self.generator = ImageDataGenerator(
                rescale=1 / 255.0,
                zoom_range=0.25,
                rotation_range=10,
                horizontal_flip=True,
                vertical_flip=True,
                fill_mode='nearest',
                validation_split=0.2
            )

            self.training_generator = self.generator.flow_from_directory(
                self.training_data,
                target_size=(180, 180),
                batch_size=32,
                class_mode='categorical',
                color_mode=self.color_mode,
                subset='training'
            )

            self.validation_generator = self.generator.flow_from_directory(
                self.training_data,
                target_size=(180, 180),
                batch_size=32,
                class_mode='categorical',
                color_mode=self.color_mode,
                subset='validation'
            )

            self.model = tf.keras.models.Sequential([
                tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(180, 180, 3)),
                tf.keras.layers.MaxPooling2D(2, 2),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D(2, 2),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D(2, 2),
                tf.keras.layers.Dropout(0.2),
                tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
                tf.keras.layers.MaxPooling2D(2, 2),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(512, activation='relu'),
                tf.keras.layers.Dropout(0.5),
                tf.keras.layers.Dense(3, activation=tf.nn.softmax)
            ])

            self.model.summary()
            self.model.compile(loss='categorical_crossentropy',
                               optimizer=tf.keras.optimizers.legacy.Adam(),
                               metrics=['accuracy'])

            self.model.fit(
                self.training_generator,
                epochs=20,
                validation_data=self.validation_generator,
                validation_steps=5,
                verbose=2)

            self.model.save('green_model.h5')

    def model_predict(self, uploaded):
        img = image.load_img(uploaded, target_size=(180, 180), color_mode=self.color_mode)

        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        images = np.vstack([x])

        classes = self.model.predict(images, batch_size=10)

        if classes[0, 0] == 1:
            self.prediction = "paper"
        elif classes[0, 1] == 1:
            self.prediction = "rock"
        else:
            self.prediction = "scissors"

    def label_and_save(self, file_path, label):
        if "paper" in label or "rock" in label or "scissors" in label:
            cur = time.time()
            shutil.move(file_path, f"{self.training_data}/{label}/image_{cur}.png")


class Camera:
    def __init__(self):
        self.img = None
        self.cap = cv2.VideoCapture(0)

        # Set height and width
        self.cap.set(3, 180)
        self.cap.set(4, 180)

    def capture_image(self):
        start_time = time.time()
        while True:
            current_time = time.time()

            ret, self.img = self.cap.read()
            cv2.imshow('Webcam', self.img)
            self.img = cv2.resize(self.img, (180, 180))
            cv2.waitKey(1)

            print(current_time - start_time)
            if current_time - start_time >= 5:
                cv2.imwrite("player_images/player_choice.png", self.img)
                break

        self.cap.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    camera = Camera()
    camera.capture_image()

    # od = ObjectDetection(load_model=True)
    # od.model_predict(uploaded="scissors.png")
    # print(od.prediction)

    # od = ObjectDetection(load_model=True)
    # od.model_predict(uploaded='rock.png')

    # dir_list = os.listdir("hand_images")
    #
    # for file in dir_list:
    #     heic_img = HEIC2PNG(f"hand_images/{file}")
    #
    #     file_name = file.replace(".HEIC", "")
    #
    #     heic_img.save(output_image_file_path=f"converted_images/{file_name}.png")

    # dir_list = os.listdir("converted_images")
    #
    # for file in dir_list:
    #     img = cv2.imread(f"scissors.png")
    #     img = cv2.resize(img, (180, 180))
    #     cv2.imwrite(f"scissors.png", img)
