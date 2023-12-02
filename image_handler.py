import cv2


class ImageHandler:
    def __init__(self):
        self.img = None

    def display_image(self, file_path):
        self.img = cv2.imread(file_path)
        cv2.namedWindow('custom window', cv2.WINDOW_KEEPRATIO)
        cv2.imshow('custom window', self.img)
        cv2.resizeWindow('custom window', 700, 700)
        cv2.moveWindow('custom window', 500, 0)
