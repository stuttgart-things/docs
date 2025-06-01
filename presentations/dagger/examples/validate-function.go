func (m *Kyverno) Validate(
	ctx context.Context,
	policy *dagger.Directory,
	resource *dagger.Directory,
) error {
	kyverno := m.container().
		WithMountedDirectory("/policy", policy).
		WithMountedDirectory("/resource", resource).
		WithWorkdir("/")

	result, err := kyverno.
		WithExec([]string{
			"kubectl-kyverno",
			"apply",
			"/policy",
			"--resource",
			"/resource"}).
		Stdout(ctx)

	if err != nil {
		return fmt.Errorf("failed to validate: %w", err)
	}

	fmt.Println(result)
	return nil
}