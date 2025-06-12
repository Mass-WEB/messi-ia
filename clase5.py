 
import streamlit as st
from groq import Groq
# importacion de libreria streamplit
st.set_page_config(page_title="Mi chat de IA", page_icon="🤦♂️")
# configuracion inicial de titulo de pestaña y de la pagina web
MODELOS = ['llama3-8b-8192' , 'llama3-70b-8192' , 'mixtral-8x7b-32768']
# lista donde se almacenaran los modelos de IA

def crear_usuario_groq():
    clave_secreta = st.secrets["CLAVE_API"]
    return Groq(api_key=clave_secreta)

def configurar_pagina():
    
    st.title("Mi Primer Chat de IA")
    st.sidebar.title("Configuracion de la IA")
    elegirModelo = st.sidebar.selectbox('Elegir un Modelo', options=MODELOS)
    return elegirModelo

# configuracion del sidbar para elegir el LLM


def configurar_modelo(cliente, modelo, mensajeDeEntrada):
    return cliente.chat.completions.create(
        model=modelo,
        messages=[{"role":"user", "content":mensajeDeEntrada}],
        stream = True
    )

def inicializar_estado():
    if "mensajes" not in st.session_state:
        st.session_state["mensajes"] = [] 



def mostrar_historial():
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["role"], avatar=mensaje["avatar"]):
            st.markdown(mensaje["content"])

def area_chat():
    contenedorDelChat = st.container(height=400, border=True)
    with contenedorDelChat:
        mostrar_historial()

def actualizar_historial(rol, contenido, avatar):
    st.session_state.mensajes.append({"role": rol, "content": contenido, "avatar": avatar})


def generar_respuesta(chat_completo):
    respuesta_completa = ""
    for frase in chat_completo:
       if frase.choices[0].delta.content:
           respuesta_completa += frase.choices[0].delta.content
           yield frase.choices[0].delta.content
    return respuesta_completa 



def main():
    modelo = configurar_pagina()
    cliente = crear_usuario_groq()
    inicializar_estado()
    mensajeDeEntrada = st.chat_input('Escribi tu mensaje')

    area_chat()
    if mensajeDeEntrada:
        actualizar_historial("user", mensajeDeEntrada, "🙌")
        chat_completo = configurar_modelo(cliente, modelo, mensajeDeEntrada)

        if chat_completo:
            with st.chat_message("assistant"):
                respuesta_completa = st.write_stream(generar_respuesta(chat_completo))
                actualizar_historial("assistant", respuesta_completa, "🤖")
                st.rerun()

if __name__ == "__main__":
    main()   