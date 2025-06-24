import os
import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate

# Initialize Ollama model
llm = ChatOllama(
    model="mistral",
    base_url="http://localhost:11434",
    temperature=0.1,
    streaming=True,
    max_tokens=1000  
)

# Streamlit UI
st.set_page_config(page_title="Simple Article Generator", page_icon="📝", layout="wide")
st.title("📝 AI Article Generator")

topic = st.text_input("Enter a topic:", placeholder="e.g., Quantum Computing, AI, Web3")

if st.button("Generate Article"):
    if not topic:
        st.warning("Please enter a topic.")
    else:
        progress_bar = st.progress(0)
        
        # ---------------- Research Agent ----------------
        researcher_prompt = ChatPromptTemplate.from_template("""
You are a Senior Research Analyst.

Perform an in-depth analysis of {topic}:
1. Overview of current landscape
2. Key players and innovations
3. Market impact and emerging opportunities
4. Technical challenges and solutions
5. Future predictions

Include examples, statistics, and insights.
""")

        researcher_chain = researcher_prompt | llm
        research_result = researcher_chain.invoke({"topic": topic})
        progress_bar.progress(50)

        # ---------------- Writer Agent ----------------
        writer_prompt = ChatPromptTemplate.from_template("""
You are an award-winning technology journalist.

Using the following research on {topic}:
{research}

Write an engaging article that:
1. Starts with attention-grabbing intro
2. Simplifies complex ideas with analogies
3. Gives real-world examples
4. Explores implications for industries
5. Ends with future outlook

Output well-formatted markdown article (12-14 paragraphs).
""")

        writer_chain = writer_prompt | llm
        final_article = writer_chain.invoke({"topic": topic, "research": research_result.content})
        progress_bar.progress(100)

        st.subheader("Generated Article:")
        st.markdown(final_article.content, unsafe_allow_html=True)

        st.download_button(
            label="Download Article",
            data=final_article.content,
            file_name=f"{topic.replace(' ', '_').lower()}_article.md",
            mime="text/markdown"
        )
