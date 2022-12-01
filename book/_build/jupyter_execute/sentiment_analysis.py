#!/usr/bin/env python
# coding: utf-8

# # Sentiment analysis of feedback
# 
# ## Authors
# *J. Foster, R. Treharne*
# 
# ## Description
# 
# This tool will perform an analysis of feedback on submissions for a given (or multiple) assignments. 
# 
# A sentiment analysis is performed to determine sentiment score for each comment, i.e. a relative measure of how positive/negative the overall language in each comment is.
# 
# A *Feedback Rating* score for each comment is calculated as the product of comment length (number of words) and sentiment score.
# 
# ## Video Walkthrough
# 
# https://liverpool.instructuremedia.com/embed/e07eec3c-06e7-4ffc-872d-9d9afaf3396f
# 
# ## Warning
# 
# There is likely to be a high level of subjectivity in the sentiment analysis and a manual audit, to compare feedback comments and corresponding sentiment scores, should be made before drawing any conclusions from the data.
# 
# Furthermore, this analysis only looks at comments made in the "comments box" on Speedgrader. It does not consider in-line comments/annotations made directly on the submitted documents.
# 
# 
# <img src="https://github.com/rtreharne/random/blob/main/telife_trans_pink.png?raw=true" width=200>

# # Step 1. Install canvasapi and configure Canvas API session

# In[5]:


# Run this cell to import the necessary modules from canvasapi and other Python modules

from canvasapi import Canvas
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta, timezone
from textblob import TextBlob
import plotly.express as px
import nltk
nltk.download('punkt')
 
API_URL = "https://canvas.liverpool.ac.uk/"
 
API_KEY = "<INPUT YOUR KEY HERE>" # Replace everything inside the quotation marks with your API KEY/TOKEN

# Where do I get my Canvas API Key from? 
# https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89


# In[6]:


# Uncomment and run the line below to create a Canvas session

# canvas = Canvas(API_URL, API_KEY)


# # Step 2. Run the following cell
# 
# This cell contains all the code needed to perform the analysis. You need to run this cell, but once you've done this you can ignore the code.

# In[7]:


import matplotlib.pyplot as plt
import numpy as np

class SpeedgraderAnalysis():
    def __init__(self, urls):
        self.urls = urls

        df_list = []
      
        if isinstance(urls, str):
            self.urls = [urls]
            
        for url in self.urls:
            course_id, assignment_id = self.get_course_assignment(url)
            assignment = canvas.get_course(course_id).get_assignment(assignment_id)
            df_list.append(self.get_submissions_comments(assignment))

        self.submissions_comments = pd.concat(df_list)

        self.sentiment_analysis()
        self.summary = self.get_averages()

    def get_course_assignment(self, url):
        return [int(x) for x in re.findall("[0-9]+", url)]
    
    def get_submissions_comments(self, assignment):
        submissions = [x for x in assignment.get_submissions(include=["submission_comments"])]
        submission_comments = []
        for sub in submissions:
            row = []
            for comment in sub.submission_comments:
                row={
                    "comment": comment["comment"],
                    "marker": comment["author_name"],
                    "score": sub.score,                  
                }
                submission_comments.append(row)
        return pd.DataFrame(submission_comments)
    
    def sentiment_analysis(self):
        comments = self.submissions_comments.comment.tolist()
        comment_length = []
        comment_sentiment = []
        for comment in comments:
            blob = TextBlob(comment)
            comment_length.append(len(blob.words))
            comment_sentiment.append(blob.sentiment.polarity)

        self.submissions_comments["comment_length"] = comment_length
        self.submissions_comments["comment_sentiment"] = comment_sentiment
        self.submissions_comments["feedback_quality"] = np.array(comment_length)*np.array(comment_sentiment)

    def plot(self, marker=None, title=""):
        data = self.submissions_comments
        data["color"] = "All"

        if marker is not None:
            if type(marker) == "str":
                data.loc[(data.marker.str.contains(marker)), "color"] = marker
            else:
                for m in marker:
                    data.loc[(data.marker.str.contains(m)), "color"] = m

        fig = px.scatter(data, x="score", 
                         y="feedback_quality", 
                         #hover_data=["Marker: " + x + ", Sentiment: " + str(y) for x, y in zip(data["marker"], data["comment_sentiment"])], 
                         size=np.array(data["comment_length"]), 
                         opacity=0.8,
                         color="color",
                         labels = {
                             "score": "Grade (%)",
                             "feedback_quality": "Feedback Rating (arb. units)"
                         },
                         #trendline='ols',
                         #trendline_scope='overall',
                         custom_data = ["marker", "comment_length", "comment_sentiment", "comment"],
                         title=title
                         )
        
        fig.update_traces(
            hovertemplate="<br>".join([
                "Feedback Rating (arb. units): %{y:.1f}",
                "Grade (%): %{x}",
                "Marker: %{customdata[0]}",
                "Comment Length (words): %{customdata[1]}",
                "Sentiment (arb. units): %{customdata[2]:.4f}"

            ])
        )

        #fig.update_traces(mode="markers+trendline")
        fig.add_hline(y=data["feedback_quality"].mean(), line_color='red', opacity=0.2, annotation_text="Mean Reedback Rating")
        fig.add_vline(x=data["score"].mean(), line_color='red', opacity=0.2, annotation_text="Mean Score")


        fig.show()

    def get_averages(self):
        summary = self.submissions_comments.groupby(["marker"]).mean()
        return summary

    def comment_length_bar(self, ascending=True, length=20):
        fig, ax = plt.subplots(figsize=(5, int(length/2)))
        self.submissions_comments.groupby(["marker"]).mean().sort_values(by=["comment_length"], ascending=ascending).tail(length).plot.barh(y="comment_length", ax=ax)
        fig.show()


# # 3. Analyse a Canvas Speedgrader assignment
# 
# Run the following commant to perform a sentiment analysis on a specific assignment:
# 
# `result = SpeedgraderAnalysis(url)`
# 
# where the `url` parameter corresponds to the url string of the corresponding assignment.
# 
# You can also submit multiple urls for simultaneous analysis by using a list, e.g:
# 
# ```
# urls = [
#     "https://canvas.liverpool.ac.uk/courses/60973/assignments/208996",
#     "https://canvas.liverpool.ac.uk/courses/60973/assignments/209009",
#     ]
# ```
# 

# In[8]:


url = "https://liverpool.instructure.com/courses/58609/assignments/218636" # LIFE223_1 as an example

# Uncomment the following line to run:

# result = SpeedgraderAnalysis(url) #!important


# In[9]:


# Once you're run the cell above you can look at the extracted sentiment data as follows:

# Uncomment the following line to run:

# result.submissions_comments


# In[10]:


# You can save this data as an Excel spreadsheet as follows (uncomment to run):

# result.submissions_comments.to_excel("sentiment_analysis.xlsx", index=False)


# In[11]:


# Plot your sentiment analysis

# Uncomment the following line to run:

# result.plot()


# In[12]:


# You can highlight the comments of any marker (or multiple markers) as follows (uncomment to run):

# result.plot(marker=["Treharne", "Mitchell"], title="Sentiment analysis of feedback comments for LIFE223-202223 Essay Assignment")


# In[14]:


# One last thing: You can plot a bar chart showing the top 20 markers (or bottom 20) listed according to comment length.

# Uncomment the following line to run:

# result.comment_length_bar(ascending=True) # change to ascending=False if you want to see the bottom 20

