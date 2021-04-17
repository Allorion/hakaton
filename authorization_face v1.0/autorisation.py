from authorization_face import face_recognition as fr
import cv2
import numpy as np


class FaceToFaceAuthorization(object):
    def __init__(self):
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.face_names = []
        self.flag = True
        self.check = 0
        self.name = "Unknown"

    def authorization_start(self):
        video_capture = cv2.VideoCapture(0)  # Захват видео с камеры
        # Фотография легитимного пользователя
        allori_image = fr.load_image_file("authorization_face/user/1.jpg")
        allori_face_encoding = fr.face_encodings(allori_image)[0]
        # Создаем список легитимных пользователей
        known_face_encodings = [
            allori_face_encoding,
        ]
        # Создаем список имен легитимных пользователей
        known_face_names = [
            "user",
        ]
        process_this_frame = True

        while self.flag == True:
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if process_this_frame:
                self.face_locations = fr.face_locations(rgb_small_frame)
                self.face_encodings = fr.face_encodings(rgb_small_frame, self.face_locations)
                self.check += 1
                # Отсутствуют пользователи
                if self.check == 600:
                    count = 2
                    self.flag = False
                    return count

                for face_encoding in self.face_encodings:
                    matches = fr.compare_faces(known_face_encodings, face_encoding)
                    face_distances = fr.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    # Пользователь подтвержден
                    if matches[best_match_index]:
                        self.name = known_face_names[best_match_index]
                        count = 1
                        return count
                    # Неизвестный пользователь
                    else:
                        count = 0
                        return count

        video_capture.release()
        cv2.destroyAllWindows()
