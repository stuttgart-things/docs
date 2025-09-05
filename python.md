# stuttgart-things/docs/python

## SNIPPETS

<details><summary>RUN A PYPIP-SERVER</summary>

```bash
# INSTALL SERVER
pip install pypiserver

# CREATE/DOWNLOADING / # OPTION1: DOWNLOAD PIP PACKAGES MANUALY
mkdir ~/packages
pip download requests -d ~/packages
pip download picker==2.3.0 -d ~/packages

# RUN SERVER
pypi-server run -p 8080 ~/package

# USE/INSTALL FROM SERVER
pip install --index-url http://localhost:8080/simple picker
```

```bash
# OPTION2: DOWNLOAD PIP PACKAGES w/ DOCKER

cat <<EOF > pip-schleuser.sh
#!/bin/sh
set -eux

BASE_IMAGE=$1
PIP_PACKAGES=$2

# Local directory on host
WHEELHOUSE="$(pwd)/wheelhouse"
mkdir -p "$WHEELHOUSE"

# Run container to build offline wheelhouse
docker run --rm -it \
  -v "$WHEELHOUSE:/wheelhouse" \
  "$BASE_IMAGE" sh -euxc "

    # 1. Create and activate venv
    python3 -m venv /venv
    . /venv/bin/activate

    # 2. Upgrade pip tooling
    pip install --upgrade pip setuptools wheel

    # 3. Download requested packages into /wheelhouse
    pip download -d /wheelhouse $PIP_PACKAGES

    # 4. Optional: install them (from wheelhouse, offline style)
    pip install --no-index --find-links=/wheelhouse $PIP_PACKAGES

    # 5. Record installed packages
    pip freeze > /wheelhouse/installed-packages.txt
  "

echo "[INFO] pip packages and wheelhouse saved under: $WHEELHOUSE"

zip -r ./pip-packages.zip wheelhouse
EOF

sh pip-schleuser.sh python:3.10.0-alpine "requests flask"
```

```yaml
# DEPLOY ON KUBERNETES
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pypiserver-pvc
  labels:
    app.kubernetes.io/name: pypiserver
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 1Gi
---
apiVersion: v1
kind: Service
metadata:
  name: pypiserver
  labels:
    app.kubernetes.io/name: pypiserver
spec:
  type: ClusterIP
  ports:
    - port: 8080
      targetPort: http
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: pypiserver
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pypiserver
  labels:
    app.kubernetes.io/name: pypiserver
spec:
  replicas: 1
  selector:
    matchLabels:
      app.kubernetes.io/name: pypiserver
  template:
    metadata:
      labels:
        app.kubernetes.io/name: pypiserver
    spec:
      containers:
        - name: pypiserver
          image: pypiserver/pypiserver:v2.3.2
          imagePullPolicy: IfNotPresent
          args:
            - run
            - -a
            - .
            - -P
            - .
            - /data/packages
          env:
            - name: PYPISERVER_PORT
              value: "8080"
          ports:
            - name: http
              containerPort: 8080
              protocol: TCP
          readinessProbe:
            httpGet:
              path: /health
              port: http
          livenessProbe:
            httpGet:
              path: /health
              port: http
          volumeMounts:
            - name: packages
              mountPath: /data/packages
      volumes:
        - name: packages
          persistentVolumeClaim
            claimName: pypiserver-pvc
```

```bash
# COPY PACKAGES TO POD
kubectl cp ~/packages/ pypiserver-fb7b96d8-cfkf8:/data/

# PORT-FORWARD SVC
kubectl port-forward svc/pypiserver 8080:8080

# INSTALL PACKAGE FROM SERVER/POD
pip install --index-url http://localhost:8080/simple picker
```

</details>

<details><summary>CLI-ARGS TO DICT</summary>

```python3
#!/usr/bin/env python3

import argparse

# PARSE ARGS
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--overwrites', default='')
args = parser.parse_args()

# SPLIT ARGS BY DELIMITER
overwrites = args.overwrites.split(";")

all_overwrites = {}

# LOOP OVER ARGS
for x in overwrites:
  split = x.split("=")
  all_overwrites[split[0]]=split[1]
```

</details>

<details><summary>MERGE DICTS</summary>

```python3
def merge_two_dicts(x, y):
    z = x.copy()   # start with keys and values of x
    z.update(y)    # modifies z with keys and values of y
    return z

defaults = {
    'cpu': "4",
    'memory': "8192",
}

overwrites = {
    'cpu': "8",
    'memory': "4096",
}

updated = merge_two_dicts(defaults, overwrites)
print(updated) # {'cpu': '8', 'memory': '4096'}
```

</details>

<details><summary>ARGS W/ DEFAULT</summary>

```python3
#!/usr/bin/env python3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--values', default='values.yaml')
args = parser.parse_args()

print(args.values)
```

