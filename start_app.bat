@echo off
cd /d C:\Users\ludov\streamlit_data_toolkit
call venv\Scripts\activate
streamlit run app.py --server.maxUploadSize=5000