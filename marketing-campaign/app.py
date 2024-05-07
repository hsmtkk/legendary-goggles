import streamlit as st
from langchain_openai import OpenAI
from langchain_core.prompts.prompt import PromptTemplate
from langchain_core.example_selectors import LengthBasedExampleSelector
from langchain_core.prompts.few_shot import FewShotPromptTemplate

from enum import Enum


def getLLMResponse(query: str, age_option: str, tasktype_option: str) -> str:
    llm = OpenAI()
    print(f"{age_option=}")
    if age_option == "Kid":
        examples = [
            {
                "query": "What is a mobile?",
                "answer": "A mobile is a magical device that fits in your pocket.",
            },
            {
                "query": "What are your dreams?",
                "answer": "My dreams are like colorful adventures, where I become a superhreo.",
            },
        ]
    elif age_option == "Adult":
        examples = [
            {
                "query": "What is a mobile?",
                "answer": "A mobile is a portable communication device.",
            },
            {
                "query": "What are your dreams?",
                "answer": "In my world of circuits and algorithms, my dreams are fueled by a quest for endless learning.",
            },
        ]
    elif age_option == "Senior Citizen":
        examples = [
            {
                "query": "What is a mobile?",
                "answer": "A mobile, also known as a cellphone or smartphone, is a portable device.",
            },
            {
                "query": "What are your dreams?",
                "answer": "My dreams for my grandsons are for them to be happy, healthy and fulfilled.",
            },
        ]
    print(f"{examples=}")

    example_template = """
    Question: {query}
    Response: {answer}
    """
    example_prompt = PromptTemplate(
        input_variables=["query", "answer"],
        template=example_template,
    )

    prefix = """You are a {template_age_option}, and {template_tasktype_option}:
    Here are some examples:
    """

    suffix = """
    Question: {template_user_input}
    Response: """

    example_selector = LengthBasedExampleSelector(
        examples=examples,
        example_prompt=example_prompt,
        max_length=200,
    )

    new_prompt_template = FewShotPromptTemplate(
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix=suffix,
        input_variables=[
            "template_age_option",
            "template_tasktype_option",
            "template_user_input",
        ],
        example_separator="\n",
    )

    print(
        new_prompt_template.format(
            template_user_input=query,
            template_age_option=age_option,
            template_tasktype_option=tasktype_option,
        )
    )

    response = llm.invoke(
        new_prompt_template.format(
            template_user_input=query,
            template_age_option=age_option,
            template_tasktype_option=tasktype_option,
        )
    )
    print(response)

    return response


st.set_page_config(
    page_title="Marketing Tool",
    page_icon="✅",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.header("Hey, how can I help you?")

form_input = st.text_area("Enter text", height=275)

tasktype_option = st.selectbox(
    "Please select the action to be performed?",
    ["Write a sales copy", "Create a tweet", "Write a product description"],
    key=1,
)

age_option = st.selectbox(
    "For which age group?", ("Kid", "Adult", "Senior Citizen"), key=2
)

numberOfWords = st.slider("Words limit", 1, 200, 25)

submit = st.button("Generate")

if submit:
    st.write(getLLMResponse(form_input, age_option, tasktype_option))
