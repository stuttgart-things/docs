#!/bin/bash

# COPY HUGO CONTENT
cp -R hugo/config.yaml ./blog
cp -R hugo/*.png ./blog/static
cp -R hugo/*.ico ./blog/static
cp -R hugo/*.md ./blog/content

# CREATE MANIFESTS AS MD
dir="manifests"
file="*.yaml"
out="manifests.md"

# CREATE HEADER
echo -e "# /MANIFESTS\n" >> ${out}

# CREATE MANIFESTS INTO MD
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

# CREATE STHINGS AS MD

dir="hugo"
file="sthings-*.png"
out="sthings.md"

# CREATE HEADER
echo -e "# /STHINGS\n" >> ${out}

for file in `cd ${dir};ls -1 ${file}` ;do
   echo ${file}
   echo '{{< expand '\"${file}\"' "..." >}}' >> ${out}
   echo -e "\n" >> ${out}
   echo -e "![${file}](/static/${file})" >> ${out}
   echo '{{< /expand >}}' >> ${out}
done