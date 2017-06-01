**Stipo - nigthlife gathering SPA, built with Django + React**
----------

Single Page Application experiment for gatherings (in restaurants, cafes etc), using Social authentication.

Objective: Create an app where user can select places to go and also see how many people will be coming.

Built with:

 - **Django**
 - **Django-rest-framework**
 - **Django allauth + Django rest auth**
 - **React**

For project overview and code details, see [here](https://azaleas.aerobatic.io/2017/06/01/stipo---nigthlife-gatherings-application/).

Hosted on [heroku](https://stipo.herokuapp.com). 

For API endpoints, see [here](https://github.com/azaleas/stipo/blob/master/API.md).

For React readme, see [here](https://github.com/azaleas/stipo/blob/master/stipo/frontend/README.md).

----------

**For Local Setup:**

- Install requirements from requirements/local.txt
 - whitenoise can be uninstalled if it's not required (it's recommended for heroku). Also, clear up wsgi.py to avoid any issues:
```
import os

from django.core.wsgi import get_wsgi_application

#Remove this
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stipo.settings")

application = get_wsgi_application()

#Remove this
application = DjangoWhiteNoise(application)
```
- Create a secrets.json file(rename secrets.json.example) and fill in the required keys and values.

- To test emails, **python -m smtpd -n -c DebuggingServer localhost:1025** can be run on a separate console. Port and host definitions are set in local.py.

- Create a secrets.json file(rename secrets.json.example) and fill in the required keys and values.
- Create a website in Django admin panel with proper url for twitter auth. Also add this url to hosts file.
- Create new social application in Django admin for twitter. (See the docs of django-rest-auth for more details)
- **adapter.py** inside polls application takes care of twitter redirect to React. **twitter_login_url** variable is imported from **variables.py**.  It:
 - should be "http://localhost:3000/twitter_logged_in" for local setup with webpack proxy.
 - should be "http://localhost:8000/twitter_logged_in" for local setup with react build completed.
 - should be "http://heroku_app_link/twitter_logged_in" for production.
- **middleware.py** takes care of adding CORS headers for Webpack proxy.
- FrontendAppView serves the index.html, from build folder of React app.
- In react app, set the TWITTER_LOGIN_URL in utils/variables.js to "http://localdjangodomain.com:8000/auth/twitter/login/" {like "http://stipoapp.com:8000/auth/twitter/login/"}

**python manage.py runserver --settings=stipo.settings.local** to run local server

**For Production Setup:**

Production:

 - setup the python runtime in runtime.txt
 - **requirements.txt** takes care of production requirement installs. 
 - Create env variables in Heroku for variables listed in settings/production.py: EMAIL_USER, EMAIL_PASS, SECRET_KEY, DATABASE_URL, ADMIN_USER, ADMIN_EMAIL, YELP_TOKEN, YELP_SECRET.
 - Set DJANGO_SETTINGS_MODULE variable on heroku to stipo.settings.production
 - add production url to ALLOWED_HOSTS.
 - build react with new url (see src/utils/variables.js)
 - Set ADMINS emails.
 - Install postgresql - **heroku addons:create heroku-postgresql:hobby-dev**
 - After pushing the code to heroku, use
    - **heroku run python stipo/manage.py migrate --settings=stipo.settings.production** to create the migrations
    - **heroku run python stipo/manage.py createsuperuser --settings=stipo.settings.production** to create new admin user
	- Create social application via django admin (add heroku domain as new website)
    - For error logs, use **heroku logs**. Emails to admins will be sent if any errors occur. Also, if emails aren't sent, DEBUG setting can be turned on (don't forget to disable it after debugging).
    - For SMTP Yandex mail was used. 

For admin url, check urls.py file. 

**Tests:**

 - stipo/places/tests - for DRF tests
 - frontend/src/tests - for React tests