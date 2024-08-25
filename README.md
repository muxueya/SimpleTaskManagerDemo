## Setup and Running Instructions 

### 1. Setting Up a Virtual Environment (Optional but Recommended) 

It's recommended to run your Flask application within a virtual environment to manage dependencies.


```bash
python3 -m venv venv
```

Activate the virtual environment:
 
- On **Windows** :

```bash
venv\Scripts\activate
```
 
- On **macOS/Linux** :

```bash
source venv/bin/activate
```

### 2. Install Required Packages 
Install Flask and other dependencies using `pip`:

```bash
pip install flask flask_sqlalchemy flask_bcrypt flask_login
```

### 3. Initialize the Database 

If you haven’t already created the database, you need to initialize it. Start a Python shell from the command line:


```bash
python
```

Then, run the following commands in the Python shell:


```python
from app import app, db
with app.app_context():
     db.create_all()
exit()
```
This will create the `main.db` SQLite database with the necessary tables.
### 4. Running the Flask Application 
Set the `FLASK_APP` environment variable to point to your Flask application file. If your file is named `app.py`: 
- On **Windows** :

```bash
set FLASK_APP=app.py
```
 
- On **macOS/Linux** :

```bash
export FLASK_APP=app.py
```

To enable debug mode (optional):
 
- On **Windows** :

```bash
set FLASK_ENV=development
```
 
- On **macOS/Linux** :

```bash
export FLASK_ENV=development
```

Run the Flask application:


```bash
flask run
```

This command will start the Flask development server.

### 5. Accessing the Application 
Open your web browser and go to `http://127.0.0.1:5000/` or `http://localhost:5000/` to access your Flask app.
### 6. Stopping the Server 
To stop the Flask server, press `CTRL+C` in the terminal where the server is running.