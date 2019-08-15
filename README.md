# Moneybook
this is a project for keeping records of debtors and their invoices.
## Setting Configurations
#### Google Login Configuration 
In order to login the website with google account, authorization key and autharization secret token from google developer console must be set inside the project settings file.

`SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '<client_id>'`

`SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = '<client_secret>'`

To obtain client_id and secret, Go to the [Google Developers Console](https://console.developers.google.com/apis/library?project=_) and 
then click on create button.
Enter project name e.g 'Django App'. Wait for a few seconds your project should be created.

On the right side there is credentials tab, select it.

Click on Create Credentials then OAuth Client ID. Select the application type Web
 app, Give any name of your choice and Enter any name in 'Product name shown to users' under OAuth Consent Screen tab.

Enter the following URI's in Authorized redirect URIs (or domain name instead of localhost)

`http://localhost:8000/auth/complete/google-oauth2/`

`http://127.0.0.1:8000/auth/complete/google-oauth2/`

Now click on library under the APIs and services tab and then search for google+, in the
 search results click on Google+ API and then click Enable.

Now, Copy the Client ID and Client Secret and paste it to settings.py.

#### Database Configuration

If you will run the project in your local development environment instead of docker,
you should configure database connection settings inside `settings.py`.

## Running The Project
### Running With Docker-Compose
docker compose file contains three images, theese are:
 - the project's image (moneybook)
 - postgresql 10
 - pgadmin 4
 
If you don't think pgadmin will be necessary, you can delete it from compose file.
In order to run project with docker, just run docker-compose,

`docker-compose up`

or to run detached from shell:

`docker-compose up -d`

and now the project should be accessible from http://127.0.0.1:8000

If you run docker-compose, pg admin shoud be running at http://127.0.0.1:5050. 
To login pgadmin, username is `pgadmin4@pgadmin.org` and the password is `admin`.

To connect project's database from pgadmin:

right click to `servers`, `create`,`Server...`
 Give a name to db, like debtors etc. In the connection tab,
 `host name: db`, `port: 5432`, `username: postgres` and the password is empty. Now you can connect to 
 database in the docker.
 
 To stop docker compose:
 `docker-compose stop`
 
 To delete images:
 `docker-compose down`
 
 ### running from local development environment
 
 Python 3 is used for this project and it is required.
 
 To create virtual environment:
 
 If you don't have virtual environment package in your computer,
 
 `pip install virtualenv`

To create virtual environment in the project,

 `python3 -m virtualenv venv`
 
 A virtual environment for python3 should be created. In order to activate it,
 
 `source venv/bin/activate`

Now, to install required packages for the project:

`pip install -r requirements`

After the installation is finished, we need to make the database migration of the project.

`python manage.py migrate`

Now, project is ready to go! Just type

`python manage.py runserver`

## Using The Api

The project api runs with token authantication. To obtain token to use api,
open the website in the browser, navigate to API page, and `Get Api Key`.
You need to send this api key with each request in the header.

`Authorization: Token <api_key>`

To make filtering and ordering to results, all parameters should be added to end of the endpoint. You can do sorting for
 the any field in the result set. For example:

`<host_name>/api/v1/debtors/?first_name=foo&last_name=bar&ordering=email`

to make ordering descending, put a minus sign:`?ordering=-pk`


If you don't want to get paginated response, just put limit at the end of url

`<host_name>/api/v1/debtors/?limit=99999`

#### Debtors
Endpoint for the debtor api is:

`<host_name>/api/v1/debtors/`

available filters are:

- first_name
- last_name
- iban
- responsible_admin (pk of the user is required)
- invoice_count
- invoice_status

sample response:
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "cancelled_invoices": 0,
      "email": "foo@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "iban": "zLmHdZdTOnUsYbtOHcYfSvzYbCRvxPcJJN",
      "open_invoices": 0,
      "overdue_invoices": 0,
      "paid_invoices": 2,
      "pk": 72
    }
  ]
}
```

#### Invoices

Endpoint for the invoice api is:

`<host_name>/api/v1/invoices/`

Available filters are:
- status
- amount
- due_date (YYYY-MM-DD)
- debtor_mail

sample response:
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "amount": "12.12",
      "status": "OPEN",
      "due_date": "2019-08-19",
      "debtor": 1,
      "debtor_email": "random@example.com"
    }
  ]
}
```
