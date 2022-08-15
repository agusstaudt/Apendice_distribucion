#!/usr/bin/env python
# coding: utf-8

# ---
# # Capítulo 3 
# 
# ## Rutina de Python para replicar el "Apéndice en la Práctica" del capítulo 3 de Pobreza y Desigualdad en América Latina 
# #### Ultima actualización: 03 de agosto de 2022
# 
# Códigos escritos en base a los apéndices del libro “Pobreza y Desigualdad en América Latina” de Gasparini, Cicowiez y Sosa Escudero. El objeto de este material es reproducir la rutina de códigos para STATA presentada en el libro al lenguaje *Python*. Este material es sólo de carácter complementario a las explicaciones y detalles conceptuales que se presentan en el libro de texto y los apéndices.
# 
# ---

# ## Set inicial
# 
# Antes de comenzar, se cargan las librerías necesarias para poder desarrollar el capítulo:
# - *os*: realizar consultas acerca de directorios o pedidos específicos al sistema opertivo.
# - *pandas*: necesario para manipulación y análisis de datos.
# - *matplotlib*: para visualización.
# - *numpy*: para creación y manipulación de vectores y matrices. También presenta una gran colección de funciones matemáticas para operar con ellas.
# - *math*: para utilizar también funciones matemáticas.
# - *scipy*: herramientas y algoritmos matemáticos. contiene módulos para optimización, álgebra lineal, integración, interpolación, funciones especiales.
# - *econtools*: herramientas econométricas.  

# In[1]:


# Importamos librerias de Python necesarias para replicar los calculos
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy import stats
get_ipython().system('pip install econtools')
import econtools
import econtools.metrics as mt
import time


# Al igual que en el capítulo 2, utilizamos colores para la ejecución de `print()`.

# In[2]:


