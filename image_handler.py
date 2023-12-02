import cv2


class ImageHandler:
    def __init__(self):
        self.img = None

    def load_image(self, file_path):
        self.img = cv2.imread(file_path, cv2.IMREAD_COLOR)

    def display_image(self):
        cv2.imshow("image", self.img)
