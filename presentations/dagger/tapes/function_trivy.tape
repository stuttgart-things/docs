Output triviy.gif

Set TypingSpeed 150ms
Set FontSize 30
Set Width 1650
Set Height 880

Sleep 500ms

Type "dagger call -m github.com/stuttgart-things/dagger/docker@v0.11.1 trivy-scan --image-ref ghcr.io/stuttgart-things/sthings-alpine:3.13-alpine --with-registry-username env:GITHUB_USER --with-registry-password env:GITHUB_TOKEN"

Sleep 500ms

Enter

Sleep 30s
