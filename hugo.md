# /HUGO

## HUGO + REVEALJS

<details><summary>INIT SITE</summary>

```bash
hugo new site k8s-backup
cd k8s-backup
hugo mod init github.com/stuttgart-things/docs/k8s-backup
hugo mod get github.com/joshed-io/reveal-hugo
```

</details>

<details><summary>SERVE (ON IP)</summary>

```bash
hugo server --bind 10.31.103.28 --baseURL http://10.31.103.28
```

</details>

<details><summary>BUILD STATIC CONTENT</summary>

```bash
hugo mod get github.com/joshed-io/reveal-hugo
hugo mod vendor
hugo --minify --baseURL="/" --cleanDestinationDir
```

```bash
# hugo.toml
#...
theme = ["github.com/joshed-io/reveal-hugo"]
[module]
  proxy = "direct"
  vendored = true
# ..
```

</details>

<details><summary>SERVE STATIC CONTENT w/ NGINX</summary>

```bash
docker run \
--rm \
-p 8080:80 \
-v "$(pwd)/public:/usr/share/nginx/html:ro" \
nginx
```

</details>

