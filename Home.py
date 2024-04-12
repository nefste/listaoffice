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


st.title('👁‍🗨 ListAnalytics Kalkulator')
# st.write('Internes Lista Office AG Analyse Tool zur "Build of Material"-Kalkulation.')

st.subheader('👋🏻 Grüezi Sammy Sales', help="Weils mit dem HSG Square nicht funktioniert hat.😉")

# st.markdown(
# """ **Disclaimer**:  
# This app is under development. It should not be used nor shared with external stakeholders.
# Information provided here should be handled with caution and should not be used to justify a change other ressources.\n
# """)


st.image("explosion.jpg", width=600)

st.subheader("📰 Newsboard")
st.warning("Heute Meeting mit Kantonsspital St.Gallen - 14:30 Uhr")
# st.success("Kunde XY hat endlich bei uns Bestellt!!!")
# st.info("Neue öffentliche Ausschreibung vom Kantonsspital St.Gallen")
# st.warning("Alle Vertriebler bitte ihre Kunden über unsere Betriebsferien informieren")
# st.success("Peter Müller hat heute Geburtstag")
st.write("---")


st.toast(
    """
    Made with passion by
    Stephan Nef, contact for help: stephan.nef@student.unisg.com. 
    
    Enjoy exploring! 🚀
    """,
    icon="❤️",)






df = pd.read_excel("data.xlsx")


# Datumsformat für Rückkaufaktion konvertieren
def convert_dates(date_str):
    if pd.isna(date_str):
        return None
    start_date, end_date = date_str.split('-')
    return [datetime.strptime(start_date.strip(), "%d.%m.%Y"),
            datetime.strptime(end_date.strip(), "%d.%m.%Y")]

df['Rückkauf Aktion'] = df['Rückkauf Aktion'].apply(convert_dates)

# Streamlit Sidebar für Filter
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Logo_lista_office.svg/2880px-Logo_lista_office.svg.png")

    
    


