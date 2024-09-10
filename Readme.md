# DriveInspector - Automated Vehicle Regulation System

## Project Overview
**DriveInspector** is an automated vehicle regulation system that enhances road safety through real-time vehicle number plate detection using computer vision and Optical Character Recognition (OCR). This system improves regulatory efficiency and contributes to safer roads.

## Key Features
- **Number Plate Detection:** Integrated YOLO for real-time detection of vehicle number plates.
- **Optical Character Recognition (OCR):** Used PaddleOCR for text recognition from number plates.
- **Backend:** Built with FastAPI, integrated with MongoDB for storing and managing vehicle data.

## Technologies Used
- **Computer Vision:** YOLO
- **OCR:** PaddleOCR
- **Backend Framework:** FastAPI
- **Database:** MongoDB
- **Programming Language:** Python

## Installation

- create virtual env with `python3.10.14`
```commandline
python -m venv venv
```

- activate the venv

- install requirements.txt
```commandline
pip install -r requirements.txt
```

- change .env file like mongo url and other details

- run main.py file
```commandline
python main.py
```

go to http://localhost:8000

- testing videos `static/demo/videos`

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
