from keras.models import load_model

from keras.preprocessing.image import ImageDataGenerator


model = load_model('C:/Users/Koo/Desktop/upper_resize_dummy/upper_color_weights_resize.hdf5')
img_rows , img_cols = 224,224
num_classes = 8
batch_size = 32
nb_epoch = 5

test_datagen = ImageDataGenerator(rescale=1./255)

test_set = test_datagen.flow_from_directory(
            'C:/Users/Koo/Desktop/upper_resize_dummy/people_upper_test',
            batch_size = batch_size,
            target_size=(img_rows, img_cols),
            class_mode='categorical')



def maxidx(x):
    maxidx = 0
    for i in range(len(x)):
        maxidx = i if x[maxidx] < x[i] else maxidx
    return maxidx


def acc(test_set):
    cnt_acc = 0
    cnt_amt = 0
    for num1 in range(len(test_set)):
        predict_box = model.predict(test_set[num1][0])
        ans_box = test_set[num1][1]

        for num2 in range(len(predict_box)):
            cnt_amt += 1
            if int(maxidx(predict_box[num2])) == int(maxidx(ans_box[num2])):
                cnt_acc += 1
    #                 print("True")
    #             else:
    #                 print("False")
    return cnt_acc / cnt_amt


print(acc(test_set))