from authorization_face.autorisation import FaceToFaceAuthorization
import time

obj = FaceToFaceAuthorization()
while True:
    status = obj.authorization_start()
    if status == 1:
        print('Проверка выполнена успешно')
        time.sleep(10)
    elif status == 0:
        print('Не удалось распознать лицо, повторная проверка через 3 сек.')
        time.sleep(3)
    elif status == 2:
        print('Заблокирован')
