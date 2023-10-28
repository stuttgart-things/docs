#!/bin/bash

dir="manifests"
file="*.yaml"
out="manifests.md"

# CREATE HEADER
echo -e "# /EXAMPLE-MANIFESTS\n" >> ${out}

for file in `cd ${dir};ls -1 ${file}` ;do
   echo ${file}
   echo '{{< expand '\"${file}\"' "..." >}}' >> ${out}
   echo -e "\n" >> ${out}
   echo -e '```yaml' >> ${out}
   cat ${dir}/${file} >> ${out}
   echo -e '\n```\n' >> ${out}
   echo '{{< /expand >}}' >> ${out}
   echo -e "\n" >> ${out}
done
