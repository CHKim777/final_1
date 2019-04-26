import cv2
from keras.preprocessing.image import ImageDataGenerator

# 각도는 15도 좌우로는 5%까지 움직이는 데이터를 랜덤으로 만들어 주는 명령어

train_datagen = ImageDataGenerator(rescale = 1./255,rotation_range=15,
                                   width_shift_range=0.05, height_shift_range=0.05,horizontal_flip = True)


batch_size = 100
path = 'F:/socool/socool/data/upper_resize_dummy/people_upper_train'


test_set = train_datagen.flow_from_directory(
            path,
            target_size=(60, 160),
            batch_size = batch_size,
            class_mode='categorical')

cnt = 0
for img in test_set[0][0][:]:
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cnt +=1
    cv2.imwrite(path + '/0white/{}_dummy.jpg'.format(cnt),img*255)
