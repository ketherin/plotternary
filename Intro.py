import streamlit as st
from streamlit_theme import st_theme

st.set_page_config(layout="wide", page_title="Plotternary")

theme = st_theme()

_, container1, _ = st.columns([35, 70, 35])

#Adding a Title
if theme['backgroundColor'] == '#0e1117':
  st.sidebar.image("sidebar_light.png",  use_container_width=True)
  container1.image("light_logo.png")
else:
  st.sidebar.image("sidebar_dark.png",  use_container_width=True)
  container1.image("dark_logo.png")

st.text(theme)
st.text("")
st.text("")

video_data='https://www.youtube.com/watch?v=fxPOP65b_kE'

_, container2, _ = st.columns([35, 70, 35])
container2.video(data=video_data)
