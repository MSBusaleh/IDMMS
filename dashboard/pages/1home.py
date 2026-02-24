import streamlit as st
import pandas as pd
import plotly.graph_objects as go
st.set_page_config(layout="wide")

def app():
  st.title("IDMMS Dashboard")
  st.header("Current Mud Properties")
  data = get_data()
  figures = get_figures(data)
  columns = st.columns(5)
  for i in range(5):
    with columns[i]:
      st.write(figures[i])
  
  columns = st.columns(3)
  with columns[1]:
    st.button(str("\nSee Decision\n"), type="primary", width='stretch')
  
  
def get_data():
  # Placeholder for data retrieval logic
  return {
    "pressure": 75,
    "pH": 10,
    "hardness": 91,
    "flowrate": 5,
    "viscosity": 20
  }

def get_figures(data):
  pressure_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["pressure"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Pressure", 'font': {'size': 32, 'color': "black"}},
      gauge = {'axis': {'range': [None, 100]},
               'steps' : [{'range': [6, 8], 'color': "lightgreen"}],
               'bar': {'color': "red" if data["pressure"] < 10 or data["pressure"] > 90 else "royalblue"},
               }))

  ph_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["pH"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "pH", 'font': {'size': 32, 'color': "black"}},
      gauge = {'axis': {'range': [None, 14]},
               'steps' : [{'range': [6, 8], 'color': "lightgreen"}],
               'bar': {'color': "red" if data["pH"] < 2 or data["pH"] > 12 else "royalblue"},
               }))

  hardness_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["hardness"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "hardness", 'font': {'size': 32, 'color': "black"}},
      gauge = {'axis': {'range': [None, 100]},
               'steps' : [{'range': [15, 30], 'color': "lightgreen"}],
               'bar': {'color': "red" if data["hardness"] >= 90 else "royalblue"},
               }))

  flowrate_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["flowrate"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Flow Rate", 'font': {'size': 32, 'color': "black"}},
      gauge = {'axis': {'range': [None, 50]},
               'steps' : [{'range': [6, 8], 'color': "lightgreen"}],
               'bar': {'color': "red" if data["flowrate"] >= 45 else "royalblue"},
               }))

  viscosity_indicator = go.Figure(go.Indicator(
      mode = "gauge+number",
      value = data["viscosity"],
      domain = {'x': [0, 1], 'y': [0, 1]},
      title = {'text': "Viscosity", 'font': {'size': 32, 'color': "black"}},
      gauge = {'axis': {'range': [None, 100]},
             'steps' : [{'range': [6, 8], 'color': "lightgreen"}],
             'bar': {'color': "red" if data["viscosity"] >= 80 else "royalblue"},
             }))
  
  return [pressure_indicator, ph_indicator, hardness_indicator, flowrate_indicator, viscosity_indicator]


if __name__ == "__main__":
  app()