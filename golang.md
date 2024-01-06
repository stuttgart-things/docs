# stuttgart-things/docs/golang

## SNIPPETS

<details><summary>COMMANDS</summary>

```bash
# TEST RECURSIVELY
go test ./... -v 
```

</details>


<details><summary>GORELEASER</summary>

```yaml
// .goreleaser.yaml
github_urls:
  api: https://git.company.com/api/v3/
  upload: https://git.company.com/api/uploads/
  download: https://git.company.com/
  # set to true if you use a self-signed certificate
  skip_tls_verify: false
```

</details>

<details><summary>TEST W/ ASSERT</summary>

### BOOL

```go
// git_test.go
import (
	"testing"
	"github.com/stretchr/testify/assert"
)

func TestCloneGitRepository(t *testing.T) {

	assert := assert.New(t)

	_, cloned := CloneGitRepository(repo, branchName, "", nil)

	assert.Equal(cloned, true)
}
```

### STRING

```go
func TestReadFileContentFromGitRepo(t *testing.T) {

	gitRepository := "https://github.com/stuttgart-things/kaeffken.git"
	gitBranch := "main"
	gitCommitID := "09de9ff7b5c76aff8bb32f68cfb0bbe49cd5a7a8"

	assert := assert.New(t)
	expectedReadMe := "# kaeffken\ngitops cluster management cli \n"

	repo, _ := CloneGitRepository(gitRepository, gitBranch, gitCommitID, nil)
	readMe := ReadFileContentFromGitRepo(repo, "README.md")
	fmt.Println(readMe)
	fmt.Println(expectedReadMe)

	assert.Equal(readMe, expectedReadMe)
	fmt.Println("TEST SUCCESSFULLY")
}

### TABLE DRIVEN BOOL

```go
func TestVerifyValues(t *testing.T) {

	type test struct {
		mandatoryFlags []string
		values         map[string]string
		want           bool
	}

	values1 := make(map[string]string)
	values1["repository"] = "https://github.com/stuttgart-things/stuttgart-things.git"
	values1["branch"] = ""

	tests := []test{
		{mandatoryFlags: []string{"repository", "branch", "clusterName", "envPath"}, values: values1, want: false},
		{mandatoryFlags: []string{"repository"}, values: values1, want: true},
	}

	assert := assert.New(t)

	for _, tc := range tests {
		validValues := VerifyValues(tc.values, tc.mandatoryFlags)
		fmt.Println(validValues)
		assert.Equal(validValues, tc.want)
	}

}
```go


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

<details><summary>CMD/PERSISTENT FLAGS</summary>

```go
// cmd/get.go
//..
Run: func(cmd *cobra.Command, args []string) {
  // READ FLAGS
  authMethod, _ := cmd.LocalFlags().GetString("auth")
  b64DecodeOption, _ := cmd.LocalFlags().GetBool("b64")

// DECLARE FLAGS AND DEFAULTS
func init() {
  rootCmd.AddCommand(getCmd)
  getCmd.Flags().String("auth", "approle", "vault auth method")
  getCmd.Flags().Bool("b64", false, "decode base64 for output")
}
```

```go
// root.go
//..
var (
  gitRepository string
  enableVault   bool
)

// DECLARE FLAGS AND DEFAULTS
func init() {
  rootCmd.PersistentFlags().StringVar(&gitRepository, "git", "https://github.com/stuttgart-things/stuttgart-things.git", "source git repository")
  rootCmd.PersistentFlags().BoolVar(&enableVault, "vault", true, "Enable vault lookups")
}
```

</details>

## SYNTAX

<details><summary>SLICES</summary>

```go
// STRING SLICE
mandatoryFlags := []string{"repository", "branch", "clusterName", "envPath"}
```

</details>

<details><summary>MAPS</summary>

```go
// STRING MAP

// DECLARE
var (
  values = make(map[string]string)
)
// ADD VALUE
values["rootPath"], _ = cmd.LocalFlags().GetString("root")
```

</details>

<details><summary>LOOPS</summary>

```go
// LOOP OVER STRING MAP + LOG ALL KEYS AND VALUES
values := make(map[string]string)
values["NAME] = "PATRICK"

for key, value := range values {
  log.Info(strings.ToUpper(key)+": ", value)
}
```

</details>
