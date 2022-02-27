# BDD with Cucumber and Behave
This project aimed to use BBD ideas and tools to reach and test a REST API

## How To Run
In the root (the same level as this README) run
```commandline
docker build --tag python-bdd .
```
After the build has successfully completed you can run the container

The project does need some configuration this can be in the form of an .ini file 
```ini
[api]
2FA=<base32 key>
public_key=123 
private_key=<base64 encoded key (default format from the api)>
url = https://dns
```
This file can then be mounted in by default the project reads config from `/opt/bdd/api_config.ini` but this can be overridden with the env var `API_CONFIG_PATH`.

```commandline
docker run -v <local_path_to_api_config.ini>:/opt/bdd/api_config.ini python-bdd
```

By default, reports are produced to the `/usr/bdd/reports` directory so mounting that directory is probably a good idea.

The `behave` framework is used and so this behavior can be controlled by using the docker CMD

```commandline
docker run -v <local_path_to_api_config.ini>:/opt/bdd/api_config.ini -v <local_path_to_reports_dir>:/usr/bdd/reports python-bdd
```

Finally the configs can also be set or overwritten using env vars:
* `API_2FA`
* `API_PUBLIC_KEY`
* `API_PRIVATE_KEY`
* `API_URL`