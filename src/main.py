import streamlit as st
import pandas as pd
from processor import generate_report, load_files, create_download_link
import time

st.title("Pending Result Processor v1.0")
st.write("**Automatically generate pending result reports.**")
st.write("Created by Devan, 2 March 2025.")

with st.sidebar:
    st.write("**Instructions:**")
    instructions = [
        "1. Go to [world.wallstreetenglish.com](https://world.wallstreetenglish.com)",
        "2. Login with `62.jak05.pk` account",
        "3. Go to `Menu -> Reports`",
        "4. Select `Pending Result`",
        "5. Select `Class Type = Class Room Activities`",
        "6. Click `Excel File` to download the report",
        "7. Select `Class Type = Others`",
        "8. Click `Excel File` again to download the report",
        "9. Repeat steps 3-8 with account `62.ino01.aa`",
        "10. Upload the downloaded files here"
    ]
    for instruction in instructions:
        st.write(instruction)


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
