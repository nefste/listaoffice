# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 17:41:56 2024

@author: StephanNef
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import hmac
from streamlit_lottie import st_lottie
import numpy as np
import plotly.graph_objects as go

import plotly.graph_objects as go
import streamlit as st

import time


st.set_page_config(
     page_title="Case Study HSG - Lista Office",
     page_icon="https://media.licdn.com/dms/image/C4D0BAQHOoqgag237Aw/company-logo_200_200/0/1630565218537/lista_office_lo_logo?e=2147483647&v=beta&t=d6Cc2A0AK_W7Ot0IgSsGJPw5Vwer6tfxeVmJJScvMx8",
     layout="wide",
)

##############################################################################
####### HEADERS -- User input ################################################


def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if hmac.compare_digest(st.session_state["password"], st.secrets["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    # Return True if the password is validated.
    if st.session_state.get("password_correct", False):
        return True

    # Show input for password.
    st.text_input(
        "Password", type="password", on_change=password_entered, key="password"
    )
    
    with st.expander("🎉 **First time here? Need assistance?** 🎉"):
        st.markdown("""Feel free to click around and test the app – just a heads up, the data you’ll see is confidential and should be kept internal. 🤫 
                    Encountering any quirks? Remember, it's just a test application and might still have a few bugs. 🐞 
                    Need more help or want to share feedback? Don’t hesitate to contact me, Stephan Nef, at stephan.nef@ibm.com. 
                    Enjoy exploring! 🚀 """)
    
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    try:
        st.lottie("https://lottie.host/ac117e33-9c74-4286-b54c-626be36e6338/lBQP5UREoA.json",height=200)
    except:
        pass
    
    return False


# if not check_password():
#     st.stop()  # Do not continue if check_password is not True.



st.title('📊 Kalkulator Differenzausgleich', help="")

st.subheader("Kunde: Kantonsspital St.Gallen")

with st.expander("🔎 Build of Material - Einzelteile Bilanz"):
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Einzelteile Absatz")
        st.write("🔩 1'500 Stück - M5 Schrauben")
        st.write("🪵 200 Stück - 30x30 Vollholzplatte")
        st.write("🦿 1'400 Stück - 10x10 Chromstahl Vierkant")
        st.write("🦿 800 Stück - 30x155 Chromstahl Vierkant")
        st.write("⚠️ geschweisste Materialien")
    
    with col2:
        st.markdown("##### Einzelteile Bedarf")
        st.write("🔩 2'000 Stück - M5 Schrauben")
        st.write("🪵 800 Stück - 30x30 Vollholzplatte")
        st.write("🦿 1'400 Stück - 10x10 Chromstahl Vierkant")
        st.write("🦿 100 Stück - 30x155 Chromstahl Vierkant")
        st.write("✅ geschraubte Materialien")
    
    st.info("Diese Bilanz ist eine erste Annahme und ohne Gewähr.")





def draw_leaf_gauge(percentage):
    # Erstelle das Gauge-Chart mit transparentem Hintergrund
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = percentage,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "[%]"},
        gauge = {
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "green"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, percentage], 'color': 'lightgreen'},
                {'range': [percentage, 100], 'color': 'rgba(0,0,0,0)'}  # Optional für zusätzliche Transparenz in Schritten
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': percentage
            }
        }
    ))

    # Setze den Hintergrund der Figur auf transparent
    fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", plot_bgcolor='rgba(0,0,0,0)', font = {'color': "darkgreen", 'family': "Arial"},height = 280)
    
    return fig


starten = st.button("Kalkulation Starten")
if starten:
    with st.status("⌛ Kalkulieren..."):
        st.write("📁 Sammle Infos...")
        time.sleep(2)
        st.write("🔗 Mappe Einzelteile...")
        time.sleep(2)
        st.write("📈 Optimiere Mapping...")
        time.sleep(1)
        st.write("☕ Kurze Kaffeepause...")
        time.sleep(2)
        st.write("✅ Berechnung erfolgreich...")
    
    st.write("---")
    
    
    st.subheader("Analyse Differenzausgleich:")
    col1, col2, col3 = st.columns(3)
      
    with col1:
        st.markdown("##### Recycled Einzelteile [%]")
        # Der Prozentsatz für die grüne Füllung
        percentage = 70
        
        # Zeichne den Tacho-Plot mit transparentem Hintergrund
        fig = draw_leaf_gauge(percentage)
    
        # Zeige den Plot in Streamlit an
        st.plotly_chart(fig, use_container_width=True)
        
    with col2:
        st.markdown("##### Upcycled Einzelteile [%]")
        # Der Prozentsatz für die grüne Füllung
        percentage = 82
        
        # Zeichne den Tacho-Plot mit transparentem Hintergrund
        fig = draw_leaf_gauge(percentage)
        
        # Zeige den Plot in Streamlit an
        st.plotly_chart(fig, use_container_width=True)
    
    
    with col3:
        st.markdown("##### Neue Einzelteile [%]")
        # Der Prozentsatz für die grüne Füllung
        percentage = 45
        
        # Zeichne den Tacho-Plot mit transparentem Hintergrund
        fig = draw_leaf_gauge(percentage)
        
        # Zeige den Plot in Streamlit an
        st.plotly_chart(fig, use_container_width=True)
        
        
    st.subheader("Empfehlung basierend auf Kalkulation:")
    st.success("✅ Wir empfehlen den Differenzausgleich zu nutzen.")
    
st.write("---")