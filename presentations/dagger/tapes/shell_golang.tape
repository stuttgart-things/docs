Output shell_golang.gif

Set TypingSpeed 75ms
Set FontSize 30
Set Width 1650
Set Height 880

Sleep 500ms

Type "echo 'container | from cgr.dev/chainguard/wolfi-base | with-exec apk add go | with-directory /src https://github.com/golang/example#master | with-workdir /src/hello | with-exec -- go build -o hello . | file ./hello | export ./gude' | dagger"

Enter

Sleep 10s

Type "/gude"

Enter

Sleep 3s
