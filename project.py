# -*- coding: utf-8 -*-
"""project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/13XkW-LdmxbC8Ddul0mvHu6Cy_ctiukBZ
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px

df = pd.read_csv("//content/drive/MyDrive/Churn_Modelling.csv")

df.head(4)

df.describe()

df.isnull().sum()

df.nunique()

df.drop("CustomerId", axis=1, inplace=True)
df.head(2)

df.drop(columns=['RowNumber','Surname'], axis=1, inplace=True)
df.head(2)

plt.figure(figsize=(7,7))
plt.title("The percentage of Customer Churn")
plt.pie([(df['Exited']==1).sum(),(df['Exited']==0).sum()], explode=(0,0.1), autopct='%1.1f%%',
        labels=('Exited','Remained'))
plt.show()

plt.figure(figsize=(7,7))
plt.hist(x=df['Age'], bins=10)
plt.show()

df.Tenure.unique()

plt.figure(figsize=(15,7))
sns.countplot(x=df['Tenure'], hue=df['Exited'])

df.nunique()

plt.figure(figsize=(7,7))
sns.countplot(x=df['Gender'], hue=df['Exited'])

plt.figure(figsize=(7,7))
sns.countplot(x=df['Geography'],hue=df['Exited'])

plt.figure(figsize=(7,7))
sns.countplot(x=df['IsActiveMember'], hue=df['Exited'])

plt.figure(figsize=(7,7))
sns.countplot(x=df['HasCrCard'], hue=df['Exited'])

plt.figure(figsize=(7,7))
sns.countplot(x=df['NumOfProducts'], hue=df['Exited'])

from numpy.random import seed
from numpy.random import randn
from matplotlib import pyplot
seed(1)
x = 20 * randn(1000) + 100
y = x + (10 * randn(1000) + 50)
pyplot.scatter(x, y)
pyplot.show()

fig, ax = plt.subplots(figsize=[6, 16])
sns.boxplot(
    data=df,
    y='Balance',
    x='IsActiveMember'
)
ax.set_title('Boxplot, Churn posibilities (+blends)')

fig, ax = plt.subplots(figsize=[6, 16])
sns.boxplot(
    data=df,
    y='Age',
    x='Tenure'
)
ax.set_title('Boxplot, Churn posibilities (+blends)')

fig, ax = plt.subplots(figsize=[6, 16])
sns.boxplot(
    data=df,
    y='CreditScore',
    x='EstimatedSalary'
)
ax.set_title('Boxplot, Churn posibilities (+blends)')



from numpy import sin
from matplotlib import pyplot
x = [x*0.1 for x in range(100)]
y = sin(x)
pyplot.plot(x, y)
pyplot.show()

plt.figure(figsize=(7,7))
sns.kdeplot(x=df['Balance'], hue=df['Exited'], legend=True, shade=True)

plt.figure(figsize=(7,7))
sns.kdeplot(x=df['CreditScore'], hue=df['Exited'], legend=True, shade=True)

plt.figure(figsize=(7,7))
sns.kdeplot(x=df['EstimatedSalary'], hue=df['Exited'], legend=True, shade=True)

Gender = pd.get_dummies(df['Gender'], drop_first=True)
Gender

def latent_space(model, train_set, it=''):
    x_latent = model.enc(train_set.data.float())
    plt.figure(figsize=(10, 7))
    plt.scatter(x_latent[0][:,0].detach().numpy(), 
                x_latent[1][:,1].detach().numpy(), 
                c=train_set.targets)
    plt.colorbar()
    plt.title("VAE Latent Space", fontsize=20)
    plt.xlabel("X", fontsize=18)
    plt.ylabel("Y", fontsize=18)
    plt.savefig('VAE_space'+str(it)+'.png', format='png', dpi=200)

plt.show()

Geography = pd.get_dummies(df['Geography'], drop_first=True)
Geography

df.drop(['Geography','Gender'], axis=1, inplace=True)

df.head(2)

df = pd.concat([df,Geography,Gender],axis=1)
df.head(2)

corr = df.corr()
plt.figure(figsize=(15,10))
sns.heatmap(corr, annot=True, cmap='BuPu')

X = df.drop('Exited', axis=1)
y = df['Exited']

X.head(2)

y.head(2)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 1)

ss = StandardScaler()
X_train = ss.fit_transform(X_train)
X_test = ss.transform(X_test)

import keras
from keras.models import Sequential
from keras.layers import Dense

model = tf.keras.Sequential([
    
    tf.keras.layers.Dense(11, activation="relu", input_shape=(X.shape[1],)),
    tf.keras.layers.Dense(6, activation="relu"),
    tf.keras.layers.Dense(1, activation="sigmoid")
    
])

model.summary()

model.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics='accuracy')

trained_model = model.fit(X_train, y_train , batch_size=100, epochs = 50)

plt.plot(trained_model.history["loss"])

y_pred = model.predict(X_test)

y_pred = np.where(y_pred >= 0.5,1,0)

from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
cm

