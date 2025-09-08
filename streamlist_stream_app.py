
import streamlit as st
from openai import OpenAI
import openai
import os

# API 클라이언트 초기화
if "client" not in st.session_state:
    api_key = os.getenv('OPENAI_API_KEY')
    openai.api_key = api_key
    st.session_state['client'] = OpenAI()

# 스트리밍 GPT 함수
def GPT_stream(prompt):
    full_response = ""
    response_stream = st.session_state['client'].chat.completions.create(
        model='gpt-4o-mini',
        messages=[{'role': 'user', 'content': prompt}],
        stream=True  # 스트리밍 활성화
    )

    for chunk in response_stream:
        if chunk.choices[0].delta.content:
            full_response += chunk.choices[0].delta.content
            yield chunk.choices[0].delta.content  # 실시간으로 한 줄씩 반환

# UI 구성
st.title('🤖 GPT 챗봇 (실시간)')
st.markdown('---')

# 입력 폼
prompt = st.text_input('👩‍🦰 프롬프트', placeholder="입력 후 Enter")

if prompt:
    st.markdown("#### 🤖 GPT 답변:")
    response_placeholder = st.empty()
    full_text = ""

    # 스트리밍 출력
    for chunk in GPT_stream(prompt):
        full_text += chunk
        response_placeholder.markdown(full_text)
