Output dagger_shell.gif

Set TypingSpeed 150ms
Set FontSize 30
Set Width 1650
Set Height 880

Sleep 500ms

Type "dagger"

Enter

Sleep 3s

Type "container | from cgr.dev/chainguard/wolfi-base | with-exec apk add curl git bash wget kubectl helm k9s cilium | with-directory /showcase https://github.com/stuttgart-things/platform-engineering-showcase.git#main | with-secret-variable KUBECONFIG vault://github.token | with-secret-variable GITHUB_TOKEN vault://eva.kubeconfig | with-secret-variable VCENTER_FQDN env://VCENTER_FQDN | terminal "

Sleep 500ms

Enter

Sleep 45s


Output dagger_shell.gif
Set FontSize 30
Set Width 1650
Set Height 880
Set TypingSpeed 120ms

Sleep 500ms
Type "dagger"
Enter
Sleep 2s

Type "container \\"
Enter
Type "  | from cgr.dev/chainguard/wolfi-base \\"
Type "  | with-exec apk add curl git bash wget kubectl helm k9s cilium \\"
Type "  | with-directory /showcase https://github.com/stuttgart-things/platform-engineering-showcase.git#main \\"
Type "  | with-secret-variable KUBECONFIG vault://github.token \\"
Type "  | with-secret-variable GITHUB_TOKEN vault://eva.kubeconfig \\"
Type "  | with-secret-variable VCENTER_FQDN env://VCENTER_FQDN \\"
Type "  | terminal"

Sleep 500ms
Enter

Sleep 25s