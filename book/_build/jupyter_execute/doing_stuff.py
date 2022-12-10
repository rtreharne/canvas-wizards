#!/usr/bin/env python
# coding: utf-8

# # Doing stuff across multiple courses
# 
# ## Authors
# *R. Treharne*
# 
# ## Description
# 
# This tool will update the assignment deadlines across multiple Canvas courses
# 
# <img src="https://github.com/rtreharne/random/blob/main/telife_trans_pink.png?raw=true" width=200>

# # Step 1. Install canvasapi and configure Canvas API session

# In[6]:


# Run this cell to import the necessary modules from canvasapi and other Python modules

from canvasapi import Canvas
import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta, timezone
from tqdm import tqdm
 
API_URL = "https://canvas.liverpool.ac.uk/"

API_KEY = "<INPUT YOUR KEY HERE>" # Replace everything inside the quotation marks with your API KEY/TOKEN
API_KEY = "15502~25CM3f7ltUxu05h6rkQWlIvpH1wRBLzDE1FL2xLqI1Ht2yr6Kzfxta6DBWWAdn0Z"
# Where do I get my Canvas API Key from? 
# https://community.canvaslms.com/t5/Admin-Guide/How-do-I-manage-API-access-tokens-as-an-admin/ta-p/89


# # Step 2. Run the following cell
# 
# This cell contains all the code needed to perform the analysis. You need to run this cell, but once you've done this you can ignore the code.

# In[113]:


class MultiCanvas():
    def __init__(self, API_URL, API_KEY, label=None, term=None, courses=None):
        self.canvas = Canvas(API_URL, API_KEY)
        if courses is None:
            if label is None:
                self.label = str(input("Input course code label (e.g. LIFE): ")).upper()
            else:
                self.label = label
            if term is None:
                self.term = str(input("Input term (e.g. 202223): "))
            else:
                self.term = term
            self.courses = self.get_courses()
        else:
            self.courses = courses
    
    def get_courses(self):
        courses = []
        for x in tqdm(
            range(100, 1000),
            desc="Getting courses from Canvas"
        ):
            try:
                course = self.canvas.get_course(
                    "{0}{1}-{2}".format(self.label, str(x), self.term),
                    use_sis_id=True
                )
                courses.append(course)
            except:
                continue
        return courses
    
    def get_assignments(self, key, value, update_key=None, update_value=None):
        assignments = []
        
        for course in tqdm(self.courses, desc="Getting assignments"):
            course_assignments = [x for x in course.get_assignments() if x.__dict__[key] is not None]
            assignments.extend(
                [x for x in course_assignments if value in x.__dict__[key]]
            )
        
        if update_key is not None and update_value is not None:
            updated_assignments = []
            for assignment in assignments:
                updated_assignments.append(assignment.edit(assignment={update_key: update_value}))
            return updated_assignments
            
        return assignments
    
    def get_modules(self, key, value, update_key=None, update_value=None):
        modules = []
        
        for course in tqdm(self.courses, desc="Getting modules"):
            course_modules = [x for x in course.get_modules() if x.__dict__[key] is not None]
            modules.extend(
                [x for x in course_modules if value in x.__dict__[key]]
            )
        
        if update_key is not None and update_value is not None:
            updated_modules = []
            for module in modules:
                updated_modules.append(module.edit(module={update_key: update_value}))
            return updated_modules
            
        return modules
            
        


# In[112]:


canvas_objects = MultiCanvas(API_URL, API_KEY, label="LIFE", term="202223")


# In[117]:


assignments = canvas_objects.get_assignments("due_at", "2023-01-23")


# In[119]:


modules = canvas_objects.get_modules("unlock_at", "2023-01")


# In[120]:


len(modules)


# In[ ]:




