import streamlit as st

# Creamos la función de la matriz de decision para usuarios novatos
def matriz_decision_novato(dataframe, a, b, c):
    dataframe['Puntuacion'] = (dataframe['C'] * (1 - a) + 10) + \
                              (dataframe['P'] * b + 10) + (dataframe['S'] * c)
    return dataframe

# Creamos la función de la matriz de decision para usuarios expertos
def matriz_decision_experto(dataframe):
    pass

# Creamos la función que agrega los precios
def agrega_precios(dataframe1, dataframe2):
    merge = dataframe1.merge(dataframe2, left_on='Version', right_on='Version')
    return merge

# Creamos la función que presenta la interfaz
def define_interfaz(level_user, data):
    if level_user == 'Novato':
        interfaz_novato(data)
    else:
        interfaz_experto(data)

def interfaz_novato(data):
    # Opciones de interfaz para usuarios novatos
    st.sidebar.caption('Seleccione sus preferencias generales')
    select_consumo = st.sidebar.slider('Bajo Consumo', 1, 5)
    select_potencia = st.sidebar.slider('Potencia', 1, 5)
    select_seguridad = st.sidebar.slider('Seguridad', 1, 5)
    # Habilita las opciones de filtrado
    with st.expander('Seleccione los criterios de filtrado de su preferencia'):
        col1, col2 = st.columns(2)
        marca = col1.multiselect('Marca del vehículo', sorted(data['Marca'].unique().tolist()))
        if marca == []:
            col1.error('Elija al menos una marca de vehículo')
        precio_max = col1.slider('Precio en miles de pesos', 0, 10000)
    # Aplica las opciones de filtrado
    filtrado = data[(data['Marca'].isin(marca)) & (data['Precio'] < precio_max)]
    # Aplica la matriz de decisión y la guarda en la variable ponderacion.
    ponderacion = matriz_decision_novato(filtrado, select_consumo, select_potencia, select_seguridad)
    # Devuelve los resultados de la recomendación ordenados por puntuación descendente.
    if marca == [] or precio_max == 0:
        st.warning('Elija sus preferencias para ver las recomendaciones')
    else:
        st.subheader('Listado de vehiculos recomendados')
        st._arrow_table(
        ponderacion.loc[:, ['Marca', 'Modelo', 'Version', 'Precio', 'Puntuacion']].sort_values(by='Puntuacion',
                                                                                               ascending=False),
        )

def interfaz_experto(data):
    # Opciones de interfaz para usuarios expertos
    st.sidebar.write('Opciones para expertos')
    st.write('Opciones para expertos')