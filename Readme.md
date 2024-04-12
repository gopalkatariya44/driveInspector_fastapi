clone repo
```commandline
git clone https://github.com/gopalkatariya44/driveinspector_fastapi.git
```

create virtual env
```commandline
python -m venv venv
```

activate the venv

install requirements.txt
```commandline
pip install -r requirements.txt
```

change .env file like mongo url and other details

run main.py file
```commandline
python main.py
```

go to http://localhost:8000


### DEMO
<img src="static/demo/home.png">
<img src="static/demo/vehicle_details.png">
<img src="static/demo/login.png">
<img src="static/demo/register.png">


#### Mongodb
```commandline
brew services start mongodb-community@7.0
```

```commandline
brew services stop mongodb-community@7.0
```