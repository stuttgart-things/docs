#!/bin/bash

SITE_NAME=$1

echo "Creating hugo site ${SITE_NAME}"
hugo new site ${SITE_NAME} -f "yaml"
rm ${SITE_NAME}/hugo.toml
git clone https://github.com/alex-shpak/hugo-book ./${SITE_NAME}/themes/hugo-book

# WORKAROUND
#cd ./${SITE_NAME}/themes/hugo-book && git checkout v9 && cd -

mkdir -p ./${SITE_NAME}/content/docs

# REWRITING DETAILS
sed -i 's@<details><summary><b>@<details><summary>@g; s@</b></summary>@</summary>@g; s@<details><summary>@{{< expand "@g; s@</summary>@" >}}@g; s@</details>@{{< /expand >}}@g' *.md

# COPY HUGO CONTENT
#cp -R hugo/config.yaml ./${SITE_NAME}
cp -R hugo/*.png ./${SITE_NAME}/static
cp -R hugo/*.ico ./${SITE_NAME}/static
cp -R hugo/*.md ./${SITE_NAME}/content
cp -R hugo/mermaid.json ./${SITE_NAME}/assets


# CREATE MANIFESTS AS MD
dir="manifests"
file="*.yaml"
out="manifests.md"

# MANIFESTS

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

# STAGETIME

# CREATE MANIFESTS AS MD
dir="stageTime"
file="*.yaml"
out="stageTime.md"

# CREATE HEADER
echo -e "# /stageTime\n" >> ${out}

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
dir=${SITE_NAME}
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

cp *.md ./${SITE_NAME}/content/docs
ls -lta ${SITE_NAME}/content/docs

# Modify and add hugo yaml
cat <<EOF | cat - hugo/hugo.yaml > temp && mv temp hugo/hugo.yaml
baseURL: 'https://stuttgart-things.github.io/docs/'
EOF

cp -f hugo/hugo.yaml ./${SITE_NAME}
