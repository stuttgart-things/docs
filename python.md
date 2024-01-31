# stuttgart-things/docs/python

## SNIPPETS

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
