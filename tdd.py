import os
import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate

llm = ChatOllama(
    model="mistral",
    base_url="http://localhost:11434",
    temperature=0.1,
    streaming=True,
    max_tokens=1000  
)

st.set_page_config(page_title="Technical Design Document Generator", page_icon="📄", layout="wide")
st.title("📄 Technical Design Document Generator")

project_name = st.text_input("Enter the Project/Feature Name:", placeholder="e.g., Payment Gateway Integration")
tech_stack = st.text_input("Enter the Technology Stack:", placeholder="e.g., React, Node.js, PostgreSQL, AWS")

if st.button("Generate Design Document"):
    if not project_name:
        st.warning("Please enter a project or feature name.")
    elif not tech_stack:
        st.warning("Please enter the technology stack.")
    else:
        progress_bar = st.progress(0)
        
        # ---------------- Research Agent ----------------
        research_prompt = ChatPromptTemplate.from_template("""
You are a Senior Systems Analyst.

Perform an in-depth analysis and gather requirements for the technical design of the project: {project}.

The technology stack to be used includes: {tech_stack}.

Include:
1. Overview and purpose of the system/feature
2. Key components and architecture
3. Technologies and tools to be used (considering the given tech stack)
4. APIs and integrations
5. Data flow and storage considerations
6. Security and compliance aspects
7. Scalability and performance considerations
8. Potential challenges and mitigation strategies

Provide detailed insights and examples.
""")

        research_chain = research_prompt | llm
        research_result = research_chain.invoke({"project": project_name, "tech_stack": tech_stack})
        progress_bar.progress(50)

        # ---------------- Writer Agent ----------------
        writer_prompt = ChatPromptTemplate.from_template("""
You are a seasoned Technical Writer.

Using the following analysis on the project: {project}:
{research}

Write a comprehensive Technical Design Document that includes:
1. Introduction and project overview
2. System architecture diagram description
3. Detailed component design
4. Technology stack explanation (include the provided tech stack: {tech_stack})
5. Integration details
6. Data management strategies
7. Security considerations
8. Performance and scalability plans
9. Conclusion and future outlook

Format the document clearly with sections and bullet points suitable for engineering teams.
Output well-structured markdown content.
""")

        writer_chain = writer_prompt | llm
        final_doc = writer_chain.invoke({
            "project": project_name,
            "research": research_result.content,
            "tech_stack": tech_stack
        })
        progress_bar.progress(100)

        st.subheader("Generated Technical Design Document:")
        st.markdown(final_doc.content, unsafe_allow_html=True)

        st.download_button(
            label="Download Design Document",
            data=final_doc.content,
            file_name=f"{project_name.replace(' ', '_').lower()}_design_doc.txt",
            mime="text/plain"
        )
