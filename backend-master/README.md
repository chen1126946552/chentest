# Backend Development

## Get Started
### Setup environment
- Install Python 3.7 and pip3
- Install latest docker if you want to run services in docker locally
- Install latest VSCode and Python extension
- pip3 install pylint
- Turn on [Python Linting](https://code.visualstudio.com/docs/python/linting) in VS Code

### Open in VSCode
- In src folder, run "code backend.code-workspace"

### Debug in VSCode
- Launch debugger with service specific configuration, like "api-gateway"

### Run in console
- In "main" folder of service, run "PYTHONPATH=../../ flask run"

### Build & run docker
- cd src
- ./builddocker.sh [service]
- ./rundocker.sh [service]
- ./rmdocker.sh [service]

### Run Pylint
- cd src
- ./lint.sh

### Run tests
- cd src
- ./testall.sh

## Service Catalog

### Overview
Datadeck's backend adopts the "single-repository" microservices approach. All services reside in one sigle Git repository. Services are organized by folders.

Project structure convention:
- "src" folder contains production source code.
    - Each toplevel folder under "src" represents a microservice (except for "common" folder) which is independently packaged and deployed.
    - "common" folder contains packages shared among multiple microservices.
- "test" folder contains scenario tests which involves calling multiple services.

### Ports
Each web service uses a distinct port (except for datasource services). This simplifies end-to-end debugging in local environment.

- api-gateway: 9080 (with HTTPS when run locally, for testing oauth callback)
- business: 9081
- data-manager: 9082
- datasources: 9090 (all datasource services use the same port)

### Api Gateway
Api Gateway is the only public-facing service, dealing with user authentication, service call dispatching, API versioning, rate limiting and etc.

When debugging locally, api-gateway project is configured to launch with HTTPS using a test certificate. To get around untrusted SSL cert error in browser, follow these steps:
1. Install the certificate under api-gateway/main/testcert.pem
2. Add a DNS entry in hosts file to point datadeck-api-gateway domain name to localhost
3. Launch api-gateway locally
4. Verify that https://datadeck-api-gateway:9080/health can be accessed in browser without any error/warning

### Business
Business provides CRUD operations for most of the important business entities in Datadeck, e.g. users, spaces, dashboards and etc. It also provides the access layer for data fetching, although real data retrieval job is done in downstream services.

### Data Manager
Data Manager provides APIs for listing datasources, CRUDing connections/datasets, data connection OAuth authorization flow, and relaying data fetching requests to appropriate datasource microservices.

### Common [Shared Packages]
Common provides packages shared among multiple services. For simplicity, backend services reference packages through code sharing directly, without using any package management system or repository. When building a service into docker image, files in "common" folder are copied into image into "libs" folder and included in PYTHONPATH environment variable for discovery. 

This code sharing dependency approach requires changes made to "common" are backward compatible. If a breaking change is to be made, author needs to make sure to change all places in existing code to ensure all services affected still function properly.
