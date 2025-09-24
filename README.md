# Frameworks_Assignment



# Project Report
 


# Data Analysis of COVID-19 ResearchExecutive Summary



This project analyzed the CORD-19 dataset, a comprehensive collection of scholarly articles on the coronavirus and related topics.



The goal was to explore the data, clean it, and present key findings through visualizations and a web-based application.



The analysis revealed significant trends in scientific publishing, identified major contributing journals, and highlighted the most frequently discussed topics in the research papers' titles.



# Key FindingsPublication Trends



The number of research papers published on COVID-19 has grown dramatically over time, particularly from 2019 onwards, reflecting the global scientific community's rapid response to the pandemic.



-Top Journals: Journals such as The Lancet and New England Journal of Medicine were identified as leading publishers of research in this field, based on the volume of articles in the dataset.



-Most Frequent Topics: A word cloud of paper titles showed that terms like "clinical," "virus," "health," and "public" were among the most common, indicating a focus on the clinical and public health aspects of the pandemic.Reflection on Challenges and Learning



-Handling Large Datasets: The initial challenge was working with a large .csv file, which required using low_memory=False to load the data efficiently. Identifying and handling columns with a high percentage of missing values was a key data cleaning step.



-File Management and Dependencies: Encountering FileNotFoundError was a common challenge. This reinforced the importance of ensuring that all scripts and data files are in the same directory and using correct file paths. This project demonstrated the value of a well-organized project structure from the start.



-Transitioning from Script to Application: Moving from a series of static analysis scripts to a dynamic Streamlit application was a major learning point. The use of @st.cache_data was critical for performance, as it prevented the app from re-loading and re-processing the large dataset every time a user interacted with a widget.


The process highlighted how a simple dashboard can bring data to life and make findings accessible to a broader audience.
