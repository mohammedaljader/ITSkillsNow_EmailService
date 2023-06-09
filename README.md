# ITSkillsNow_EmailService
Email service is responsible for sending emails to users in ITSkillsNow application. 
## Table of Contents
- [Contributors](#contributors)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Testing](#testing)
- [Acknowledgments](#acknowledgments)


## Contributors
- [Mohammed Aljader](https://www.linkedin.com/in/mohammed-aljader-12a376162/)

## Prerequisites
Make sure you have the following prerequisites installed:
- IDE: [PyCharm](https://www.jetbrains.com/help/pycharm/installation-guide.html) or [Visual Studio Code](https://code.visualstudio.com/download)
- [Python (version 3.7 or higher)](https://www.python.org/downloads/)
- [pip (Python package installer)](https://pip.pypa.io/en/stable/installation/)
- [RabbitMQ image on docker](https://hub.docker.com/_/rabbitmq)

## Installation
1. Clone the repository to your local machine:
   ```
   https://github.com/mohammedaljader/ITSkillsNow_EmailService.git
   ```
2. Navigate to the project directory:
   ```
   cd ITSkillsNow_EmailService
   ```
3. Install the project dependencies:
   ```
   pip install -r requirements.txt
   ```
## Usage
- Run RabbitMQ image. 
- Start the FastAPI server:
  ```
  uvicorn main:app --reload
  ``` 
  or
  ```
  main.py
  ```
- Once the server is running, you can access the API at http://localhost:8000 in your browser or any REST client tool.
- You can open Swagger UI http://localhost:8000/docs

## Testing
To run the tests for this project, execute the following command:
```
pytest
```

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com) - The web framework used in this project.
