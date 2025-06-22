import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from apideck_utils import fetch_file_list, download_file
from llm_utils import summarize_pdf


def main():
    st.set_page_config(page_title="PDF Summarizer", page_icon="📄", layout="centered")

    try:
        header_image = Image.open("header_image.png")
        st.image(header_image, use_container_width=True)
    except FileNotFoundError:
        st.title("PDF Summarizer using Apideck's File Storage API")

    st.markdown(
        "<h3 style='text-align: center; color: #3366ff;'>Select a PDF from your Box account, using Apideck's File Storage API, and get a quick summary powered by a local AI model.</h3>",
        unsafe_allow_html=True,
    )

    load_dotenv()
    api_key = os.getenv("APIDECK_API_KEY")
    app_id = os.getenv("APIDECK_APP_ID")
    consumer_id = os.getenv("APIDECK_CONSUMER_ID")
    model_name = "gemma3:4b-it-qat"

    if not all([api_key, app_id, consumer_id]):
        st.error("Apideck credentials not found. Please check your .env file.")
        return

    if "summaries" not in st.session_state:
        st.session_state.summaries = []

    with st.sidebar:
        st.markdown(
            "## <span style='color:#FF4B4B;'>⚙️ Controls</span>", unsafe_allow_html=True
        )

        with st.spinner("Fetching files..."):
            files = fetch_file_list(api_key, app_id, consumer_id)

        if not files:
            st.warning("No files found in your Box account.")
            return

        file_map = {file.name: file.id for file in files}
        selected_filename = st.selectbox(
            "Choose a PDF file:", options=list(file_map.keys())
        )

        if st.button("Summarize File", type="primary", use_container_width=True):
            if selected_filename:
                with st.spinner(f"Processing '{selected_filename}'..."):
                    selected_file_id = file_map[selected_filename]

                    downloaded_file_path = download_file(
                        file_id=selected_file_id,
                        file_name=selected_filename,
                        api_key=api_key,
                        app_id=app_id,
                        consumer_id=consumer_id,
                    )

                    if downloaded_file_path:
                        summary = summarize_pdf(downloaded_file_path, model_name)
                        # Add new summary to the start of the list
                        st.session_state.summaries.insert(
                            0, {"name": selected_filename, "summary": summary}
                        )
                        os.remove(downloaded_file_path)
                    else:
                        st.error("Failed to download the file.")

    if st.session_state.summaries:
        st.markdown(
            "<h2 style='color: #28a745;'>Generated Summaries</h2>",
            unsafe_allow_html=True,
        )
        for item in st.session_state.summaries:
            with st.container(border=True):
                st.markdown(
                    f"<h4 style='color: #6f42c1;'>Summary for: {item['name']}</h4>",
                    unsafe_allow_html=True,
                )
                st.markdown(item["summary"])


if __name__ == "__main__":
    main()
