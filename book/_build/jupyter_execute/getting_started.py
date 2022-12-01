#!/usr/bin/env python
# coding: utf-8

# # Getting Started
# 
# ## What is an API?
# 
# An **application programming interface** (API) is a set of stored functions or procedures that allow you get, create or edit data from an application without having to use a graphical interface (e.g. a website). The Canvas API will allow you to do almost anything that you currently do using the standard user interface. 
# 
# The Canvas API is extremely well documented and, while the documentation may seem impenetrable at first, reading the docs can solve most problems. Check it out at <a href="https://canvas.instructure.com/doc/api/" target="_blank">https://canvas.instructure.com/doc/api/</a>.
# 
# *"So what?"* - I hear you say. Well, the power of the API lies with the ability to prepare snippets of code (we're going to use **Python** here) to make use of the API's functions in order to automate repetitive tasks and cut your workload dramatically.
# 
# *"OMG, I have to write code?"*. Well, yes. Get over it. It's really not that bad and this book is going to guide you all the way. Deep breath now, let's dive in.

# ## Setup and Configuration
# 
# There are about a **zillion** different ways that you could create a coding environment in which you can begin your tranformation to Canvas wizard. The best way for you get started will be to click the little *rocket icon* at the top of this page and then click the *Binder* button. You might have to wait a couple of minutes while the environment is created but once it's ready you'll be good to go without having to download or install a single thing. Wizard!
# 
# Or, you can click the *Colab* button and open a notebook using the Google Colab platform for online notebooks. You will also need use the "Copy to Drive" button to run the code on the page - this will require you to login using a Google account.
# 
# If you're hardcore you can click the download button in the top-right and download the .ipynb for each section and run it on your local machine using **Jupyter Notebook**. For advice on how to install Jupyter Notebook checkout <a href="https://www.geeksforgeeks.org/how-to-install-jupyter-notebook-in-windows/" target="_blank">this article</a>.
# 
# ```{note}
# If you're new to all of this then the Binder option above is strongly recommended. 
# ```

# ## Ready for a Test Drive
# 
# OK. I think you're ready to try a few lines of code yourself. Let's start simple. How about trying to get a list of all the Canvas courses you're currently enrolled on? This is pretty easy.
# 
# First, ensure that you've imported the canvasapi module for Python by running the following cell:

# In[1]:


from canvasapi import Canvas


# ```{note}
# 
# If you're using Colab of Jupyter Notebook you'll need to install the canvasapi first using the following command:
# ```
# 
# ```{code}
# !pip install canvasapi
# ```

# In[ ]:





# In[ ]:




