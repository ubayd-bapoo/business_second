# Business Second
Will provide an API end point that will calculate the total number 
of business seconds between two given times. Due to the simplicity 
of the task we will be using Flask for the web application.

A business second is defined as any whole second that elapses 
after 08:00 and before 17:00 during a weekday (Monday - Friday) 
that is not a public holiday in the Republic of South Africa. 
The end point supports only list GET requests and will take 
two parameters: start_time and end_time. Parameter values will be 
in ISO-8601 format. The start_time must be before end_time. The end 
point must respond with only a single integer value for successful 
requests or a suitable error message string for failed requests.

end point url: "/api/v1/bus_sec"

## Installation
### Requirements
Python 3.7
Virtualenv

### Setup
Once Python is installed. Install virtualenv via pip so that all 
dependencies are stored inside the virtual environment.

In the command line run the following command:
```bash
pip install virtualenv
```

Create virtual environment using the following command:
```bash
virtualenv venv_business_second
```

Activate the virtual environment. On Windows use the following.
```bash
venv_business_second\Scripts\activate.bat
```

Install the required packages, using pip and the requirements file.
```bash
pip install -r requirements.txt
```

Run the test.py file using the following command:
```bash
python test.py
```

If it ran without any errors then you are already for development.

## Running the web service
In the command line run the following command:
```bash
python main.py
```

You can hit the end point with the following URL:
[localhost:5000/api/v1/bus_sec](localhost:5000/api/v1/bus_sec)
