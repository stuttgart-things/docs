client, err := dagger.Connect(ctx)
src := client.Host().Directory(".")
container := client.Container().
	From("alpine").
	WithMountedDirectory("/src", src).
	WithWorkdir("/src").
	WithExec([]string{"sh", "-c", "echo Hello from Dagger!"})
output, err := container.Stdout(ctx)