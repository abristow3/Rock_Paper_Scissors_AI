# import tensorflow as tf
# from keras.preprocessing.image import ImageDataGenerator
# from keras.preprocessing import image
# import matplotlib.image as mpimg
# # import pandas as pd
# import numpy as np
# import os
# import matplotlib.pyplot as plt
# from keras_squeezenet import SqueezeNet
#
# import cv2
# import time
#
#
# class OCR:
#     def __init__(self):
#         self.training_data = "assets/training"
#         self.color_mode = "rgb"
#
#         self.generator = ImageDataGenerator(
#             rescale=1 / 255.0,
#             zoom_range=0.25,
#             rotation_range=10,
#             horizontal_flip=True,
#             vertical_flip=True,
#             fill_mode='nearest',
#             validation_split=0.2
#         )
#
#         self.training_generator = self.generator.flow_from_directory(
#             self.training_data,
#             target_size=(180, 180),
#             batch_size=32,
#             class_mode='categorical',
#             color_mode=self.color_mode,
#             subset='training'
#         )
#
#         self.validation_generator = self.generator.flow_from_directory(
#             self.training_data,
#             target_size=(180, 180),
#             batch_size=32,
#             class_mode='categorical',
#             color_mode=self.color_mode,
#             subset='validation'
#         )
#
#         self.model = tf.keras.models.Sequential([
#             tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(180, 180, 3)),
#             tf.keras.layers.MaxPooling2D(2, 2),
#             tf.keras.layers.Dropout(0.2),
#             tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
#             tf.keras.layers.MaxPooling2D(2, 2),
#             tf.keras.layers.Dropout(0.2),
#             tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
#             tf.keras.layers.MaxPooling2D(2, 2),
#             tf.keras.layers.Dropout(0.2),
#             tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
#             tf.keras.layers.MaxPooling2D(2, 2),
#             tf.keras.layers.Flatten(),
#             tf.keras.layers.Dense(512, activation='relu'),
#             tf.keras.layers.Dropout(0.5),
#             tf.keras.layers.Dense(3, activation=tf.nn.softmax)
#         ])
#
#         self.model.summary()
#         self.model.compile(loss='categorical_crossentropy',
#                            optimizer=tf.keras.optimizers.legacy.Adam(),
#                            metrics=['accuracy'])
#
#         self.model.fit(
#             self.training_generator,
#             steps_per_epoch=25,
#             epochs=16,
#             validation_data=self.validation_generator,
#             validation_steps=5,
#             verbose=2)
#
#         uploaded = 'rock_choice.png'
#         img = image.load_img(uploaded, target_size=(180, 180), color_mode=self.color_mode)
#
#         x = image.img_to_array(img)
#         x = np.expand_dims(x, axis=0)
#         images = np.vstack([x])
#
#         classes = self.model.predict(images, batch_size=10)
#
#         print(classes)
#         if classes[0, 0] == 1:
#             print('Paper')
#         elif classes[0, 1] == 1:
#             print('Rock')
#         else:
#             print('Scissors')
#
#
# class Camera:
#     def __init__(self):
#         self.img = None
#         self.cap = cv2.VideoCapture(0)
#
#         # Set height and width
#         self.cap.set(3, 180)
#         self.cap.set(4, 180)
#
#     def capture_video(self):
#         while True:
#             ret, self.img = self.cap.read()
#             cv2.imshow('Webcam', self.img)
#             self.img = cv2.resize(self.img, (150, 150))
#
#             if cv2.waitKey(1) == ord('q'):
#                 cv2.imshow("player_choice", self.img)
#                 cv2.imwrite("rock_choice.png", self.img)
#                 break
#
#         self.cap.release()
#         cv2.destroyAllWindows()
#
#
# if __name__ == '__main__':
#     # camera = Camera()
#     # camera.capture_video()
#     ocr = OCR()
