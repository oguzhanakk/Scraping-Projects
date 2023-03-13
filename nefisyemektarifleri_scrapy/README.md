# nefisyemektarifleri_scrapy
It is a python program that, when you give a category name on https://www.cimri.com/, goes to that category and scans all its pages and extracts data such as the relevant date, product name, product price, brand, and if you do not provide a category, it extracts data for all main and sub-categories. After the given is imported, it transfers it to the Postgre database. After connecting to lambda in aws the log will be up and running.

# Requirements
To run this project, you will need to have the following software requirements:

• scrapy
• postgre
• pandas
• flask

# Setup
To run this project on your own computer, follow these steps:

1. Clone or download this repository.
2. Install the requirements. For example: pip install -r requirements.txt
3. Run main.py to run the project.

# Contributing
If you would like to contribute to this project, please follow these steps:

1. Fork this repository.
2. Make the desired changes.
3. Commit and push your changes.
4. Create a pull request.