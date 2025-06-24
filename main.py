import streamlit as st
import ollama

def get_ollama_response(input_text, no_words, blog_style):
    prompt = (
        f"Generate a high-value technology article on the topic: '{input_text}'. "
        f"The article should be aimed at {blog_style}, and should be within {no_words} words. "
        f"Ensure it's informative, engaging, and easy to understand."
    )

    response = ollama.generate(
        model="llama3.2:1b-instruct-fp16",
        prompt=prompt
    )

    return response['response']

st.set_page_config(
    page_title="Tech Article Generator",
    page_icon='🤖',
    layout='centered',
    initial_sidebar_state='collapsed'
)

st.header("Tech Article Generator")

input_text = st.text_input("Enter the Article Topic")
col1, col2 = st.columns(2)

with col1:
    no_words = st.text_input('Word Count', value="300")

with col2:
    blog_style = st.selectbox(
        'Target Audience',
        ('Executives', 'Engineers', 'Developers', 'Common People'),
        index=0
    )

submit = st.button("Generate")

if submit:
    if not input_text:
        st.warning("Please enter a topic.")
    elif not no_words.isdigit():
        st.warning("Please enter a valid number for word count.")
    else:
        st.info("Generating your article with LLaMA 3.2, please wait...")
        try:
            result = get_ollama_response(input_text, no_words, blog_style)
            st.subheader("Generated Article:")
            st.write(result)
        except Exception as e:
            st.error(f"Failed to generate article: {e}")
