import glob
import mongoDBController as mc

import Yolo_Color_Height as ych

mct = mc.MDBCtrl()
mct.setUserInfo()
mct.setDBCollections()

class IMYOUR:
    __dir_url = r"F:/socool/socool/webserver/src/static/videos"
    def run(self):
        def getFileList(url = self.__dir_url):
            res = list()
            EnableFormatList = ["mp4", "avi"]

            files = glob.glob(url + "/*")

            for name in files:
                ns = name.split(".")
                if len(ns) < 2:
                    res.extend(getFileList(name))
                elif ns[1] in EnableFormatList:
                    res.append(str.replace(name, '\\', "/"))
            return res
        fileList = getFileList()
        cnt = 0
        for filename in fileList:
            cnt+=1
            print(cnt)
            print(filename)
            try:
                info_list = ych.yolo_color(filename)
                print(len(info_list))
                for info in info_list:
                    mct.insertOneDocu(info)
            except:
                pass
        return


a = IMYOUR()
a.run()
