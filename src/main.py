import streamlit as st
import pandas as pd
from processor import generate_report, load_files, create_download_link
import time

st.title("Pending Result Processor v1.0")
st.write("**Automatically generate pending result reports.**")
st.write("Created by Devan, 2 March 2025.")

st.write("---")
st.header("Upload Your Files")
st.write("Upload multiple Excel files containing pending results.")

# File uploader
uploaded_files = st.file_uploader(
    "Choose Excel files", type=["xlsx", "xls"], accept_multiple_files=True
)


# File processing
if uploaded_files:
    st.success("Files uploaded successfully!", icon="📂")

    if st.button("Process Files"):
        with st.spinner("Processing files..."):
            time.sleep(3)  # Simulated processing delay

            # Load and process files
            combined_df = load_files(uploaded_files)
            if combined_df is None:
                st.error("No valid data found. Please check your files.")
            else:
                result = generate_report(combined_df)

                # ---- DOWNLOAD SECTION ----
                st.header("Download the Result")
                download_buffer = create_download_link(result)

                st.success("Your file is ready!", icon="✅")
                st.download_button(
                    label="Click to download",
                    data=download_buffer,
                    file_name="Result.xlsx",
                    mime="application/vnd.ms-excel",
                )
