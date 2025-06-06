Output shell_node_publish2.gif

Set TypingSpeed 125ms
Set FontSize 30
Set Width 1650
Set Height 880

Sleep 1000ms

Type "dagger"
Enter

Sleep 3500ms

Type "github.com/dagger/dagger/modules/wolfi | container --packages=nginx,bash | publish ttl.sh/fb-meeting:1h"
Enter

Sleep 20s

Type "container | from ttl.sh/fb-meeting:1h | terminal"
Enter

Sleep 10000ms

Type "nginx"
Enter

Sleep 10000ms

Type "exit"

Enter

Sleep 10000ms
