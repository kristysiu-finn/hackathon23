## Local dev
### Set up env
```
pipenv shell
pip install -r requirements.txt
```
### Set up env var
Create a `.env` file:
```
OPENAI_API_KEY = '<your_key>'
```
### Lauch app
```
uvicorn main:app --reload
```

## Deploy
Follow https://63ed3437f56a5a0b8b5107a3--fastapi.netlify.app/deployment/deta/

```
space login
space new
space push
```