"""
Kubernetes Deployment Pattern Example

This file demonstrates the generic Kubernetes Deployment and Service resource structure.
Reference this example from RULE.mdc using @examples_kubernetes.py syntax.
"""

# ============================================================================
# Kubernetes Deployment Pattern
# ============================================================================

DEPLOYMENT_MANIFEST = """
apiVersion: apps/v1
kind: Deployment
metadata:
  name: application-deployment
  labels:
    app: application
spec:
  replicas: 3
  selector:
    matchLabels:
      app: application
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  template:
    metadata:
      labels:
        app: application
    spec:
      containers:
      - name: application
        image: application:latest
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: "100m"
            memory: "256Mi"
          limits:
            cpu: "500m"
            memory: "512Mi"
        livenessProbe:
          httpGet:
            path: /health/live
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health/ready
            port: 8000
          initialDelaySeconds: 5
          periodSeconds: 5
"""

SERVICE_MANIFEST = """
apiVersion: v1
kind: Service
metadata:
  name: application-service
spec:
  selector:
    app: application
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: ClusterIP
"""

HPA_MANIFEST = """
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: application-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: application-deployment
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
"""

# ============================================================================
# ConfigMap and Secret (inject via env in Deployment)
# ============================================================================

CONFIGMAP_MANIFEST = """
apiVersion: v1
kind: ConfigMap
metadata:
  name: application-config
data:
  LOG_LEVEL: "info"
  SERVICE_ENDPOINT: "http://other-service:8000"
"""

SECRET_MANIFEST = """
apiVersion: v1
kind: Secret
metadata:
  name: application-secrets
type: Opaque
stringData:
  API_KEY: "your-api-key"
  DB_PASSWORD: "your-db-password"
"""
