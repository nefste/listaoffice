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


if not check_password():
    st.stop()  # Do not continue if check_password is not True.


st.title('Musterkunde Heptagon', help="Weils mit dem HSG Square nicht funktioniert hat.😉")

st.markdown(
""" **Disclaimer**:  
This app is under development. It should not be used nor shared with external stakeholders.
Information provided here should be handled with caution and should not be used to justify a change other ressources.\n
""")
st.info("For any questions please contact Stephan Nef stephan.nef@student.unisg.ch.")

st.warning("This page is used for a Case Study in University St.Gallen and is not ment for public distribution!")

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
st.sidebar.header('🔍 Filter (optional)')
selected_manufacturer = st.sidebar.multiselect('Hersteller auswählen', options=df['Hersteller'].unique())
selected_group = st.sidebar.multiselect('Produktgruppe auswählen', options=df['Produkt Gruppe'].unique())

# Filter anwenden
if selected_manufacturer:
    df = df[df['Hersteller'].isin(selected_manufacturer)]
if selected_group:
    df = df[df['Produkt Gruppe'].isin(selected_group)]
    
# Den minimalen und maximalen Preis im gefilterten DataFrame bestimmen
min_preis = df['Preis'].min() if not df.empty else 0
max_preis = df['Preis'].max() if not df.empty else 0

# Slider für die Preisspanne in der Sidebar erstellen
preis_range = st.sidebar.slider('Preisspanne auswählen [CHF]',
                                min_value=int(min_preis),
                                max_value=int(max_preis),
                                value=(int(min_preis), int(max_preis)))

# Weitere Logik zur Anwendung der Preisspannenfilterung, falls erforderlich
df = df[(df['Preis'] >= preis_range[0]) & (df['Preis'] <= preis_range[1])]




