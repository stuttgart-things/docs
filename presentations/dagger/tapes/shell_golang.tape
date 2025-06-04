Output shell_golang.gif

Set TypingSpeed 150ms
Set FontSize 30
Set Width 1650
Set Height 880

Sleep 500ms

Type "dagger"

Enter

Sleep 5s

Type "container | from cgr.dev/chainguard/wolfi-base | with-exec apk add go | with-directory /src https://github.com/golang/example#master | with-workdir /src/hello | with-exec -- go build -o hello . | file ./hello | export ./gude"

Enter

Sleep 180s

Type "./gude"

Enter

Sleep 3s
