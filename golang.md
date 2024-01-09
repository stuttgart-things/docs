# stuttgart-things/docs/golang

## SNIPPETS

<details><summary>TEST</summary>

```bash
# TEST RECURSIVELY
go test ./... -v 
```

</details>

<details><summary>BUILD</summary>

## GO INSTALL

```bash
# GOLANG INSTALL FOR LINUX IN CURRENT DIR ./ (EXAMPLE)
go install
```

## GO BUILD

```bash
# BUILD GOLANG FOR LINUX IN CURRENT DIR ./ (EXAMPLE)
CGO_ENABLED=0 go build -buildvcs=false -o /bin/machineShop

# BUILD GOLANG FOR LINUX IN DIFFRENT DIR (EXAMPLE)
CGO_ENABLED=0 go build -o /bin/stcTestProducer tests/testProducer.go
```

## BUILD W/ LDFLAGS (E.G. VERSION INFORMATION GIVEN AT BUILD TIME)

```bash
CGO_ENABLED=0 go build -o /bin/stageTime-creator \
-ldflags="-X ${GO_MODULE}/internal.version=${VERSION} -X ${GO_MODULE}/internal.date=${BUILD_DATE} -X 
```

## BUILD W/ DOCKERFILE (MULTISTAGE)

```
FROM golang:1.21.4 AS builder
LABEL maintainer="Patrick Hermann patrick.hermann@sva.de"

ARG GO_MODULE="github.com/stuttgart-things/stageTime-creator"
ARG VERSION=""
ARG BUILD_DATE=""
ARG COMMIT=""

WORKDIR /src/
COPY . .

RUN go mod tidy
RUN CGO_ENABLED=0 go build -o /bin/stageTime-creator \
    -ldflags="-X ${GO_MODULE}/internal.version=${VERSION} -X ${GO_MODULE}/internal.date=${BUILD_DATE} -X ${GO_MODULE}/internal.commit=${COMMIT}"

RUN CGO_ENABLED=0 go build -o /bin/stcTestProducer tests/testProducer.go
RUN CGO_ENABLED=0 go build -o /bin/stcTestConsumer tests/testConsumer.go

FROM alpine:3.18.4
COPY --from=builder /bin/stageTime-creator /bin/stageTime-creator

# FOR SERVICE TESTING
COPY --from=builder /bin/stcTestProducer /bin/stcTestProducer
COPY --from=builder /bin/stcTestConsumer /bin/stcTestConsumer

ENTRYPOINT ["stageTime-creator"]
```

</details>


<details><summary>GOLINT</summary>

```bash
# INSTALL GOLINT
go install github.com/golangci/golangci-lint/cmd/golangci-lint@v1.55.2
golangci-lint run
```

<details><summary>EXAMPLE LINT CONFIG</summary>

