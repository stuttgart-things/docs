# LINUX

## BASH-SNIPPETS

<details><summary><b>CUT FOLDERPATH W/ SED FROM URL</b></summary>

```bash
git clone https://github.com/stuttgart-things/stuttgart-things.git
cd $(echo $(params.REPO_URL) | sed 's|.*/||' | sed 's/.git//g')
# https://github.com/stuttgart-things/stuttgart-things.git -> stuttgart-things
```

</details>


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

<details><summary><b>CONCATENATE SET PARAMETERS + FOR LOOP</b></summary>

```bash
set 'scanners vuln' 'timeout 30m'
output=" "; for argument in "$@"; do output=${output}'--'$argument' '; done
echo ${output} #--scanners vuln --timeout 30m
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

<details><summary><b>CHECK TEKTON PIPELINERUN STATUS IN WHILE LOOP W/ OPERATORS</b></summary>

```bash
#!/bin/bash
sleep=10
failed_prs=0
succeeded_prs=0
retries=0
max_retries=3

all_prs=$(tkn pr list -n tektoncd | grep -c alpine)
echo all pipelineRuns: ${all_prs}

while [[ ${failed_prs} -le 0  ]] || [[ ${succeeded_prs} -eq ${all_prs} ]] || [[ ${retries} -eq ${max_retries} ]]
do
    echo ${retries_left} retries left
    echo check/retry in ${sleep} seconds..
    sleep ${sleep}

    failed_prs=$(tkn pr list -n tektoncd | grep alpine | grep -c Failed)
    echo Failed pipelineRuns: ${failed_prs}
    tkn pr list -n tektoncd | grep alpine | grep Failed

    succeeded_prs=$(tkn pr list -n tektoncd | grep alpine | grep -c Succeeded)
    echo Succeeded pipelineRuns: ${succeeded_prs}
    tkn pr list -n tektoncd | grep alpine | grep Succeeded

    retries=`expr ${retries} + 1`
    retries_left=`expr ${max_retries} - ${retries}`
done

echo "Done watching pipelineRuns!"
echo Failed pipelineRuns: ${failed_prs}
echo Succeeded pipelineRuns: ${succeeded_prs}
```

</details>

