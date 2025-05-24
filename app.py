import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import (
    load_data, get_year_range,
    get_names_by_gender, get_foreign_names_trend,
    get_names_with_decline, get_names_with_increase,
    get_most_common_foreign_names, get_filtered_names
)

# Set page config
st.set_page_config(
    page_title="Analisi Nomi Piacenza",
    page_icon="👶",
    layout="wide"
)

# Title and description
st.title("Analisi dei Nomi Registrati a Piacenza")
st.write("Esplora i dati sui nomi registrati nel Comune di Piacenza dal 1987 al 2025.")

# Load data
file_path = "comune-di-piacenza-nomi-iscritti-per-nascita.csv"
df = load_data(file_path)

# Get year range
min_year, max_year = get_year_range(df)
st.write(f"Periodo analizzato: {min_year} - {max_year}")

# Sidebar for filters
st.sidebar.header("Filtri")
min_occurrences = st.sidebar.slider("Numero minimo di occorrenze", 1, 10, 3)

# 1. Tables of names by gender
st.header("Tabelle dei Nomi per Genere")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Nomi Femminili")
    female_names = get_names_by_gender(df, 'F', min_occurrences)
    st.dataframe(female_names, height=400)

with col2:
    st.subheader("Nomi Maschili")
    male_names = get_names_by_gender(df, 'M', min_occurrences)
    st.dataframe(male_names, height=400)

# 2. Searchable tables
st.header("Ricerca Nomi per Occorrenze")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Ricerca Nomi Femminili")
    female_search = st.text_input("Cerca un nome femminile")
    if female_search:
        filtered_female = get_filtered_names(df, 'F', female_search)
        st.dataframe(filtered_female, height=400)

with col2:
    st.subheader("Ricerca Nomi Maschili")
    male_search = st.text_input("Cerca un nome maschile")
    if male_search:
        filtered_male = get_filtered_names(df, 'M', male_search)
        st.dataframe(filtered_male, height=400)

# 3. Trend of foreign names
st.header(f"Andamento dei Nomi Stranieri ({min_year}-{max_year})")
foreign_trend = get_foreign_names_trend(df)
fig = px.line(
    foreign_trend, 
    x='Anno Nascita', 
    y='Occorrenze',
    title=f'Andamento dei Nomi Stranieri ({min_year}-{max_year})'
)
st.plotly_chart(fig, use_container_width=True)

# 4. Names with highest decline
st.header(f"Nomi con Maggior Declino dal {min_year} al {max_year}")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Nomi Femminili in Declino")
    female_decline = get_names_with_decline(df, 'F', min_occurrences)
    if not female_decline.empty:
        fig_female_decline = px.bar(
            female_decline,
            x='Nome',
            y='Declino',
            title=f'Top 20 Nomi Femminili con Maggior Declino',
            color='Declino',
            color_continuous_scale='Reds'
        )
        st.plotly_chart(fig_female_decline, use_container_width=True)
    else:
        st.write("Nessun nome femminile soddisfa i criteri di ricerca.")

with col2:
    st.subheader("Nomi Maschili in Declino")
    male_decline = get_names_with_decline(df, 'M', min_occurrences)
    if not male_decline.empty:
        fig_male_decline = px.bar(
            male_decline,
            x='Nome',
            y='Declino',
            title=f'Top 20 Nomi Maschili con Maggior Declino',
            color='Declino',
            color_continuous_scale='Blues'
        )
        st.plotly_chart(fig_male_decline, use_container_width=True)
    else:
        st.write("Nessun nome maschile soddisfa i criteri di ricerca.")

# 5. Names with highest increase
st.header(f"Nomi con Maggior Aumento dal {min_year} al {max_year}")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Nomi Femminili in Aumento")
    female_increase = get_names_with_increase(df, 'F', min_occurrences)
    if not female_increase.empty:
        fig_female_increase = px.bar(
            female_increase,
            x='Nome',
            y='Aumento',
            title=f'Top 20 Nomi Femminili con Maggior Aumento',
            color='Aumento',
            color_continuous_scale='Greens'
        )
        st.plotly_chart(fig_female_increase, use_container_width=True)
    else:
        st.write("Nessun nome femminile soddisfa i criteri di ricerca.")

with col2:
    st.subheader("Nomi Maschili in Aumento")
    male_increase = get_names_with_increase(df, 'M', min_occurrences)
    if not male_increase.empty:
        fig_male_increase = px.bar(
            male_increase,
            x='Nome',
            y='Aumento',
            title=f'Top 20 Nomi Maschili con Maggior Aumento',
            color='Aumento',
            color_continuous_scale='Purples'
        )
        st.plotly_chart(fig_male_increase, use_container_width=True)
    else:
        st.write("Nessun nome maschile soddisfa i criteri di ricerca.")

# 6. Most common foreign names
st.header("Nomi Stranieri più Ricorrenti")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Nomi Femminili Stranieri")
    foreign_female = get_most_common_foreign_names(df, 'F')
    st.dataframe(foreign_female, height=400)

with col2:
    st.subheader("Nomi Maschili Stranieri")
    foreign_male = get_most_common_foreign_names(df, 'M')
    st.dataframe(foreign_male, height=400)

# Footer
st.markdown("---")
st.caption("Dati forniti dal Comune di Piacenza")
