Output module.gif

Set TypingSpeed 125ms
Set FontSize 30
Set Width 1650
Set Height 880

Sleep 1000ms

Type "dagger init --sdk=go --source=./ci --name ci"
Enter

Sleep 20s

Type "bat dagger.json  -r 0:8"

Sleep 10s

Enter

Sleep 10s

Type "cat ci/main.go"

Enter

Sleep 10s

Type "dagger install github.com/stuttgart-things/dagger/go@v0.12.0"

Enter

Sleep 60s

Type "bat dagger.json  -r 0:8"

Sleep 10s

Enter