
# Authz Service

Implementation of CanDIG Authorization Service.

## Installation

The Authz service can be installed in a Python 3.6+ virtual enviroment:
```
pip install -r requirements.txt
```

Alternatively, you could also install from source

```
git install git+https://github.com/candig/candig_authz_service.git
```

### Preparing Access List

Before you start the service, you need to create an access_list.tsv at the root of the directory of the app.

The access_list.tsv needs to be of format like this

Please make sure your tsv file is correctly formatted by using tabs as the delimiter, not spaces.

```
issuer      username        project1        project2        project3        projectN

https://candigauth.bcgsc.ca/auth/realms/candig      userA   4       4       4       4
https://candigauth.bcgsc.ca/auth/realms/candig      userB   4       X       0       1

https://candigauth.uhnresearch.ca/auth/realms/CanDIG        userC   4       3       2       1
https://candigauth.uhnresearch.ca/auth/realms/CanDIG        userD   X       X       4       4
```

### Running

The service can be started with:

```
candig_authz_service --host 0.0.0.0 --port 8000
```
