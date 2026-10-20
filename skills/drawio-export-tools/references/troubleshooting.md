# Troubleshooting

**Permission errors:**

```bash
docker run -u $(id -u):$(id -g) -e HOME=/data/home ...
```

**Timeouts:**

```bash
docker run -e DRAWIO_DESKTOP_COMMAND_TIMEOUT=60s ...
```

**Debug mode:**

```bash
docker run -e SCRIPT_DEBUG_MODE=true ...
```
