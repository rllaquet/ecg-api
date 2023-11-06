# ECG API

### Summary
A simple API to store and retrieve ECG data. Written in Python using FastAPI and 
MongoDB.

### Formatting
ecg_api uses [black](https://black.readthedocs.io/en/stable/) to keep a consistent  
coding style and formatting across the codebase. To format the codebase, run `black .`
from the root of the project.

### Requirements
ecg_api recommends using [docker](https://docs.docker.com/engine/install/) and 
[docker-compose](https://docs.docker.com/compose/install/) to run.

### Testing

#### Using Docker
Both unit and integration tests are containerized and can be run with docker compose —
simply run any of the following commands depending on which tests you want to run:
```bash
docker-compose run unit-tests
docker-compose run integration-tests
```
Both allow reloading the codebase without having to rebuild the container, just run 
the tests again and they'll pick up the changes.

#### Locally
To run locally, you'll need to have Python 3.11+ and all python dependencies installed:

```bash
pip install -r requirements.txt -r requirements-test.txt
```

Environment variables must be set:
```bash
source .env.test
```

Then, to run unit tests, simply run:
```bash
pytest tests/unit
```
In case of integration tests, we'll also need to start a MongoDB instance:
```
docker-compose up -d mongo
MONGODB_URL=mongodb://localhost:27017 pytest tests/integration
docker-compose down
```

### Running

ecg_api is containerized and can be run with docker compose.
To start the API, simply run:
```bash
docker-compose up -d api
```
This will run in the background and will make the API available on http://0.0.0.0:8000/

### Usage

Best way to see how to use the API is to access the OpenAPI docs at 
http://0.0.0.0:8000/docs

An admin user is needed to start, for now you can just run the create_admin.py 
script from inside the container:
```bash
docker exec -ti ecg-local python /utils/create_admin.py
```

A custom username and pass can be set adding the -u and -p flags respectively:
```bash
docker exec -ti ecg-local python /utils/create_admin.py -u myuser -p mypass
```

You can use the authorisation button in the top right corner of the docs to log in, 
this will automatically set the Bearer token for all requests.

The rest of the endpoints should be pretty self documented, even though I didn't do 
proper models for all responses. Creating ECGs can be done by a user, and will only 
be available to fetch for that user. Similarly, creating users can only be made by 
admin users,


### Considerations

This was a test and I didn't go too deep into it — there's much more that could (and 
should!) be done to make this a production-ready service: CI/CD, secrets management, 
logging, monitoring, proper authentication for MongoDB, etc.

Architecture-wise, I deliberately chose to opt for simplicity in a few places that 
could potentially benefit from a more complex solution. For example, in models/ecg.py 
I define simple functions for CRUD operations on ECG objects, but it could be 
beneficial to have an extra layer of abstraction to give more flexibility
(explicit DB schema, simplifying repeated code, adding functionality to all 
operations of the same type, etc.).

I'm also not a FastAPI expert! I've used it on personal projects but never on a huge 
projects, so I'm sure with a bit more hands-on experience I would've been able to 
spot a bunch of points of improvement.

I made a different document that goes more in depth, didn't want to have an 
overwhelming README.md file. You can find it [here](considerations.md).

Thanks for reading!
