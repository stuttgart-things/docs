+++
weight = 20
+++
{{< slide id=velero >}}

## DAGGEER

- Stateful application data (e.g., databases using persistent volumes)
- Cluster state (e.g., etcd backup)
- Namespace or resource-level (e.g., using kubectl to export resource definitions)

<br>
<br>

[see the code on github](https://github.com/joshed-io/reveal-hugo)


---

## PUSH & PRAY

<img src="https://private-user-images.githubusercontent.com/47567770/440137535-37b51685-bf2d-4583-96d0-83da30ebba5b.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NDYyOTU3NzgsIm5iZiI6MTc0NjI5NTQ3OCwicGF0aCI6Ii80NzU2Nzc3MC80NDAxMzc1MzUtMzdiNTE2ODUtYmYyZC00NTgzLTk2ZDAtODNkYTMwZWJiYTViLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNTA1MDMlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjUwNTAzVDE4MDQzOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTVkNGJjNmE4MjJhZjExMzViMTdjOTJiZGFmYTgzZWYxNDk2MGUyNmZiZTgzYTI4OTBkODI3OTQ5ODIyYzgwN2UmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.zW2PFnF2GMch4X4CfZnwONbUHmz0gPzo60T_GNzSHTQ" alt="Description" width="400"/>

---

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