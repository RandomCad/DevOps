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
        imagePullPolicy: IfNotPresent
        image: {{ .image | default (print "balindner/" .name) }}
        ports:
        - containerPort: {{ .port }}
{{- end }}