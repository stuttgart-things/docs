# stuttgart-things/docs/golang

## SNIPPETS

<details><summary>GORELEASER</summary>

```yaml
# .goreleaser.yaml
github_urls:
  api: https://git.company.com/api/v3/
  upload: https://git.company.com/api/uploads/
  download: https://git.company.com/
  # set to true if you use a self-signed certificate
  skip_tls_verify: false
```

</details>

## CLI

<details><summary>INIT CLI W/ COBRA</summary>

```bash
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

</details>

<details><summary>SET DEFAULT CMD W/ COBRA</summary>

```go
// main.go
func main() {
  defCmd:="mydefaultcmd"
  cmd.Execute(defCmd)
}
```

```go
// root.go
func Execute(defCmd string) {
  var cmdFound bool
  cmd :=rootCmd.Commands()

  for _,a:=range cmd{
    for _,b:=range os.Args[1:] {
      if a.Name()==b {
       cmdFound=true
        break
      }
    }
  }
  if !cmdFound {
    args:=append([]string{defCmd}, os.Args[1:]...)
    rootCmd.SetArgs(args)
  }
  if err := rootCmd.Execute(); err != nil {
    fmt.Println(err)
    os.Exit(1)
  }
```

</details>

<details><summary>ADD COMMANDS W/ COBRA</summary>

```bash
cobra-cli add version
cobra-cli add vm
cobra-cli add create -p 'vmCmd' # like sthings vm create
```

</details>