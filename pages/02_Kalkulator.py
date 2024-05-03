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
from streamlit_extras.let_it_rain import rain 

import webbrowser
from urllib.parse import quote

import socket

st.set_page_config(
     page_title="ListAnalytics",
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
                    
    st.info("⚖️ Disclaimer: The content presented in this web application is created and owned by Stephan Nef exclusively for private and educational purposes. It has no affiliation, connection, or relation to the company 'Lista Office' whatsoever.")
    
    if "password_correct" in st.session_state:
        st.error("😕 Password incorrect")
    try:
        st.lottie("https://lottie.host/ac117e33-9c74-4286-b54c-626be36e6338/lBQP5UREoA.json",height=200)
    except:
        pass
    
    return False

if not check_password():
      st.stop()  # Do not continue if check_password is not True.

st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Logo_lista_office.svg/2880px-Logo_lista_office.svg.png")



st.title('📊 Kalkulator Differenzausgleich', help="Die Absatzmenge wird in seinen Einzelteilen analysiert und es wird geschaut welche Komponenten wiederverwendet werden. Dabei werden auch Aufwände wie Transportkosten, Montagekosten, Wiederaufbereitungskosten berücksichtigt. In diesem Prototyp nur eine fiktive Kalkulation zur Darstellung.")



# if 'customer' not in st.session_state:
#     st.info("⬅️ Gehe bitte zuerst auf die Bedarfs-Analyse und wähle Kunde, Absatz und Bedarf aus. Die Seitennavigation findest du links in der Sidebar.")
#     st.stop()
# else:  
#     customer = st.session_state['customer']


st.session_state['customer'] = "Swisscom"  
    
st.subheader(f"Kunde: {st.session_state['customer']}")
st.write('---')

st.subheader("Ermittelter Absatz & Bedarf")

absatz, bedarf = st.columns(2)

def show_column_info(column, state_key, message):
    with column:
        defined = False
        for i in range(100):
            key = f'{state_key}_{i}'
            if key in st.session_state:
                st.info(st.session_state[key])
                defined = True
            elif not defined:
                st.warning(message)
                defined = True
                break  

show_column_info(absatz, 'absatz', "Wähle bitte Produkte zum Absetzen auf der Bedarfs-Analyse Seite.")
show_column_info(bedarf, 'bedarf', "Wähle bitte Produkte zum Beschaffen auf der Bedarfs-Analyse Seite.")


with st.expander("🔎 Build of Material - Einzelteile Bilanz"):
    
    st.info("Fiktive Daten zur Darstellung.")
    
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
        st.write("🦿 1'600 Stück - 10x10 Chromstahl Vierkant")
        st.write("🦿 100 Stück - 30x155 Chromstahl Vierkant")
        st.write("✅ geschraubte Materialien")
        
        
    # Namen der Produkte
    produkte = ['M5 Schrauben', '30x30 Vollholzplatte', '10x10 Chromstahl Vierkant', '30x155 Chromstahl Vierkant']
    
    # Daten für Absatz und Bedarf
    absatz = [1500, 200, 1400, 800]
    bedarf = [2000, 800, 1600, 100]
    
    # Berechnung der Differenz zwischen Bedarf und Absatz
    differenz = [b - a for a, b in zip(absatz, bedarf)]
    
    # Erstellen des Balkendiagramms zur Darstellung der Differenz
    fig = go.Figure(data=[
        go.Bar(name='Differenz', x=produkte, y=differenz, marker_color=['red' if x < 0 else 'green' for x in differenz])
    ])
    
    # Anpassen des Layouts
    fig.update_layout(
        title='Diskrepanz zwischen Bedarf und Absatz pro Produkt',
        xaxis_title='Produkte',
        yaxis_title='Differenz (Bedarf - Absatz)',
        barmode='group',
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        )
    )
    
    # Anzeigen des Plots in Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
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
    fig.update_layout(paper_bgcolor = "rgba(0,0,0,0)", plot_bgcolor='rgba(0,0,0,0)', font = {'color': "darkgreen", 'family': "Arial"})
    
    return fig

st.write('---')

st.subheader("Kalkulation")

with st.expander("🤔 Was wird berechnet?"):
    st.write("Die Absatzmenge wird in seinen Einzelteilen analysiert und es wird geschaut welche Komponenten wiederverwendet werden. Dabei werden auch Aufwände wie Transportkosten, Montagekosten, Wiederaufbereitungskosten berücksichtigt. In diesem Prototyp nur eine fiktive Kalkulation zur Darstellung.")
    

