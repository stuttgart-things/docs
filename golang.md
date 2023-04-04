# GOLANG

## init project w/ cobra-cli
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

## add create command w/ cobra
```
cobra-cli add version
```

## add subcommand to vm command w/ cobra 
```
cobra-cli add vm
cobra-cli add create -p 'vmCmd' # like sthings vm create
```
