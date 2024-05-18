# CITS5505_Group_Project

## Project Introduction
RequestHub is an interactive web platform that allows users to create accounts, post requests, and answer other users' requests. You can post requests, solve problems, and interact with the community here. The purpose of this application is to provide users with a fun and useful platform to enhance communication and collaboration through various forms of requests and responses.

### Main features
- **Introduction page**: Users can learn more about the application on this page.
- **User account management**: Users can register and log in to manage their own profile. 
- **dashboard**.
- **Create requests**: Users can create requests based on their own questions. 
- **Find and accept requests**: Users can browse existing requests and choose to accept the challenge or provide help. 
- **Answer Request**: Users can answer received requests.
- **Set personal information and user avatar**: Users can reset the user name and user email. Users can also search for images to set their avatar. 
- **Search information**: Users can search for Wikipedia information they want to know through the search bar on the answer interface.
- **Interactive elements**: Users can communicate including leaving comments and expressing likes.
- **Using flask wtform and flask login modules**: User data security is ensured through these two modules.





## Group Member
| Student ID | Student Name | GitHub Name |
|----------|-------------|---------------|
| 24065267 | Zhenhao Zhu | dynamicCat    |
| 23797775 | Zihan Peng | ZihanPeng      |
| 23769386 | Yuchen Wang | kkglovemy       |
| 23964581 | Renjun Liu | Ethaicraft |

## Application Architecture

This application uses Flask as the backend framework and uses SQLite database for data management through SQLAlchemy. The front end uses HTML, CSS, and Bootstrap for style design, and JQuery and AJAX for dynamic content loading. Websockets is used for real-time interactive functions. 

### Technology Stack

- **Front-end**: HTML, CSS, Bootstrap, JQuery
- **Back-end**: Flask, Websockets
- **Database**: SQLite (via SQLAlchemy)

## Start the application

To start the application locally, follow these steps:
1. Clone the repository:
```bash
git clone https://github.com/dynamicCat/CITS5505_Group_Project.git
```

2. Install dependencies:   
Before starting the program, you can create a file called ".env" in the root directory. Its purpose is to define the "SECRET_KEY" and "DATABASE_URL" content required by the application to store database encryption and storage.
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
flask run
```
4. Visit `http://localhost:5000` in your browser to get started. 

## Run the test

To ensure that the application is working correctly, you can run the provided unit tests and functional tests. There are three main test scripts: `test_models.py`, `test_routes.py`, and `test_selenium.py`.

### 1. test_models.py
This script tests the application's models to ensure they function as expected. 

#### Example Test Cases:
- User creation and password hashing.

#### Running the Test:
```bash
python3 -m unittest tests/test_models.py
```

### 2. test_routes.py
This script tests the application's routes to ensure they return the correct responses.

#### Example Test Cases:
- Home route returns status code 200 and contains 'Welcome' text.

#### Running the Test:
```bash
python3 -m unittest tests/test_routes.py
```

### 3. test_selenium.py
This script uses Selenium to perform functional tests by simulating user interactions with the application.

#### Requirements:
- Google Chrome browser
- ChromeDriver (compatible with your version of Chrome)

#### Setting Up ChromeDriver:
ChromeDriver can be installed using the `webdriver_manager` package, which is already included in the `requirements.txt`.

#### Example Test Cases:
- Logging in with incorrect and correct credentials.
- Navigating through different parts of the application.
- Verifying responsiveness of the application.

#### Running the Test:
```bash
python3 tests/test_selenium.py
```
### Notes:
- Ensure that the Flask application is running locally before executing Selenium tests.
- The Selenium tests open a browser window and perform actions on the application, so you might see browser windows opening and closing during the test.

By following these steps, you can run the tests to verify that the application is functioning correctly. If any tests fail, review the test output for details on what went wrong and adjust the code as necessary.
