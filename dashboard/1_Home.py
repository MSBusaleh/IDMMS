import json
import random
import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import serial
from pyparsing import line

st.set_page_config(layout="wide")
if 'mode' not in st.session_state:
    st.session_state.mode = "monitoring" # Default state


@st.fragment(run_every=4.0) # Automatically reruns this function every 1 second
def app():
  if st.session_state.mode == "monitoring":
    render_monitoring()
  elif st.session_state.mode == "loading":
    render_loading()
    
def render_monitoring():
  st.title("IDMMS Dashboard")
  st.header("Current Mud Properties")
  status = st.empty()
  data_area = st.columns(5)
  
  
  try:
    with open("../data.json", "r") as f:
      data = json.load(f)
      
    figures = get_figures(data)
    for i in range(len(figures)):
      data_area[i].plotly_chart(figures[i], width="stretch")
      
    button_area = st.columns(3)
    if button_area[1].button(
      str("\nSee Decision\n"), 
      type="primary", 
      width='stretch', 
      help="See the AI's recommendation based on the current mud properties"
      ):
        st.switch_page("pages/2_Decision.py")
    
    seconds_since_update = time.time() - data["received_at"]
    
    with status.container():
      if seconds_since_update > 8:
        st.warning(f'Data is {seconds_since_update:.0f} seconds old.')
        
    time.sleep(0.1)
          
  
  except Exception as e:
    print(f"Error occurred: {e}")
    with status.container():
      st.info("Waiting for data...")
  
def render_loading():
  st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

  # Hide the sidebar entirely on this page so the user can't navigate away
  st.markdown("""
      <style>
          [data-testid="stSidebar"] {display: none;}
      </style>
  """, unsafe_allow_html=True)

  st.title("Waiting for mud to be stabilized...")
  progress_text = "Applying additives and stabilizing mud properties..."
  my_bar = st.progress(0, text=progress_text)

  # Simulate the mixing process
  for percent_complete in range(100):
      time.sleep(0.04) 
      my_bar.progress(percent_complete + 1, text=progress_text)

  st.success("Additives applied successfully! Syncing sensors...")
  time.sleep(1.5)

  # After finishing, send them back home
  st.session_state.mode = "monitoring"

def get_figures(data):
  if not data:
    data = {"ph": 0, "density": 0, "hardness": 0, "pressure": 0, "rheology": 0}
  
  pressure_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["pressure"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Pressure (psi)", 'font': {'size': 32}},
      gauge = {'axis': {'range': [50, 150]},
              'steps' : [{'range': [20, 80], 'color': "lightgreen"}],
              'bar': {'color': "red" if data["pressure"] < 10 or data["pressure"] > 120 else "royalblue"},
              }))
  
  density_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["density"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Density (ppg)", 'font': {'size': 32}},
      gauge = {'axis': {'range': [None, 50]},
              'steps' : [{'range': [9, 10], 'color': "lightgreen"}],
              'bar': {'color': "red" if data["density"] < 3 or data["density"] > 40 else "royalblue"},
              }))

  ph_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["ph"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "pH", 'font': {'size': 32}},
      gauge = {'axis': {'range': [None, 14]},
              'steps' : [{'range': [6, 8], 'color': "lightgreen"}],
              'bar': {'color': "red" if data["ph"] < 2 or data["ph"] > 12 else "royalblue"},
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

  rheology_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["rheology"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "rheology (cp)", 'font': {'size': 32}},
      gauge = {'axis': {'range': [None, 20]},
              'steps' : [{'range': [3, 7], 'color': "lightgreen"}],
              'bar': {'color': "red" if data["rheology"] < 1 or data["rheology"] > 17 else "royalblue"},
              }))
  return [ pressure_indicator, density_indicator, ph_indicator, hardness_indicator, rheology_indicator]

def update_figures(figures, data):
  figures[0].data[0].value = data["pressure"]
  figures[1].data[0].value = data["density"]
  figures[2].data[0].value = data["ph"]
  figures[3].data[0].value = data["hardness"]
  figures[4].data[0].value = data["rheology"]


if __name__ == "__main__":
  app()