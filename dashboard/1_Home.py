import json
import random
import time
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import serial
from pyparsing import line
URL = 'socket://localhost:4000'

# Connect to port to receive data
if 'ser' not in st.session_state:
    st.session_state.ser = None
    
try:
  st.session_state.ser = serial.serial_for_url(URL, timeout=1)
    
except Exception as e:
  print(f"Connection failed: {e}")

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
  
  if st.session_state.ser is None:
    try:
      st.session_state.ser = serial.serial_for_url(URL, timeout=1)
    
    except Exception as e:
      print(f"Connection failed: {e}")
    

  st.title("IDMMS Dashboard")
  st.header("Current Mud Properties")
  data = get_data()
  figures = get_figures(data)
  data_area = st.empty()
  if figures:
    data_area = st.columns(len(figures))
    for i in range(len(figures)):
      with data_area[i]:
        st.write(figures[i])
    
    columns = st.columns(3)
    with columns[1]:
      if st.button(str("\nSee Decision\n"), type="primary", width='stretch', help="See the AI's recommendation based on the current mud properties"):
        st.session_state.update({"timer_active": True})
        st.switch_page("pages/2_Decision.py")
  else:
    data_area.info("Waiting for data from the Virtual Arduino...")
  
def get_data():
    try:
      line = st.session_state.ser.readline().decode('utf-8').strip() 
      if line:
        data = json.loads(line)
        return data
    except Exception as e:
      print(f"Error reading from serial: {e}")
      st.info("Connecting to Virtual Arduino...")
            

def get_figures(data):
  if not data:
    print("get_figures: No data received yet.")
    return None

  density_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["density"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Density (ppg)", 'font': {'size': 32}},
      gauge = {'axis': {'range': [None, 20]},
              'steps' : [{'range': [9, 10], 'color': "lightgreen"}],
              'bar': {'color': "red" if data["density"] < 10 or data["density"] > 90 else "royalblue"},
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

  rhelogy_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["rhelogy"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Rhelogy (cp)", 'font': {'size': 32}},
      gauge = {'axis': {'range': [None, 20]},
              'steps' : [{'range': [3, 7], 'color': "lightgreen"}],
              'bar': {'color': "red" if data["rhelogy"] < 1 or data["rhelogy"] > 17 else "royalblue"},
              }))

  print("get_figures: Data received and figures created.")
  return [density_indicator, ph_indicator, hardness_indicator, rhelogy_indicator]


if __name__ == "__main__":
  app()