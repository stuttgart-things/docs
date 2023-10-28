#!/bin/bash

dir="manifests"
file="*.yaml"
out="manifests.md"

for file in `cd ${dir};ls -1 ${file}` ;do
   echo ${file}
   echo -e "# /Manifests\n" >> ${out}
   echo '{{< expand '\"${file}\"' "..." >}}' >> ${out}
   echo -e "\n" >> ${out}
   echo -e '```yaml' >> ${out}
   cat ${dir}/${file} >> ${out}
   echo -e '\n```\n' >> ${out}
   echo '{{< /expand >}}' >> ${out}
   echo -e "\n" >> ${out}
done
