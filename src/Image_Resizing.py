import sys
sys.path.append("C:/DL_3D_AND_YOLO/darkflow")
import os
os.chdir("C:/DL_3D_AND_YOLO/darkflow")
from darkflow.net.build import TFNet
import glob
import cv2

# 학습된 데이터인 cfg/yolov2-tiny.cfg, bin/yolov2-tiny.weights 를 이용하여 모델생성
options = {
    'model' : 'cfg/yolov2-tiny.cfg',
    'load' : 'bin/yolov2-tiny.weights',
    'threshold' : 0.3,
    'gpu': 1.0
}

# 학습이 끝난 모델
tfnet = TFNet(options)

# 욜로로 리턴된 객체들의 사이즈 측정하는 함수
def result_area(result):
    width = result['topleft']['x'] - result['bottomright']['x']
    height = result['topleft']['y'] - result['bottomright']['y']
    return width * height

# 욜로로 리턴된 객체들중 하나를 선택하여 자르고 리턴하는 함수
def resizing(filename):
    img = cv2.imread(filename, cv2.IMREAD_COLOR)
    # 학습된 모델에서 객체의 정보들을 리턴하는 함수
    results = tfnet.return_predict(img)
    check = {'topleft': {'x': 0, 'y': 0},'bottomright': {'x': 0, 'y': 0}}
    for result in results:
        if (result['label'] == 'person') and result_area(result) > result_area(check):
            check = result
    # 리턴된 정보를 이용하여 객체를 구분하는 사각형을 만들어줌
    if result_area(check)==0:
        return 0
    tl = (check['topleft']['x'],check['topleft']['y'])
    br = (check['bottomright']['x'],check['bottomright']['y'])
    img2 = img[tl[1]:br[1],tl[0]:br[0]]
    # 반환된 꼭지점 좌표를 이용하여 이미지에 맞는 사각형을 만들어줌
    shrink = cv2.resize(img2, (60,160), interpolation=cv2.INTER_LINEAR)
    name = filename.split('.')
    new_name = name[0]+'_resize.'+name[1]
    new_name = new_name[:26] +'_resize_dummy' +new_name[26:]
    cv2.imwrite(new_name,shrink)



# 해당 폴더의 하부 파일을 모두 읽어들여 위의 함수를 실행시켜주는 코드

class IMYOUR:
    __dir_url = r"F:/socool/socool/data/upper_resize_dummy/people_upper_test"

    def run(self):

        def getFileList(url = self.__dir_url):
            res = list()
            EnableFormatList = ["jpg", "png"]

            files = glob.glob(url + "/*")

            for name in files:
                ns = name.split(".")
                if len(ns) < 2:
                    res.extend(getFileList(name))
                elif ns[1] in EnableFormatList:
                    res.append(str.replace(name, '\\', "/"))
            return res

        fileList = getFileList()

        for filename in fileList:
            try:
                resizing(filename)

            except:
                pass
        return


a = IMYOUR()
a.run()