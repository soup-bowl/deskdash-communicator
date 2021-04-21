# Desktop Dashboard - Communicator API
Cross-platform low requirement Python API to report system information and current stats across the network. Currently, this can:

* Collect and return system information.
* Report system usage and (sometimes) temperatures.
* Collect information about Nvidia GPUs.
* (optionally) Can use nmap to scan the enclosed local network.

## Development
For convinience, a `docker-compose.yml` file is provided which will create an API. This will not work for 'production' use as the container can only see the API released by the container filesystem, which is not a true account.

Start off by running `dev.sh`, which will install dependencies for the Python API project.

* For testing, run `py.test`.
* Run `python -m communicator` to run the API server, accessible via http://localhost:43594.
