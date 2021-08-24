# pact-example
End-to-end contract testing example using PACT for Python provider and JavaScript consumer

This example is based on the [pact-js e2e example](https://github.com/pact-foundation/pact-js/tree/master/examples/e2e). We extend the pact-js example, by adding Python provider. Python provider exposes similar functionality to the provider from JavaScript e2e example, but is implemented using Python fastapi. Provider could be built using any Python REST framework.

## Create Consumer Contract

Consumer is JavaScript. You need to have [Node.js](https://nodejs.org/en/) installed in order to proceed. At the time this application was created Node.js version 14.17 as used.

```bash
$ cd e2e
$ npm install -ci
...
$ npm run test:consumer
```

Pact file will be created and stored under `e2e/pacts` folder.

Here is a sample output:

```
> e2e@1.0.0 test:consumer C:\Sandbox\PoC\pact-contract-testing\js\pact-example\e2e
> mocha test/consumer.spec.js

(node:19156) ExperimentalWarning: Conditional exports is an experimental feature. This feature could change at any time


  Pact
    when a call to list all animals from the Animal Service is made
      and the user is not authenticated
        √ returns a 401 unauthorized
      and the user is authenticated
        and there are animals in the database
          √ returns a list of animals
    when a call to the Animal Service is made to retreive a single animal by ID
      and there is an animal in the DB with ID 1
        √ returns the animal
      and there no animals in the database
        √ returns a 404
    when a call to the Animal Service is made to create a new mate
      √ creates a new mate


  5 passing (4s)
```



## Python Provider Contract Testing

Create virtual environment:

```bash
$ python -m venv .venv
$ source .venv/Scripts/activate
```

Install dependencies:

```bash
# Switch to the Python provider
$ cd fastapi-provider

# Install Python package dependencies using pip
$ pip install -r requirements.txt
...
```

Start the provider server:

```bash
$ uvicorn main:app --reload
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [28088] using watchgod
INFO:     Started server process [9716]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
...
```

In a new shell session, execute the contract verification:

```bash
# Activate virtual environment
$ source .venv/Scripts/activate

# Switch to the Python provider folder
$ cd fastapi-provider

# Execute the contract verification
$ pact-verifier --pact-url ../e2e/pacts/e2e_consumer_example-e2e_provider_example.json --provider-base-url=http://localhost:8000 --provider-states-setup-url http://127.0.0.1:8000/fixture
```

Here is what the output looks like:

```
WARN: Only the first item will be used to match the items in the array at $['body']
INFO: Reading pact at ../e2e/pacts/e2e_consumer_example-e2e_provider_example.json


Verifying a pact between e2e Consumer Example and e2e Provider Example
  Given is not authenticated
    a request for all animals
      with GET /animals/available
        returns a response which
          has status code 401
  Given Has some animals
    a request for all animals
      with GET /animals/available
        returns a response which
          has status code 200
          has a matching body
          includes headers
            "Content-Type" which equals "application/json; charset=utf-8"
  Given Has an animal with ID 1
    a request for an animal with ID 1
      with GET /animals/1
        returns a response which
          has status code 200
          has a matching body
          includes headers
            "Content-Type" which equals "application/json; charset=utf-8"
  Given Has no animals
    a request for an animal with ID 100
      with GET /animals/100
        returns a response which
          has status code 404
  A request to create a new mate
    with POST /animals
      returns a response which
        has status code 200
        has a matching body
        includes headers
          "Content-Type" which equals "application/json; charset=utf-8"

5 interactions, 0 failures
WARN: Only the first item will be used to match the items in the array at $['body']
```

