"""
Robocorp Task for Extracting News Articles

This file contains a Robocorp task function `extract_news_from_website` that interacts with the 
Robocorp work item system to extract news articles from a website. It uses the `main` function 
from the `main` module to perform the extraction based on parameters obtained from the current 
work item payload.

The task function:
- Retrieves the search phrase, categories, and time frame from the work item payload.
- Calls the `main` function with these parameters to execute the news extraction process.

Dependencies:
- `robocorp.tasks`: For defining the task and interacting with Robocorp's task framework.
- `robocorp.workitems`: For accessing the current work item and its payload.
- `main.main`: The main function to perform the news extraction, imported from the `main` module.

Usage:
- This script is intended to be used as part of a Robocorp automation workflow, where it 
  extracts news articles based on dynamically provided parameters.
"""
from robocorp.tasks import task
from robocorp import workitems
from main import main
@task
def extract_news_from_website():
    """
    Extract news articles from a website based on the provided parameters.

    This function is defined as a Robocorp task and is responsible for extracting news articles 
    from a website using the `main` function from the `main` module. It retrieves the parameters 
    for the extraction (search phrase, categories, and time frame) from the current work item 
    payload and passes them to the `main` function to execute the extraction process.

    Robocorp Task:
    - Decorated with the `@task` decorator to be recognized as a Robocorp task.

    Parameters:
    - Retrieves the following from the work item payload:
    - `phrase` (str): The search phrase to filter the news articles.
    - `categories` (str): The category to filter the news articles.
    - `month` (int): The time frame in months to consider for the news articles.

    Returns:
        None: This function does not return any value. It triggers the news extraction process 
        based on the provided parameters.
    """
    item = workitems.inputs.current
    phrase = item.payload.get("phrase")
    categorys = item.payload.get("categories")
    month = item.payload.get("month")
    main(phrase, categorys, month)
    