with st.expander("🛋️ Deine gekauften Produkte [klick hier]"):
    # Erstelle die Paginierungsbuttons dynamisch basierend auf der Länge des DataFrames
   anzahl_pro_seite = 15
   total = len(df)
   buttons_per_row = 5
   rows = (total // anzahl_pro_seite) + (1 if total % anzahl_pro_seite > 0 else 0)
   
   # Berechne die Anzahl der benötigten Buttonreihen
   for row in range(0, rows, buttons_per_row):
       cols = st.columns(buttons_per_row)
       for i, col in enumerate(cols):
           index = row + i
           von = index * anzahl_pro_seite
           bis = min(von + anzahl_pro_seite, total)
           if von < total:
               button_label = f"{von+1}-{bis}"
               if col.button(button_label, key=f"button_{index}"):
                   st.session_state['von'] = von
                   st.session_state['bis'] = bis
   
   # Verwende die aktualisierten von- und bis-Indizes, um die angezeigten Produkte zu bestimmen
   for i in range(st.session_state['von'], st.session_state['bis']):
        st.subheader(f"{df['Produktname'].iloc[i]}")
        st.write(f"Hersteller: {df['Hersteller'].iloc[i]}")
        st.write(f"Modell: {df['Modell'].iloc[i]}")
        st.write(f"Artikelnummer: {df['Artikelnummer'].iloc[i]}")
        
        st.info(f"Bezahlter Preis: {df['Preis'].iloc[i]} CHF")
        
        listenpreis = df['Preis'].iloc[i]
        # Zufällige Schwankung generieren: +10% bis -60%
        schwankung = np.random.uniform(-0.4, 0.1)  
        abkaufpreis = listenpreis * (1 + schwankung)
        

        
        
        
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                st.image(f"{df['Produktname'].iloc[i]}.png") # Pfad zu den Bildern anpassen
            except:
                st.image("logo.jpg")
        
        with col2:
            # Vergleich und Anzeige der Nachrichten
            if abkaufpreis < listenpreis:
                st.success(f"⭐ Unser Abkaufpreis {abkaufpreis:.2f} CHF")
            elif abkaufpreis > listenpreis:
                st.warning(f"😔 Unser Abkaufpreis {abkaufpreis:.2f} CHF ist leider noch höher als ihr bezahlter Preis.")
            else:
                st.info("Unser Abkaufpreis entspricht genau dem Listenpreis.")
                
            # Simulierte Preisdaten vorbereiten
            aktuelles_datum = datetime(2024, 3, 1)
            datumsangaben = pd.date_range(end=aktuelles_datum, periods=12, freq='M')
            
            
            aktueller_preis = df['Preis'].iloc[i]
            preisschwankung = 0.15
            simulierte_preise = [aktueller_preis * (1 + np.random.uniform(-preisschwankung, preisschwankung)) for _ in range(11)]
            simulierte_preise.append(aktueller_preis)
            
            # Durchschnittspreis berechnen
            durchschnittspreis = np.mean(simulierte_preise)
            
            # DataFrame für die Visualisierung
            preisentwicklung_df = pd.DataFrame({
                'Datum': datumsangaben,
                'Preis': simulierte_preise
            })
            
            # Erstellung der Plotly-Linienchart
            fig = px.line(preisentwicklung_df, 
                          x="Datum", 
                          y="Preis", 
                          labels={"Preis [CHF]": "Preis [CHF]", "Datum": "Datum"}, 
                          title="Preisentwicklung der letzten 12 Monate",
                          markers=True)
            
            # Farbe basierend auf dem Vergleich bestimmen
            linienfarbe = "green" if abkaufpreis < listenpreis else "red"
            
            # Horizontale Linie für den Abkaufpreis hinzufügen
            fig.add_trace(go.Scatter(x=[datumsangaben.min(), datumsangaben.max()], y=[abkaufpreis, abkaufpreis],
                                     mode='lines', line=dict(color=linienfarbe, dash='dash'),
                                     showlegend=False))  # Legende für diese Linie ausschalten
            # Anzeigen der Chart in Streamlit
            st.plotly_chart(fig, use_container_width=True)
            
            st.link_button("See in Configurator", f"{df['Link'].iloc[i]}")
            
        st.write('---')
    
    


with st.expander("💸 Ihre Comodity Entwicklung [klick hier]"):
    datumsangaben = pd.date_range(end=datetime.now(), periods=12, freq='M')
    
    data = []
    for datum in datumsangaben:
        for hersteller in df['Hersteller']:
            schwankung = np.random.uniform(-0.35, 0.1)  # Zufällige Schwankung
            preis = listenpreis * (1 + schwankung)
            data.append({'Hersteller': hersteller, 'Datum': datum, 'Preis': preis})
    
    df_preise = pd.DataFrame(data)
    
    # Datum für Gruppierung in Perioden umwandeln, um Summierungsfehler zu vermeiden
    df_preise['Monat'] = df_preise['Datum'].dt.to_period('M')
    
    # Die größten vier Kunden identifizieren
    top_kunden = df_preise.groupby('Hersteller')['Preis'].sum().nlargest(4).index
    
    # Alle anderen Kunden in "Others" zusammenfassen
    df_preise['Hersteller'] = df_preise['Hersteller'].apply(lambda x: x if x in top_kunden else 'Others')
    
    # Daten für die größten vier Kunden und "Others" zusammenfassen
    df_summiert = df_preise.groupby(['Hersteller', 'Monat'])['Preis'].sum().round(0).reset_index()
    df_summiert['Monat'] = df_summiert['Monat'].dt.to_timestamp()
    df_summiert = df_summiert.sort_values(by=['Monat', 'Preis'], ascending=[True, False])
    
    
    st.subheader("💸 Ihre Comodity Entwicklung über die letzten 12 Monate")
    # Gestapeltes Balkendiagramm erstellen
    fig = px.bar(df_summiert, 
                 x="Monat", 
                 y="Preis", 
                 color="Hersteller", 
                 labels={"Preis": "Gesamtpreis [CHF]", "Monat": "Datum"}, 
                 text="Preis")
    
    fig.update_layout(barmode='stack')
    
    # Diagramm in Streamlit anzeigen
    st.plotly_chart(fig, use_container_width=True)



with st.expander("💰 Unsere geplanten Rückkaufaktionen [klick hier]"):
    st.subheader("💰 Unsere geplanten Rückkaufaktionen")
    
    
    # Gantt-Chart für Produkte mit Rückkaufaktion
    df_gantt = df.dropna(subset=['Rückkauf Aktion'])
    fig = px.timeline(df_gantt, x_start=df_gantt['Rückkauf Aktion'].apply(lambda x: x[0]),
                      x_end=df_gantt['Rückkauf Aktion'].apply(lambda x: x[1]),
                      y='Produktname')
    st.plotly_chart(fig)
    
    
    # Filtern der Produkte, die für eine Rückkaufaktion verfügbar sind
    produkte_fuer_rueckkauf = df


with st.expander('📝 Interesse an einer Rückkaufaktion'):
    with st.form("ruckkauf"):
        st.write("Kontakt Formular")
        
        st.text_input("Name",placeholder="Nef")
        st.text_input("Vorname",placeholder="Stephan")
        st.text_input("Mail",placeholder="stephan.nef@student.unisg.ch")
        st.write('---')
        # Multiselect für die Auswahl der Produkte
        ausgewaehlte_produkte = st.multiselect("Wählen Sie die Produkte aus, für die Sie sich für ein Rückkauf interessieren:",
                                               options=produkte_fuer_rueckkauf)
    
        # Absenden-Button
        submit_button = st.form_submit_button("Senden")
    
    if submit_button:
        if ausgewaehlte_produkte:
            st.success("Vielen Dank für Ihr Interesse! Wir werden uns bezüglich der Rückkaufaktion bei Ihnen melden.")
        else:
            st.error("Bitte wählen Sie mindestens ein Produkt aus.")




# with st.expander("Meine Daten:"):
#     st.dataframe(df)
    
    
    


