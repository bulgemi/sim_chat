import requests
import json
from typing import List

import streamlit as st
from streamlit_chat import message

from config import (
    get_openai_endpoint,
    get_header,
    get_huggingface_model,
    get_interface
)


st.set_page_config(
    page_title="생성형 AI Demo",
    page_icon="images/favicon.ico",
)

st.title("💬 Chatbot")
st.divider()

interface_info = get_interface()
# st.info(f"interface_info: {interface_info}")

tokenizer = None
model = None


def query_huggingface(user_input: str):
    import torch
    from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast

    global tokenizer
    global model

    if tokenizer is None:
        tokenizer = PreTrainedTokenizerFast.from_pretrained(get_huggingface_model(),
                                                            bos_token='</s>', eos_token='</s>', unk_token='<unk>',
                                                            pad_token='<pad>', mask_token='<mask>')
    if model is None:
        model = GPT2LMHeadModel.from_pretrained(get_huggingface_model())

    input_ids = tokenizer.encode(user_input, return_tensors='pt')
    gen_ids = model.generate(input_ids,
                             max_length=128,
                             repetition_penalty=2.0,
                             pad_token_id=tokenizer.pad_token_id,
                             eos_token_id=tokenizer.eos_token_id,
                             bos_token_id=tokenizer.bos_token_id,
                             use_cache=True)
    msg = tokenizer.decode(gen_ids[0])
    res_list = [
        {
            'index': 0,
            'finish_reason': 'stop',
            'message': {
                'role': 'assistant',
                'content': msg
            }
        }
    ]
    # st.info(f"msg={msg}", icon="ℹ️")
    return res_list


def query_openai(context_list) -> List:
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


container = st.container()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "무엇을 도와드릴까요?"}]

with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])
    user_input = a.text_input(
        label="Your message:",
        placeholder="Send a message.",
        label_visibility="collapsed",
    )
    submitted = b.form_submit_button("Send", use_container_width=True)

if submitted or user_input:
    user = {"role": "user", "content": user_input}
    st.session_state.messages.append(user)
    if interface_info['interface'] == 'azure':
        response = query_openai(context_list=[user])
        # st.info(f"response={response}", icon="ℹ️")
        msg = response[0]['message']
    else:
        response = query_huggingface(user_input)
        msg = response[0]['message']
    st.session_state.messages.append(msg)

with container:
    if st.session_state['messages']:
        for msg in st.session_state['messages']:
            if msg['role'] == 'user':
                message(msg['content'], is_user=True, avatar_style='initials', seed='사용자')
            elif msg['role'] == 'assistant':
                message(msg['content'], avatar_style='bottts-neutral', seed="Aneka")
            else:
                pass
