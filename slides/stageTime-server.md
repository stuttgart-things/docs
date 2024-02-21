# STAGETIME-SERVER
--
# GOLANG
* Same language in which Kubernetes is built <!-- .element: class="fragment fade-up" -->
* Most natural fit for k8s extensions, custom controls and operators <!-- .element: class="fragment fade-up" -->
--
# GRPC
[<img src="https://grpc.io/img/landing-2.svg" width="800"/>](https://www.sva.de/index.html)
<!-- .element: class="fragment fade-up" -->
--
# PROTO DEFINITION
* Generate clients and servers in any of gRPC's supported languages

```
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
<!-- .element: class="fragment fade-up" -->
--
# COMPILE/GENERATE FOR GOLANG

```
protoc --go_out=. --go_opt=paths=source_relative \
--go-grpc_out=. --go-grpc_opt=paths=source_relative \
revisionrun/*.proto
```
<!-- .element: class="fragment fade-up" -->
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
<!-- .element: class="fragment fade-up" -->
--
# SERVER

```
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
<!-- .element: class="fragment fade-up" -->
--
# CLIENT

```
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
<!-- .element: class="fragment fade-up" -->
--
# /TASKFILE
--
### /What is Taskfile?
[<img src="https://tsh.io/wp-content/uploads/2021/04/taskfile-preference-meme.png" width="700"/>](https://www.sva.de/index.html)
--
### /What is Taskfile?
*  make executing terminal commands or even lists of commands needed for specific operations easier <!-- .element: class="fragment fade-up" -->
* The syntax is based on YAML, which requires a specific structure <!-- .element: class="fragment fade-up" -->
* It's a much simpler solution compared to GNU make <!-- .element: class="fragment fade-up" -->
--
### /EXAMPLE


# HELMFILE

# HELM


--
