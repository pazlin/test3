import pandas as pd
import numpy as np

def load_data(file_path):
    """Load the CSV file containing names data"""
    df = pd.read_csv(file_path)
    return df

def get_year_range(df):
    """Get the minimum and maximum years in the dataset"""
    min_year = df['Anno Nascita'].min()
    max_year = df['Anno Nascita'].max()
    return min_year, max_year

def get_names_by_gender(df, gender, min_occurrences=3):
    """Get names by gender with their total occurrences, sorted in ascending order"""
    filtered_df = df[df['Sesso'] == gender]
    names_df = filtered_df.groupby('Nome')['Occorrenze'].sum().reset_index()
    names_df = names_df[names_df['Occorrenze'] >= min_occurrences]
    names_df = names_df.sort_values('Occorrenze')
    return names_df

def get_foreign_names_trend(df):
    """Get trend of foreign names from 1987 to 2024"""
    foreign_df = df[df['Cittadinanza'] == 'Stranieri']
    trend_df = foreign_df.groupby('Anno Nascita')['Occorrenze'].sum().reset_index()
    trend_df = trend_df.sort_values('Anno Nascita')
    return trend_df

def get_names_with_decline(df, gender, min_occurrences=3, top_n=20):
    """Get names with highest decline from start year to end year"""
    min_year, max_year = get_year_range(df)
    
    # Filter by gender and min occurrences in start year
    start_year_df = df[(df['Sesso'] == gender) & 
                       (df['Anno Nascita'] == min_year) & 
                       (df['Occorrenze'] >= min_occurrences)]
    
    # Get names that appear in both start and end years
    end_year_df = df[(df['Sesso'] == gender) & (df['Anno Nascita'] == max_year)]
    start_names = set(start_year_df['Nome'])
    end_names = set(end_year_df['Nome'])
    common_names = start_names.intersection(end_names)
    
    # Calculate decline for each name
    decline_data = []
    for name in common_names:
        start_occurrences = start_year_df[start_year_df['Nome'] == name]['Occorrenze'].sum()
        end_occurrences = end_year_df[end_year_df['Nome'] == name]['Occorrenze'].sum()
        
        if start_occurrences >= min_occurrences:
            decline = start_occurrences - end_occurrences
            decline_data.append({
                'Nome': name,
                'Occorrenze_Inizio': start_occurrences,
                'Occorrenze_Fine': end_occurrences,
                'Declino': decline
            })
    
    # Sort by decline and get top N
    decline_df = pd.DataFrame(decline_data)
    if not decline_df.empty:
        decline_df = decline_df.sort_values('Declino', ascending=False).head(top_n)
    
    return decline_df

def get_names_with_increase(df, gender, min_occurrences=3, top_n=20):
    """Get names with highest increase from start year to end year"""
    min_year, max_year = get_year_range(df)
    
    # Filter by gender and min occurrences in start year
    start_year_df = df[(df['Sesso'] == gender) & 
                       (df['Anno Nascita'] == min_year) & 
                       (df['Occorrenze'] >= min_occurrences)]
    
    # Get names that appear in both start and end years
    end_year_df = df[(df['Sesso'] == gender) & (df['Anno Nascita'] == max_year)]
    start_names = set(start_year_df['Nome'])
    end_names = set(end_year_df['Nome'])
    common_names = start_names.intersection(end_names)
    
    # Calculate increase for each name
    increase_data = []
    for name in common_names:
        start_occurrences = start_year_df[start_year_df['Nome'] == name]['Occorrenze'].sum()
        end_occurrences = end_year_df[end_year_df['Nome'] == name]['Occorrenze'].sum()
        
        if start_occurrences >= min_occurrences:
            increase = end_occurrences - start_occurrences
            increase_data.append({
                'Nome': name,
                'Occorrenze_Inizio': start_occurrences,
                'Occorrenze_Fine': end_occurrences,
                'Aumento': increase
            })
    
    # Sort by increase and get top N
    increase_df = pd.DataFrame(increase_data)
    if not increase_df.empty:
        increase_df = increase_df.sort_values('Aumento', ascending=False).head(top_n)
    
    return increase_df

def get_most_common_foreign_names(df, gender):
    """Get most common foreign names by gender, sorted in ascending order by occurrences"""
    foreign_df = df[(df['Cittadinanza'] == 'Stranieri') & (df['Sesso'] == gender)]
    names_df = foreign_df.groupby('Nome')['Occorrenze'].sum().reset_index()
    names_df = names_df.sort_values('Occorrenze')
    return names_df

def get_filtered_names(df, gender, name_search):
    """Search for names by gender and search term"""
    filtered_df = df[df['Sesso'] == gender]
    names_df = filtered_df.groupby('Nome')['Occorrenze'].sum().reset_index()
    names_df = names_df[names_df['Nome'].str.contains(name_search, case=False)]
    names_df = names_df.sort_values('Occorrenze')
    return names_df
