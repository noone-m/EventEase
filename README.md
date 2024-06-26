# EventEase : Simplify Event Planning with Streamlined Booking
EventEase empowers events creation process by granting you access to a comprehensive suite of booking services, eliminating the need to juggle multiple vendors. From finding the perfect venue and caterer to securing a DJ and other amenities, EventEase streamlines the entire event planning process, saving you time and effort.
## How to integerate with the APIs?

To integrate with the EventEase API, you'll need to install postgreSQL using their official website : https://www.postgresql.org/download/

install Python on your system. You can typically find installation instructions on the official Python website: https://www.python.org/downloads/
Once you have Python set up, proceed with creating virtual environment.

create a virtual environment on windows using:
```bash
python -m venv <environment_name>
```
**then activate the venv**
```bash
   <name-of-your-env>\Scripts\activate.bat
```
**clone the repo**
```bash
git clone https://github.com/noone-m/EventEase.git
```

**install required dependencies**
```bash
pip install -r requirements.txt
```
**Create a new database:**
```bash
createdb exampledb
```

**Import the schema:**
```bash
psql -U yourusername -d exampledb -f schema.sql
```
**Import the data:**
```bash
psql -U yourusername -d exampledb -f data.sql
```

**Important Note:** 

Your Django project relies on environment variables for secure operation. You'll need to create a `.env` file in your project's root directory to configure these variables.

**1. Create a `.env` File:**

Using a text editor, create a new file named `.env` in the root directory of your project. This file should **not** be added to version control (e.g., Git).

**2. copy `.env.example` to `.env` then fill variables with your specific values.**

**launch the development server** 
```bash
py manage.py runserver
```
