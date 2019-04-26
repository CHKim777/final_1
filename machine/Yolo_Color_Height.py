import sys
sys.path.append("C:/DL_3D_AND_YOLO/darkflow")
import os
os.chdir("C:/DL_3D_AND_YOLO/darkflow")
from keras.models import load_model
import math
import cv2
from darkflow.net.build import TFNet
import datetime

# 키 분석해주는 코드
class height_analysis_class:
    __cam_ang, __view_ang, __cam_hei = math.radians(60), math.radians(30), 2

    def __init__(self, ca, va, ch):
        __cam_ang, __view_ang, __cam_hei = ca, va, ch

    def set_ang_hei(self, ca, va, ch):
        __cam_ang, __view_ang, __cam_hei = math.radians(ca), math.radians(va), ch

    def ang_hei_input(self):
        __cam_ang = math.radians(float(input("카메라 각도 :")))
        __view_ang = math.radians(float(input("카메라 화각 :")))
        __cam_hei = int(float("카메라 높이(m) :"))

    def hei_ans(self, char_st, char_end, pic_len):
        tem_tan1 = math.tan(self.__view_ang) * (2 * char_st / pic_len - 1)
        tem_tan2 = math.tan(self.__view_ang) * (2 * char_end / pic_len - 1)

        cam_tan = math.tan(self.__cam_ang)

        tem_len1 = (cam_tan + tem_tan1) / (1 - cam_tan * tem_tan1)
        tem_len2 = (cam_tan + tem_tan2) / (1 - cam_tan * tem_tan2)

        char_hei = self.__cam_hei * (tem_len2 - tem_len1) / tem_len2

        return char_hei

def cam_check(c_id):
    if c_id == 'a0001':
        return [60,15,5]
    elif c_id == 'a0002':
        return [60,15,7]
    elif c_id == 'a0003':
        return [70,15,2.7]
    else:
        return 0


# 학습된 데이터인 cfg/yolov2-tiny.cfg, bin/yolov2-tiny.weights 를 이용하여 YOLO모델생성

options = {
    'model' : 'cfg/yolov2-tiny.cfg',
    'load' : 'bin/yolov2-tiny.weights',
    'threshold' : 0.3,
    'gpu': 1.0
}

# 학습이 끝난 YOLO 모델
tfnet = TFNet(options)

# 색상구분 모델 객체 생성
car_color_model = load_model('F:/socool/socool/data/car_color_resize_dummy/car_weight_color_resize_dummy.hdf5')
person_color_model = load_model('F:/socool/socool/data/upper_resize_dummy_ver2/upper_color_weights_resize_ver2.hdf5')
def color_check(car_color):
    m = 0
    pos = 0
    for i in range(8):
        if car_color[i] > m:
            m = car_color[i]
            pos = i
    if pos == 0:
        return 'black'
    elif pos == 1:
        return 'blue'
    elif pos == 2:
        return 'gray'
    elif pos == 3:
        return 'green'
    elif pos == 4:
        return 'orange'
    elif pos == 5:
        return 'red'
    elif pos == 6:
        return 'white'
    elif pos == 7:
        return 'yellow'

def color_NAME2BGR(color):
    if color =='black':
        return (0,0,0)
    elif color =='blue':
        return (255,0,0)
    elif color =='gray':
        return (120,120,120)
    elif color =='green':
        return (0,255,0)
    elif color =='orange':
        return (15,133,220)
    elif color =='red':
        return (0,0,255)
    elif color =='white':
        return (255,255,255)
    elif color =='yellow':
        return (0,255,255)
    elif color =='beige':
        return (213,239,255)
    elif color =='cyan':
        return (255,255,0)
    elif color =='purple':
        return (128,0,128)
    elif color =='wine':
        return (0,0,139)
    elif color =='pink':
        return (180,105,255)
    elif color =='brown':
        return (19,69,139)


