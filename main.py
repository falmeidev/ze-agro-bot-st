# import library
import streamlit as st

# import method that gets AI answer
from app.api_ai_client import ChatGptApiClient

# Exibe o logo no topo da página
st.image("logo.jpeg", width=100)

# page title
st.write("### Zé Agro")

st.write("Primeiros caracteres da chave:", st.secrets["open_ai_credentials"]["openai_api_key"][:5])

# page subtitle
st.write("##### O assistente do agricultor, com informações oficiais da EMBRAPA.")


# create the session state to list the messages (memory of streamlit)
if not "msg_list" in st.session_state:
    st.session_state["msg_list"] = [] # create a empty list

# chat input
user_msg = st.chat_input("Olá! Escreva sua pergunta aqui.")

# show historical messages
for message in st.session_state["msg_list"]:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).write(content)

# check if there are messages
if user_msg:
    print(user_msg)
    # user (message from user)
    st.chat_message("user").write(user_msg)
    # check msg sent
    msg = {"role":"user", "content": user_msg}
    # add new msg to session state
    st.session_state["msg_list"].append(msg)

    # assistant (message from assistance)
    # request answer
        # Obter resposta da API
    with st.spinner("Zé Agro está buscando as informações..."):
        reply = ChatGptApiClient.zeagro_answer(user_msg)
    st.chat_message("assistant").write(reply)
    # check msg sent
    msg_ai = {"role":"assistant", "content": reply}
    # add new msg to session state
    st.session_state["msg_list"].append(msg_ai)

