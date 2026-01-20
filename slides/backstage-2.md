### Demo: Modify files + Create Mr 0/8

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/demo2_0.png" alt="Alt Text" width="1200" style="border: none; box-shadow: none;" />

---

### Demo: Modify files + Create Mr 1/8

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/demo2_1.png" alt="Alt Text" width="1200" style="border: none; box-shadow: none;" />

---

### Demo: Modify files + Create Mr 2/8

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/demo2_2.png" alt="Alt Text" width="1200" style="border: none; box-shadow: none;" />

---

### Demo: Modify files + Create Mr 3/8

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/demo2_3.png" alt="Alt Text" width="1200" style="border: none; box-shadow: none;" />

---

### Demo: Modify files + Create Mr 4/8

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/demo2_4.png" alt="Alt Text" width="1200" style="border: none; box-shadow: none;" />

---

### Demo: Modify files + Create Mr 5/8

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/demo2_5.png" alt="Alt Text" width="1200" style="border: none; box-shadow: none;" />

---

### Demo: Modify files + Create Mr 6/8

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/demo2_6.png" alt="Alt Text" width="1200" style="border: none; box-shadow: none;" />

---

### Demo: Modify files + Create Mr 7/8

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/demo2_7.png" alt="Alt Text" width="1200" style="border: none; box-shadow: none;" />

---




### TECHDOCS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/backstage8.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

---

### TECHDOCS

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/techdocs.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- TechDocs View in Backstage

---

### CI/CD GITLAB PIPELINES

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/backstage7.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

---

### CI/CD GITLAB PIPELINES

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/gitlab-pipeline.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Detailed view of the Components GitLab Pipelines

---
### KUBERNETES

<img src="https://artifacts.demo-infra.sthings-vsphere.labul.sva.de/images/kubernetes.png" alt="Backstage" style="width:100%; border: none; box-shadow: none;" />

- Detailed view of Kubernetes Clusters

---

## Why Plugins Matter

- Backstage is a **framework**, not a product
- Plugins turn it into a real **Internal Developer Portal**
- Good plugin choices:
  - Improve developer experience
  - Reduce cognitive load
  - Enable self-service

---

### GitHub / GitLab Plugins 🧑‍💻

- GitHub Actions / GitLab CI (Frontend+Backend Plugins)
- Pull Requests
- Repo insights

**➡️ Pick what matches your SCM**

---

### CI/CD Plugins ⚙️

- GitHub Actions
- GitLab Pipelines
- CircleCI
- Argo / Flux (GitOps)

**➡️ Visibility without leaving Backstage**

---

### CUSTOM FRONTEND + BACKEND PLUGINS

Building custom plugins extends Backstage to fit your organization's needs

**Frontend Plugins**
- Custom UI components & pages
- Entity cards & tabs
- Custom pickers & selectors

**Backend Plugins**
- API integrations
- Custom data providers
- Authentication & authorization

---

### Example: Custom Picker Template

```typescript
// Custom RepositoryPicker component
import { FieldExtensionComponent } from '@backstage/plugin-scaffolder-react';

export const CustomRepoPicker: FieldExtensionComponent<string> = ({
  onChange,
  schema
}) => {
  const [repos, setRepos] = useState([]);

  // Fetch repositories from your custom API
  useEffect(() => {
    fetchCustomRepos().then(setRepos);
  }, []);

  return (
    <Select onChange={(e) => onChange(e.target.value)}>
      {repos.map(repo => (
        <MenuItem value={repo.id}>{repo.name}</MenuItem>
      ))}
    </Select>
  );
};
```

**Use case**: Provide custom repository selection in Software Templates

---
