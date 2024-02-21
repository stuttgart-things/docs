# STAGETIME-SERVER
--
# GOLANG
* same language in which Kubernetes is built
* and the most natural fit for Kubernetes extensions, custom controls and operators
--

# GRPC


# PROTO DEFINITION

```go
syntax = "proto3";

package revisionrun;

import "revisionrun/pipelinerun.proto";

message CreateRevisionRunRequest {
    string repo_name = 1;
    string pushed_at = 2;
    string author = 3;
    string repo_url = 4;
    string commit_id = 5;
    repeated Pipelinerun pipelineruns = 6;
}
```
--
# COMPILE/GENERATE FOR GOLANG

```bash
protoc --go_out=. --go_opt=paths=source_relative \
--go-grpc_out=. --go-grpc_opt=paths=source_relative \
revisionrun/*.proto
```
--
# GENERATED CODE

```
//..
func (x *CreateRevisionRunRequest) ProtoReflect()
protoreflect.Message {
	mi := &file_revisionrun_revisionrun_proto_msgTypes[0]
	if protoimpl.UnsafeEnabled && x != nil {
		ms :=
		protoimpl.X.MessageStateOf(protoimpl.Pointer(x))
		if ms.LoadMessageInfo() == nil {
			ms.StoreMessageInfo(mi)
		}
		return ms
	}
	return mi.MessageOf(x)
}
```
--
# SERVER

```go
listener, err := net.Listen("tcp", "0.0.0.0"+serverPort)
if err != nil {
	log.Fatalln(err)
}
grpcServer := grpc.NewServer()
reflection.Register(grpcServer)
registerServices(grpcServer)

func registerServices(s *grpc.Server) {
	revisionrun.RegisterStageTimeApplicationServiceServer
	(s, &Server{})
	revisionrun.RegisterStatusesServer
	(s, &StatusService{})
}
```
--
# CLIENT

```go
//..
conn, err := grpc.Dial(address, grpc.WithTransportCredentials(insecure.NewCredentials()))

if err != nil {
  fmt.Println(err)
}
defer conn.Close()

stsClient := NewClient(conn, time.Second)
err = stsClient.CreateRevisionRun(context.Background(), bytes.NewBuffer(revisionRunJson))
//..
```
--
# /TASKFILE
--
### /What is Taskfile?
[<img src="https://tsh.io/wp-content/uploads/2021/04/taskfile-preference-meme.png" width="700"/>](https://www.sva.de/index.html)
--
### /What is Taskfile?
*  tool designed to make executing terminal commands or even lists of commands needed for specific operations easier <!-- .element: class="fragment fade-up" -->
* Task is a tool written in Golang <!-- .element: class="fragment fade-up" -->
* The syntax is based on YAML, which requires a specific structure <!-- .element: class="fragment fade-up" -->
* It's a much simpler solution compared to GNU make <!-- .element: class="fragment fade-up" -->
* Getting started with Taskfile is very easy <!-- .element: class="fragment fade-up" -->
--

# HELMFILE

--

# TASKFILE

```yaml
tasks:
  pr:
    desc: Create pull request into main
    cmds:
      - task: commit
      - gh pr create -t "{{ .BRANCH }}" -b "{{ .BRANCH }} branch into main"
      - sleep 20s
      - gh pr checks $(gh pr list | grep "^[^#;]" | awk '{print $1}') --watch
      - gh pr merge $(gh pr list | grep "^[^#;]" | awk '{print $1}') --auto --rebase --delete-branch
      - git checkout main && git pull
```
