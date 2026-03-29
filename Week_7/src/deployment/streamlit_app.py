import streamlit as st
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.deployment.app import ask, ask_image, ask_sql_endpoint
from src.memory.memory_store import get_memory, clear_memory

st.set_page_config(
    page_title="Enterprise Knowledge Assistant",
    page_icon="🤖",
    layout="wide"
)

st.title("Enterprise Knowledge Intelligence System")
st.caption("Day 1–5 | Text RAG + Image RAG + SQL QA | Powered by Groq")

# sidebar — memory
with st.sidebar:
    st.header("Conversation Memory")
    memory = get_memory()
    if memory:
        for m in memory:
            role  = "You" if m["role"] == "user" else "Assistant"
            st.text(f"{role}: {m['content'][:60]}...")
    else:
        st.text("No memory yet.")
    if st.button("Clear Memory"):
        clear_memory()
        st.success("Memory cleared!")
        st.rerun()

# three tabs
tab1, tab2, tab3 = st.tabs(["Ask Documents", "Ask Images", "Ask Database"])

# tab 1 — document QA
with tab1:
    st.subheader("Ask your documents")
    question = st.text_input("Enter your question", placeholder="What are Crombie's pension benefits?", key="doc_q")
    if st.button("Ask", key="doc_btn"):
        if question:
            with st.spinner("Searching documents and generating answer..."):
                result = ask(question)
            st.markdown("### Answer")
            st.write(result["answer"])

            col1, col2 = st.columns(2)
            with col1:
                score = result["faithfulness"]
                color = "green" if score >= 0.8 else "orange" if score >= 0.5 else "red"
                st.metric("Faithfulness score", f"{score}")
            with col2:
                risk = result["hallucination_risk"]
                st.metric("Hallucination risk", risk.upper())

            st.markdown("### Sources")
            for s in result["sources"]:
                st.text(f"- {s['source'].split('/')[-1]} p.{s['page']} (score: {s['score']})")
        else:
            st.warning("Please enter a question.")

# tab 2 — image QA
with tab2:
    st.subheader("Ask your images")
    query = st.text_input("Describe what you're looking for", placeholder="correlation matrix heatmap", key="img_q")
    if st.button("Search Images", key="img_btn"):
        if query:
            with st.spinner("Searching images..."):
                result = ask_image(query)
            st.markdown("### Answer")
            st.write(result["answer"])
            st.markdown("### Images found")
            for img in result["images"]:
                st.text(f"- {img['filename']} (score: {img['score']})")
                st.caption(f"Caption: {img['caption']}")
        else:
            st.warning("Please enter a search query.")

# tab 3 — SQL QA
with tab3:
    st.subheader("Ask your database")
    sql_question = st.text_input("Ask a question about the data", placeholder="How many customers are there?", key="sql_q")
    if st.button("Run Query", key="sql_btn"):
        if sql_question:
            with st.spinner("Generating and running SQL..."):
                result = ask_sql_endpoint(sql_question)
            if result.get("error"):
                st.error(f"Error: {result['error']}")
            else:
                st.markdown("### Answer")
                st.write(result.get("answer", ""))
                st.markdown("### Generated SQL")
                st.code(result.get("sql", ""), language="sql")
                if result.get("rows"):
                    st.markdown("### Raw Results")
                    st.dataframe(
                        [dict(zip(result["columns"], row)) for row in result["rows"][:20]]
                    )
        else:
            st.warning("Please enter a question.")