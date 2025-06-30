from kubernetes import client, config
from prometheus_api_client import PrometheusConnect
import time

# === CONFIGURATION ===
PROMETHEUS_URL = "http://localhost:9091"  # Adjust if running elsewhere
DEPLOYMENT_NAME = "inference-deployment"
NAMESPACE = "default"
LATENCY_THRESHOLD = 0.5  # seconds
MIN_REPLICAS = 1
MAX_REPLICAS = 5
POLL_INTERVAL = 30  # seconds

# === INITIALIZATION ===
config.load_kube_config()
apps_v1 = client.AppsV1Api()
prom = PrometheusConnect(url=PROMETHEUS_URL, disable_ssl=True)

def get_p99_latency():
    query = 'histogram_quantile(0.99, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))'
    result = prom.custom_query(query)
    if result:
        return float(result[0]['value'][1])
    return None

def get_current_replicas():
    deploy = apps_v1.read_namespaced_deployment(DEPLOYMENT_NAME, NAMESPACE)
    return deploy.spec.replicas

def scale_deployment(replicas):
    print(f"Scaling to {replicas} replicas...")
    body = {'spec': {'replicas': replicas}}
    apps_v1.patch_namespaced_deployment_scale(
        name=DEPLOYMENT_NAME, namespace=NAMESPACE, body=body
    )

def autoscale():
    while True:
        latency = get_p99_latency()
        if latency is None:
            print("Could not fetch latency")
        else:
            print(f"Current P99 latency: {latency:.3f}s")
            current = get_current_replicas()

            if latency > LATENCY_THRESHOLD and current < MAX_REPLICAS:
                scale_deployment(current + 1)
            elif latency < LATENCY_THRESHOLD * 0.5 and current > MIN_REPLICAS:
                scale_deployment(current - 1)
            else:
                print("No scaling needed.")

        time.sleep(POLL_INTERVAL)

if __name__ == "__main__":
    autoscale()
