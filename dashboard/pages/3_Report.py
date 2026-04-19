import streamlit as st
from datetime import datetime as dt

def app():
  st.page_link("pages/2_Decision.py", label="Back to Decision", icon="⬅️")
  st.title("IDMMS Dashboard")
  st.header("Report")
  st.write("Here is the report based on the current mud properties and the AI's recommendations.")
  id = str(dt.now().year) + "-" + "001"
  with st.container(width='stretch', height='content', horizontal_alignment='center', vertical_alignment='center', border=True, horizontal=False):  
    # st.subheader("Mud Properties")
    # st.write("- Property 1: Value")
    # st.write("- Property 2: Value")
    # st.write("- Property 3: Value")
    
    # st.subheader("AI Recommendations")
    # st.write("- Additive A: Amount")
    # st.write("- Additive B: Amount")
    
    # st.subheader("Analysis")
    # st.write("The AI recommends using Additive A and Additive B based on the current mud properties. \nThis will help improve the drilling performance and reduce costs.")
    
    st.subheader(f"Report Reference: {id}")
    st.subheader(f"Generation Timestamp: {dt.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    st.subheader("1. Physical Telemetry Log (Input Data)")
    st.table({
        "Property": ["Fluid Density","Viscosity","pH Level","Conductivity","Pressure"],
        "Unit": ["g/cm³", "cP", "pH", "μS/cm", "psi"],
        "Value": [1.2, 50, 8, 500, 3000],
        "variance":["High","Medium","Low","Medium","High"],
    })
    
    st.subheader("2. AI Diagnostic Results (Analytical Logic)")
    st.text("The automated interpretation of the telemetry variance.\n•	Primary Diagnostic ID: [WARNING_ID_1-7]\n•	Detected Condition: [CONDITION_NAME]\n•	Confidence Score: [XX.X%]\n•	Logical Justification: [TEXT_DESCRIPTION_OF_AI_REASONING]")
    
    st.subheader("3. Control Decision (Output Execution)")
    st.text("•	Selected Additive: [ADDITIVE_NAME]\n•	Source Reservoir: [PORTABLE_CELL_ID]\n•	Required Volume: [VALUE] [UNIT]\n•	Actuator Sequence: [OPEN_VALVE_ID] -> [RUN_PUMP_ID] -> [FLUSH_SEQUENCE]\n•	Calculated Pump Runtime: [VALUE] SECONDS")
  
if __name__ == "__main__":
  app()