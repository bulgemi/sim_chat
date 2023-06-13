from typing import List
import requests
import json

import streamlit as st
from config import get_openai_endpoint, get_header


st.set_page_config(
    page_title="생성형 AI Demo",
    page_icon="images/favicon.ico",
)

st.title("💻 Code Assistant")
st.divider()


def query(context_list) -> List:
    data = {"messages": context_list}
    response = requests.post(get_openai_endpoint(), headers=get_header(), json=data)

    if response.status_code == 200:
        json_resp = json.loads(response.content)
        res_list = json_resp['choices']
        # st.info(f"res_list={res_list}", icon="ℹ️")
    else:
        res_list = [
            {
                'index': 0,
                'finish_reason': 'stop',
                'message': {
                    'role': 'assistant',
                    'content': 'Error.'
                }
            }
        ]
    return res_list


with st.form("code_assistant_input", clear_on_submit=True):
    a, b = st.columns([4, 1])
    user_input = a.text_input(
        label="Your message:",
        placeholder="Send a message.",
        label_visibility="collapsed",
    )
    submitted = b.form_submit_button("Send", use_container_width=True)

if submitted or user_input:
    user = {"role": "user", "content": user_input}
    response = query(context_list=[user])
    # st.info(f"response={response}", icon="ℹ️")
    msg = response[0]['message']
    st.markdown(msg['content'])
