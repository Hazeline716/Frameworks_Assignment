import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
import warnings

# Suppress the FutureWarning from seaborn to keep the output clean
warnings.filterwarnings("ignore", category=FutureWarning)

@st.cache_data
def load_and_prepare_data(filepath):
    """
    Loads, cleans, and prepares the metadata.csv file.
    This function is cached by Streamlit to run only once.
    """
    try:
        df = pd.read_csv(filepath, low_memory=False)
    except FileNotFoundError:
        st.error(f"Error: {filepath} not found. Please ensure the file is in the same directory.")
        return pd.DataFrame() # Return an empty DataFrame on error

    # Drop columns that are not useful for this analysis
    columns_to_drop = ['sha', 'pmcid', 'pubmed_id', 'full_text_file', 's2_id', 'source_x']
    df_cleaned = df.drop(columns=columns_to_drop, errors='ignore')

    # Fill missing values in key text columns with an empty string
    df_cleaned['abstract'] = df_cleaned['abstract'].fillna('')
    df_cleaned['title'] = df_cleaned['title'].fillna('')

    # Convert the publish_time column to datetime format
    df_cleaned['publish_time'] = pd.to_datetime(df_cleaned['publish_time'], errors='coerce')
    df_cleaned.dropna(subset=['publish_time'], inplace=True)

    # Extract the year for time-based analysis
    df_cleaned['year'] = df_cleaned['publish_time'].dt.year.astype(int)
    
    return df_cleaned

# --- Streamlit App Layout ---
st.title('COVID-19 Research Paper Analysis')
st.markdown(
    """
    This interactive dashboard explores the CORD-19 dataset, analyzing publication trends, top journals, 
    and key topics in COVID-19 research.
    """
)

# Load the data using the cached function
df = load_and_prepare_data('metadata.csv')

if not df.empty:
    # --- Sidebar for user input ---
    st.sidebar.header('Data Filters')
    
    # Create a slider to filter the data by year range
    min_year = int(df['year'].min())
    max_year = int(df['year'].max())
    year_range = st.sidebar.slider(
        'Select a Year Range',
        min_value=min_year,
        max_value=max_year,
        value=(min_year, max_year)
    )

    # Filter the DataFrame based on the selected year range
    filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

    # --- Display a sample of the data ---
    st.header('Sample of Filtered Data')
    st.dataframe(filtered_df[['title', 'authors', 'journal', 'publish_time', 'abstract']].head(10))

    # --- Visualizations ---
    st.header('Data Visualizations')
    
    # Chart 1: Publications Over Time (Line Chart)
    st.subheader('Number of Publications Over Time')
    papers_by_year = filtered_df['year'].value_counts().sort_index()
    fig1, ax1 = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=papers_by_year.index, y=papers_by_year.values, ax=ax1)
    ax1.set_title('Publications by Year')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Number of Publications')
    st.pyplot(fig1)

    # Chart 2: Top Publishing Journals (Bar Chart)
    st.subheader('Top Publishing Journals')
    top_journals = filtered_df['journal'].value_counts().head(10)
    fig2, ax2 = plt.subplots(figsize=(10, 7))
    sns.barplot(x=top_journals.values, y=top_journals.index, palette='viridis', ax=ax2)
    ax2.set_title(f'Top 10 Publishing Journals ({year_range[0]} - {year_range[1]})')
    ax2.set_xlabel('Number of Publications')
    ax2.set_ylabel('Journal')
    st.pyplot(fig2)

    # Chart 3: Word Cloud of Paper Titles
    st.subheader('Word Cloud of Paper Titles')
    
    # Define simple stop words to create a meaningful word cloud
    stop_words = set(
        "the,a,an,in,of,to,and,with,for,on,by,is,are,as,at,from,but,or,it,its,covid-19,coronavirus,sar,sars,cov,ncov,sars-cov-2".split(',')
    )
    
    title_text = " ".join(filtered_df['title'].dropna()).lower()
    
    if title_text:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color='white',
            stopwords=stop_words,
            max_words=200
        ).generate(title_text)

        fig3, ax3 = plt.subplots(figsize=(10, 7))
        ax3.imshow(wordcloud, interpolation='bilinear')
        ax3.set_title(f'Word Cloud for Paper Titles ({year_range[0]} - {year_range[1]})')
        ax3.axis('off')
        st.pyplot(fig3)
    else:
        st.write("No titles found for the selected year range.")
