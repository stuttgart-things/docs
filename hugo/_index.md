---
title: Introduction
type: docs
---

# STUTTGART-THINGS/DOCS/

  <p>
    <img src="sthings-city.png" alt="sthings" width="450" />
  </p>
  <p>
    <strong>[sˈθɪŋz]</strong>- using modularity to speed up parallel builds
  </p>

## stuttgart-things 🍿
microservice development, configuration/infrastructure as code & creation of clis based on surveys.

{{< button relref="/" >}}Get Home{{< /button >}} {{< button href="https://github.com/stuttgart-things" >}}Contribute{{< /button >}}


{{- $pathURL := .Get "pathURL" -}}
{{- $path := .Get "path" -}}
{{- $files := readDir $path -}}
<table>
    <th>Size in bytes</th>
    <th>Name</th>
{{- range $files }}
    <tr>
        <td>{{ .Size }}</td>
        <td><a href="{{ $pathURL }}{{ .Name | relURL }}"> {{ .Name }}</a></td>
    </tr>
{{- end }}
</table>
