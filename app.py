import streamlit as st # type: ignore
import pandas as pd # type: ignore
import os
from io import BytesIO 
import emoji


st.set_page_config(page_title="Data sweeeper", layout='wide')

# Custom CSS for styling
st.markdown("""
    <style>
         body {
            background-color: #ffcc00;
            color: #e0e0e0;
            font-family: 'Poppins', sans-serif;
        }
       </style>
""", unsafe_allow_html=True)

st.title("🌎Data seweeper")
st.write("Transform your fiels between CSV and EXDEL FORMATE with ")

upload_files =st.file_uploader("Uload ur files (CSV or EXCEL):" , type=["CSV","XLSX"],accept_multiple_files=True)
if upload_files:
    for file in upload_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported fiel type:{file_ext}")
            continue

        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

        st.write("Preview the head of the DataFrame")
        st.dataframe(df.head())

        st.subheader(" 💾 Data Cleaning Options")
        if st.checkbox(f"clean Data for {file.name}"):
            coll, col2 =st.columns(2)

            with coll:
                if st.button(f"Remove Dulicate from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed")
            with col2:
                if st.button(f"File Missing Values for {file.name}"):
                    numeric_cols =df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values Have been Filled!")

            # chosse spacific columns to keep or convert 
            st.subheader("📊Select colunms to convert")
            columns = st.multiselect(f"Chose Columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

            # cretae some Visualization
            st.subheader("📈Data Visualization")
            if st.checkbox("show Visualization for {file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

            # convert the file 
            st.subheader("Conversion Options")
            conversion_type =st.radio(f"Convert {file.name} to:",["CSV","EXCEL"], key=file.name)
            if st.button(f"Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer,index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"

                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)

               # Download button
                st.download_button(
                    label=f"Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,  # ✅ Change 'filename' to 'file_name'
                    mime=mime_type
                )
st.success("🤳 All file Procceed")                


