+++
weight = 20
+++

{{< slide id=introduction background-color="#D4B9FF" type="slide" transition="zoom" transition-speed="fast" >}}

{{% section %}}

# /PRACTICES AND TOOLS
---

### /IAC

```bash
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

{{% fragment %}}

- BAD

```js
// Calculating area of a circle in two places
let area1 = 3.14 * radius1 * radius1;
let area2 = 3.14 * radius2 * radius2;
```

{{% /fragment %}}

- BETTER

{{% fragment %}}

```js
function calculateCircleArea(radius) {
  return Math.PI * radius * radius;
}
let area1 = calculateCircleArea(radius1);
let area2 = calculateCircleArea(radius2);
```

{{% /fragment %}}

---

### /CICD

![cicdcd](https://miro.medium.com/v2/resize:fit:786/format:webp/0*IC_N9P4Eu1NO1UkE.png)

---

### /CICD

![cicdcd](https://miro.medium.com/v2/resize:fit:786/format:webp/0*OC11hb1WJ-th-154.png)

---

### /CICD

- Develop — developers write the code.
- Build — Then the team compiles the code into a build
- Test — operations team runs tests
- Deploy – deployment to the end-users

---

### /STAGING

![staging](https://codefresh.io/wp-content/uploads/2023/07/same-artifact-for-all.png)


{{% /section %}}
