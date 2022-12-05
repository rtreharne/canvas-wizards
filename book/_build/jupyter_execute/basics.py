#!/usr/bin/env python
# coding: utf-8

# # Basics
# 
# In this section we'll cover:
# + Enrollments
# + Assignments
# + Submissions
# 
# Before we begin, create your `canvas` session variable again by running the cell below with `API_URL` AND `API_KEY` set to your own personal values.

# In[2]:


# Create your Canvas session
from canvasapi import Canvas
API_URL = "https://canvas.liverpool.ac.uk"
API_KEY = "15502~f4Ezll8DlucRLthAlSKTjFqNQeED6FfpId6mZnyS9wvHmYqMHXd8ZJj7AkIjy15K"
canvas = Canvas(API_URL, API_KEY)


# ## Enrollments

# ### Getting all enrollments on a course

# In[3]:


course_id = 0000 # REPLACE 0000 WITH YOUR COURSE ID
course = canvas.get_course(course_id)


# ```{note}
# You can get the course id by going to any course homepage on Canvas and then looking at the last number in the URL string, e.g. for https://canvas.liverpool.ac.uk/courses/60371 the course id is 60371
# ```

# In[ ]:


course.__dict__


# In[4]:


# You can also get a course based on the course_sis_id which is usually the course name as it appears
# in the top left of the course homepage on Canvas. You need to use the additional parameter `use_sis_id` in 
# the `get_course` function, and make sure it's set to True

course = canvas.get_course("<COURSE_SIS_ID>", use_sis_id=True)


# In[5]:


# To get all the enrollments on a course
enrollments = course.get_enrollments()


# The line above will successfully return all enrollments for a course and store them in the variable `enrollments`. However, all the information will stored in an object called a `PaginatedList` which isn't that useful when trying to do stuff in Python. For example, if you want to figure out how many enrollments there are you might try and use the `len()` function (very sensible), but for a `PaginatedList` you'd encounter a `TypeError`.

# In[6]:


len(enrollments)


# To avoid `TypeErrors`, it is recommended that you retrieve list of things from canvas by using the relevant function, in this case `course.get_enrollments()`, within what is known as a "list comprehension" in Python. Without going into any futher detail, the code you need is as follows ...

# In[7]:


enrollments = [x for x in course.get_enrollments()]


# In[18]:


len(enrollments) # That's better!


# Also, you can now slice your list of enrollments, e.g. to pick out a single enrollment from the list to look at it, by doing something like this ...

# In[20]:


# Pick out the first enrollment from the list
enrollments[0]


# To make the data associated with the enrollment a bit more readable you can use the `__dict__` method.

# In[22]:


# Use .__dict__ to print out the dictionary map for the enrollment object. Beatuful!
enrollments[0].__dict__


# You can access any "key value" associated with the enrollment object by using `.<key_name>` on any enrollment object. For example, to get the role associated with any enrollment:

# In[24]:


enrollments[0].role


# In[26]:


enrollments[0].__dict__["user"]


# In[27]:


def get_enrollment_from_key_substring(enrollments, key, substring):
    for e in enrollments:
        if substring in e.__dict__[key]:
            return e
    print("User Not Found")
    return None          


# ### Export course enrollments

# In[12]:


import pandas as pd

rows = []
for e in enrollments:
    row = {
        "user_id": e.user_id,
        "sortable_name": e.user["sortable_name"],
        "role": e.role,
        "course_section_id": e.course_section_id
    }
    rows.append(row)


# In[14]:


enrollments_df = pd.DataFrame(rows, index=False)


# In[15]:


enrollments_df.head()


# In[16]:


enrollments_df.to_excel("course_enrollments.xlsx")


# ## Assignments

# ## Submissions

# In[ ]:




