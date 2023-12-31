import tensorflow as tf

import keras
from keras.models import Sequential
from keras.layers import Dense

import keras.optimizers

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import seaborn as sns # data visualization library

import matplotlib.pyplot as plt
from pandas import DataFrame as df

np.random.seed(42)
random_state = 42

df = pd.read_csv('DEPRESSION_PROJECT.csv')
# uncomment the line below for when running in google colab and comment the line above
# df = pd.read_csv('/content/drive/MyDrive/datasets/DEPRESSION_PROJECT.csv')


df.head()  # head method shows only first 5 rows

# y includes our labels and x includes our features
y = df['CLASS']    # DEPRESSION or OTHERS

X = df.drop(['CLASS'], axis = 1)

#X.head()

sns.countplot(df, x="CLASS");

D, O = y.value_counts()
print('Number of Depression: ',D)
print('Number of Others : ',O)


X.describe()

x_=pd.get_dummies(X)

x_.to_csv('data.csv')
X=pd.read_csv('data.csv')
# uncomment the lines below for when running in google colab and comment the lines above
# x_.to_csv('/content/drive/MyDrive/datasets/data.csv')
# X=pd.read_csv('/content/drive/MyDrive/datasets/data.csv')


X.shape

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X_std = scaler.fit_transform(X)

df=pd.DataFrame(X_std)

df.hist(bins=50, figsize=(16, 10));

X.shape

#y


df.head(10)  # show the first 10 rows

df

from sklearn.preprocessing import LabelBinarizer
lb = LabelBinarizer()
y_=lb.fit_transform(y)


scaled_df = pd.concat([pd.DataFrame(X_std, columns=X.columns), y], axis=1)

scaled_df.head(10)

scaled_df.to_csv('Scaled.csv')

from sklearn.decomposition import PCA
# feature extraction
pca = PCA(n_components=10)
X_pca = pca.fit_transform(X_std)


PCA_df = pd.DataFrame()
PCA_df['PCA_1'] = X_pca[:,0]
PCA_df['PCA_2'] = X_pca[:,1]
PCA_df['PCA_3'] = X_pca[:,2]
PCA_df.head(5)

plt.figure(figsize=(8,6))
plt.plot(PCA_df['PCA_1'][scaled_df['CLASS'] == 'DEPRESSION'],PCA_df['PCA_2'][scaled_df['CLASS'] == 'DEPRESSION'],'o', alpha = 0.7, color = 'r')
plt.plot(PCA_df['PCA_1'][scaled_df['CLASS'] == 'OTHERS'],PCA_df['PCA_2'][scaled_df['CLASS'] == 'OTHERS'],'o', alpha = 0.7, color = 'b')

plt.xlabel('PCA_1')
plt.ylabel('PCA_2')
plt.legend(['DEPRESSION','OTHERS'])
plt.show()

# The amount of variance that each PC explains
var_exp = pca.explained_variance_ratio_
var_exp

# Cumulative Variance explains
cum_var_exp = np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4))
cum_var_exp

plt.figure(figsize=(8,6))
plt.bar(range(1, len(pca.components_) + 1), var_exp, alpha=0.5, align='center', label='individual explained variance')
plt.step(range(1, len(pca.components_) + 1), cum_var_exp, where='mid', label='cumulative explained variance')
plt.plot(range(1, len(pca.components_) + 1), var_exp, 'ro-')
plt.xticks(range(1, len(pca.components_) + 1))
plt.ylabel('Explained Variance Ratio')
plt.xlabel('Principal Components')
plt.title('Scree Plot')
plt.legend(loc='best');

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, f1_score,confusion_matrix

# split data train 50 % and test 50 %
#X_train, X_test, y_train, y_test = train_test_split(X_std, y_, test_size=0.1, random_state=random_state)
X_train, X_test, y_train, y_test = train_test_split(X_pca, y_, test_size=0.5, random_state=random_state)

model = Sequential()
model.add(Dense(16, activation='relu', input_dim=10))
model.add(Dense(2, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

optimizer = keras.optimizers.legacy.SGD(lr=0.001,decay=0.0001, momentum=0.99)

model.compile(loss='binary_crossentropy', optimizer=optimizer,metrics=['accuracy'])

model.summary()
model.save('Depression.h5')
results = model.fit(X_train, y_train, epochs=130, batch_size=12,validation_split=0.3)

#Training the model
scores = model.evaluate(X_train,y_train, verbose = 0)
print(print("%s,%.2f%%" % ( model.metrics_names[1], scores[1] * 100)))
#Testing of the model
scores = model.evaluate(X_test,y_test, verbose = 0)
print(print("%s,%.2f%%" % (model.metrics_names[1], scores[1] * 100)))


#correlelogram- plot heatmap to find correlation among features
corrmat =df.corr()
f, ax = plt.subplots(figsize=(30,20))
sns.heatmap(corrmat, square=True, annot=True,linewidth=0.6, cmap='RdBu')

#Summarize history for accuracy
import matplotlib.pyplot as plt
plt.plot(results.history['accuracy'])
plt.title('tr_acc')
plt.ylabel('tr_acc')
plt.xlabel('tr_acc')
plt.legend(['tr_acc'], loc='upper left')
plt.show()
plt.plot(results.history['loss'])
plt.title('tr_loss')
plt.ylabel('tr_loss')
plt.xlabel('tr_epoch')
plt.legend(['tr_loss'], loc='upper left')
plt.show()

plt.plot(results.history['val_accuracy'])
plt.title('val_accuracy')
plt.ylabel('val_accuracy')
plt.xlabel('val_accuracy')
plt.legend(['val_accuracy'], loc='upper left')
plt.show()
plt.plot(results.history['val_loss'])
plt.title('val_loss')
plt.ylabel('val_loss')
plt.xlabel('val_epoch')
plt.legend(['val_loss'], loc='upper left')
plt.show()
#model = load_model('depression.h5')

plt.plot(results.history['accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

plt.plot(results.history['loss'])
plt.plot(results.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()

plt.show()

y_pred=model.predict(X_test)
y_pred=(y_pred>0.5)
y_pred.shape
y_test.shape
#y_pred=np.argmax(y_pred,axis=-1).reshape(-1,1)



#Test Accuracy

accu = accuracy_score(y_test,np.round(y_pred))
print('Accuracy is: ', accu)

cm = confusion_matrix(y_test,y_pred)
#plt.figure(figsize=(3,3))
sns.heatmap(cm, annot=True, fmt="d")

from sklearn.metrics import f1_score
f1_score(y_pred, y_test)



