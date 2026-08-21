# LabDA: Wildcard-DNS + Cilium-LB + Vault-Zertifikate pro Cluster

Wie ein Cluster in LabDA seine Services unter eigenen Namen erreichbar macht — eine LoadBalancer-IP, ein Wildcard-Record, Zertifikate aus Vault-PKI.

**Am 2026-08-21 auf `seed-labda-1` (rke2, `10.100.136.52`) Ende zu Ende durchgemessen** und von einem Laptop ausserhalb des Cluster-Subnetzes per Namen aufgerufen. Vorlage fuer den naechsten Platform-Cluster.

```
Cilium gibt eine LB-IP frei
  -> PowerDNS: *.<cluster>.4sthings.tiab.ssc.sva.de -> diese IP
    -> Service antwortet
      -> Zertifikat aus Vault-PKI
```

## Die Landschaft, bevor es losgeht

Es gibt in LabDA **zwei getrennte DNS-Welten**, und die Verwechslung kostet am meisten Zeit:

| Zone | Autoritaet | fuer uns |
|---|---|---|
| `tiab.labda.sva.de`, `labda.sva.de` | Infoblox (`infoblox01.labwi`, `infoblox02.labda`, …) | Konzern-DNS, **nicht schreibbar**. Hier leben die Node-Namen. |
| `4sthings.tiab.ssc.sva.de` | **PowerDNS `10.100.136.115`** (`pdns-vsphere.tiab.labda.sva.de`), API auf `:8443` | unsere Zone. Hier entstehen die Wildcards. |

Der PowerDNS antwortet auf `tiab.labda.sva.de` mit **REFUSED** — wer dort Cluster-Namen sucht, fragt den falschen Server. Die Delegation von Infoblox auf ihn ist korrekt eingetragen (`4sthings.tiab.ssc.sva.de NS -> pdns-vsphere.tiab.labda.sva.de`).

**Das Muster in der Zone ist ein Wildcard pro Cluster**, TTL 60, Typ A. Bestand am 2026-08-21: `*.app`/`*.mgmt`/`*.preapp`/`*.sthings-infra-dev` -> `.220` (Altbestand, antwortet nicht mehr), `*.test2` -> `.222`, `*.dev7` -> `.223`, `*.dev8` -> `.226`, `*.dev11` -> `.228`, `*.seed-labda-1` -> `.221`.

**IP-Bereich:** `10.100.136.220–229` ist fuer uns reserviert und im DNS ausgenommen. Es gibt in LabDA (Stand 2026-08-21) **kein clusterbook**, die IP wird also von Hand vergeben — freie pruefen, indem man die Wildcards der Zone auflistet (siehe Schritt 3).

Der API-Key des PowerDNS steht in Vault unter `apps/powerdns`, nicht in diesem Dokument.

---

## Schritt 1 — Vault: PKI-Rolle und Recht darauf

Der von der Platform emittierte Issuer (`vault-pki-k8s`) signiert `pki/sign/tiab.labda.sva.de` — die **falsche Domain** fuer diese Zone. `pkiRole` im Platform-XRD ist ein einzelner String und deckt nur einen Issuer ab, es braucht also einen zweiten.

Auf dem **LabDA-Vault** (`vault-vsphere.tiab.labda.sva.de:8200`) existiert die Rolle `4sthings.tiab.ssc.sva.de` bereits. Was fehlt, ist das Recht der cert-manager-Rolle darauf.

**1a. Policy anlegen** (Token mit Schreibrecht auf `sys/policies/acl/*`):

```hcl
# vault policy write pki-issue-4sthings -
path "pki/sign/4sthings.tiab.ssc.sva.de" {
  capabilities = ["create", "update"]
}
```

Nur `sign`, **nicht `issue`**: cert-manager benutzt ausschliesslich den sign-Endpunkt; `issue` wuerde zusaetzlich erlauben, sich den privaten Schluessel von Vault erzeugen zu lassen.

Eine eigene Policy statt `pki-issue` zu erweitern, weil `pki-issue` der XRD-Default fuer **jeden** Cluster ist — sie zu erweitern gaebe den Signierpfad an alles frei, was sie traegt.

**1b. Der Rolle zuordnen**, im ClusterStack (`stuttgart-things`, `crossplane/xrs/clusterstack/labda/<cluster>.yaml`):

```yaml
spec:
  platform:
    vaultIssuer:
      pkiRole: tiab.labda.sva.de
      tokenPolicies:
        - pki-issue
        - pki-issue-4sthings
```

