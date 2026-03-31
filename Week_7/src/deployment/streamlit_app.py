import streamlit as st
import os
import sys
from PIL import Image

try:
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
except:
    pass

BASE_DIR  = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
TEMP_DIR  = os.path.join(BASE_DIR, "src", "data", "images")

try:
    from src.deployment.app import ask, ask_image, ask_sql_endpoint
    from src.memory.memory_store import clear_memory
except:
    pass

st.title("RAG Assistant")

mode = st.radio("Mode", ["Text RAG", "Image RAG", "SQL RAG"], horizontal=True)

if mode == "Text RAG":
    question = st.text_area("Question")
    if st.button("Ask"):
        try:
            with st.spinner("Thinking..."):
                result = ask(question)
            answer = result.get("answer", "")
            st.write(answer if answer else "No answer returned.")
            e = result.get("evaluation", {})
            st.caption(f"Faithfulness: {e.get('faithfulness', 0)} | Confidence: {e.get('confidence', 0)} | Hallucination: {e.get('hallucination_risk', 'N/A')}")
        except:
            st.write("Error occurred while processing request.")

elif mode == "Image RAG":
    image_mode = st.radio("Image mode", ["Text → Image", "Image → Image", "Image → Text Answer"])

    if image_mode == "Text → Image":
        query = st.text_input("Describe the image")
        if st.button("Search"):
            if not query.strip():
                st.warning("Please enter a description to search.")
            else:
                try:
                    with st.spinner("Searching..."):
                        result = ask_image(query=query, mode="text")
                    st.write(result["answer"])
                    for item in result.get("context_used", []):
                        try:
                            if os.path.exists(item["source"]):
                                st.image(Image.open(item["source"]), width=400)
                            st.caption(f"Score: {item['score']}")
                        except:
                            pass
                    if not result.get("context_used"):
                        st.info("No similar images found above the similarity threshold")
                except:
                    st.write("Error occurred during image search.")

    elif image_mode == "Image → Image":
        upload = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
        if st.button("Search") and upload:
            try:
                temp = os.path.join(TEMP_DIR, f"temp_{upload.name}")
                with open(temp, "wb") as f:
                    f.write(upload.getbuffer())
                with st.spinner("Searching..."):
                    result = ask_image(image_path=temp, mode="image")
                os.remove(temp)
                st.write(result["answer"])
                for item in result.get("context_used", []):
                    try:
                        if os.path.exists(item["source"]):
                            st.image(Image.open(item["source"]), width=400)
                        st.caption(f"Score: {item['score']}")
                    except:
                        pass
            except:
                st.write("Error occurred during image search.")

    else:
        upload = st.file_uploader("Upload image", type=["jpg", "jpeg", "png"])
        if st.button("Get Answer") and upload:
            try:
                temp = os.path.join(TEMP_DIR, f"temp_{upload.name}")
                with open(temp, "wb") as f:
                    f.write(upload.getbuffer())
                with st.spinner("Extracting text from image..."):
                    result = ask_image(
                        query="Extract and describe all text and content visible in this image",
                        image_path=temp,
                        mode="image"
                    )
                os.remove(temp)
                st.write(result["answer"])
            except:
                st.write("Error occurred while processing image.")

else:
    question = st.text_area("Ask about the database")
    if st.button("Run"):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Running SQL..."):
                    result = ask_sql_endpoint(question)

                if result.get("error"):
                    st.error(f"Blocked: {result['error']}")
                else:
                    st.write(result.get("answer", ""))
                    if result.get("sql"):
                        st.code(result["sql"], language="sql")
                    if result.get("rows") and result.get("columns"):
                        st.dataframe([dict(zip(result["columns"], row)) for row in result["rows"][:20]])
            except:
                st.write("Error occurred while running SQL.")