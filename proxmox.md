# stuttgart-things/docs/proxmox

## MONITORING

<details><summary><b>INSTALL PUB CERTS PROXMOX</b></summary>

```bash
mkdir -p /etc/pve/nodes/<node>/certificates/custom

wget -O /etc/pve/nodes/<node>/certificates/custom/custom-ca.crt https://<vault url>:8200/v1/pki/ca/pem --no-check-certificate
```

</details>

<details><summary><b>DEPLOY INFLUXDB</b></summary>

</details>

<details><summary><b>CONFIGURE INFLUXDB</b></summary>

BUCKET/TOKEN ETC..

</details>

<details><summary><b>CONFIGURE METRIC SHIPPING ON PROXMOX WEB UI</b></summary>
  
PVE -> Datacenter -> Metric Server -> Add -> InfluxDB

|Create: InfluxDB|  |  |  |
|--|--|--|--|
|Name|influxdb-automation|Enabled|YES|
|Server|<influxdb.ingress address>|Organization|influxdata|
|Port|443|Bucket|_monitoring|
|Protocol|HTTPS|Token|<32bit Token>|
|API Path Prefix|leave empty|Batch Size (b)|leave default|
|Timeout (s)|leave default|MTU|leave default|
|Verify Certificate|Yes|  |  |

</details>

<details><summary><b>CONFIGURE GRAFANA DASHBOARD</b></summary>
  
Grafana -> Connections -> Add new connection -> InfluxDB

Change Query language  
Query language -> Flux

|HTTP|  |
|----|--|
|URL|http://influxdb-influxdb2.influxdb.svc.cluster.local|
|Allowed Cookies|Don't needed|
|Timeout|Don't needed|

|AUTH|  |  |  |
|----|--|--|--|
|Basic auth|NO|With Credentials|NO|
|TLS Client Auth|NO|With CA Cert|NO|
|Skip TLS Verify|YES|||
|Forward OAuth Identity|NO|||

|InfluxDB Details||
|---|---|
|Organization|influxdata|
|Token|<InfluxDB Admin's Token>|
|Default Bucket|_monitoring|
|Min time interval|leave default|
|Max series|leave default|

</details>
