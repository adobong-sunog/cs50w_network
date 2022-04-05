# CS50W Project 4 - Network
Status: **INCOMPLETE**
  
## Description
* [Project specification](https://cs50.harvard.edu/web/2020/projects/4/network/#specification)
* **[Django](https://www.djangoproject.com) is used as web framework** and SQLite as the database.

## Setup 
> Python, [Git](https://git-scm.com) and [Django](https://www.djangoproject.com) must be installed on your computer

Clone this repository
```bash
git clone https://github.com/AncientSoup/cs50w_network/
cd cs50w_network
```  
Install any required dependencies
```bash
pip install -r requirements.txt
```  
Setup the database
```bash
python manage.py makemigrations
python manage.py migrate
```
Run the development server through the terminal
```bash
python manage.py runserver
```
  
## Note on academic honesty
If you're taking CS50W, either through [Harvard Extension School](https://extension.harvard.edu/), [Harvard Summer School](https://summer.harvard.edu/) or [OpenCourseWare](https://cs50.harvard.edu/web/), please do not blindly copy paste my code. You are putting yourself at a huge risk for getting excluded from the course by the staff themselves as they grade each project thoroughly. This is a course offered by Harvard, and you will be put up to their standard.
