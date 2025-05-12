+++
weight = 20
+++

{{< slide id=introduction background-color="#D4B9FF" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /PRACTICES AND TOOLS
---

## **What is IaC?**
- Define infrastructure (servers, networks, databases) **using code** instead of manual processes.
- Treat infrastructure like software: **versioned**, **reusable**, and **testable**.
- Example in **Ansible**:

```python
- name: Create a VM from a template
  hosts: localhost
  tasks:
  - name: Clone the template
    vmware_guest:
      hostname: "{{ vcenter_ip }}"
      username: "{{ vcenter_username }}"
      password: "{{ vcenter_password }}"
      validate_certs: False
      name: testvm_2
      template: template_el7
      datacenter: "{{ datacenter_name }}"
```

---

## **Why IaC?**
- 🏭 **Consistency** Eliminate "works on my machine" issues.
- 🚀 **Speed** Deploy entire environments in minutes.
- 📈 **Scalability** - Replicate stacks across regions/clouds.
- 💸 **Cost Control** - Destroy unused resources automatically.

---

## **Best Practices**

- 🔄 **Idempotency**: Scripts should safely run multiple times without side effects.
- 🧩 **Modularity**: Reuse code with modules/templates for flexibility.
- 🌿 **Version Control**: Track changes in Git (e.g., GitHub, GitLab) for auditability.

---

### /SOURCE CONTROL DO

[<img src="https://codefresh.io/wp-content/uploads/2023/07/everything-in-git.png" width="800"/>](https://www.sva.de/index.html)

---
### /SOURCE CONTROL DONT

[<img src="https://codefresh.io/wp-content/uploads/2023/07/not-everything-in-git.png" width="800"/>](https://www.sva.de/index.html)

---

### /DRY

[<img src="https://preview.redd.it/r2e86rrndns41.jpg?width=1080&crop=smart&auto=webp&s=4fe4832eaa7d75762850ec174b7e9f99bc358bc9" width="800"/>](https://www.sva.de/index.html)

---

### /DRY (EXAMPLE)

- BAD

```js
// Calculating area of a circle in two places
let area1 = 3.14 * radius1 * radius1;
let area2 = 3.14 * radius2 * radius2;
```

---

### /DRY (EXAMPLE)

- BETTER

```js
function calculateCircleArea(radius) {
  return Math.PI * radius * radius;
}
let area1 = calculateCircleArea(radius1);
let area2 = calculateCircleArea(radius2);
```

---

### /RELATED CONCEPTS

- **YAGNI** ("You Ain’t Gonna Need It")
Don’t add features "just in case."
- **KISS** ("Keep It Simple, Stupid")
Simplicity > complexity.

---

### /CICD

![cicdcd](https://miro.medium.com/v2/resize:fit:786/format:webp/0*IC_N9P4Eu1NO1UkE.png)

---

### /CICD-PHASE

- **Develop** — developers write the code.
- **Build** — Then the team compiles the code into a build
- **Test** — operations team runs tests
- **Deploy** – deployment to the end-users

---

### /PIPELINE

![cicdcd](https://miro.medium.com/v2/resize:fit:786/format:webp/0*OC11hb1WJ-th-154.png)

---

### /Containerization
**Build Once, Run Anywhere**

```dockerfile
# Start from a base image
FROM node:18-alpine

# Set working directory
WORKDIR /app

# Copy dependencies and install
COPY package*.json ./
RUN npm install

# Copy app source code
COPY . .

# Expose port and define runtime command
EXPOSE 3000
CMD ["npm", "start"]
```

Dockerfile Example

---

### Build % run

```bash
docker build -t my-node-app:latest .
```

```bash
docker run -d -p 8080:3000 --name my-app my-node-app:latest
```
- `-d`: Run in detached mode
- `-p 8080:3000`: Map host port 8080 → container port 3000
- `--name`: Assign a container name

---
### /Docker: The Standard for Modern App Packaging 🐳

- **Portability**: Works identically on dev machines, cloud, or Kubernetes.
- **Isolation**: Apps run in sandboxed environments.
- **Reproducibility**: No more "but it worked on my laptop!"

---

### /STAGING

![staging](https://codefresh.io/wp-content/uploads/2023/07/same-artifact-for-all.png)

---

## 🔄 Shift Left

**Definition:**
Moving testing, security, and quality practices earlier in the development lifecycle.

**Why it matters:**
- Detect issues earlier = lower cost
- Faster feedback loops
- Supports CI/CD efficiency

**Practices include:**
- Early unit & integration testing
- Code linting & SAST in CI
- Infrastructure-as-Code validation

---

## 🛠️ Platform Engineering

**Definition:**
Building and maintaining Internal Developer Platforms (IDPs) to streamline developer workflows.

**Goals:**
- Reduce cognitive load on dev teams
- Standardize infrastructure and tooling
- Improve delivery speed and reliability

**Typical Components:**
- Self-service deployment portals
- Paved paths (golden paths)
- Observability, secrets, CI/CD tooling integrated


{{% /section %}}
