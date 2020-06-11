
# Authz Service

Implementation of CanDIG Authorization Service.

## Installation

The Authz service can be installed in a Python 3.6+ virtual enviroment:
```
pip install -r requirements.txt
```

Alternatively, you could also install from source

```
pip install git+https://github.com/candig/candig_authz_service.git
```

### Preparing Access List

Before you start the service, you need to create an access_list.tsv at the root of the directory of the app.

The access_list.tsv needs to be of format like this

Please make sure your tsv file is correctly formatted by using tabs as the delimiter, not spaces.

```
issuer      username        project1        project2        project3        projectN

https://candigauth.bcgsc.ca/auth/realms/candig      user_a   4       4       4       4
https://candigauth.bcgsc.ca/auth/realms/candig      user_b   4       X       0       1

https://candigauth.uhnresearch.ca/auth/realms/CanDIG        user_c   4       3       2       1
https://candigauth.uhnresearch.ca/auth/realms/CanDIG        user_d   X       X       4       4
```

### Running

The service can be started with:

```
candig_authz_service --host 0.0.0.0 --port 8000
```

### Known Limitations

In the access_list.tsv you provide, the username must all be in lower case, this is because the look-up will convert all incoming requests' usernames to lower case.
