# LINUX

## BASH-SNIPPETS

<details><summary><b>SPLIT STRINGS BY DELIMITER (+-) W/ AWK</b></summary>

```bash
path=$(awk -F+- '{print $1}' <<< 'git/data/github:token+-false+-GITHUB_TOKEN') # =git/data/github:token
convert=$(awk -F+- '{print $2}' <<< 'git/data/github:token+-false+-GITHUB_TOKEN') # =false
token=$(awk -F+- '{print $3}' <<< 'git/data/github:token+-false+-GITHUB_TOKEN') # =GITHUB_TOKEN
```

</details>

<details><summary><b>LOOP OVER PARAMETERS W/ SET + FOR LOOP</b></summary>

```bash
set great foo bar # set parameters
echo "$@" # test output
for argument in "$@"; do echo $argument ; done # loop over parameters

# loop over parameters andchange +- to : w/ sed
for argument in "$@"; do echo $argument | sed -e "s/+-/: /g" ; done 
```

</details>

<details><summary><b>GET VERSION NUMBER W/ AWK</b></summary>

```bash
python3 --version # Python 3.10.12
python3 --version | awk '{print $2}' # 3.10.12
```

</details>

<details><summary><b>UNTIL LOOP</b></summary>

```bash
#!/bin/bash

until skopeo inspect docker://registry.fedoraproject.org/fedora:latest
do
    echo checking..
    sleep 1
done
```

</details>
