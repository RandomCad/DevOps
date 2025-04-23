{{/* simple deployment + service */}}
{{- define "devnotes.service" }}
apiVersion: v1
kind: Service
metadata:
  name: {{ .name }}-svc
spec:
  selector:
    app.kubernetes.io/name: {{ .name }}
  ports:
    - protocol: TCP
      port: 80
      targetPort: {{ .port }}
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ .name }}
  labels:
    app: {{ .name }}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {{ .name }}
  template:
    metadata:
      labels:
        app: {{ .name }}
    spec:
      topologySpreadConstraints:
      - maxSkew: 1
        topologyKey: node.kubernetes.io/instance-type # all nodes should have 'k3s'
        whenUnsatisfiable: ScheduleAnyway
        labelSelector:
          matchExpressions:
          - key: app
            operator: Exists
      containers:
      - name: {{ .name }}
        imagePullPolicy: Always
        image: {{ .image | default (print "balindner/" .name) }}
        ports:
        - containerPort: {{ .port }}
{{- end }}

{{/* ingress: path -> service */}}
{{- define "devnotes.ingress" }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: devnotes-ingress-{{ .service }}
  namespace: dhge
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt
spec:
  ingressClassName: traefik
  rules:
  - host: "notes.pein-gera.de"
    http:
      paths:
      - path: {{ .path }}
        pathType: Prefix
        backend:
          service:
            name: {{ .service }}-svc
            port:
              number: 80
  tls:
  - secretName: notes-pein-gera-de-tls
    hosts:
    - notes.pein-gera.de
{{- end }}