
import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt             #vissualisierung

fashion_mnist = keras.datasets.fashion_mnist
(trainingImages,trainingLables),(testImages,testLables) = fashion_mnist.load_data()

classNames = ['TShirt','Hose','Pullover','Kleid','Mantel','Sandale','Hemt','Sneeker','Rucksack','Englisch']

#plt.figure()
#plt.imshow(trainingImages[300])
#plt.colorbar()
#plt.grid(False)
#plt.show()

trainingImages = trainingImages / 255.0
testImages = testImages / 255.0

model = keras.Sequential([
    keras.layers.Flatten(),
    keras.layers.Dense(128,activation='relu'),
    keras.layers.Dense(10,activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy'])

test_acc_last = 0
test_loss, test_acc = model.evaluate(testImages,testLables,verbose=0)

while test_acc > test_acc_last or test_acc < 0.88:
    test_acc_last = test_acc
    print(test_acc)
    model.fit(trainingImages,trainingLables,epochs=1)
    test_loss, test_acc = model.evaluate(testImages,testLables,verbose=0)

print(test_loss, test_acc)