# newspaper-agency-system
___
## Description
This project helps users track newspapers, their topics and assigned redactors.

DB structure:
![DB_structure](documentation/Newspaper_Agency.png)

Home page:
![Home_page](documentation/Home.PNG)

Topic list page:
![Topic_list](documentation/Topic_list.PNG)

Topic create page:
![Topic_create](documentation/Topic_create.PNG)

Topic update page:
![Topic_update](documentation/Topic_update.PNG)

Topic delete page:
![Topic_delete](documentation/Topic_delete.PNG)

Newspaper list page:
![Newspaper_list](documentation/Newspaper_list.PNG)

Newspaper detail page:
![Newspaper_list](documentation/Newspaper_detail.PNG)

Newspaper create page:
![Newspaper_create](documentation/Newspaper_create.PNG)

Newspaper update page:
![Newspaper_update](documentation/Newspaper_update.PNG)

Newspaper delete page:
![Newspaper_delete](documentation/Newspaper_delete.PNG)

Redactor list page:
![Redactor_list](documentation/Redactor_list.PNG)

Redactor detail page:
![Redactor_list](documentation/Redactor_detail.PNG)

Redactor create page:
![Redactor_create](documentation/Redactor_create.PNG)

Redactor update page:
![Redactor_update](documentation/Redactor_update.PNG)

Redactor delete page:
![Redactor_delete](documentation/Redactor_delete.PNG)

Login page:
![Login](documentation/Login.PNG)

Logout page:
![Logout](documentation/Logout.PNG)

404 page:
![404](documentation/404.PNG)
___
## Check it out
[Newspaper agency system project deployed to Render](https://newspaper-agency-system-wpx6.onrender.com)

To view the website, use this user:
```
login: user
password: user12345
```
___
## Installation
1. Clone the repository:
```
git clone https://github.com/bknyrik/newspaper-agency-system.git
```
2. Create a virtual environment `python -m venv .venv`;
3. Activate the virtual environment:
    - Windows - `newspaper_agency_system\Scripts\activate`;
    - macOS/Linux - `source newspaper_agency_system/bin/activate`.
4. Install all dependencies `pip install -r requirements.txt`;
5. Apply migrations `python manage.py migrate`;
6. Run the server `python manage.py runserver`
___
## Usage
Visit `http://127.0.0.1:8000/` in your browser to use the application. And also don't forget to create a superuser:
```python manage.py createsuperuser```
## Contact
Email: knyrikkolesnichenko2004@gmail.com
