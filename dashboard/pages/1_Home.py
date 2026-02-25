import random
import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
st.set_page_config(layout="wide")
if 'proceeding' not in st.session_state:
    st.session_state.proceeding = False

@st.fragment(run_every=4.0) # Automatically reruns this function every 4 second
def app():
  if st.session_state.proceeding:
    progress_text = "Applying additives on mud..."
    my_bar = st.progress(0, text=progress_text)

    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1, text=progress_text)
    time.sleep(1)
    my_bar.empty()
    
    st.success("Additives applied successfully! Returning to Home page...")
    time.sleep(4)
    st.session_state.proceeding = False

  st.title("IDMMS Dashboard")
  st.header("Current Mud Properties")
  data = get_data()
  figures = get_figures(data)
  columns = st.columns(len(data))
  for i in range(len(data)):
    with columns[i]:
      st.write(figures[i])
  
  columns = st.columns(3)
  with columns[1]:
    if st.button(str("\nSee Decision\n"), type="primary", width='stretch', help="See the AI's recommendation based on the current mud properties"):
      st.switch_page("pages/2_Decision.py")
  
def get_data():
  return {
    "density": random.randint(0, 20),
    "pH": random.randint(1, 14),
    "hardness": random.randint(0, 100),
    "rhelogy": random.randint(0, 10),
  }

def get_figures(data):
  density_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["density"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Density (ppg)", 'font': {'size': 32}},
      gauge = {'axis': {'range': [None, 100]},
               'steps' : [{'range': [9, 10], 'color': "lightgreen"}],
               'bar': {'color': "red" if data["density"] < 10 or data["density"] > 90 else "royalblue"},
               }))

  ph_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["pH"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "pH", 'font': {'size': 32}},
      gauge = {'axis': {'range': [None, 14]},
               'steps' : [{'range': [6, 8], 'color': "lightgreen"}],
               'bar': {'color': "red" if data["pH"] < 2 or data["pH"] > 12 else "royalblue"},
               }))

  hardness_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["hardness"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Hardness (mg/L)", 'font': {'size': 32}},
      gauge = {'axis': {'range': [None, 100]},
              'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 80},
               'bar': {'color': "red" if data["hardness"] >= 90 else "royalblue"},
               }))

  rhelogy_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["rhelogy"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Rhelogy (cp)", 'font': {'size': 32}},
      gauge = {'axis': {'range': [None, 10]},
               'steps' : [{'range': [3, 7], 'color': "lightgreen"}],
               'bar': {'color': "red" if data["rhelogy"] < 1 or data["rhelogy"] > 10 else "royalblue"},
               }))
  

  
  return [density_indicator, ph_indicator, hardness_indicator, rhelogy_indicator]


if __name__ == "__main__":
  app()