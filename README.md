# LiteConnect
A basic social networking/blogging website

The website is written in Django 2.1 (using python3 of course). The website has basic functionality that any social networking website does, including - 
1. Follow/Unfollow other users (if you follow foobar, foobar's posts will appear in the newsfeed)
2. Write posts
3. Allow users to delete/edit their own posts.
4. Store post edit history (so that nobody gets away with posting offensive content)
5. Subscribe to users (When you subscribe to a user foobar, you will get an email notification whenever foobar makes a post)
6. Allow users to change their profile information.
7. Allow users to change their passwords.
8. Allow users to upload a profile photo.
9. Comment on posts 
10. View other users' profiles

The frontend of the website is basic and minimal.
If you want to run this website on Django's development server (python manage.py runserver), you'll need to do the following - 
1. Create a virtualenvironment (python3 -m venv /path/to/folder/virtual/environment/directory) and activate it (source /path-to-venv/bin/activate)
2. Install Pillow (pip3 install Pillow)
3. Install Django Allauth (pip3 install django-allauth)
4. Install Social_Django (pip3 install social-auth-app-django)
5. Install Bootstrap 3 (pip3 install django-bootstrap3)
6. Install Openpyxl (pip3 install openpyxl)

Along with that, you also need to configure the settings.py file to use sqlite3 as your database (for development purposes only!). In production, I have used MySQL instead of sqlite3.