```yaml
# .golangci.yaml
linters:
  disable-all: true
  enable:
    - asasalint
    - asciicheck
    - bidichk
    - bodyclose
    - depguard
    - dogsled
    - errcheck
    - errname
    - errorlint
    - exportloopref
    - gocheckcompilerdirectives
    - gocritic
    - goprintffuncname
    - gosec
    - gosimple
    - govet
    - ineffassign
    - interfacebloat
    - lll
    - makezero
    - nakedret
    - nilerr
    - nolintlint
    - perfsprint
    - prealloc
    - predeclared
    - revive
    - sqlclosecheck
    - staticcheck
    - tenv
    - testifylint
    - tparallel
    - typecheck
    - unconvert
    - unparam
    - unused

linters-settings:
  depguard:
    rules:
      # Name of a rule.
      main:
        # Packages that are not allowed where the value is a suggestion.
        deny:
          - pkg: log
            desc: 'Use injected telegraf.Logger instead'
        # List of file globs that will match this list of settings to compare against.
        # Default: $all
        files:
          - "!**/agent/**"
          - "!**/cmd/**"
          - "!**/config/**"
          - "!**/filter/**"
          - "!**/internal/**"
          - "!**/logger/**"
          - "!**/metric/**"
          - "!**/models/**"
          - "!**/plugins/serializers/**"
          - "!**/scripts/**"
          - "!**/selfstat/**"
          - "!**/testutil/**"
          - "!**/tools/**"
          - "!**/*_test.go"
  errcheck:
    # List of functions to exclude from checking, where each entry is a single function to exclude.
    # See https://github.com/kisielk/errcheck#excluding-functions for details.
    exclude-functions:
      - "(*hash/maphash.Hash).Write"
      - "(*hash/maphash.Hash).WriteByte"
      - "(*hash/maphash.Hash).WriteString"
  gocritic:
    # Which checks should be enabled; can't be combined with 'disabled-checks'.
    # See https://go-critic.github.io/overview#checks-overview.
    # To check which checks are enabled run `GL_DEBUG=gocritic golangci-lint run`.
    # By default, list of stable checks is used.
    enabled-checks:
      # diagnostic
      - argOrder
      - badCall
      - badCond
      - badLock
      - badRegexp
      - badSorting
      - builtinShadowDecl
      - caseOrder
      - codegenComment
      - commentedOutCode
      - deferInLoop
      - dupArg
      - deprecatedComment
      - dupBranchBody
      - dupCase
      - dupSubExpr
      - dynamicFmtString
      - emptyDecl
      - evalOrder
      - exitAfterDefer
      - externalErrorReassign
      - filepathJoin
      - flagName
      - mapKey
      - nilValReturn
      - offBy1
      - regexpPattern
      - sloppyTestFuncName
      - sloppyReassign
      - sloppyTypeAssert
      - sortSlice
      - sprintfQuotedString
      - sqlQuery
      - syncMapLoadAndDelete
      - truncateCmp
      - uncheckedInlineErr
      - unnecessaryDefer
      - weakCond
      # performance
      - appendCombine
      - equalFold
      - indexAlloc
      - hugeParam
      - preferDecodeRune
      - preferFprint
      - preferStringWriter
      - preferWriteByte
      - rangeExprCopy
      - rangeValCopy
      - sliceClear
      - stringXbytes

    # Settings passed to gocritic.
    # The settings key is the name of a supported gocritic checker.
    # The list of supported checkers can be find in https://go-critic.github.io/overview.
    settings:
      hugeParam:
        # Size in bytes that makes the warning trigger.
        # Default: 80
        sizeThreshold: 512
      rangeValCopy:
        # Size in bytes that makes the warning trigger.
        # Default: 128
        sizeThreshold: 512

  gosec:
    # To select a subset of rules to run.
    # Available rules: https://github.com/securego/gosec#available-rules
    # Default: [] - means include all rules
    includes:
      - G101
      - G102
      - G103
      - G106
      - G107
      - G108
      - G109
      - G110
      - G111
      - G112
      - G114
      - G201
      - G202
      - G203
      - G301
      - G302
      - G303
      - G305
      - G306
      - G401
      - G403
      - G404
      - G501
      - G502
      - G503
      - G505
      - G601
      # G104, G105, G113, G204, G304, G307, G402, G504 were not enabled intentionally
    # To specify the configuration of rules.
    config:
      # Maximum allowed permissions mode for os.OpenFile and os.Chmod
      # Default: "0600"
      G302: "0640"
      # Maximum allowed permissions mode for os.WriteFile and ioutil.WriteFile
      # Default: "0600"
      G306: "0640"
  govet:
    settings:
      ## Check the logging function like it would be a printf
      printf:
        funcs:
          - (github.com/influxdata/telegraf.Logger).Debugf
          - (github.com/influxdata/telegraf.Logger).Infof
          - (github.com/influxdata/telegraf.Logger).Warnf
          - (github.com/influxdata/telegraf.Logger).Errorf
          - (github.com/influxdata/telegraf.Logger).Debug
          - (github.com/influxdata/telegraf.Logger).Info
          - (github.com/influxdata/telegraf.Logger).Warn
          - (github.com/influxdata/telegraf.Logger).Error
  lll:
    # Max line length, lines longer will be reported.
    # '\t' is counted as 1 character by default, and can be changed with the tab-width option.
    # Default: 120.
    line-length: 160
    # Tab width in spaces.
    # Default: 1
    tab-width: 4
  nolintlint:
    # Enable to require an explanation of nonzero length after each nolint directive.
    # Default: false
    require-explanation: true
    # Enable to require nolint directives to mention the specific linter being suppressed.
    # Default: false
    require-specific: true
  prealloc:
    # Report pre-allocation suggestions only on simple loops that have no returns/breaks/continues/gotos in them.
    # Default: true
    simple: false
  revive:
    rules:
      - name: argument-limit
        arguments: [ 6 ]
      - name: atomic
      - name: bare-return
      - name: blank-imports
      - name: bool-literal-in-expr
      - name: call-to-gc
      - name: confusing-naming
      - name: confusing-results
      - name: constant-logical-expr
      - name: context-as-argument
      - name: context-keys-type
      - name: deep-exit
      - name: defer
      - name: dot-imports
      - name: duplicated-imports
      - name: early-return
      - name: empty-block
      - name: empty-lines
      - name: error-naming
      - name: error-return
      - name: error-strings
      - name: errorf
      - name: function-result-limit
        arguments: [ 3 ]
      - name: identical-branches
      - name: if-return
      - name: import-shadowing
      - name: increment-decrement
      - name: indent-error-flow
      - name: modifies-parameter
      - name: modifies-value-receiver
      - name: package-comments
      - name: range
      - name: range-val-address
      - name: range-val-in-closure
      - name: receiver-naming
      - name: redefines-builtin-id
      - name: string-of-int
      - name: struct-tag
      - name: superfluous-else
      - name: time-naming
      - name: unconditional-recursion
      - name: unexported-naming
      - name: unnecessary-stmt
      - name: unreachable-code
      - name: unused-parameter
      - name: var-declaration
      - name: var-naming
      - name: waitgroup-by-value
  nakedret:
    # make an issue if func has more lines of code than this setting and it has naked returns; default is 30
    max-func-lines: 1
  tenv:
    # The option `all` will run against whole test files (`_test.go`) regardless of method/function signatures.
    # Otherwise, only methods that take `*testing.T`, `*testing.B`, and `testing.TB` as arguments are checked.
    # Default: false
    all: true
  testifylint:
    # Enable specific checkers.
    # https://github.com/Antonboom/testifylint#checkers
    # Default: ["bool-compare", "compares", "empty", "error-is-as", "error-nil", "expected-actual", "float-compare", "len", "require-error", "suite-dont-use-pkg", "suite-extra-assert-call"]
    enable:
      - bool-compare
      - compares
      - empty
      - error-is-as
      - error-nil
      - expected-actual
      - len
      - require-error
      - suite-dont-use-pkg
      - suite-extra-assert-call
      - suite-thelper

run:
  # timeout for analysis, e.g. 30s, 5m, default is 1m
  timeout: 10m

  # which dirs to skip: issues from them won't be reported;
  # can use regexp here: generated.*, regexp is applied on full path;
  # default value is empty list, but default dirs are skipped independently
  # from this option's value (see skip-dirs-use-default).
  # "/" will be replaced by current OS file path separator to properly work
  # on Windows.
  skip-dirs:
    - assets
    - docs
    - etc

  # which files to skip: they will be analyzed, but issues from them
  # won't be reported. Default value is empty list, but there is
  # no need to include all autogenerated files, we confidently recognize
  # autogenerated files. If it's not please let us know.
  # "/" will be replaced by current OS file path separator to properly work
  # on Windows.
  skip-files:
    - plugins/parsers/influx/machine.go*

issues:
  # Maximum issues count per one linter. Set to 0 to disable. Default is 50.
  max-issues-per-linter: 0

  # Maximum count of issues with the same text. Set to 0 to disable. Default is 3.
  max-same-issues: 0

  # List of regexps of issue texts to exclude.
  #
  # But independently of this option we use default exclude patterns,
  # it can be disabled by `exclude-use-default: false`.
  # To list all excluded by default patterns execute `golangci-lint run --help`
  #
  # Default: https://golangci-lint.run/usage/false-positives/#default-exclusions
  exclude:
    # revive:var-naming
    - don't use an underscore in package name
    # EXC0001 errcheck: Almost all programs ignore errors on these functions and in most cases it's ok
    - Error return value of .((os\.)?std(out|err)\..*|.*Close.*|.*Flush|.*Disconnect|.*Clear|os\.Remove(All)?|.*print(f|ln)?|os\.(Un)?Setenv). is not checked
    # EXC0013 revive: Annoying issue about not having a comment. The rare codebase has such comments
    - package comment should be of the form "(.+)...
    # EXC0015 revive: Annoying issue about not having a comment. The rare codebase has such comments
    - should have a package comment

  # Excluding configuration per-path, per-linter, per-text and per-source
  exclude-rules:
    - path: plugins/parsers/influx
      linters:
        - govet

    - path: cmd/telegraf/(main|printer|cmd_plugins).go
      text: "Error return value of `outputBuffer.Write` is not checked" #errcheck

    - path: _test\.go
      text: "Potential hardcoded credentials" #gosec:G101

    - path: _test\.go
      text: "Use of weak random number generator" #gosec:G404

  # Independently of option `exclude` we use default exclude patterns,
  # it can be disabled by this option.
  # To list all excluded by default patterns execute `golangci-lint run --help`.
  # Default: true.
  exclude-use-default: false

# output configuration options
output:
  # Format: colored-line-number|line-number|json|tab|checkstyle|code-climate|junit-xml|github-actions
  #
  # Multiple can be specified by separating them by comma, output can be provided
  # for each of them by separating format name and path by colon symbol.
  # Output path can be either `stdout`, `stderr` or path to the file to write to.
  # Example: "checkstyle:report.json,colored-line-number"
  #
  # Default: colored-line-number
  format: tab
  # Make issues output unique by line.
  # Default: true
  uniq-by-line: false
  # Sort results by: filepath, line and column.
  sort-results: true
```

</details>


</details>

<details><summary>GORELEASER</summary>

```bash
# INSTALL
go install github.com/goreleaser/goreleaser@v1.23.0 #@latest
```

```bash
# INIT
goreleaser init
git add .goreleaser.yaml
git commit -am 'added goreleaser' && git push
goreleaser release --snapshot --clean
goreleaser check
git tag -a v0.1.0 -m "First release"
git push origin v0.1.0
goreleaser release
```


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
```

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
```

</details>

## CLI

<details><summary>INIT CLI W/ COBRA</summary>

```bash
go install github.com/spf13/cobra-cli@latest
PROJECT_NAME=toolkit-chart-creator
mkdir ./${PROJECT_NAME} && cd ${PROJECT_NAME}
go mod init ${PROJECT_NAME} # or w/ github: go mod init github.com/stuttgart-things/kaeffken
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

<details><summary>FILENAME/DIR FROM PATH</summary>

```go
import (
  "path/filepath"
)
//..
path := filepath.Base("/this/that/hello.yaml")
dir := filepath.Dir("/this/that/hello.yaml")

fmt.Println(path) // /this/that/
fmt.Println(dir) // hello.yaml
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
