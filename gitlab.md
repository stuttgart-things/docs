# stuttgart-things/docs/gitlab

## SNIPPETS

<details><summary>GITLAB RUNNER</summary>

[linux](https://docs.gitlab.com/runner/install/linux-repository.html)

```bash
curl -L "https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh" | sudo bash
sudo apt install gitlab-runner
gitlab-runner register  --url ${GITLAB_URL} --token ${RUNNER_TOKEN}
```

```bash
cat ${HOME}/.gitlab-runner/config.toml # SHELL RUNNER FOR DAGGER
gitlab-runner run # START RUNNER ADHOC
sudo gitlab-runner start # START SERVICE
```

</details>


<details><summary>GITLAB CLI</summary>

```bash
# INSTALL
wget https://gitlab.com/gitlab-org/cli/-/releases/v1.43.0/downloads/glab_1.43.0_Linux_x86_64.tar.gz
tar xvfz glab_1.43.0_Linux_x86_64.tar.gz
sudo mv bin/glab /usr/bin/glab

# CONFIG
glab auth login

# TEST
glab issue list
```

</details>
