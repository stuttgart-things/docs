# stuttgart-things/docs/elastic

## EXPORT/IMPORT DASHBOARDS FROM/TO KIBANA

### EXPORT

```
curl http://10.31.103.144:32241/s/sthings/api/kibana/dashboards/export?dashboard=314b4030-d936-11ed-9bb1-4bda85068abe > export.json
```

### IMPORT

```
curl -k -H "Content-Type: application/json" \
-H "kbn-xsrf: true" https://kibana.dev2.sthings-pve.labul.sva.de/s/sthings/api/kibana/dashboards/import 20 \
--data-binary @export.json
```
