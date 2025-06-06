Output shell_node_nginx.gif

Set TypingSpeed 125ms
Set FontSize 30
Set Width 1650
Set Height 880

Sleep 1000ms

Type "dagger"
Enter

Sleep 3500ms

Type "repo=$(git https://github.com/dagger/hello-dagger | head | tree)"
Enter

Sleep 10000ms

Type "env=$(container | from node:23 | with-directory /app $repo | with-workdir /app)"
Enter

Sleep 10000ms

Type "build=$($env | with-exec npm install | with-exec npm run build | directory ./dist)"
Enter

Sleep 10000ms

Type "container | from nginx | with-directory /usr/share/nginx/html $build | terminal --cmd=/bin/bash"
Enter

Sleep 10000ms

Type "ls /usr/share/nginx/html"
Enter

Sleep 8000ms

Type "exit"
Enter

Sleep 5000ms

Type "exit"
Enter

Sleep 5000ms
