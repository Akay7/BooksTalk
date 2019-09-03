## Readme

### What is it

This is repo of simple Facebook messenger bot.

### What it can do
1. Welcome the user by using their first name.
2. Ask the user if they want to search books by name or by ID (Goodreads ID). 
3. Use Goodreads API to search books.
4. Retrieve a maximum of 5 books and let the user select one of them. 
4. Retrieve the selected book’s reviews from Goodreads and use IBM Watson to do a semantic analysis for the most recent reviews. 
6. Suggest the user if they should buy the book or not based on the semantic analysis done in the previous step.  

### Local development

1. You must have installed python 3.6.
2. Then call command 

    `pip install -r requirements/tests.txt` 
    
3. You must copy file and update settings, for not stuck with environment variables
    
    `cp books_talk/books_talk/settings/container.py books_talk/books_talk/settings/dev.py`
    
 4. And then run with command 
 
    `python books_talk/manage.py runserver --settings=books_talk.settings.dev`

### Run BooksTalk in docker container

1. Build image

    `docker build . --tag books-talk`

2. Run container and proxy port to localhost

    ```
   docker run --rm -it -p 8000:80 \ 
        -e ENV_VARIABLE=VALUE \ # don't forget add all necessary environment variables
        books-talk
   ```
