# stuttgart-things/docs/dagger

## SNIPPETS

<details><summary><b>AI AGENTS</b></summary>

## USECASE POSTGRESDB

```bash
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
curl -fsSL https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo gpg --dearmor -o /etc/apt/trusted.gpg.d/postgresql.gpg
sudo apt update && sudo apt install postgresql-client-17

psql -h $(hostname -f) -p 31641 -U dev
CREATE DATABASE appdb;

cat <<EOF > ./bootstrap.sql
-- Create database (only if it doesn't exist)
DO
$$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'appdb') THEN
      CREATE DATABASE "appdb";
   END IF;
END
$$;

-- Switch to new DB
\c appdb;

-- Drop tables if exist (clean run)
DROP TABLE IF EXISTS tasks CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks table
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    project_id INT REFERENCES projects(id) ON DELETE CASCADE,
    assignee_id INT REFERENCES users(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL,
    status VARCHAR(50) DEFAULT 'open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    due_date DATE
);

-- Insert sample users
INSERT INTO users (username, email) VALUES
('alice', 'alice@example.com'),
('bob', 'bob@example.com'),
('charlie', 'charlie@example.com');

-- Insert sample projects
INSERT INTO projects (name, description) VALUES
('AI Platform', 'Build internal AI platform'),
('Infra Migration', 'Migrate to new Kubernetes cluster');

-- Insert sample tasks
INSERT INTO tasks (project_id, assignee_id, title, status, due_date) VALUES
(1, 1, 'Design database schema', 'in-progress', '2025-09-15'),
(1, 2, 'Implement API service', 'open', '2025-09-30'),
(2, 3, 'Migrate Helm charts', 'done', '2025-08-20'),
(2, NULL, 'Set up monitoring', 'open', NULL);
EOF

psql -h $(hostname -f) -p 31641 -U dev -d appdb -f bootstrap.sql 
```

```bash
export GEMINI_API_KEY="SET-HERE-OR-GPT-OR-ANY-OTHER-SUPPORTED-AI"
export DB_URL="postgres://$USER:$PASSWORD@maverick.db.host:31641/appdb?sslmode=disable"
dagger call -m github.com/jasonmccallister/database-agent ask --db-url=env:DB_URL --question="What tables do you have?" -vv
```

</details>

<details><summary><b>DAGGER SHELL</b></summary>

```bash
# JUMP INTO CONTAINER (e.g. PACKAGE-TEST-INSTALLATION)
dagger -c 'container | from cgr.dev/chainguard/wolfi-base:latest | terminal'
```

</details>

<details><summary><b>LIST DIRECTORY CONTENTS</b></summary>

```go
// LIST ALL ENTRIES
entries, err := src.Entries(ctx)
if err != nil {
	panic(err)
}

// PRINT ALL ENTRIES
for _, entry := range entries {
	println(entry)
}
```

</details>

<details><summary><b>PERSIST CONTAINER STATE OVER MULTIPLE CI-STEPS</b></summary>

```go
// MOUNT BUILDDIR AND SET WORKING DIRECTORY
base := m.container(packerVersion, arch).
    WithMountedDirectory("/src", buildDir).
    WithWorkdir("/src")

// RUN PACKER INIT AND PERSIST CONTAINER STATE
initContainer := base.WithExec([]string{"packer", "init", "hello.pkr.hcl"})

// OPTIONALLY GET INIT OUTPUT (FROM A SEPARATE EXECUTION)
initOut, err := initContainer.WithExec([]string{"packer", "version"}).Stdout(ctx)
if err != nil {
    panic(fmt.Errorf("failed to verify init: %w", err))
}
fmt.Println("Init complete - Packer version:", initOut)
```

</details>

<details><summary><b>BROWSE DAGGER DIRECTORY</b></summary>

