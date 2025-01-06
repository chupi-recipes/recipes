# recipes
Work in progress

## Dev env

From root
1. `python -m venv`
2. `pip install -r requirements.txt`

### Local server

1. python -m http.server
2. `Remove-Item -Path "./dist/*" -Recurse -Force; Copy-Item -Path "./public/*" -Destination "./dist" -Recurse -Force; python ./src/generate.py`
3. http://localhost:8000/dist/index.html
