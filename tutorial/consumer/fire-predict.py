import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import json
from kafka import KafkaConsumer, TopicPartition

consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
auto_offset_reset='latest', value_deserializer=lambda m: json.loads(m.decode('utf-8')))

consumer.subscribe('python-topic-1')
for message in consumer:
    message = message.value;
    #print('{}'.format(message))
    dataset_forestfire = pd.read_json('{}'.format(message))
    print(dataset_forestfire)
    break

#dataset_forestfire = pd.read_json('./forest_fire.json')
dataset_forestfire.head()

dataset_forestfire.month.replace(('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'),(1,2,3,4,5,6,7,8,9,10,11,12), inplace=True)
dataset_forestfire.day.replace(('mon','tue','wed','thu','fri','sat','sun'),(1,2,3,4,5,6,7), inplace=True)

dataset_forestfire.describe()

dataset_forestfire['Log-area']=np.log10(dataset_forestfire['area']+1)

for i in dataset_forestfire.describe().columns[:-2]:
    dataset_forestfire.plot.scatter(i,'Log-area',grid=True)

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

dataset_forestfire.month.replace((1,2,3,4,5,6,7,8,9,10,11,12),('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec'), inplace=True)
dataset_forestfire.day.replace((1,2,3,4,5,6,7),('mon','tue','wed','thu','fri','sat','sun'), inplace=True)
dataset_forestfire.head(13)

enc = LabelEncoder()
enc.fit(dataset_forestfire['month'])

enc.classes_

dataset_forestfire['month_encoded']=enc.transform(dataset_forestfire['month'])
dataset_forestfire.head(10)

enc.fit(dataset_forestfire['day'])

enc.classes_


dataset_forestfire['day_encoded']=enc.transform(dataset_forestfire['day'])
dataset_forestfire.head(20)

test_size=0.4

X_data=dataset_forestfire.drop(['area','Log-area','month','day'],axis=1)
y_data=dataset_forestfire['Log-area']

X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=test_size)

X_data.head(21)

y_train = y_train.values.reshape(y_train.size,1)


def rec(m,n,tol):
    if type(m)!='numpy.ndarray':
        m=np.array(m)
    if type(n)!='numpy.ndarray':
        n=np.array(n)
    l=m.size
    percent = 0
    for i in range(l):
        if np.abs(10**m[i]-10**n[i])<=tol:
            percent+=1
    return 100*(percent/l)

tol_max=20

from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

scaler = StandardScaler()

param_grid = {'C': [0.01,0.1,1, 100], 'epsilon': [10,1,0.1,0.01,0.001,0.0001], 'kernel': ['rbf']}

grid_SVR = GridSearchCV(SVR(),param_grid,refit=True,verbose=0,cv=5)
grid_SVR.fit(scaler.fit_transform(X_train),scaler.fit_transform(y_train))

print("Melhores paramêtros por Grid Search:",grid_SVR.best_params_)

a=grid_SVR.predict(X_test)
print("RMSE para Support Vector Regression:",np.sqrt(np.mean((y_test-a)**2)))

plt.xlabel("Área atual queimada")
plt.ylabel("Error")
plt.grid(True)
plt.scatter(10**(y_test),10**(a)-10**(y_test))

plt.title("Histograma de erros de previsão\n",fontsize=18)
plt.xlabel("Erros de previsão (ha)",fontsize=14)
plt.grid(True)
plt.hist(10**(a.reshape(a.size,))-10**(y_test),bins=50)


rec_SVR=[]
for i in range(tol_max):
    rec_SVR.append(rec(a,y_test,i))

plt.figure(figsize=(10,10))
plt.title("Curva REC para o Support Vector Regressor\n",fontsize=15)
plt.xlabel("Erro absoluto (tolerância) na previsão (ha)")
plt.ylabel("Porcentagem de previsão correta")
plt.xticks([i*1 for i in range(tol_max+1)])
plt.ylim(0,100)
plt.yticks([i*5 for i in range(21)])
plt.grid(linestyle='-', linewidth=2)
plt.plot(range(tol_max),rec_SVR)

print('Porcentagem de previsão correta\n',rec_SVR)