import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import time

from sensors import SensorCVD, SensorConfig
from database import DataBase

st.set_page_config(
    page_title = "Monitor Lab Electronica",
    layout = 'wide',
    initial_sidebar_state="expanded"
)

SENSORES_CONFIG = {
    'particulas': SensorConfig(
        nombre="Sensor de Particulas PM2.5",
        unidad="ug/m^3",
        rango=(0, 100),
        color="chartreuse",
        alertas={'advertencia': 35, 'critico': 75}
    ),
    'temperatura': SensorConfig(
        nombre="Temperatura Ambiental",
        unidad="°C",
        rango=(15, 35),
        color= "cyan",
        alertas={'advertencia': 28, 'critico': 32}
    ),
    'humedad': SensorConfig(
        nombre="Humedad Relativa",
        unidad="%",
        rango=(30, 70),
        color= "violet",
        alertas={'advertencia': 65, 'critico': 70}
    ),
        'cov': SensorConfig(
        nombre="Nivel COV",
        unidad="ppb",
        rango=(0, 1000),
        color = "burlywood",
        alertas={'advertencia': 500, 'critico': 800}
    )
}

class MonitorLabElect:
    def __init__(self):
        self.db = DataBase('data/sensor_data_5.db')
        self.sensores = {
            nombre: SensorCVD(config)
            for nombre, config in SENSORES_CONFIG.items()
        }
        
    def ejecutar(self):
        st.title("Sistema de Monitoreo Ambiental")
        st.subheader("Laboratorio Electronica")
        with st.sidebar:
            intervalo = st.slider("Intervalo de actualización (s)", 1, 10, 2)
            
            modo_demo = st.checkbox("Modo Demo", True)
            st.divider()
            st.markdown("""
                        ### Información del porceso
                        Este sistema monitorea la calidad del aire, humedad y elementos ambientales de un Laboratorio de Electrónica
                        """)
        
        col1, col2, col3, col4= st.columns(4)
        graficas = st.container()
        
        contenedores = {
            'particulas': col1.empty(),
            'temperatura': col2.empty(),
            'humedad': col3.empty(),
            'cov': col4.empty()

        }
        
        while modo_demo:
            for nombre, sensor in self.sensores.items():
                # Lectura del sensor
                valor = sensor.leer()
                estado = sensor.verificar_alarma(valor)
                
                # Guardar en base de datos
                if nombre == 'particulas':
                    self.db.guardar_lectura_air(nombre, valor, estado)
                elif nombre == 'temperatura':
                    self.db.guardar_lectura_temp(nombre,valor,estado)
                elif nombre == 'humedad':
                    self.db.guardar_lectura_hum(nombre,valor,estado)
                elif nombre == 'cov':
                    self.db.guardar_lectura_voc(nombre,valor,estado)
                else:
                    print("Error guardado")
                
                # Actualizar visualización
                contenedor = contenedores[nombre]
                config = SENSORES_CONFIG[nombre]
                
                contenedor.metric(
                    label=config.nombre,
                    value=f"{valor} {config.unidad}",
                    delta=f"{valor - sensor.valor_base:.1f}",
                    delta_color="inverse" if estado != 'normal' else "normal"
                )
            
            # Actualizar gráficas
            with graficas:
                self.actualizar_graficas()
            
                time.sleep(intervalo)

    def actualizar_graficas(self):
        # Verificar si existe la gráfica en session_state
        if 'fig' not in st.session_state:
            fig = go.Figure()
            fig.update_layout(
                title="Monitoreo en Tiempo Real",
                height=400,
                margin=dict(l=0, r=0, t=30, b=0)
            )
            st.session_state.fig = fig
            st.session_state.placeholder = st.empty()  # Placeholder para actualizar sin duplicar
        else:
            fig = st.session_state.fig
            fig.data = []  # Limpiar trazas previas para evitar duplicados

        # Agregar los datos actualizados de cada sensor
        for nombre, sensor in self.sensores.items():
            datos = self.db.obtener_historico(nombre, 100)
            config = SENSORES_CONFIG[nombre]

            fig.add_trace(go.Scatter(
                x=datos['timestamp'],
                y=datos['VALOR'],
                name=config.nombre,
                line=dict(color=config.color)
            ))

        # Mostrar la gráfica sin duplicar el contenedor
        st.session_state.placeholder.plotly_chart(fig, use_container_width=True)



if __name__ == "__main__":
    monitor = MonitorLabElect()
    monitor.ejecutar()

        
        