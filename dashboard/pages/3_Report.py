import streamlit as st

def app():
  st.page_link("pages/2_Decision.py", label="Back to Decision", icon="⬅️")
  st.title("IDMMS Dashboard")
  st.header("Report")
  st.write("Here is the report based on the current mud properties and the AI's recommendations.")
  with st.container(width='stretch', height='content', horizontal_alignment='center', vertical_alignment='center', border=True, horizontal=False):  
    st.subheader("Mud Properties")
    st.write("- Property 1: Value")
    st.write("- Property 2: Value")
    st.write("- Property 3: Value")
    
    st.subheader("AI Recommendations")
    st.write("- Additive A: Amount")
    st.write("- Additive B: Amount")
    
    st.subheader("Analysis")
    st.write("The AI recommends using Additive A and Additive B based on the current mud properties. This will help improve the drilling performance and reduce costs.")
  
if __name__ == "__main__":
  app()