def yolo_color(path):
    file_name = path.split('/')[-1]
    file_name = file_name.split('.')[0]
    c_id, date = file_name.split('_')
    date = str(datetime.datetime.strptime(date, "%Y%m%d").date())

    # 영상파일에 해당하는 경로를 넣은 객체를 생성
    cap = cv2.VideoCapture(path)
    # 영상의 프레임을 가지고 오는 명령어
    frameSec = round(cap.get(cv2.CAP_PROP_FPS))

    cam_info = cam_check(c_id)
    if cam_info == 0:
        cam_heian = height_analysis_class
    else:
        cam_heian = height_analysis_class(cam_info[0], cam_info[1], cam_info[2])

    return_box = []
    people_temp_info_box = []
    car_temp_info_box = []
    while True:
        # 영상데이터를 담은 객체로 부터 정보를 읽어서 이미지 데이터를 넣은 객체로 저장
        retval, frame = cap.read()
        if not retval:
            break

        people_temp = people_temp_info_box
        car_temp = car_temp_info_box

        for info in people_temp:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) - max(info['frame']) > 2 * frameSec:
                people_temp_info = people_temp_info_box.pop(people_temp_info_box.index(info))
                return_box.append(people_temp_info)

        for info in car_temp:
            if cap.get(cv2.CAP_PROP_POS_FRAMES) - max(info['frame']) > 2 * frameSec:
                car_temp_info = car_temp_info_box.pop(car_temp_info_box.index(info))
                return_box.append(car_temp_info)
                # 연산량을 줄이기 위해서 약 0.5초에 한번만 판별을 진행
        if cap.get(cv2.CAP_PROP_POS_FRAMES) % 10 == 0:
            try:
                results = tfnet.return_predict(frame)
                for result in results:
                    tl = (result['topleft']['x'], result['topleft']['y'])
                    br = (result['bottomright']['x'], result['bottomright']['y'])
                    label = result['label']
                    if label == 'person':
                        person_yolo = frame[tl[1]:br[1], tl[0]:br[0]]
                        person_yolo = cv2.cvtColor(person_yolo, cv2.COLOR_BGR2RGB)
                        person_resize = cv2.resize(person_yolo, (224, 224), interpolation=cv2.INTER_LINEAR)
                        person_resize = person_resize / 255
                        person_color = person_color_model.predict([[person_resize]])
                        person_color = color_check(person_color[0])


                        # 사람의 키 분석
                        pic_len = frame.shape[1]
                        char_end = frame.shape[1] - tl[1]
                        char_st = frame.shape[1] - br[1]

                        cam_heian = height_analysis_class(60,30,2)
                        char_hei = cam_heian.hei_ans(char_st, char_end, pic_len)

                        # 객체 정보의 이름& 키 이미지에 표시
                        result['color'] = [person_color]
                        result['height'] = [round(char_hei, 2)]
                        result['frame'] = [cap.get(cv2.CAP_PROP_POS_FRAMES)]

                        botton = True

                        for info in people_temp_info_box:
                            x1 = max(info['topleft']['x'], result['topleft']['x'])
                            y1 = min(info['topleft']['y'], result['topleft']['y'])
                            x2 = min(info['bottomright']['x'], result['bottomright']['x'])
                            y2 = max(info['bottomright']['y'], result['bottomright']['y'])
                            if info['color'] == result['color']:
                                if (x2 - x1 > 0) and (y2 - y1 > 0):
                                    old_area = (info['bottomright']['x'] - info['topleft']['x']) * (
                                                info['bottomright']['y'] - info['topleft']['y'])
                                    new_area = (x2 - x1) * (y2 - y1)
                                    if ((new_area / old_area) > 0.7) or ((old_area/new_area) > 0.7):
                                        info['topleft'] = result['topleft']
                                        info['bottomright'] = result['bottomright']
                                        info['height'] += result['height']
                                        info['frame'] += result['frame']
                                        botton = False
                                        break
                        if botton:
                            people_temp_info_box.append(result)

                    if label in ['car','truck']:

                        car_yolo = frame[tl[1]:br[1], tl[0]:br[0]]
                        car_yolo = cv2.cvtColor(car_yolo, cv2.COLOR_BGR2RGB)
                        car_resize = cv2.resize(car_yolo, (224, 224), interpolation=cv2.INTER_LINEAR)

                        car_resize = car_resize / 255
                        car_color = car_color_model.predict([[car_resize]])

                        car_color = color_check(car_color[0])

                        car_color_bgr = color_NAME2BGR(car_color)

                        # 객체 정보의 이름& 키 이미지에 표시

                        result['label'] = 'car'
                        result['color'] = [car_color]
                        result['frame'] = [cap.get(cv2.CAP_PROP_POS_FRAMES)]

                        botton = True

                        for info in car_temp_info_box:
                            x1 = max(info['topleft']['x'], result['topleft']['x'])
                            y1 = min(info['topleft']['y'], result['topleft']['y'])
                            x2 = min(info['bottomright']['x'], result['bottomright']['x'])
                            y2 = max(info['bottomright']['y'], result['bottomright']['y'])
                            if info['color'] == result['color']:
                                if (x2 - x1 > 0) and (y2 - y1 > 0):
                                    old_area = (info['bottomright']['x'] - info['topleft']['x']) * (
                                                info['bottomright']['y'] - info['topleft']['y'])
                                    new_area = (x2 - x1) * (y2 - y1)
                                    if ((new_area / old_area) > 0.7) or ((old_area/new_area) > 0.7):
                                        info['topleft'] = result['topleft']
                                        info['bottomright'] = result['bottomright']
                                        info['frame'] += result['frame']
                                        botton = False
                                        break
                        if botton:
                            car_temp_info_box.append(result)

            except:
                pass
        # 객체가 사람인 경우에만 객체를 분석해옴


    return_box += people_temp_info_box
    return_box += car_temp_info_box

    # 저장된 객체를 지정된 형식으로 변환하여 반환함
    ans = []
    for info in return_box:
        temp_info = {}
        if len(info['frame']) >= (frameSec/2):
            start_time = str(datetime.timedelta(seconds=info['frame'][0]//frameSec))
            end_time = str(datetime.timedelta(seconds=info['frame'][-1]//frameSec))
            temp_info['time'] = [start_time, end_time]
            temp_info['c_id'] = c_id
            temp_info['date'] = date
            if info['label'] == 'person':
                temp_info['kind'] = 'human'
                num = round(len(info['height'])/4)
                box = info['height'][num:-num]
                temp_info['info'] = {'height':round(sum(box) / len(box),2),'color':info['color'][0]}

            elif info['label'] == 'car':
                temp_info['kind'] = 'car'
                temp_info['info'] = {'color':info['color'][0]}

            ans.append(temp_info)

    if cap.isOpened():
        cap.release()

    return ans