# Utilizamos algunos estilos 
class style():
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[1;32m' # negrita
    underline = '\033[4m'
    mark = '\33[44m'
    italic = '\33[3;32m'
    endc = '\033[0m'


# A continuación cargamos las bases que vamos a utilizar. Se importan los archivos desde *google drive* de la misma manera que en el capítulo 2, con la diferencia de que al ser bases para diferentes países primero armamos una lista con los *id* de las bases que necesitamos, y las cargas se guardan en un diccionario de *python*. Los diccionarios aquí nos permiten crear mapeos a partir de una *key* y *values*, donde a partir de un nombre clave podemos almacenar listas o incluso un dataframe entero. Los mismos resultan muy útiles para problemas como el de almacenar diferentes *dataframes* en un solo lugar. Para más información acerca de diccionarios pueden consultar [***freeCodeCamp***](https://www.freecodecamp.org/espanol/news/compresion-de-diccionario-en-python-explicado-con-ejemplos/#:~:text=%C2%BFQu%C3%A9%20es%20un%20diccionario%20en,un%20par%20de%20corchetes%20%7B%7D%20.). Los diccionarios tienen la siguiente forma:    
# 
# `mi_diccionario = {"key1":<value1>,"key2":<value2>,"key3":<value3>,"key4":<value4>}`
# 
# Donde cada *value* puede referirse a un vector o base de datos. Para el siguiente bucle, cada *dataframe* cargado se guardará en *df_todos*. Nada nuevo a lo que venimos realizando, con la excepción de la función `sleep()` de la librería `time`. Google maneja ciertos límites para realizar sucesivas *queries* o pedidos, por lo que dada cierta repetición de solicitudes en un período corto de tiempo *python* podría arrojarnos un error. Por lo que en cada iteración pausamos el tiempo por la cantidad de segundos indicado en el bucle, en nuestro caso demoramos el proceso 4 segundos por repetición.

# In[3]:


# Cargamos las bases
df_todos = {}
links = ["1fgHKvdLDe3x5tCQheoXRL1JMGNDW0W7n", "1udEv9SNL9IiOCmfXg8MLdru1v9C_Sds2",
        "1ZBX4B4IrGPGIN9VwZLknaddCJ4AqAE07", "1f5p2qF1N9tgqoQ-bdY8QMvzSnt2FCFWY",
        "1-a7OTv-I6SJXDhFhrCixbitx7KT4_lgx"]
dfs = ["df_ecu", "df_mex", "df_nic", "df_per", "df_pan"]
for i in range(0, len(links)):
    print(f'iteration{i}: {style.green}{dfs[i]}{style.endc}')
    df_todos[dfs[i]] = pd.read_stata('https://drive.google.com/uc?id=' + links[i]) 
    time.sleep(4) # restringimos la velocidad de cada query  
df_todos


# ## 3.1 Cociente de quintiles
# 
# [***Páginas 151-152***](https://drive.google.com/file/d/1MwQrMylnYL0VHrLRM3JafsCBE9NkisAJ/view)
# 
# El siguiente bloque de código puede utilizarse para computar el cociente de quintiles extremos presentado en el cuadro 3.2 del texto del libro, el cual es un indicador de desigualdad extendido en la literatura, que denota la magnitud de las brechas entre los más ricos y más pobres. Para realizar el cálculo se trabaja sobre un bucle que va a iterar sobre cada una de las bases importadas. En primer lugar, se filtra del diccionario el *dataframe* de interés denominado *df* y se eliminan las observaciones *ipcf* nulas para luego ordenarlas de manera ascendente con `sort_values()`. Posteriormente, se crea la proporción de población acumulada *shrpop* utilizando el factor de expansión *pondera*, ya que a partir de *shrpop* podemos identificar los 5 quintiles. La variable *quintil* vale 1 para el 20% más pobre de la población, 2 para el 20% siguiente, y así sucesivamente. Una vez obtenida la variable *quintil* computamos el ingreso promedio ponderado para las observaciones del quintil 1 y 5. En el cálculo de los *ipcf* promedios le indicamos a python con `loc()` que solo queremos quedarnos con las observaciones del quintil 1 (en *meadia_q1*) y el quintil 5 (en *media_q5*). A partir de la generación del *ipcf* promedio para ambos quintiles pasamos a calcular el ratio de estos dos valores e imprimimos el resultado con la función `print()`. 

# In[4]:


# Calculamos el cociente de quintiles para todas las base
for name in dfs: 
    # Ordenar las observaciones del dataframe segun el IPCF
    df = df_todos[name]
    df = df[df["ipcf"]>0]
    df = df.sort_values(by=['ipcf'])

    # Creamos una variable con la proporcion de poblacion acumulada
    df.loc[:,"shrpop"] = df["pondera"].cumsum()
    df["shrpop"]= df["shrpop"]/ df["pondera"].sum()

    # Identificamos quintiles del IPCF
    df.loc[(df["shrpop"]>=0 & (df["shrpop"]<=0.2)),"quintil"]=1
    df.loc[(df["shrpop"]>0.2) & (df["shrpop"]<=0.4),"quintil"]=2
    df.loc[(df["shrpop"]>0.4) & (df["shrpop"]<=0.6),"quintil"]=3
    df.loc[(df["shrpop"]>0.6) & (df["shrpop"]<=0.8),"quintil"]=4
    df.loc[(df["shrpop"]>0.8) & (df["shrpop"]<=1),"quintil"]=5

    # Calculamos el IPCF promedio de ese quintil
    media_q1 = np.average(df.loc[df["quintil"]==1, "ipcf"], 
                          weights=df.loc[df["quintil"]==1, "pondera"])
    
    # Calculamos el IPCF promedio de ese quintil
    media_q5 = np.average(df.loc[df["quintil"]==5, "ipcf"], 
                          weights=df.loc[df["quintil"]==5, "pondera"])

    print('Utilizando', style.italic + name + style.endc,'el cociente de quintiles es igual a', style.green + "{:.0f}".format(media_q5/media_q1) + style.endc)


# Los valores obtenidos indican que la mayor brecha de quintiles extremos se da en Panamá, cuyo quintil 5 es 23 veces más alto que el del quintil 1.

# ## 3.2 Replicar programa ratq51
# 
# [***Páginas 153-154***](https://drive.google.com/file/d/1MwQrMylnYL0VHrLRM3JafsCBE9NkisAJ/view)
# 
# En la siguientes líneas de código proponemos escribir una función que permite computar el cociente de quintiles extremos muy fácilmente. Se define una función llamada *ratq51* que tiene como argumento la variable a utilizar *x* y opcionalmente el ponderador *weight*. Notarán que a diferencia de la función en Stata aquí no se incluye ningún condicional dentro de los argumentos de la función, esto es debido a que la misma se realiza implícitamente al indicar la base de datos a utilizar. Como aprendimos antes, podemos filtrar las observaciones que queremos utilizar y ubicar la sentencia dentro del argumento data. Por ejemplo, si quisieramos realizar el cálculo sobre la región 1 podríamos hacer lo siguiente:
# 
# `ratq51(df.loc[df['region']==1,:], ...)`
# 
# La creación de `ratq51()` se realiza mediante un método alternativo al que vimos en `descriptive_stats()` del capítulo 2. Como argumento primero establecemos la base de datos que necesitará la función, denominado *data*, y a continuación la variable que nos interesa dentro del dataset indicado. ¿Podríamos haber pasado directamente el vector de interés a la función? Por supuesto que sí, el contenido de la función sería un poco diferente, pero se podría como alternativa. Aunque para mostrar otra forma de encarar la elaboración de una función, se decidió optar por un camino alterno, donde primero indicamos la base de datos y posteriormente los nombres de la columna que interesan para ejecutar la función. Esto se deriva en que necesitamos indicar obligatoriamente un *dataset* y una columna de interés que se encuentre dentro de este, lo cual será evaluado en primera instancia como error fatal. De no cumplirse esto, la función arrojará un error. En el caso del ponderador, este no corre la misma suerte que los argumentos explicados antes. El factor de expansión es opcional, por lo que al no indicarlo la función computará el ratio sin ponderar. Lo que sigue es exactamente lo mismo que calculamos en la rutina anterior, con la diferencia de que readaptamos el código para volver al procedimiento uno genérico. 
# 
# Un detalle no menor se encuentra también en la forma de definir la variable *x* y el ponderador *weight* como argumentos de la función. El hecho de definir a ambas como string con la opción `str` hace que la función automáticamente entienda a ambos como caracteres, en vez de algún otro *type*, por lo que en el desarrollo de la función cada vez que nombramos a los argumentos lo podemos hacer sin incluir las comillas `''`. Mientras que al ejecutar dicha función se especifican los nombres de las variables entre comillas `''`. Por último, al seguir la ejecución del ratio de quintiles extremos realizado antes la función estaría filtrando el dataframe con valores mayores a cero.   

# In[5]:


def ratq51(data, x:str = None, weight:str = None):
    ### Errores fatales
    # Falta especificar dataset
    if data.empty:
        raise ValueError('Falta asignar valor a x')
    else:
        pass
    # Falta indicar una variable dentro del dataframe a utilizar
    if x is None:
        raise ValueError('Falta asignar valor a x')
    else:
        pass
    # Como el ponderador es opcional, contemplamos ambas posibilidades
    if weight is None:
        df = data[x]
        df[weight] = data[x]*0+1
    else:
        df = data.loc[:, [x, weight]]
    # Creamos el shrpop  
    df = df.sort_values(by=[x])
    df = df[df[x]>0]
    df.loc[:,"shrpop"]= df[weight].cumsum()
    df["shrpop"]= df["shrpop"]/ df[weight].sum()
    
    # Identificar quintiles
    df.loc[(df["shrpop"]<=0.2) & (df["shrpop"]>=0),"quintil"]=1
    df.loc[(df["shrpop"]>0.2) & (df["shrpop"]<=0.4),"quintil"]=2
    df.loc[(df["shrpop"]>0.4) & (df["shrpop"]<=0.6),"quintil"]=3
    df.loc[(df["shrpop"]>0.6) & (df["shrpop"]<=0.8),"quintil"]=4
    df.loc[(df["shrpop"]>0.8) & (df["shrpop"]<=1),"quintil"]=5
    
    # Calculamos el IPCF promedio de ese quintil
    media_q1 = np.average(df.loc[df["quintil"]==1, x], 
                          weights=df.loc[df["quintil"]==1, weight])
    
    # Calculamos el IPCF promedio de ese quintil
    media_q5 = np.average(df.loc[df["quintil"]==5, x], 
                          weights=df.loc[df["quintil"]==5, weight])

    return media_q5/media_q1


# In[6]:


pd.options.mode.chained_assignment = None  # default='warn' https://stackoverflow.com/questions/20625582/how-to-deal-with-settingwithcopywarning-in-pandas
#Volvemos a calcular el ratio para todas las bases pero utilizando la nueva funcion y almacenando los resultados en un df
results = pd.DataFrame(columns = ['Pais', 'Año', 'Q5/Q1'])
results['Pais'] = ['Ecuador', 'Mexico', 'Nicaragua', 'Peru', 'Panama']
results['Año'] = ['2006', '2006', '2005', '2006', '2006']

j = 0

for name in dfs:    
    df = df_todos[name]
    results.iloc[j]['Q5/Q1'] = ratq51(data = df, x ='ipcf', weight = 'pondera')
    j = j + 1


# In[7]:


# Verificamos que los resultados se hayan almacenado correctamente
results


# ## 3.3 Replicar programa gcuan 
# 
# [***Páginas 154-155***](https://drive.google.com/file/d/1MwQrMylnYL0VHrLRM3JafsCBE9NkisAJ/view)
# 
# El bloque de código a continuación permite identificar cuantiles de cualquier variable. En términos de la función `ratq51()` nos permite generar variables similares al quintil pero que pueden identificar también deciles, ventiles, percentiles, etc. 
# 
# Por esta razón, esta función tendrá más argumentos, aquí además de los anteriores debemos detallar la cantidad de cuantiles a generar (argumento *num*) y la variable que los almacena (*newvar*). Esta última tendrá como nombre por defecto *'cuantil'*, pero el usuario podría asignar el nombre que desea (siempre entre comillas). Notar que aquí *weight* sigue siendo opcional, de no agregarse el código realizará los cálculos sin factor de expansión. No obstante, la forma de comprobar la existencia del ponderador se realiza a través de la función `len()`, que verifica si hay una longitud positiva de la serie que se va a utilizar como factor de expansión, la cual representa una manera alternativa de realizar el chequeo.    
# 
# Luego el código y la secuencia son idénticos a la de la función anterior, salvo que aquí el objeto “num” indica cuantos cuantiles deben generarse, haciendo iterar al bucle “num” cantidad de veces, y define los intervalos de población acumulada de forma equivalente. Por ejemplo, si queremos generar deciles (num=10), necesitamos 10 cuantiles y cada cuantil se asigna en intervalos de población acumulada iguales a 0.10 (1/10). Una vez identificado los cuantiles `gcuan()` computa la media, el desvío estándar y la cantidad de observaciones para cada cuantil y asigna los resultados a un *dataframe* llamado *result*, el cual es impreso como output de la función,

# In[20]:


def gcuan(x, num: int, weight, newvar = 'cuantil'):
    dict = {}
    if int(num)!= num:
        raise ValueError('Los cuantiles tienen que ser números enteros')
    else:
        pass
    
    if len(weight)==0:
        weight = x*0+1
    else:
        weight = weight 

    df = pd.concat([x, weight], axis=1, keys=['x', 'weight'])
    df = df.sort_values(by=['x'])
    df = df[df["x"]>0]
    df.loc[:,"shrpop"] = df["weight"].cumsum()
    df["shrpop"] = df["shrpop"]/df["weight"].sum()    

    shrcuantil = 1/num

    df[newvar]=0

    for i in range(1, num+1):
        
        df.loc[(df['shrpop']>(i-1)*shrcuantil) & (df['shrpop']<=i*shrcuantil), newvar] = i 

    result = pd.DataFrame({'mean':df.groupby([newvar], group_keys=False).apply(lambda x: np.average(x.x, weights=x.weight)),
                          'std':df.groupby([newvar], group_keys=False).apply(lambda x: math.sqrt(np.average((x.x-np.average(x.x, weights=x.weight))**2, weights=x.weight))),
                          'obs':df.groupby([newvar], group_keys=False).apply(lambda x: x.weight.sum())})
    return result


# Para probar la función, utilizamos el *dataframe* de México dentro del diccionario *df_todos*.

# In[16]:


#Aplicamos la funcion creando 5 cuantiles en la base de Ecuador 
gcuan(df_todos['df_mex']['ipcf'], 5, weight=df_todos['df_mex']['pondera'])


# ## 3.4 Tamaño de los hogares
# 
# [***Páginas 156***](https://drive.google.com/file/d/1MwQrMylnYL0VHrLRM3JafsCBE9NkisAJ/view)
# 
# El código siguiente puede utilizarse para computar las estadísticas sobre proporción de hogares unipersonales y multipersonales presentadas en el cuadro 3.4 del texto. Con este código podremos calcular qué proporción del total de hogares se compone de 1, 2, 3, 4,…, n miembros y combinado con los códigos anteriores, analizar cómo esta configuración cambia al agrupar por regiones, percentil de ingreso, condición de pobreza, etc. 
# 
# En primer lugar, cargamos las bases que vamos a utilizar, las cuales son representativas de los países de Honduras, México, República Dominicana y Uruguay. Las mismas son improtadas y guardadas en el diccionario *df_todos*.

# In[23]:


df_todos = {}
links = ["1pLly5AnoWj9fPyBcBZ8bCgDWqZ1eppgD", "1udEv9SNL9IiOCmfXg8MLdru1v9C_Sds2",
        "1BxiFvCMrUSjDsgYs73-1yi2cGMuKJV22", "1XI6dexijKCd2jIZlyZfV6C9sAU2mq39y"]
dfs = ["df_hon", "df_mex", "df_dom", "df_ury"]
cnt = ["Honduras", "México", "Rep. Dominicana", "Uruguay"]
for i in range(0, len(links)):
    print(f'iteration{i}: {style.green}{dfs[i]}{style.endc}')
    df_todos[dfs[i]] = pd.read_stata('https://drive.google.com/uc?id=' + links[i]) 
    time.sleep(4) # restringimos la velocidad de cada query  
df_todos


# A continuación, pasamos a calcular la proporción de hogares según tamaño o cantidad de integrantes para cada país. Para hacerlo, realizamos el siguiente procedimiento para cada país:
# 1. ordenamos las observaciones según *id* de forma ascendente y jefe de hogar de manera descendente, e identificamos al primer integrante de cada hogar
# 2. creamos una variable unitaria *aux* que utilizamos para sumar la cantidad de integrantes por hogar
# 3. creamos la variable *tamanio* que va a representar la cantidad de miembros por hogar, truncando en 6, es decir, el valor 6 representará la condición `...>=6`
# 4. una vez que creamos *tamanio* filtramos la base para quedarnos solamente con una observación del hogar, en nuestro caso la primera de cada *id* que sería el jefe de hogar. También, realizamos un filtro para quedarnos con hogares con al menos un miembro
# 5. agregamos las observaciones por cantidad de miembros en el hogar, sumando cada observación utilizando su ponderador. Al quedarnos solamente con una observación por hogar esta suma equivale a la suma de hogares por cantidad de miembros. Luego, calculamos su frecuencia realtiva
# 6. el output generado para cada país es unido a la base final *df_total*

# In[24]:


# Creamos nuevas columnas con la cantidad de miembros por hogar y una clasificacion de tamaño
df_total = {'tamanio': [1, 2, 3, 4, 5, 6]}
df_total = pd.DataFrame(data=df_total)
c = 0
for name in df_todos:
    print(f'iteration{i}: {style.green}{name}{style.endc}')
    df = df_todos[name]
    df = df.sort_values(by=['id']).reset_index()
    df["tag_hogar"] = df.groupby('id').cumcount() == 0
    df['aux'] = 1 
    df['miembros']=df.groupby('id')['aux'].transform(sum)

    df["tamanio"]=0
    df.loc[(df["miembros"]==1) & (df["tag_hogar"] == True),"tamanio"]= 1 #Hogar unipersonal
    df.loc[(df["miembros"]==2) & (df["tag_hogar"] == True),"tamanio"]= 2 #Hogar de dos personas
    df.loc[(df["miembros"]==3) & (df["tag_hogar"] == True),"tamanio"]= 3 #Hogar de tres personas
    df.loc[(df["miembros"]==4) & (df["tag_hogar"] == True),"tamanio"]= 4 #Hogar de cuatro personas
    df.loc[(df["miembros"]==5) & (df["tag_hogar"] == True),"tamanio"]= 5 #Hogar de cinco personas
    df.loc[(df["miembros"]>=6) & (df["tag_hogar"] == True),"tamanio"]= 6 #Hogar de seis personas o mas
    
    # Creamos un nuevo data frame con la cantidad de observaciones para cada categoria de tamaño y su porcentaje respecto al total
    df_agg = df[df['tag_hogar'] == True] # Nos quedamos solo con un miembro del hogar
    df_agg = df_agg[df_agg['tamanio']>0] # Descartamos las observaciones con valor igual a 0
    df_agg = df_agg.groupby(by=['tamanio']).agg({'pondera':'sum'}) 
    df_agg['porcentaje'] = df_agg['pondera']/df_agg["pondera"].sum()*100
    df_agg.columns = ['total', cnt[c]]
    df_total = df_total.merge(df_agg[cnt[c]], on = 'tamanio')
    c += 1
# verificamos resultado post iteración en bucle
df_total


# ## 3.5 Distribución intrahogar
# 
# [***Páginas 157***](https://drive.google.com/file/d/1MwQrMylnYL0VHrLRM3JafsCBE9NkisAJ/view)
# 
# El fragmento de código siguiente puede utilizarse para generar resultados similares a los presentados en el cuadro 3.7 del texto, que muestra cómo se modifica la desigualdad calculada a través del cociente de deciles extremos cuando cambia la distribución del ingreso hacia el interior del hogar. Cabe recordar que la distribución del ingreso intrahogar se modifica mediante un impuesto proporcional al ingreso per cápita familiar combinado, con un subsidio que solo recibe el jefe de hogar. En la implementación, utilizamos quintiles en lugar de deciles ingreso. 
# 
# Para esta sección trabajaremos con diferentes bases nuevamente, por lo que podríamos pensar si no nos serviría una función que importe los países de interés. Sabemos hasta ahora que todas las bases corresponden a países en años específicos en formato *.dta*. Así que podríamos utilizar lo visto hasta ahora para crear una nueva función `import_dta()` cuyos argumentos sean los países que interesan y el/los años. 

# In[89]:


def import_dta(cnt, year):
    # list of possible countries 
    countries = {'argentina_92':"1ICi2BF3YkQt2a_fBkxt00CV1_ipmsEIP",
                'argentina_06':"194pyYGovurVuCw8zpfqe2dJ7XAbYdG4s",
                'argentina2_06':"1IiHzxWrO-5dETM-jdiXx9ayP5PAqU0Yp",
                'honduras_06':"1pLly5AnoWj9fPyBcBZ8bCgDWqZ1eppgD",
                'mexico_06':"1udEv9SNL9IiOCmfXg8MLdru1v9C_Sds2",
                'republica_dominicana_06':"1BxiFvCMrUSjDsgYs73-1yi2cGMuKJV22",
                'uruguay_06':"1XI6dexijKCd2jIZlyZfV6C9sAU2mq39y",
                'ecuador_06':"1fgHKvdLDe3x5tCQheoXRL1JMGNDW0W7n",
                'nicaragua_05':"1ZBX4B4IrGPGIN9VwZLknaddCJ4AqAE07",
                'costa_rica_06':"17Bq2ee5cSdV0N_tqj4yiuMmOfJaDJ_LD",
                'peru_06':"1f5p2qF1N9tgqoQ-bdY8QMvzSnt2FCFWY",
                'panama_06':"1-a7OTv-I6SJXDhFhrCixbitx7KT4_lgx",
                'paraguay_07':"1DdvUN2auRHyDHX49gLpyBKD_mvulQpqN",
                'venezuela_06':"1En_N99oLlbDlQU1X60NLnBNKRXq8waUi",
                'bolivia_05':"1O4KAVOLNy9FCgW-YhPu8hkAQJ_kLgVr9",
                'brasil_07':"1uWBruRaNYDSy7LrYWFw8cQ1wQCQn80RA",
                'colombia_06':"1YNoQiSiHI3iGuHds7dsrcPVR6_eR_FaF"} 
    # creating list of actual countries requested
    li = []
    for r in range(0, len(cnt)):
        cnt[r] = cnt[r].replace(' ', '_')
        if type(year[r]) == list:
            for i in year[r]:
                cntName = [f'{cnt[r]}_{i}']
                li = li + cntName
        else:
            cntName = [f'{cnt[r]}_{year[r]}']
            li = li + cntName
    # main loop with the actual countries
    df_todos = {}
    c = 1
    for name in li:
        print(f'iteration {c}: {style.green}{name}{style.endc}')
        if name == 'argentina_92':
            df_todos[name] = pd.read_stata('https://drive.google.com/uc?id=' + countries[name], convert_categoricals=False) 
        else:
            df_todos[name] = pd.read_stata('https://drive.google.com/uc?id=' + countries[name], convert_categoricals=False) 
        time.sleep(4) # restringimos la velocidad de cada query  
        c+=1
    return df_todos


# Podemos probar si funciona, creando una lista de países y una lista de años. 

# In[14]:


# Importamos las bases de Argentina, Honduras, Paraguay y Venezuela (2006)
paises = ['argentina', 'honduras', 'paraguay', 'venezuela']
y = ['06', '06', '07', '06']
df_todos = import_dta(cnt=paises, year=y)


# Ahora tenemos una función que acepta lista de países y de años para importar y cargar cada *dataset* dentro de un diccionario. La función es mutable, iremos agregando bases a las opciones a medida que avancemos en el desarrollo del anexo y mejorando la misma en términos de prolijidad y estructura. Claramente, la función es mejorable y pensar en escenarios donde la misma no funcione resulta un buen ejercicio para mejorarla. A continuación, trabajaremos con las bases importadas en la rutina de arriba. 
# 
# Una vez cargadas las bases, creamos el objeto *ty_todos* que toma valores de diferentes tasas del impuesto aplicada sobre el *ipcf*. Teniendo esta lista realizamos un bucle sobre cada impuesto y cada país utilizado aplicando el siguiente procedimiento:
# 1. ordenamos las observaciones por *id*
# 2. identificamos al primer miembro del hogar
# 3. creamos la variable impuesto, que va a ser la alícuota *ty* que se multiplica al *ipcf* 
# 4. creamos *subsidio*, que se calcula sumando por hogar la recaudación de impuestos, es decir, sumamos la variable *impuesto* por hogar
# 5. seteamos a cero el valor del subsidio para todos los miembros del hogar distintos al primero, de esta manera, el subsidio solo lo recibe un integrante
# 6. creamos una variable para el nuevo valor de ingreso per cápita familiar, restando el impuesto y sumando el subsidio
# 7. hacemos uso de nuestra función `ratq51` para computar el cociente del ingreso promedio de los quintiles 5 y 1 como indicador de desigualdad, a partir del ingreso modificado

# In[25]:


# Armamos listas con las bases para las que vamos a calcular el cociente de quintiles y las alicuotas del impuesto simulado
ty_todos = [0, 0.1, 0.2, 0.3]
# Armamos un dataframe vacio para almacenar los resultados
results = pd.DataFrame()
# Rellenamos el dataframe con los cocientes de quintiles para cada combinacion de pais y alicuota
j = 0
for ty in ty_todos:
    for name in df_todos.keys():
        df = df_todos[name]
        df = df.sort_values(by=['id']).reset_index()
        df["tag_hogar"] = df.groupby('id').cumcount() == 0
        df["impuesto"] = df["ipcf"]*ty
        #Recaudacion impuesto por hogar:
        df["subsidio"] = df.groupby(['id']).impuesto.transform('sum')
        df.loc[df["tag_hogar"] != True,"subsidio"]= 0
        df["ipcf_star"] = df["ipcf"] - df["impuesto"] + df["subsidio"]
        results.loc[ty,j] = ratq51(data=df, x="ipcf_star",weight="pondera")
        if j > 2:
            j = j - 3
        else:
            j= j + 1


# In[26]:


# Asignamos nombres a las columnas y verificamos los resultados
results.columns = ['Argentina', 'Honduras', 'Paraguay', 'Venezuela']
results


# ## 3.6 Empleo de ponderadores
# 
# [***Páginas 157***](https://drive.google.com/file/d/1MwQrMylnYL0VHrLRM3JafsCBE9NkisAJ/view)
# 
# El bloque de código que sigue puede utilizarse para construir un cuadro como el 3.9 del texto, que muestra la relación entre el ingreso per cápita familiar y el valor de la variable de ponderación. En primer lugar, volvemos a descargar las bases que vamos a utilizar. 

# In[29]:


# Importamos las bases de Argentina, Honduras, Paraguay y Venezuela (2006)
paises = ['argentina', 'honduras', 'mexico', 'nicaragua']
y = ['06', '06', '06', '05']
df_todos = import_dta(cnt=paises, year=y)


# Con las bases ya cargadas pasamos a realizar el siguiente procedimiento, en un bucle para los países:
# 1. ordenamos por *id*
# 2. generamos la variable *shrpop*
# 3. identificamos el quintil de la observación según *shrpop*, creando la variable *quintil*
# 4. calculamos el valor promedio del factor de expansión agrupando por *quintil* previamente
# 5. unimos el resultado al *dataframe* *df_total* 

# In[39]:


import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
# Creamos un data frame para ir almacenando los datos de cada pais
df_total = {'quintil': [1, 2, 3, 4, 5]}
df_total = pd.DataFrame(data=df_total)
# # Rellenamos el data frame con el valor de ponderacion promedio por quintil para cada pais
# df_todos = [df_arg, df_cri, df_mex, df_nic]

i=1
for name in df_todos.keys():
    print(f'iteration{i}: {style.green}{name}{style.endc}')
    df = df_todos[name]
    df= df.sort_values(by=['ipcf']).reset_index()
    df["shrpop"]= df["pondera"].cumsum()
    df["shrpop"]= df["shrpop"]/ df["pondera"].sum()
    
    df["quintil"]=0
    df.loc[df["shrpop"] <= 0.2,"quintil"]=1
    df.loc[(df["shrpop"] <= 0.4) & (df["shrpop"] > 0.2),"quintil"]=2
    df.loc[(df["shrpop"] <= 0.6) & (df["shrpop"] > 0.4),"quintil"]=3
    df.loc[(df["shrpop"] <= 0.8) & (df["shrpop"] > 0.6),"quintil"]=4
    df.loc[(df["shrpop"] <= 1) & (df["shrpop"] > 0.8),"quintil"]=5
    df_agg = df.groupby(by=['quintil']).agg({'pondera':'mean'}) 
    df_total = df_total.merge(df_agg['pondera'], on = 'quintil')
    i += 1


# In[40]:


#Asignamos nombres a las columnas y verificamos los resultados
df_total.columns = ['Quintil', 'Argentina', 'Honduras', 'Mexico', 'Nicaragua']
df_total


# Seguidamente se calculan las tasas de pobreza con y sin ponderadores para cada una de las regiones de México en 2006, correspondientes al cuadro 3.10 del texto. En la primer línea el objeto "lp" almacena el valor de la línea de pobreza, en base a la cual se genera la variable binaria *pobreza*, que vale 1 para los individuos debajo de este umbral (es decir, `ipcf < lp`) y 0 para el resto. Al computar el promedio de esta variable obtenemos la proporción de personas por debajo de la línea de la pobreza, la misma se realiza con y sin ponderador para cada una de las regiones, en un bucle para las 9 regiones de México. 

# In[51]:


# Cargamos la base de Mexico de 2006
df_mex = df_todos['mexico_06']
# Establecemos una linea de pobreza y añadimos una columna a la base de datos con una variable que vale 1 si el IPCF de un 
# individuo es inferior a esa linea y 0 en caso contrario. 
lp = 633.90918
df_mex["pobreza"] = (df_mex["ipcf"] < lp) * 1
# Creamos un dataframe para almacenar las tasas de pobreza por region 
tasas_pobreza = {'region': ['Noroeste', 'Norte', 'Noreste', 'Centro-Occidente', 'Centro-Este', 'Sur', 'Oriente', 'Peninsula de Yucatan', 'Nacional']}
tasas_pobreza = pd.DataFrame(data=tasas_pobreza)
tasas_pobreza['pob_sin_pond'] = 0
tasas_pobreza['pob_pond'] = 0

# Rellenamos el dataframe con las tasas de pobreza
j = 0
for i in range(1,9): 
    df_mex_1 = df_mex[df_mex['region'] == i].copy()
    pondera_1 = df_mex_1["pondera"]
    tasas_pobreza.loc[j, 'pob_sin_pond'] = np.average(df_mex_1["pobreza"])
    tasas_pobreza.loc[j, 'pob_pond'] = np.average(df_mex_1["pobreza"],weights=pondera_1)   
    j += 1


# In[50]:


# Agregamos la tasa de pobreza nacional y verificamos los datos
pondera = df_mex["pondera"]
tasas_pobreza.loc[8, 'pob_sin_pond'] = np.average(df_mex["pobreza"])
tasas_pobreza.loc[8, 'pob_pond'] = np.average(df_mex["pobreza"], weights=pondera) 
tasas_pobreza.columns = ['Region', 'Pobreza sin ponderador', 'Pobreza con ponderador']
tasas_pobreza


# ## 3.7 Diseño muestral
# 
# [***Páginas 160***](https://drive.google.com/file/d/1MwQrMylnYL0VHrLRM3JafsCBE9NkisAJ/view)
# 
# En este apartado se muestra cómo puede considerarse la estructura muestral al momento de computar un indicador relativamente sencillo; ver cuadro 3.11 del texto del capítulo. A modo de ejemplo, se emplea la Encuesta de Hogares de Propósitos Múltiples (EHPM) de Costa Rica para el año 2006 para calcular la proporción de trabajadores empleados en las industrias alimenticia y textil. 

# In[54]:


# Importamos la base de Costa Rica para 2006
paises = ['costa rica']
y = ['06']
df_todos = import_dta(cnt=paises, year=y)
df_cri = df_todos['costa_rica_06']


# En primer lugar, se generan quintiles de ingreso laboral (variable *ila*) para los individuos
# ocupados y que declaran sector de empleo.

# In[60]:


# Reducimos la muestra a los ocupados sin valores faltantes en las variables 'sector' e 'ila'
df_cri = df_cri[df_cri['ocupado'] == 1].copy()
df_cri = df_cri.dropna(subset=['sector'])
df_cri = df_cri.dropna(subset=['ila'])

# Creamos quintiles en base al ingreso laboral de los ocupados
df_cri= df_cri.sort_values(by=['ila']).reset_index()
df_cri["shrpop"]= df_cri["pondera"].cumsum()
df_cri["shrpop"]= df_cri["shrpop"]/ df_cri["pondera"].sum()
    
df_cri["quintil"]=0
df_cri.loc[df_cri["shrpop"] <= 0.2,"quintil"]=1
df_cri.loc[(df_cri["shrpop"] <= 0.4) & (df_cri["shrpop"] > 0.2),"quintil"]=2
df_cri.loc[(df_cri["shrpop"] <= 0.6) & (df_cri["shrpop"] > 0.4),"quintil"]=3
df_cri.loc[(df_cri["shrpop"] <= 0.8) & (df_cri["shrpop"] > 0.6),"quintil"]=4
df_cri.loc[(df_cri["shrpop"] <= 1) & (df_cri["shrpop"] > 0.8),"quintil"]=5


# Luego, la variable lowtec que vale 1 para los individuos empleados en las industrias alimenticia y textil (variable *sector=2*), 0 para los trabajadores empleados en otros sectores, y missing para quienes no tienen asignado un quintil de ingreso laboral.

# In[61]:


# Generamos una variable que indique si el sector corresponde a una industria de baja tecnologia
df_cri['lowtec'] = (df_cri["sector"] == 2) * 1  


# La estratificación de la **EHPM** de Costa Rica emplea dos criterios: región y zona urbana o rural. Por lo tanto, es necesario crear la variable de estratificación que permita identificar a cuál de los estratos pertenece cada observación de la encuesta. Utilizamos `econtools.group_id` para generar la variable *estrato*, que identifica con un número a cada uno de los "grupos" diferentes en que puede dividirse la base de datos al combinar las variables que recibe como argumento. El primero de los grupos recibe el número 1, el segundo grupo recibe el número 2, y así sucesivamente. Lueog, calculamos la proporción de ocupados en industria de baja tecnologia por quintil, junto con su desvío y error estándar y la cantidad de observaciones.

# In[68]:


# Generamos una nueva variable que agrupe las variables 'region' y 'urbano'
df_cri = econtools.group_id(df_cri, cols=['region', 'urbano'], merge = True)
df_cri = df_cri.rename(columns={'group_id': 'estrato'})
# computos por quintil
df_agg = df_cri.groupby(by=['quintil']).agg({'lowtec':['mean', 'std', 'count']}) 
df_agg.reset_index(inplace=True)  
df_agg.columns = list(map(''.join, df_agg.columns.values))
df_agg.columns = ['Quintil', 'Media', 'Desvio', 'N']
df_agg['Error estandar'] = df_agg['Desvio']/(df_agg['N'])**(1/2)


# In[69]:


# Visualizamos
df_agg


# Luego, realizamos el mismo ejercicio pero incluyendo a los ponderadores. Para ello, con la variable *quintil* ya creada realizamos un bucle filtrando en cada instancia el quintil de interés, donde se realizan los mismos cálculos realizados antes. Una vez realizado el cálculo de la media y el desvío estándar le agregamos los dos estadísticos que faltan, el error estándar y la cantidad de observaciones.   

# In[71]:


# Dataframe vacio para ir colocando los valores
df_pondera = {'Quintil': [1, 2, 3, 4, 5], 'Media': [0, 0, 0, 0, 0], 'Desvio': [0, 0, 0, 0, 0]}
df_pondera = pd.DataFrame(data=df_pondera)

# Rellenamos el dataframe
j = 0
for i in range(1,6): 

    df_cri_1 = df_cri[df_cri['quintil'] == i].copy()
    lowtec_1 = df_cri_1["lowtec"]
    pondera_1 = df_cri_1["pondera"]
    media_1 = np.average(lowtec_1, weights=pondera_1)  
    var_1 = np.average((lowtec_1-media_1)**2, weights=pondera_1) 
    de_1 = math.sqrt(var_1)
    df_pondera.loc[j, 'Media'] = media_1
    df_pondera.loc[j, 'Desvio'] = de_1
    j = j + 1
# Agregamos columnas con el numero de observaciones y el error estandar y verificamos
N = df_agg.drop(['Media', 'Desvio', 'Error estandar'], axis=1)
df_pondera = df_pondera.merge(N, on = 'Quintil')
df_pondera['Error estandar'] = df_pondera['Desvio']/(df_pondera['N'])**(1/2)
# visualizamos
df_pondera


# ## 3.8 Fuentes de ingreso
# 
# [***Páginas 161***](https://drive.google.com/file/d/1MwQrMylnYL0VHrLRM3JafsCBE9NkisAJ/view)
# 
# El bloque de código a continuación muestra cómo computar la importancia que tiene cada fuente de ingresos identificada en las encuestas de hogares (cuadro 3.13). Dentro de las fuentes de ingreso consideramos: laboral (variable *ila*), jubilaciones (*ijubi*), capital (*icap*), transferencias (*itran*) y otros (*ionl*). En primer lugar, cargamos las bases de los países que vamos a utilizar. Luego, utilizando un bucle para cada país realizamos el siguiente procedimiento:
# 1. generamos la variable ingreso total (*itot*), como la suma de las columnas para cada ingreso
# 2. a cada fuente de ingreso la multiplicamos por el factor de expansión *pondera*
# 3. creamos las variables de participación en el ingreso calculando el ratio de cada concepto sobre el ingreso total
# 4. repetimos para cada país y visualizamos resultados

# In[93]:


# Cargamos las bases de Argentina, Bolivia, Colombia, R. Dominicana y Uruguay (circa 2007)
# Importamos la base de Costa Rica para 2006
paises = ['argentina2','bolivia','colombia','republica dominicana','uruguay']
y = ['06','05','06','06','06']


df_todos = import_dta(cnt=paises, year=y)


# In[98]:


#Creamos un dataframe para almacenar los resultados
results = pd.DataFrame(columns = ['Pais', 'Año', 'Laborales', 'Capital', 'Transferencias'])
results['Pais'] = ['Argentina', 'Bolivia', 'Colombia', 'R. Dominicana', 'Uruguay']
results['Año'] = ['2006', '2005', '2006', '2006', '2006']


# In[102]:


# Rellenamos el dataframe
j = 0
for name in df_todos.keys():
    print(f'iteration: {style.green}{name}{style.endc}')
    df = df_todos[name]
    df['itot'] = df.fillna(0)['ila'] + df.fillna(0)['ijubi'] + df.fillna(0)['icap'] + df.fillna(0)['itran'] + df.fillna(0)['ionl'] 
    ila = np.sum(df['ila']*df['pondera'])
    ijubi = np.sum(df['ijubi']*df['pondera'])
    icap = np.sum(df['icap']*df['pondera'])
    itran = np.sum(df['itran']*df['pondera'])
    ionl = np.sum(df['ionl']*df['pondera'])
    itot = np.sum(df['itot']*df['pondera'])
    
    results.loc[j, 'Laborales'] = ila/itot
    results.loc[j, 'Capital'] = icap/itot
    results.loc[j, 'Transferencias'] = (ijubi + itran)/itot
    
    j = j + 1 

#Verificamos que los datos se hayan cargado correctamente
results

