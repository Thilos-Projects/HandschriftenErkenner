from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import pandas as pd                         #data analyse + manipulation
import matplotlib.pyplot as plt             #vissualisierung
from IPython.display import clear_output    #clear output

import tensorflow as tf
from tensorflow._api.v2 import data

Mode = "Classification"

if Mode == "linear Regression":

    #x = [1,2,2.5,3,4]
    #y = [1,4,7,9,15]
    #plt.plot(x,y,'ro')
    #plt.axis([0,6,0,20])
    #plt.plot(np.unique(x),np.poly1d(np.polyfit(x,y,1))(np.unique(x)))
    #plt.show()

    dTrain = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/train.csv')
    dEval = pd.read_csv('https://storage.googleapis.com/tf-datasets/titanic/eval.csv')

    #print(dTrain.shape)

    #print(dTrain.describe())

    #print(dTrain.shape)
    #print(dEval.shape)

    y_Train = dTrain.pop('survived')
    y_Eval = dEval.pop('survived')

    #print(dTrain.shape)
    #print(y_Train.shape)
    #print(dEval.shape)
    #print(y_Eval.shape)

    CategorigalColumne = ['sex','n_siblings_spouses','parch','class','deck','embark_town','alone']
    NumericColumnes = ['age','fare']

    featureColumnes = []
    for featureName in CategorigalColumne:
        voc = dTrain[featureName].unique()                                                                  #erstellt ein vocabular mit nummer representation für nicht nummerische werte
        featureColumnes.append(tf.feature_column.categorical_column_with_vocabulary_list(featureName,voc))  #erstellt einfeature für tensor flow

    for featureName in NumericColumnes:
        featureColumnes.append(tf.feature_column.numeric_column(featureName,dtype=tf.float32))

    #print(featureColumnes[0])       #hilft zum verstehen

    def make_input_fn(data_df, lable_df, num_epochs=10, shuffle=True, batch_size=32):
        def input_function():
            ds = tf.data.Dataset.from_tensor_slices((dict(data_df),lable_df))
            if shuffle:
                ds = ds.shuffle(1000)
            ds = ds.batch(batch_size).repeat(num_epochs)
            return ds
        return input_function

    train_input_fn = make_input_fn(dTrain,y_Train)
    eval_input_fn = make_input_fn(dEval,y_Eval,num_epochs=1,shuffle=False)

    linearEst = tf.estimator.LinearClassifier(feature_columns=featureColumnes)

    linearEst.train(train_input_fn)         #training
    result = linearEst.evaluate(eval_input_fn)

    clear_output()
    print(result['accuracy'])

    result = list(linearEst.predict(eval_input_fn))
    print(dEval.loc[0])
    print(result[0]['probabilities'][1],y_Eval.loc[0])

if Mode == "Classification":
    CSVColumnNames = ['SepalLength','SepalWidth','PetalLength','PetalWidth','Species']
    Species = ['Setosa','Versicolor','Virginica']

    trainPath = tf.keras.utils.get_file("iris_training.csv","https://storage.googleapis.com/download.tensorflow.org/data/iris_training.csv")
    testPath = tf.keras.utils.get_file("iris_test.csv","https://storage.googleapis.com/download.tensorflow.org/data/iris_test.csv")

    train = pd.read_csv(trainPath,names=CSVColumnNames, header=0)
    test = pd.read_csv(testPath,names=CSVColumnNames, header=0)

    y_train = train.pop('Species')
    y_test = test.pop('Species')

    def input_fn(features, lables, shuffle=True, batch_size=256):
        dataset = tf.data.Dataset.from_tensor_slices((dict(features),lables))
        if shuffle:
            dataset = dataset.shuffle(1000).repeat()
        return dataset.batch(batch_size)

    featureColumns = []
    for key in train.keys():
        featureColumns.append(tf.feature_column.numeric_column(key=key))
    
    classifier = tf.estimator.DNNClassifier(
        feature_columns=featureColumns,
        hidden_units=[30,10],
        n_classes=3)

    classifier.train(
        input_fn=lambda: input_fn(train,y_train,shuffle=True),
        steps=20000)

    result = classifier.evaluate(
        input_fn=lambda: input_fn(test,y_test,shuffle=False,batch_size=32)
    )

    print(result)