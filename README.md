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
git clone
```

```shell
python manage.py migrate
```


```shell
python manage.py createsuperuser --username root --email root@localhost
```


```shell
python manage.py pollution_csv_import air_pollution/data/air-pollution.csv
```

## 

https://www.sqlite.org/draft/percentile.html

## Possible improvements

- Database can be changed to PostgreSQL/AWS-Aurora for production
- API can be versioned (URL prefix) to allow backward compatibility
- Swagger can be used to document the API as an industry standard
- Cache can be used to improve performance (as the data is static)
- Authentication can be improved to use JWT tokens to allow stateless authentication
- FactoryBoy & Faker can be used to create test data in a more readable and reusable way
- In the Dockerfile we run the server with `python manage.py runserver` which is not recommended for production. We can use Gunicorn or Uvicorn instead.
