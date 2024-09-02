# HVV tender Presale test task for a backend developer

## Task

### Infrastructure (applies to both lots, frontend and backend)

Please provide a codebase that is versioned in GitHub/GitLab. 

For demonstration purposes, a dev branch is sufficient. Provide a CI/CD pipeline that carries out
automated tests after accepting a merge request on the dev branch. Only if all tests pass is the
application built and stored in a container repo. A few tests are sufficient as an example.

### Lot 1: Frontend

is not a part of this repository

### Lot 2: Backend

Specify a REST API that provides air pollution data accessible. (https://www.kaggle.com/datasets/rejeph/air-pollution)
Provide endpoints that expose the average, median, and standard deviation for each country and
year for the metrics contained in the dataset. Implement the REST API in Python or Go.

Outline how you would protect access to the API from unauthorized access.

## Solution

### Stack

For the solution was used a stack of technologies that are listed below:
- Python 3.11
- Django 5
- Django REST Framework 3
- SQLite (to make it easier to implement without production-level database)
- tailslide package (to calculate percentiles), but with some limitations

### Our vision

According the task:
> Provide endpoints that expose the average, median, and standard deviation for each country and
year for the metrics contained in the dataset

- We decided to use one endpoint to provide all the data by one request. 
- As we have unique pair of Country/Year and average, median, and standard deviation are informative for several rows: 
  - we decided to calculate this metrics for each country for all years.
  - we decided to use a nested structure to represent the data.

According to the second part of the task:
> Outline how you would protect access to the API from unauthorized access.

As we do not have any information about the requirements, we decided to use a simple solution:
- We used the default DRF authentication parameters (BasicAuthentication and SessionAuthentication)


### Local deployment

Clone the repository
```shell
git clone https://github.com/ilya-ibulaev-at-sloboda/ps_hvv_tender_backend.git
```

Create a virtual environment
```shell
python3 -m venv .venv
```

Install the requirements
```shell
pip install -r requirements.txt
```

Apply the migrations
```shell
python manage.py migrate
```

Create a superuser for the Django admin (optional) if you want to control imported data
```shell
python manage.py createsuperuser --username root --email root@localhost
```

Import the CSV data from the built-in dataset from the repository
```shell
python manage.py pollution_csv_import air_pollution/data/air-pollution.csv
```

Run the server
```shell
python manage.py runserver
```

### API documentation

The DRF browsable API is available at the same URL as the endpoints. 
So if we have our api on URL http://localhost:8000/air-pollution/entity/Germany/ 
we can see the browsable API on http://localhost:8000/air-pollution/entity/Germany/


### Local testing

Run the tests
```shell
python manage.py test
```

### Found issues on local

The tailslide package has some limitations for the percentile calculation using SQLite on MacOS.
https://www.sqlite.org/draft/percentile.html
So the Median calculation is not implemented in the current version of the solution. (The code is commented out)
It will work ok with PostgreSQL or MySQL, or with the SQLite on Linux.
But to keep solution simple and easy to deploy we decided to remove the Median calculation and 
use only Average and Standard Deviation using SQLite.

### Remote deployment

According to the task:
> Please provide a codebase that is versioned in GitHub/GitLab. 

> For demonstration purposes, a dev branch is sufficient. Provide a CI/CD pipeline that carries out
> automated tests after accepting a merge request on the dev branch. Only if all tests pass is the
> application built and stored in a container repo. A few tests are sufficient as an example.

We have a GitHub Actions workflow that 
- runs tests on every PR and on every push to the main branch.
- builds a Docker image on every push/merge to the main branch.

So the tests are run on every PR and on every push to non-accepted PRs.


## Possible improvements

- Database can be changed to PostgreSQL/AWS-Aurora for production
- API can be versioned (URL prefix) to allow backward compatibility
- Swagger can be used to document the API as an industry standard
- Cache can be used to improve performance (as the data is static)
- Authentication can be improved to use JWT tokens to allow stateless authentication
- FactoryBoy & Faker can be used to create test data in a more readable and reusable way
- In the Dockerfile we run the server with `python manage.py runserver` which is not recommended for production. We can use Gunicorn or Uvicorn instead.
- For GitHub Actions we can add more tests and linters to improve the quality of the code
