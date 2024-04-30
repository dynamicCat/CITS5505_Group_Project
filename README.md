# CITS5505_Group_Project

## Project Introduction
RequestHub is an interactive web platform that allows users to create accounts, post requests, and answer other users' requests. You can post requests, solve problems, and interact with the community here. The purpose of this application is to provide users with a fun and useful platform to enhance communication and collaboration through various forms of requests and responses.

### Main features
- **User account management**: Users can register and log in to manage their own profile. 
- **Create requests**: Users can create requests based on their own questions. 
- **Find and accept requests**: Users can browse existing requests and choose to accept the challenge or provide help. 
- **Interactive elements**: Users can communicate including leaving comments and expressing likes.

## Group Member
| Student ID | Student Name | GitHub Name |
|----------|-------------|---------------|
| 24065267 | Zhenhao Zhu | dynamicCat    |
| 23797775 | Zihan Peng | ZihanPeng      |
| 23769386 | Yuchen Wang |        |
| 23964581 | Renjun Liu |         |

## Application Architecture

This application uses Flask as the backend framework and uses SQLite database for data management through SQLAlchemy. The front end uses HTML, CSS, and Bootstrap for style design, and JQuery and AJAX for dynamic content loading. Websockets is used for real-time interactive functions. 

### Technology Stack

- **Front-end**: HTML, CSS, Bootstrap, JQuery
- **Back-end**: Flask, Websockets
- **Database**: SQLite (via SQLAlchemy)

## Start the application

To start the application locally, follow these steps:
1. Clone the repository:
   \```bash
   git clone https://github.com/dynamicCat/CITS5505_Group_Project.git
   \```
2. Install dependencies:
    \```bash
    pip install -r requirements.txt
    \```
3. Run the application:
    \```bash
    flask run
    \```
4. Visit `http://localhost:5000` in your browser to get started. 

## Run the test
