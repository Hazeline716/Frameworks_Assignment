import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
import warnings

# Suppress the FutureWarning from seaborn, which is common with older library versions
warnings.filterwarnings("ignore", category=FutureWarning)

# --- 1. Load the cleaned dataset ---
print("--- Loading the cleaned_metadata.csv file ---")
try:
    df = pd.read_csv('cleaned_metadata.csv')
    print("Cleaned dataset loaded successfully!")
except FileNotFoundError:
    print("Error: cleaned_metadata.csv not found. Please make sure to run part2_cleaning.py first to create it.")
    exit()

# --- 2. Perform basic data analysis ---
print("\n--- Basic Data Analysis ---")

# Count papers by publication year
papers_by_year = df['year'].value_counts().sort_index()
print("Number of papers published by year:")
print(papers_by_year.tail(10)) # Display the last 10 years for relevance

# Identify the top 10 journals publishing research
top_journals = df['journal'].value_counts().head(10)
print("\nTop 10 journals publishing COVID-19 research:")
print(top_journals)

# Find the most frequent words in paper titles
# First, define a list of common words to ignore (stop words)
stop_words = set(
    "the,a,an,in,of,to,and,with,for,on,by,is,are,as,at,from,but,or,it,its,covid-19,coronavirus,sar,sars,cov,ncov,sars-cov-2".split(',')
)

# Join all titles into a single string, convert to lowercase, and find all words
title_text = " ".join(df['title'].dropna()).lower()
words = re.findall(r'\b\w+\b', title_text)
# Filter out the stop words
filtered_words = [word for word in words if word not in stop_words]

# Count the frequency of the filtered words and show the top 15
word_freq = pd.Series(filtered_words).value_counts().head(15)
print("\nMost frequent words in paper titles:")
print(word_freq)

# --- 3. Create visualizations ---
print("\n--- Creating Visualizations ---")

# Plot 1: Line chart of publications over time
plt.figure(figsize=(12, 6))
sns.lineplot(x=papers_by_year.index, y=papers_by_year.values)
plt.title('Number of Publications Over Time')
plt.xlabel('Year')
plt.ylabel('Number of Publications')
plt.grid(True)
plt.show()

# Plot 2: Bar chart of top publishing journals
plt.figure(figsize=(12, 8))
sns.barplot(x=top_journals.values, y=top_journals.index, palette='viridis')
plt.title('Top 10 Publishing Journals')
plt.xlabel('Number of Publications')
plt.ylabel('Journal')
plt.tight_layout()
plt.show()

# Plot 3: Histogram of abstract word count distribution
plt.figure(figsize=(10, 6))
sns.histplot(df['abstract_word_count'], bins=50, kde=True)
plt.title('Distribution of Abstract Word Counts')
plt.xlabel('Word Count')
plt.ylabel('Frequency')
plt.show()

# Plot 4: Word cloud of paper titles
wordcloud = WordCloud(
    width=800,
    height=400,
    background_color='white',
    stopwords=stop_words,
    max_words=200
).generate(title_text)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation='bilinear')
plt.title('Word Cloud of Paper Titles')
plt.axis('off')
plt.show()
