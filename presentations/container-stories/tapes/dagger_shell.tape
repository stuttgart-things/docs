Output dagger_shell.gif

Set TypingSpeed 150ms
Set FontSize 30
Set Width 1650
Set Height 880

Sleep 500ms

Type "dagger"

Enter

Sleep 3s

Type "container | from cgr.dev/chainguard/wolfi-base | with-exec apk add curl git bash wget kubectl helm k9s cilium | with-directory /showcase https://github.com/stuttgart-things/platform-engineering-showcase.git#main | with-mounted-secret kube vault://sthings-runner.kubeconfig | with-env-variable KUBECONFIG kube | with-secret-variable GITHUB_TOKEN env://GITHUB_TOKEN | terminal"

Sleep 3s

Enter

Sleep 10s

Type "kubectl get nodes"

Sleep 2s

Enter

Type "ls showcase/"

Sleep 10s

Enter

Output dagger_shell.gif
