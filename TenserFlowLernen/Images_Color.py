import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.python.ops.gen_math_ops import mod             #vissualisierung

(trainingImages,trainingLables),(testImages,testLables) = keras.datasets.cifar10.load_data()

trainingImages = trainingImages / 255.0
testImages = testImages / 255.0

className = ['Airplane','Automobil','Bird','Cat','Deer','Dog','Frog','Horse','Ship','Truck']

ImgIndex = 1

#print(trainingImages[ImgIndex].shape)
#plt.imshow(trainingImages[ImgIndex], cmap=plt.cm.binary)
#plt.xlabel(className[trainingLables[ImgIndex][0]])
#plt.show()

datagen = keras.preprocessing.image.ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

#data augmentation start

testImg = trainingImages[ImgIndex]
img = keras.preprocessing.image.img_to_array(testImg)
img = img.reshape((1,)+img.shape)
i = 0
for batch in datagen.flow(img,save_prefix='test', save_format='jpeg', save_to_dir='F:\Python\InteligenteSysteme\TenserFlowLernen\Test'):
    plt.figure(i)
    plot = plt.imshow(keras.preprocessing.image.img_to_array(batch[0]))
    i += 1
    if i > 4:
        break
plt.show()

#data augmentation ende

model = keras.models.Sequential()
model.add(layer=keras.layers.Conv2D(32, (3, 3), activation='relu'))
model.add(layer=keras.layers.MaxPooling2D((2, 2)))
model.add(layer=keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layer=keras.layers.MaxPooling2D((2, 2)))
model.add(layer=keras.layers.Conv2D(64, (3, 3), activation='relu'))

model.add(layer=keras.layers.Flatten())
model.add(layer=keras.layers.Dense(64,activation='relu'))
model.add(layer=keras.layers.Dense(10))

model.compile(
    optimizer='adam',
    loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
    metrics=['accuracy'])

test_acc_last = 0
test_loss, test_acc = model.evaluate(testImages,testLables,verbose=0)

while test_acc > test_acc_last or test_acc < 0.7:
    test_acc_last = test_acc
    history = model.fit(trainingImages,trainingLables, epochs=1, validation_data=(testImages,testLables))
    test_loss, test_acc = model.evaluate(testImages,testLables,verbose=0)

print(test_loss,test_acc)