starten = st.button("🤯 Kalkulation starten", help="fiktive Kalkulation zur Darstellung")
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
    col1, col2, = st.columns(2)
      
    # with col1:
    #     st.markdown("##### Recycled Einzelteile [%]")
    #     # Der Prozentsatz für die grüne Füllung
    #     percentage = 70
        
    #     # Zeichne den Tacho-Plot mit transparentem Hintergrund
    #     fig = draw_leaf_gauge(percentage)
    
    #     # Zeige den Plot in Streamlit an
    #     st.plotly_chart(fig, use_container_width=True)
        
    with col1:
        st.markdown("##### Upcycled Einzelteile von Absatz [%]")
        # Der Prozentsatz für die grüne Füllung
        percentage = 65
        
        # Zeichne den Tacho-Plot mit transparentem Hintergrund
        fig = draw_leaf_gauge(percentage)
        
        # Zeige den Plot in Streamlit an
        st.plotly_chart(fig, use_container_width=True)
    
    
    with col2:
        st.markdown("##### Upcycled Einzelteile in Bedarf [%]")
        # Der Prozentsatz für die grüne Füllung
        percentage = 35
        
        # Zeichne den Tacho-Plot mit transparentem Hintergrund
        fig = draw_leaf_gauge(percentage)
        
        # Zeige den Plot in Streamlit an
        st.plotly_chart(fig, use_container_width=True)
        
    # time.sleep(5)    
    st.subheader("Empfehlung basierend auf Kalkulation:")
    st.success("""✅ Wir empfehlen den Differenzausgleich zu nutzen.""")
    rain( 
    emoji="🍃", 
    font_size=50,  # the size of emoji 
    falling_speed=2,  # speed of raining 
    animation_length=2,  # for how much time the animation will happen 
    ) 
    
    st.write("---")


    st.subheader("💰 Kostenersparnis")
    
    col11, col22, = st.columns(2)
    
    with col11:
        st.metric("Listenpreis", value="27'000 CHF")
        
    
    with col22:
        st.metric("Angebotspreis", value="22’950 CHF", delta="-4'050 CHF", delta_color="inverse")
    
    st.success("Ersparnis von 4'050 CHF")



# Email details
subject = f"ListAnalytics Angebot - {st.session_state['customer']}"
to = "ann-kathrin.koepple@student.unisg.ch; stephan.nef@student.unisg.ch"
body = f"""Hallo Karin Kunde - {st.session_state['customer']}

Danke für Ihr interesse an Lista Office Möbel. 
Es freut uns das wir Ihnen ein attraktives Angebot dank dem ListAnalytics Kalkulator rechnen konnten. 

**********************************************************
Gerne sende ich Ihnen folgendes Angebot:
(fiktive Daten, hardcoded)
---------------------------------------------------------- 
- Rücknahmen von:
    - 50 Stück LO Pure Tischen 
    
- Kauf von: 
    - 60 LO Extend Tischen
    Preis Listenpreis: 450.00 CHF/Stück
    Reduktion aufgrund Rücknahme: 4'050 CHF
----------------------------------------------------------  
    
Total Kosten: 22’950 CHF (ohne Mehrwertsteuer, inkl. Transport und 2 Jahre Garantie)

----------------------------------------------------------
**********************************************************


Bitte lass uns wissen, ob weitere Informationen benötigen oder wenn wir den Auftrag für Sie vorbereiten sollen.

Freundliche Grüsse,
Sammy Sales, Lista Office AG


                                                                                                    
----------------------------------------------------------
Disclaimer:
Dieses Angebot ist vertraulich und ausschließlich für den Adressaten bestimmt. Wenn Sie nicht der vorgesehene Adressat sind, informieren Sie bitte den Absender sofort und löschen Sie diese E-Mail. Eine Weitergabe, Vervielfältigung oder Nutzung des Inhalts dieser E-Mail ist ohne schriftliche Genehmigung des Absenders nicht gestattet. Dieses Angebot ist unverbindlich und freibleibend. Preise und Konditionen können sich ändern. Für Tippfehler oder Irrtümer in der Kommunikation übernimmt der Absender keine Haftung.
----------------------------------------------------------


"""

st.write('---')

st.subheader("Angebot erstellen")
 
with st.expander("📧 Angebot erstellen"):

    def create_mailto_link(to, subject, body):
        subject_encoded = quote(subject)
        body_encoded = quote(body)
        return f"mailto:{to}?subject={subject_encoded}&body={body_encoded}"
    
    # Streamlit button to open the email in Outlook
    if st.button('Sende Angebot',help='Outlook öffnet sich nur wenn App lokal läuft, siehe GitHub Repo https://github.com/nefste/listaoffice'):
        starten = True
        link = create_mailto_link(to, subject, body)
        webbrowser.open(link)
        st.info('Ein Outlook-Fenster sollte sich mit Ihrer E-Mail-Vorlage öffnen.')
    
    email_list = to.split("; ")  # Teilt den String in eine Liste von E-Mail-Adressen
    selected_emails = st.multiselect("Mail an:", email_list, default=email_list) 

    st.text_area("Betreff:", subject,height=20)
    st.text_area("Angebots Mail zum bearbeiten:",body, height=450)

