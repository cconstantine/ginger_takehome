# Ginger Engineering Test Project

### TODO

 - [x] Create django project / app
 - [x] Load arxiv article and author data into database
   - Use the arxiv pip package to simplify api access
   - Load data into local database to eliminate unnecessary api calls arxiv
   - Do this in a simple cli for now, allow usage in future periodic background jobs
   - The listed topics don't map clealy to categories in arXiv, so I've made up a query
 - [x] Make pages for listing and showing articles
 - [x] Make pages for listing and showing authors
 - [x] Linkify authors <-> articles in author and article pages
 - [ ] Add styles to html


## How to run

## Prerequisites

To run this example you need to have docker and docker-compose installed.  See https://docs.docker.com/get-docker/ for more details.

## Build basic runtime environment

``` sh
host-$ ./scripts/run.sh dev /bin/bash  # Build development image and run docker-compose dev environment
cont-$ pip install -r requirements.txt # Install python deps
cont-$ python manage.py migrate        # Build and migrate database
```

## Run tests
``` sh
cont-$ python manage.py test
```

## Populate database with articles and authors from arXiv and run dev server
``` sh
cont-$ python manage.py populate_from_arxiv
cont-$ python manage.py runserver 0.0.0.0:8000
```

Then go to http://localhost:8000/vixra to see a gloriously unstyled product.