```go
// CLONE
repoContent, err := m.ClonePrivateRepo(ctx, repoURL, branch, token)
if err != nil {
	fmt.Errorf("failed to clone repo: %w", err)
}

// BROWSE
entries, err := repoContent.Entries(ctx)
if err != nil {
    panic(err)
}
fmt.Println("Top-level entries:", entries)
```

</details>


<details><summary><b>TROUBLESHOOTING</b></summary>

```bash
# ERROR
rpc error: code = NotFound desc = socket /run/user/1112/vscode-ssh-auth-sock-713734249 not found
# SOLUTION
unset SSH_AUTH_SOCK
```

</details>

<details><summary><b>DEPLOY CUSTOM ENGINE</b></summary>

[custom-ca](https://docs.dagger.io/configuration/custom-ca)
[connection-interface](https://docs.dagger.io/configuration/custom-runner/#connection-interface)

```bash
## STOP ANY EXISTING/RUNNING ENGINE(S) w/ DOCKER STOP.. 

docker run -d --rm \
-v /var/lib/dagger \
-v /usr/local/share/ca-certificates/:/usr/local/share/ca-certificates/ \
--name dagger-engine-custom \
--privileged \
registry.dagger.io/engine:v0.16.2

export _EXPERIMENTAL_DAGGER_RUNNER_HOST=docker-container://$(docker ps -qf "name=dagger-engine-custom")
```

</details>

<details><summary><b>CALL HELP FUNCTION (OF SUBCOMMAND)</b></summary>

```bash
dagger call -m "github.com/sagikazarmark/daggerverse/gh@main" release create --help
```

</details>

<details><summary><b>INIT MODULE</b></summary>

```bash
dagger init --sdk=go --source=./cicd --name cicd
```

</details>

<details><summary><b>CALL LOCAL MODULE</b></summary>

```bash
dagger call -m cicd/ go-pipeline --src ./
```

</details>

<details><summary><b>INSTALL DEPENDECY/b></summary>

```bash
dagger install github.com/stuttgart-things/dagger/go@v0.1.0
```

</details>

<details><summary><b>CALL FUNCTION (FROM DAGGERVERSE)</b></summary>

```bash
# OUTPUT TEXT
dagger call -m github.com/shykes/daggerverse/hello@v0.1.2 hello --giant=false --name=pat

# SCAN IMAGE REF W/ AQUA TRIVY
dagger call -m github.com/jpadams/daggerverse/trivy@v0.3.0 scan-image --image-ref alpine/git:latest

# BUILD GO BINARY
dagger call -m github.com/felipecruz91/daggerverse/go build --source . --goVersion 1.23.1 -o bin

# LINT DOCKERFILE
dagger call -m github.com/disaster37/dagger-library-go/image lint --source . --dockerfile images/sthings-packer/Dockerfile

# BUILD & PUSH CONTAINER IMAGE
dagger call -m github.com/disaster37/dagger-library-go/image build --source . --dockerfile images/sthings-packer/Dockerfile push --repository-name stuttgart-things/test --registry-url ttl.sh --version 60m

# CLONE A GITHUB REPO
export GITHUB_TOKEN=whatever
dagger call --progress plain -m github.com/sagikazarmark/daggerverse/gh@main \
repo clone \
--repository stuttgart-things/stuttgart-things \
--token=env:GITHUB_TOKEN export --path=/tmp/repo/sthings
```

</details>

<details><summary><b>INSTALL DAGGER-CLI</b></summary>

```bash
curl -fsSL https://dl.dagger.io/dagger/install.sh | BIN_DIR=$HOME/.local/bin sh
```

</details>

<details><summary><b>BASIC COMMANDS</b></summary>

https://docs.dagger.io/quickstart/daggerize

```bash
# CREATE MODULE (GO); SOURCE: ./hello; NAME: modules
dagger init --sdk=go --source=./hello --name modules

# RUN PIPELINE (PUBLISH=METHOD NAME)
dagger call publish --source=.
```


</details>
