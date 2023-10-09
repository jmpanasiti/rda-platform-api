# Plataforma web RDA Mobility

## Environment Settings
### Dependencies
* Python 3.10+
* MySQL 8.0

### Setup
1. **Create and activate a virtual env for this python project:** I recomend to use pyenv, but you can use the python native venv module.
2. **Install dependencies**: Depending of the environment that you are configuring you must install from the file `requirements.txt` or from the file `requirements-dev.txt`
    * `pip install -r requirements.txt`
    * `pip install -r requirements-dev.txt`

3. **Run the server**: Just run:
    * `uvicorn server.app:app --reload --host 0.0.0.0`
    * The `reload` flag is for the hot-reloading of the server when some file changes. ***THIS IS ONLY FOR DEVELOPMENT ENVIRONMENTS***

## Project file structure
```
project/
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── __init__.py
├── logs/
│   └── *.log files
├── tests/
│   └── test_*.py files
├── .env.example  # An example of a .env file with the needed variables
├── README.md
├── requirements.txt
├── requirements-dev.txt
└── main.py
```
