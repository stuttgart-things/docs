# stuttgart-things/docs/python

## SNIPPETS

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
