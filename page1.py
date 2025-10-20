import streamlit as st
from openai import OpenAI

st.title("page1.py")
st.caption("page1")

# 🔑 OpenAI APIキーを設定（環境変数を利用 or 画面で入力）
OPENAI_API_KEY = st.secrets.get("OPENAI_API_KEY", None)
if OPENAI_API_KEY is None:
    OPENAI_API_KEY = st.text_input("OpenAI APIキーを入力してください", type="password")

if OPENAI_API_KEY:
    client = OpenAI(api_key=OPENAI_API_KEY)

    # 💬 チャット履歴をセッションで保持
    if "messages" not in st.session_state:
        st.session_state.messages = []

    st.title("Chat with OpenAI")

    # 過去のメッセージを表示
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # ✍ ユーザー入力
    prompt = st.chat_input("あなた: ")

    if prompt:
        # 履歴にユーザー発話を追加
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # OpenAI API で応答生成
        completion = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.messages
        )

        ai_content = completion.choices[0].message.content
        st.session_state.messages.append({"role": "assistant", "content": ai_content})

        # AI応答の表示
        with st.chat_message("assistant"):
            st.markdown(ai_content)
