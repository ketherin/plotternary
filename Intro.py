import streamlit as st


st.set_page_config(layout="wide", page_title='Plotternary')

#Adding a Title

st.sidebar.image("light_logo.png",  use_container_width=True)


st.text("")
st.text("")
st.text("")

video_data='https://www.youtube.com/watch?v=fxPOP65b_kE'

_, container2, _ = st.columns([35, 70, 35])
container2.video(data=video_data)
