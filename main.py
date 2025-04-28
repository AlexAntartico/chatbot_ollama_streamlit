import ollama
import streamlit as st


# Title
st.title("Your Local LLL")

# Chat init
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Load available models
response = ollama.list()
models_list = response['models']
model_names = [m.model for m in models_list]
# print(model_names)

# Show model menu
st.session_state["model"] = st.selectbox("Select a model", model_names)

# chat func
def model_response():
    stream = ollama.chat(
        model = st.session_state["model"],
        messages = st.session_state["messages"],
        stream = True
    )
    for chunk in stream:
        yield chunk['message']['content']

# show msg history
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("What question you have for me?"):
    st.session_state["messages"].append({"role": "user", "content": prompt})
    # add to markdown
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        # add response
        message = st.write_stream(model_response())
        # add to history
        st.session_state["messages"].append({"role": "assistant", "content": message})  

        