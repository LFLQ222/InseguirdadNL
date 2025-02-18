import streamlit as st
import pandas as pd
import plotly.express as px

def load_data():
    #Aqui es la parte en donde se combinan los diferentes archivos de los cuartos
    df_0324 = pd.read_csv('ENSU_CB_0324.csv')
    df_0624 = pd.read_csv('ENSU_CB_0624.csv')
    df_0924 = pd.read_csv('ENSU_CB_0924.csv')
    df_1224 = pd.read_csv('ENSU_CB_1224.csv')
    
   
    df_combined = pd.concat([df_0324, df_0624, df_0924, df_1224], ignore_index=True)
    
    # Aqui filtramos por el estado de Nuevo Leon
    return df_combined[df_combined['CVE_ENT'] == 19]

#Aqui es el diccionario de las ubicaciones de la inseguridad
location_dict = {
    'BP1_2_01': 'Su casa',
    'BP1_2_02': 'Su trabajo',
    'BP1_2_03': 'Las calles que habitualmente usa',
    'BP1_2_04': 'La escuela',
    'BP1_2_05': 'El mercado',
    'BP1_2_06': 'El centro comercial',
    'BP1_2_07': 'El banco',
    'BP1_2_08': 'El cajero automático en vía pública',
    'BP1_2_09': 'El transporte público',
    'BP1_2_10': 'El automóvil',
    'BP1_2_11': 'La carretera',
    'BP1_2_12': 'El parque o centro recreativo'
}


#Aqui son las respuestas de la pregunta de la inseguridad
response_dict = {
    1: 'Seguro',
    2: 'Inseguro',
    3: 'No aplica',
    4: 'No sabe'
}

def main():
    st.title("Perspectiva de Inseguridad en Nuevo León")
    
    df = load_data()
    
   
    st.subheader("Dashboard por Género")
    col1, col2, col3 = st.columns(3)
    
    #Aqui definimos los diferentes botones para los generos
    with col1:
        if st.button('Hombre'):
            gender_df = df[df['SEXO'] == 1]
            gender_label = 'Hombres'
    with col2:
        if st.button('Mujer'):
            gender_df = df[df['SEXO'] == 2]
            gender_label = 'Mujeres'
    with col3:
        if st.button('Ambos'):
            gender_df = df
            gender_label = 'Ambos'
    
    if 'gender_df' not in locals():
        gender_df = df
        gender_label = 'Ambos'
    
    # Aqui es donde creeamos tres diferentes columnas para las metricas
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        total_count = len(gender_df)
        st.metric(f"Total de {gender_label}", f"{total_count:,}")
    
    with metric_col2:
        
        insecure_pct = (gender_df['BP1_1'] == 2).mean() * 100
        st.metric("Percepción de Inseguridad", f"{insecure_pct:.1f}%")
    
    with metric_col3:
        # Aqui es la formula para calcular el lugar mas inseguro
        location_insecurity = {}
        for loc in location_dict.keys():
            insecure_pct = (gender_df[loc] == 2).mean() * 100
            location_insecurity[loc] = insecure_pct
        
        most_insecure_loc = max(location_insecurity.items(), key=lambda x: x[1])
        most_insecure_pct = most_insecure_loc[1]  
        st.metric(
            "Lugar Más Inseguro", 
            f"{location_dict[most_insecure_loc[0]]}", 
        )
    # Aqui es para rankear los municipios mas inseguros de NL
    st.subheader("Ranking de Municipios por Inseguridad")
    
    mun_security = (
        gender_df.groupby('NOM_MUN')['BP1_1']
        .apply(lambda x: (x == 2).mean() * 100)
        .reset_index()
    )
    mun_security.columns = ['Municipio', 'Porcentaje de Inseguridad']
    mun_security = mun_security.sort_values('Porcentaje de Inseguridad')
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("Municipios Menos Inseguros")
        most_secure = mun_security.head(1)
        for idx, row in most_secure.iterrows():
            st.write(f"{row['Municipio']}: {row['Porcentaje de Inseguridad']:.1f}%")
    
    with col2:
        st.write("Municipios Más Inseguros")
        most_insecure = mun_security.tail(1)
        for idx, row in most_insecure.iloc[::-1].iterrows():
            st.write(f"{row['Municipio']}: {row['Porcentaje de Inseguridad']:.1f}%")
    
    st.subheader("Percepción de Inseguridad a través del tiempo")
    
    # Aqui lo usamos para calcular la inseguridad por el año
    time_series = (
        gender_df.groupby('PER')['BP1_1']
        .apply(lambda x: (x == 2).mean() * 100)
        .reset_index()
    )
    time_series.columns = ['Periodo', 'Porcentaje de Inseguridad']
    
    fig = px.line(
        time_series,
        x='Periodo',
        y='Porcentaje de Inseguridad',
        title=f'Tendencia de Inseguridad - {gender_label}',
        markers=True
    )
    fig.update_layout(
        xaxis_title="Periodo",
        yaxis_title="Porcentaje de Inseguridad (%)",
        yaxis_range=[0, 100]
    )
    
    st.plotly_chart(fig)

    st.subheader("Análisis de Seguridad por Ubicación")
    selected_location = st.selectbox(
        'Seleccionar Ubicación:',
        options=list(location_dict.keys()),
        format_func=lambda x: location_dict[x]
    )
    
    # Aqui creamos un piechart para poder ver como se manifiesta la inseguridad en cada lugar
    location_data = df[selected_location].value_counts().reset_index()
    location_data.columns = ['Respuesta', 'Cantidad']
    
    location_data['Respuesta'] = location_data['Respuesta'].map(response_dict)
    
    fig = px.pie(
        location_data, 
        values='Cantidad', 
        names='Respuesta',
        title=f'Percepción de Seguridad: {location_dict[selected_location]}'
    )
    st.plotly_chart(fig)
    

if __name__ == "__main__":
    main()