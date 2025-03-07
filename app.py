import streamlit as st
import pandas as pd 
import os
from io import BytesIO

# set our app
st.set_page_config(page_title="📀 Data sweeper" , layout= "wide")
st.title("📀 Data sweeper")
st.write("Transform your files betwwen CSV and Excel formats with built-in data cleaning and visualization")
uploaded_files = st.file_uploader ("Uploade your files (CSV or Excel):", type=["csv" , "xlsx"], accept_multiple_files=True)
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df =pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type : {file_ext}")
            continue

        #display info about the file 
        st.write(f"**FILE NAME:** {file.name}")
        st.write(f"**FILE SIZE:** {file.size/1024}")

        #show 5 rows of our data frame
        st.write("🔍Preview the head of the Datafream") 
        st.dataframe(df.head())

        # options for data cleaning 
        st.subheader("🛠 Data cleaning options")
        if st.checkbox(f"Clean data for {file.name}"):
            col1 , col2 = st.columns(2)
            with col1:
                if st.button(f"Removes Dublicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill missing values for {file.name}"):
                    numaric_col =df.select_dtypes(include=['number']).columns
                    df[numaric_col] = df[numaric_col].fillna(df[numaric_col].mean())
                    st.write("Missing values have been filled!")

    # CHOOSE SPECIFIC COLUMNS TO KEEP OR CONVERT
    st.subheader("Select columns to convert") 
    columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
    df = df[columns]

     # Create some visualization 
    st.subheader("📊 Data Visualization")
    if st.checkbox(f"Show Visualization for {file.name}"):
     st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])   

     # Convert the csv file into excel or excel to csv
    st.subheader("Conversion Option")
    conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key= file.name)
    if st.button(f"Convert {file.name}"):
        buffer = BytesIO()
        if conversion_type == "CSV":
            df.to_csv(buffer, index=False)
            file_name = file.name.replace(file_ext, ".csv")
            mime_type = "text/csv"
        elif conversion_type == "Excel":
              df.to_excel(buffer, index=False)
              file_name = file.name.replace(file_ext, ".xlsx")
              mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
              buffer.seek(0)
    
        st.download_button(
           label=f"⬇️ Download {file.name} as {conversion_type}",
            data=buffer,
            file_name = file_name,
            mime=mime_type
        )
    
        st.success("🎉 All File Processed")


      
                
                         
