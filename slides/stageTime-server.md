# STAGETIME-SERVER
--
### /GOLANG
[<img src="https://miro.medium.com/v2/resize:fit:2000/1*8bPiDNL1K1ZdK9O_T5IVKw.png" width="700"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->

* Same language in which Kubernetes is built <!-- .element: class="fragment fade-up" -->
* Most natural fit for Kubernetes extensions, custom controls and operators <!-- .element: class="fragment fade-up" -->
--
### /REST
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/rest.png" width="1000"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->
--
### /GRPC
[<img src="https://artifacts.automation.sthings-vsphere.labul.sva.de/images/grpc.png" width="1000"/>](https://www.sva.de/index.html) <!-- .element: class="fragment fade-up" -->
--
### /PROTO DEFINITION
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
### /COMPILE-GENERATE FOR GOLANG
```
protoc --go_out=. --go_opt=paths=source_relative \
--go-grpc_out=. --go-grpc_opt=paths=source_relative \
revisionrun/*.proto
```
<!-- .element: class="fragment fade-up" -->
--
### /GENERATED CODE
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
### /SERVER

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
### /CLIENT

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
# TASKFILE

# HELMFILE

--
