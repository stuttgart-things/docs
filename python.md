# stuttgart-things/docs/python

## SNIPPETS

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
