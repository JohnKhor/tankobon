# tankobon
Browse the covers of Shonen Jump manga

# Getting Started
## Downloading Covers
Switch to parser directory
```
cd parser
```

If using pip:
```
pip install -r requirements.txt
```

If using Pipenv:
```
pipenv install
pipenv shell
```

Run the script
```
python 01_shonenjump.py
```

Move the covers to web app
```
mv img/* ../src/static/img
```

Remove unused stuff
```
rmdir img
rm data.json
```

Back to root directory before doing installation in next section
```
cd ..
```

## Installation
If using pip:
```
pip install -r requirements.txt
```

If using Pipenv:
```
pipenv install
pipenv shell
```

Start local development server
```
set FLASK_APP=src/app.py
set FLASK_ENV=development
flask run
```
