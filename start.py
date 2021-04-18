from face_identification.autorisation import FaceToFaceAuthorization
from color_identification.script import start
from multiprocessing.pool import ThreadPool
import time
#status = obj.authorization_start()
#async_result = pool.apply_async(colorzRGB, ('img.png',))
 #       rgba = async_result.get()

obj = FaceToFaceAuthorization()
color = start()
while True:
    if color == False:
        time.sleep(5)
        status = obj.authorization_start()
        if status == 0 or status ==2:
            print('Я выключился')
            break
        elif status == 1:
            print('Живем')
            time.sleep(10)
            color = start()

