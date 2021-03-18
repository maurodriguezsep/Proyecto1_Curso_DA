import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

get_ipython().run_line_magic('matplotlib', 'inline')
plt.style.use('seaborn')

df=pd.read_csv('results.csv')


# In[2]:


df.head(10)


# In[3]:


df['SMA_Stgo_10']=df['t_stgo'].rolling(10,min_periods=1).mean()
df['SMA_Barcelona_10']=df['t_barcelona'].rolling(10,min_periods=1).mean()
df['SMA_Nairobi_10']=df['t_nairobi'].rolling(10,min_periods=1).mean()
df['SMA_Sydney_10']=df['t_sydney'].rolling(10,min_periods=1).mean()
df['SMA_Global10']=df['t_global'].rolling(10,min_periods=1).mean()

                                         
                                         


# In[4]:


df.head(11)


# In[5]:


df=df.drop(columns=['t_stgo','t_barcelona','t_nairobi','t_sydney','t_global'])

df.set_index('year',inplace=True)

df.head(5)


# In[6]:


# colors for the line plot
colors = ['green', 'red', 'purple','blue','yellow']

# line plot - the yearly average air temperature in Barcelona
df.plot(color=colors, linewidth=3, figsize=(12,6))

# modify ticks size
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(labels =df.columns, fontsize=14)
                          
# title and labels
plt.title('The yearly temperature in Santiago', fontsize=20)
plt.xlabel('Year', fontsize=16)
plt.ylabel('Temperature [°C]', fontsize=16)


# In[7]:


df.corr(method="pearson")


# In[8]:


df.reset_index(inplace=True)
print(df.head(5))


# In[9]:


df2=df[['SMA_Global10','year']]

data=df2[['year']]
X_train = np.array(data)
print(df2['SMA_Global10'].shape)
print(X_train.shape)


#X_train = (df2['SMA_Global10']).astype(int).values
y_train = df2['SMA_Global10']


regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)


# Hacemos las predicciones que en definitiva una línea (en este caso, al ser 2D)
y_pred = regr.predict(X_train)
 
# Veamos los coeficienetes obtenidos, En nuestro caso, serán la Tangente
print('Coefficients: \n', regr.coef_)
# Este es el valor donde corta el eje Y (en X=0)
print('Independent term: \n', regr.intercept_)
# Error Cuadrado Medio
print("Mean squared error: %.2f" % mean_squared_error(y_train, y_pred))
# Puntaje de Varianza. El mejor puntaje es un 1.0
print('Variance score: %.2f' % r2_score(y_train, y_pred))

from sklearn.metrics import r2_score

r2 = r2_score(y_train, y_pred )
print(r2)



print('MODELO 2')

df3=df[['SMA_Global10','SMA_Stgo_10']]

data=df3[['SMA_Global10']]
X_train = np.array(data)
print(df3['SMA_Stgo_10'].shape)
print(X_train.shape)


y_train = df3['SMA_Stgo_10']


regr = linear_model.LinearRegression()
regr.fit(X_train, y_train)


# Hacemos las predicciones que en definitiva una línea (en este caso, al ser 2D)
y_pred = regr.predict(X_train)
 
# Veamos los coeficienetes obtenidos, En nuestro caso, serán la Tangente
print('Coefficients: \n', regr.coef_)
# Este es el valor donde corta el eje Y (en X=0)
print('Independent term: \n', regr.intercept_)
# Error Cuadrado Medio
print("Mean squared error: %.2f" % mean_squared_error(y_train, y_pred))
# Puntaje de Varianza. El mejor puntaje es un 1.0
print('Variance score: %.2f' % r2_score(y_train, y_pred))

from sklearn.metrics import r2_score

r2 = r2_score(y_train, y_pred )
print(r2)


