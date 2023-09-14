# LINUX

## SPLIT STRINGS BY DELIMITER (+-) W/ AWK

```bash
path=$(awk -F+- '{print $1}' <<< 'git/data/github:token+-false+-GITHUB_TOKEN') # =git/data/github:token
convert=$(awk -F+- '{print $2}' <<< 'git/data/github:token+-false+-GITHUB_TOKEN') # =false
token=$(awk -F+- '{print $3}' <<< 'git/data/github:token+-false+-GITHUB_TOKEN') # =GITHUB_TOKEN
```

## LOOP OVER PARAMETERS W/ SET + FOR LOOP

```bash
set great foo bar # set parameters
echo "$@" # test output
for argument in "$@"; do echo $argument ; done # loop over parameters

# loop over parameters andchange +- to : w/ sed
for argument in "$@"; do echo $argument | sed -e "s/+-/: /g" ; done 
```

 parameters
