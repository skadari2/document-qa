import streamlit as st
from openai import OpenAI

st.title("📄 Document question answering")

openai_api_key = st.text_input("OpenAI API Key", type="password")

if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    uploaded_file = st.file_uploader("Upload a document (.txt or .md)", type=("txt", "md"))

    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        document = uploaded_file.read().decode()

        with client.responses.stream(
            model="gpt-4.1-mini",
            input=[
                {
                    "role": "user",
                    "content": f"Here's a document:\n{document}\n\n---\n\n{question}",
                }
            ],
        ) as stream:

            response_text = ""
            response_placeholder = st.empty()

            for event in stream:
                if event.type == "response.output_text.delta":
                    response_text += event.delta
                    response_placeholder.write(response_text)
