# kstack-agent

Exposes a REST api for managing docker containers.


## Quick Start

```bash
docker run -d \
  --name kstack-agent \
  --restart always \
  --privileged \
  --user root \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v kstack_agent_data:/app/data \
  -p 5000:5000 \
  -e AGENT_HOST=0.0.0.0 \
  -e AGENT_PORT=5000 \
  -e AGENT_DATA_DIR=/app/data \
  fmlabs/kstack-agent:latest
```


## Development

Uses [poetry](https://python-poetry.org/) for dependency management.

```bash
poetry install
potry run python ./agent.py
```

The kstack-agent REST api server is served at `http://localhost:5000/` by default.



## Useful links

- [Docker Reference](https://docs.docker.com/reference/)
- [Docker SDK for Python](https://docker-py.readthedocs.io/en/stable/)
- [Docker SDK for Python API Reference](https://docker-py.readthedocs.io/en/stable/api.html)


**Related projects:**
- [kstack-ui](https://github.com/fm-labs/kstack-ui) - A web ui for kstack-agent