`tokenPolicies`, nicht `policies` — letzteres verlangt einen AppRole, der Policies schreiben darf. Nach dem Anwenden reconciled der vault-auth-Workspace und schreibt die Policies an die Kubernetes-Auth-Rolle. Kontrolle:

```bash
kubectl -n crossplane-system get workspace <cluster>-certmanager-vault-auth \
  -o json | jq -r '.spec.forProvider.vars[]|select(.key=="token_policies")|.value'
```

## Schritt 2 — ClusterIssuer fuer die Zone

Gleiche Anmeldung wie der vorhandene Issuer, nur ein anderer Pfad:

```yaml
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: vault-pki-4sthings
spec:
  vault:
    server: https://vault-vsphere.tiab.labda.sva.de:8200
    path: pki/sign/4sthings.tiab.ssc.sva.de
    caBundleSecretRef:
      key: ca.crt
      name: vault-pki-ca        # legt der vaultIssuer-Zweig der Platform an
    auth:
      kubernetes:
        mountPath: /v1/auth/<cluster>-certmanager
        role: certmanager
        serviceAccountRef:
          name: cert-manager
```

> **`Ready: True` heisst hier NICHT, dass er signieren darf.** cert-manager prueft beim Verify nur die Anmeldung. Der Beweis ist das erste ausgestellte Zertifikat.

## Schritt 3 — Cilium: LoadBalancer-IP

Voraussetzung ist `enable-l2-announcements=true` in der cilium-Config (auf den machinery-Clustern gesetzt). **L2-Announcement traegt nur auf einem echten Netzsegment** — auf kind waere die IP von aussen tot.

Freie IP finden:

```bash
curl -sSk -H "X-API-Key: $PDNS_KEY" \
  https://pdns-vsphere.tiab.labda.sva.de:8443/api/v1/servers/localhost/zones/4sthings.tiab.ssc.sva.de. \
  | jq -r '.rrsets[]|select(.name|startswith("*"))|"\(.name) -> \(.records[0].content)"'
```

**Achtung auf die API-Versionen** — bei Cilium 1.19.3 sind sie gemischt:

```yaml
apiVersion: cilium.io/v2          # Pool: schon v2
kind: CiliumLoadBalancerIPPool
metadata:
  name: <cluster>-lb
spec:
  blocks:
    - start: 10.100.136.221
      stop: 10.100.136.221
---
apiVersion: cilium.io/v2alpha1    # L2-Policy: noch v2alpha1
kind: CiliumL2AnnouncementPolicy
metadata:
  name: <cluster>-l2
spec:
  loadBalancerIPs: true
  nodeSelector:
    matchLabels:
      kubernetes.io/os: linux
```

Kontrolle: `kubectl get ciliumloadbalancerippool` muss `IPS AVAILABLE 1` und `CONFLICTING False` zeigen.

## Schritt 4 — Wildcard im PowerDNS

```bash
Z=4sthings.tiab.ssc.sva.de.
curl -sSk -H "X-API-Key: $PDNS_KEY" -X PATCH \
  -d '{"rrsets":[{"name":"*.<cluster>.'"$Z"'","type":"A","ttl":60,
       "changetype":"REPLACE","records":[{"content":"10.100.136.221","disabled":false}]}]}' \
  "https://pdns-vsphere.tiab.labda.sva.de:8443/api/v1/servers/localhost/zones/$Z"
```

HTTP **204** heisst angenommen. Kontrolle direkt am autoritativen Server, nicht ueber den eigenen Resolver:

```bash
dig +short @10.100.136.115 beliebig.<cluster>.4sthings.tiab.ssc.sva.de
```

## Schritt 5 — Service mit Zertifikat

**Ein Zertifikat pro Service**, nicht eines pro Cluster — siehe „Bekannte Grenzen".

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata: {name: test-svc, namespace: default}
spec:
  secretName: test-svc-tls
  issuerRef: {name: vault-pki-4sthings, kind: ClusterIssuer}
  commonName: test.<cluster>.4sthings.tiab.ssc.sva.de
  dnsNames: ["test.<cluster>.4sthings.tiab.ssc.sva.de"]
---
apiVersion: v1
kind: Service
metadata: {name: test-svc, namespace: default}
spec:
  type: LoadBalancer
  loadBalancerIP: 10.100.136.221
  selector: {app: test-svc}
  ports: [{port: 443, targetPort: 443}]
```

Ausstellung dauert ~20 s. Der Rest ist ein beliebiger Pod, der TLS mit `test-svc-tls` terminiert.

## Verifikation

Die Reihenfolge ist bewusst so — jeder Schritt schliesst eine Fehlerursache aus:

```bash
# 1. autoritativ: gibt es den Namen?
dig +short @10.100.136.115 test.<cluster>.4sthings.tiab.ssc.sva.de

