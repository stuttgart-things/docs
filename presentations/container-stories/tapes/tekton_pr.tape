Output tekton_pr.gif

Set TypingSpeed 150ms
Set FontSize 30
Set Width 1650
Set Height 880

Sleep 500ms

Type "kubectl apply -f pr-buildah.yaml -n tekton-ci"

Enter

Sleep 30s

Type "tkn pr logs -f pr-buildah-837 -n tekton-ci"

Enter

Sleep 10s

Enter

Output tekton1_pr.gif
