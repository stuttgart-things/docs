Output crossplane.gif

Set TypingSpeed 75ms
Set FontSize 30
Set Width 1650
Set Height 880

Sleep 500ms

Type "kubectl apply -f proxmox-vm.yaml"

Enter

Sleep 20s

Type "crossplane beta trace proxmoxvmansible manager-dev36 -n proxmox"


Enter

Sleep 20s

Type "kubectl describe proxmoxvmansible manager-dev36 -n proxmox"


Enter

Sleep 20s


Type "tkn pr logs -f manager-dev36-2qpgg-43107375b986 -n tekton-pipelines"

Enter

Sleep 20s
