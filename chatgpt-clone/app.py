import streamlit as st
from streamlit_chat import message
from langchain_openai import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationSummaryMemory

if "conversation" not in st.session_state:
    st.session_state["conversation"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "API_KEY" not in st.session_state:
    st.session_state["API_KEY"] = ""

st.set_page_config(page_title="Chat GPT Clone", page_icon=":robot_face:")
st.markdown(
    "<h1 style='text-align: center;'>How can I assist you? </h1>",
    unsafe_allow_html=True,
)

st.sidebar.title("😎")
st.session_state["API_KEY"] = st.sidebar.text_input(
    "Enter your OpenAI API key", type="password"
)
summarise_button = st.sidebar.button("Summarize the conversation", key="summaries")
if summarise_button:
    summarise_placeholder = st.sidebar.write(
        "Nice chatting with you my friend ❤:\n\n"
        + st.session_state["conversation"].memory.buffer
    )


def get_response(user_input: str, api_key: str) -> str:
    if st.session_state["conversation"] is None:
        llm = OpenAI(temperature=0, openai_api_key=api_key)
        st.session_state["conversation"] = ConversationChain(
            llm=llm,
            verbose=True,
            memory=ConversationSummaryMemory(llm=llm),
        )
    response = st.session_state["conversation"].predict(input=user_input)
    print(st.session_state["conversation"].memory.buffer)
    return response


response_container = st.container()
container = st.container()

with container:
    with st.form(key="my_form", clear_on_submit=True):
        user_input = st.text_area("Your question goes here:", key="input", height=100)
        submit_button = st.form_submit_button(label="Send")
        if submit_button:
            st.session_state["messages"].append(user_input)
            model_response = get_response(user_input, st.session_state["API_KEY"])
            st.session_state["messages"].append(model_response)

            with response_container:
                for i in range(len(st.session_state["messages"])):
                    if i % 2 == 0:
                        message(
                            st.session_state["messages"][i],
                            is_user=True,
                            key=str(i) + "_user",
                        )
                    else:
                        message(st.session_state["messages"][i], key=str(i) + "_AI")
