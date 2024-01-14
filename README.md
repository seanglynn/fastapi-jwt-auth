<h1 align="left" style="margin-bottom: 20px; font-weight: 500; font-size: 50px; color: black;">
  FastAPI JWT Auth
</h1>


1. Copy environment configuration and update config  
    ```sh
    cp example.env .env
    ```
   
1. Install the requirements:

    ```sh
    poetry install -v
    ```

1. Init python environment:
    ```sh
    poetry shell
    ```

1. Run the app:

    ```sh
    python main.py
    ```

1. Test at [http://localhost:8080/docs](http://localhost:8080/docs)

1. Get bearer token by logging in with expected client configuration:

    ```sh
    curl -X 'POST' \
     'http://localhost:8080/client/login' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{"team_name": "ateam", "client_id": "123456789", "client_secret": "weaksecret"}'
    ```
1. Use the bearer token returned from the last step to authenticate with protected endpoints.

   ```sh
   curl -X 'POST' \
     'http://localhost:8080/posts' \
     -H 'accept: application/json' \
     -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOiIxMjM0NTY3ODkiLCJleHBpcmVzIjoxNzA1MjU3MDAyLjEyMjIxNDh9.MwOF8WhIwSbiiqVZ_q6J-HHZbyUavx1Di-I7_CtT-vQ' \
     -H 'Content-Type: application/json' \
     -d '{
     "id": 0,
     "title": "string",
     "content": "string"
   }'
   ```