func (m *Kyverno) container() *dagger.Container {

	ctr := dag.Container().From("cgr.dev/chainguard/wolfi-base:latest")

	ctr = ctr.WithExec([]string{"apk", "add", "--no-cache", "kyverno-cli"})
	ctr = ctr.WithEntrypoint([]string{"kubectl-kyverno"})

	return ctr
}