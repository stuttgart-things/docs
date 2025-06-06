Output service.gif

Set TypingSpeed 125ms
Set FontSize 30
Set Width 1650
Set Height 880

Sleep 10000ms

Type "dagger init --sdk=go --source=./build --name build"

Sleep 10000ms

Enter

Sleep 10000ms

cat dagger.json

Sleep 10000ms

Enter


bat build/main.go -r 20:40

Sleep 60s

Ctrl+C
