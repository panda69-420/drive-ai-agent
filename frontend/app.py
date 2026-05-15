import streamlit as st
import requests

st.set_page_config(page_title="Drive AI Agent")

st.title("📁 Drive AI Agent")

st.write("Search your Google Drive files using natural language.")

user_input = st.text_input(
    "Ask something:",
    placeholder="Find PDF reports"
)

if st.button("Search"):

    with st.spinner("Searching Drive..."):

        url = "http://127.0.0.1:8000/chat"

        params = {
            "user_input": user_input
        }

        response = requests.get(url, params=params)

        data = response.json()

        st.subheader("Generated Drive Query")

        st.code(data["generated_query"])

        st.subheader("Results")

        results = data["results"]

        if not results:
            st.warning("No matching files found.")

        else:
            for file in results:

                st.markdown(f"### 📄 {file['name']}")

                st.write(f"**File Type:** {file['mimeType']}")

                file_link = f"https://drive.google.com/file/d/{file['id']}/view"

                st.markdown(
                    f"[Open File]({file_link})"
                )

                st.divider()