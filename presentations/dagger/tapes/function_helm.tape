Output function_helm.gif

Set TypingSpeed 75ms
Set FontSize 30
Set Width 1650
Set Height 880

Sleep 500ms

Type "dagger call -m github.com/sagikazarmark/daggerverse/helm@v0.14.0 package --chart app/ --app-version 1.23 export --path=app-1.23.tgz"

Enter

Sleep 7s

Type "helm template app-1.23.tgz"

Enter

Sleep 3s
