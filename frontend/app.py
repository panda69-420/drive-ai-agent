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

        #url = "https://drive-ai-agent-backend-5ghb.onrender.com/chat"
        url = "http://127.0.0.1:8000/chat"
        params = {
            "user_input": user_input
        }

    response = requests.get(url, params=params)

    st.write("Status Code:", response.status_code)

    st.write("Raw Response:")
    st.text(response.text)

    try:
        data = response.json()

        st.subheader("Generated Drive Query")
        st.code(data["generated_query"])

        st.subheader("Results")

        results = data["results"]

        if not results:
            st.info(
                f"No files matched:\n\n{data['generated_query']}"
            )

        else:
            for file in results:

                st.markdown(f"### 📄 {file['name']}")

                st.write(f"**File Type:** {file['mimeType']}")

                file_link = f"https://drive.google.com/file/d/{file['id']}/view"

                st.markdown(f"[Open File]({file_link})")

                st.divider()

    except Exception as e:
        st.error(f"JSON Error: {e}")