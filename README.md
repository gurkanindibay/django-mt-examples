Sample Application for Django Multitenant

Installation

1. Install the dependencies
    ```
    pip install -r tutorial/requirements.txt
    ```
2. Start the database
    ```
    docker-compose --project-name django-multitenant up -d || { docker-compose logs && false ; }
    ```
3. Execute migrations
    ```
    ./migrate.py migrate
    ```
4. Start the application
    ```
    ./migrate.py runserver
    ```
5. Open the rest app UI
    ```
    http://localhost:8000/
    ```
6. Login with the turkiye_user and usa_user consecutively and see the projects and accounts are totally isolated. You can check the data in migrations 