# 2. LB, L2 und Zertifikat, am DNS vorbei
curl --cacert vault-ca.pem \
  --resolve test.<cluster>.4sthings.tiab.ssc.sva.de:443:10.100.136.221 \
  https://test.<cluster>.4sthings.tiab.ssc.sva.de/

# 3. mit echter Aufloesung, vom Arbeitsplatz
curl -k https://test.<cluster>.4sthings.tiab.ssc.sva.de/
```

Schritt 2 **mit `--cacert` gegen die Vault-CA**, nicht mit `-k`: sonst prueft man nur, dass irgendein TLS steht.

---

## Fallen, die uns Zeit gekostet haben

**Vaults `403 permission denied` bedeutet drei verschiedene Dinge:** verboten, Pfad existiert nicht, oder die PKI-Rolle lehnt die Anfrage ab (z. B. ein Wildcard bei `allow_glob_domains: false`). Der Fehler unterscheidet das nicht — er verraet absichtlich nicht, ob ein Pfad existiert. Nur ein Blick in `pki/roles/<name>` trennt es auf.

**Ein `Ready`-Status ist kein Koennen.** Der ClusterIssuer meldete `VaultVerified`, obwohl jede Signieranfrage mit 403 scheiterte.

**macOS: `dig` und `curl` loesen unterschiedlich auf.** `dig` fragt die Nameserver der Reihe nach, der System-Resolver (und damit `curl` und Browser) fragt sie **parallel und nimmt die schnellste Antwort**. Ein Heimrouter, der in 7 ms NXDOMAIN sagt, schlaegt den Firmen-Resolver mit 20 ms. Abhilfe pro Arbeitsplatz:

```bash
sudo tee /etc/resolver/4sthings.tiab.ssc.sva.de >/dev/null <<'EOF'
nameserver 10.100.136.115
EOF
sudo dscacheutil -flushcache; sudo killall -HUP mDNSResponder
```

Dabei den **PowerDNS selbst** eintragen, nicht den Firmen-Resolver: bei Split-Tunneling wird `10.100.0.0/16` geroutet, `10.10.0.0/16` aber nicht — und `scutil`s `reach: Reachable` ist da optimistisch. Dass der PowerDNS nicht rekursiv ist, stoert nicht, die Datei leitet ihm nur seine eigene Zone zu.

**Negative Antworten haelt die Zone 60 Minuten** (SOA-Minimum 3600 s), waehrend die Records selbst TTL 60 haben. Ein NXDOMAIN auf einen frisch angelegten Namen ist trotzdem zuerst ein *Resolver*-Verdacht, kein Cache-Verdacht.

## Bekannte Grenzen

**Keine Wildcard-Zertifikate.** Die PKI-Rolle `4sthings.tiab.ssc.sva.de` hat `allow_glob_domains: false` (`allowed_domains: 4sthings.tiab.ssc.sva.de`, `allow_subdomains: true`, `allow_bare_domains: false`). Ein `*.<cluster>.…` wird mit 403 abgelehnt, ein normaler Name darunter in ~20 s ausgestellt. Der Wildcard im **DNS** ist davon unberuehrt. Wer ein Wildcard-**Zertifikat** will, muss die Rolle im Vault aendern — dann traegt allerdings ein einziger kompromittierter Pod den Schluessel fuer alle Namen des Clusters.

**In-cluster loest die Zone nicht auf.** CoreDNS forwardet `.` an die `/etc/resolv.conf` des Nodes, dort steht `10.100.101.5` — und dieser Resolver erreicht `10.100.136.115:53` nicht (er beantwortet die Elternzonen und die NS-Abfrage, laeuft aber beim Folgen der Delegation in den Timeout). Von aussen ist das egal; fuer Service-zu-Service ueber diese Namen braucht es einen CoreDNS-Stub auf `10.100.136.115`, den ein Pod nachweislich direkt erreicht.

**Der PowerDNS selbst ist alt.** 4.5.2, Uptime 40,8 Monate, Pflicht-Sicherheitsadvisory (2022-01) fuellt 99 % des Log-Rings, kein DNSSEC, kein NS-Record im Apex der Zone (die Delegation traegt der Elternteil). RFC2136-Updates werden abgelehnt — fuer statische Wildcards irrelevant.

**Fuer ein ganzes Team gehoert die Zone ins Split-DNS des VPN.** Sonst braucht jeder Arbeitsplatz die `/etc/resolver`-Datei, und wer sie vergisst, haelt den Dienst fuer kaputt.
