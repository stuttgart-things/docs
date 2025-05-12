
## DAGGER SHELL - RUN FUNCTION

```bash
dagger -m github.com/stuttgart-things/dagger/docker@v0.9.0
.help trivy-scan
trivy-scan nginx:latest
```

## DAGGER SHELL - JUMP INTO CONTAINER

```bash
container |
  from alpine |
  with-exec apk add git |
  terminal
```

## DAGGER SHELL - SIMPLE CONTAINER BUILD

```bash


```

This creates an Alpine container, drops in a text file with your message, sets it to display that message when run, and publishes it to a temporary registry. All in one pipeline - no context switching between Dockerfile creation, build commands, and registry pushes.


https://dagger.io/blog/a-shell-for-the-container-age-introducing-dagger-shell