</details>

<details><summary>DICTS</summary>

```python3
# ..
disk = {
   'S': 32,
   'M': 64,
   'L': 81920,
   'XL': 12288,
}

os = {
   'labul-vsphere': {
      'ubuntu23': 'sthings-u23'
   }
}

print(disk['L'])
print(os['labul-vsphere']['ubuntu23'])
```

</details>

<details><summary>GET RANDOM VALUE FROM LIST</summary>

```python3
import random

# GET RANDOM ITEM FROM LIST
def get_random_fromlist(list):
  random_num = random.choice(list)
  print("Random select is : " + str(random_num))

  return str(random_num)
```

</details>

<details><summary>READ YAML FILE</summary>

```yaml
# values.yaml
---
source: github.com/stuttgart-things/aws-ec2-vm
region:
  - eu-central-1
  - eu-central-2
  - eu-central-3
vpc: vpc-ec6e8e86
ami: ami-023adaba598e661ac
itype:
  - t2.micro
  - t3.micro
  - t4.micro
```

```python3
import yaml

# OPEN YAML AS DICT
with open('values.yaml', 'r') as f:
    values = yaml.load(f, Loader=yaml.SafeLoader)

# ITERATE OVER THE VALUES DICTIONARY
for key in values:
  print(key)
  print(values[key])
```

</details>

<details><summary>SET/OVERWRITE YAML VALUE</summary>

```python3
values['call']['source'] = "local"
```

</details>

<details><summary>GET YAML (SUB-)KEY</summary>

```yaml
# values.yaml
---
name: hello
call:
  source: '"github.com/stuttgart-things/aws-ec2-vm"'
  region:
```

```python3
with open(args.values, 'r') as f:
    values = yaml.load(f, Loader=yaml.SafeLoader)

renderedTemplate = render_template(values.get('call'))
```

</details>

<details><summary>CONCATENATE STRING AND INT</summary>

```python3
now = datetime.now()
scan_id = f'{now.year}-{now.month}-{now.day}-{now.minute}-{now.second}'
```

</details>

<details><summary>INLINE JINJA RENDERING</summary>

```python3
#!/usr/bin/env python3
from jinja2 import Template
name = input("Enter your name: ")
tm = Template("Hello {{ name }}")
msg = tm.render(name=name)
print(msg)
```

```python3
#!/usr/bin/env python3

from jinja2 import Template
import os

inlineTemplate = "{% for count in range(0, vm_count) %}{% if loop.first%}{{ vm }}{% else %}{{ vm }}-{{ loop.index }}{% endif %}{% if not loop.last %}, {% endif %}{% endfor %}"

def render_template(values):
  template = Template(inlineTemplate)
  renderedTemplate = template.render(values)

  return str(renderedTemplate)

def main():

    values = {
       'vm': 'minnesota',
       'vm_count': 4,
    }

    rendered = render_template(values)
    print(rendered)

if __name__ == '__main__':
    main()
```

</details>

<details><summary>FILE TEMPLATE RENDERING</summary>

## EXAMPLE 1

```bash
# template.json
#...
"source": "url",
          "type": "json",
          "url": "{{ uploaded_data_url }}",
          "url_options": {
            "data": "",
            "method": "GET"
#..
```

```python3
# RENDER GRAFANA TEMPLATE/DASHBOARD
environment = Environment(loader=FileSystemLoader(current_dir+'/'))
template = environment.get_template(grafana_template_filename)
rendered_template = template.render(
    uploaded_data_url = upload_address + "/" +data_json_outputfile
)

print(rendered_template)

# WRITE RENDERED TEMPLATE TO DISK
file_object = open(template_json_outputfile, "w")
file_object.write(rendered_template)
file_object.close()
```

## EXAMPLE 2

```bash
# message.txt
{# templates/message.txt #}

Hello {{ name }}!

I'm happy to inform you that you did very well on today's {{ test_name }}.
You reached {{ score }} out of {{ max_score }} points.

See you tomorrow!
Pat
```

```python3
#!/usr/bin/env python3
# write_messages.py

from jinja2 import Environment, FileSystemLoader
import os

max_score = 100
test_name = "Python Challenge"
students = [
    {"name": "Sandrine",  "score": 100},
    {"name": "Gergeley", "score": 87},
    {"name": "Frieda", "score": 92},
]

path = os.path.dirname(os.path.realpath(__file__))
print(path+"/")

environment = Environment(loader=FileSystemLoader(path+"/"))
template = environment.get_template("message.txt")

for student in students:
    filename = f"message_{student['name'].lower()}.txt"
    content = template.render(
        student,
        max_score=max_score,
        test_name=test_name
    )
    with open(filename, mode="w", encoding="utf-8") as message:
        message.write(content)
        print(f"... wrote {filename}")
```

</details>
