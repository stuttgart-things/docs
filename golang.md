# stuttgart-things/docs/golang

## CLI w/ COBRA

### INIT CLI 

```
go install github.com/spf13/cobra-cli@latest
PROJECT_NAME=toolkit-chart-creator
mkdir ./${PROJECT_NAME} && cd ${PROJECT_NAME} 
go mod init ${PROJECT_NAME}
cobra-cli init

# install locally 
go install ./${PROJECT_NAME} # build binary to $GOPATH/bin
# or build binary
go build -o ./${PROJECT_NAME} # build binary to target dir
```

### ADD CMD

```
cobra-cli add version
```

### ADD SUB-CMD

```
cobra-cli add vm
cobra-cli add create -p 'vmCmd' # like sthings vm create
```


