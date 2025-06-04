//...
redis := dag.Container().
	From("redis:7").
	WithExposedPort(6379).
	AsService()

app := dag.Container().
	From("golang:1.22").
	WithServiceBinding("redis", redis).
	WithExec([]string{"go", "test", "./..."})
//...
