#!/usr/bin/env python3

from prometheus_client import CollectorRegistry, Gauge, Enum, Info, generate_latest
import docker

registry = CollectorRegistry()
namespace = "containers_health"

exporter_version = Info(
    "exporter_version",
    "Exporter version",
    namespace=namespace,
    registry=registry,
)

container_id_name_labels = ["id", "name"]
containers_state_status = Enum(
    "containers_state",
    "Container's status (string representation); can be one of [running, paused, ...]",
    [*container_id_name_labels],
    namespace=namespace,
    registry=registry,
    states=["running", "paused", "exited"]
)
containers_state_health = Enum(
    "containers_state_health",
    "Container healthyness; can be \"healthy\", \"unhealthy\" or \"unchecked\" if health-check is not specified",
    [*container_id_name_labels],
    namespace=namespace,
    registry=registry,
    states=["healthy", "unhealthy", "unchecked"]
)
containers_state_health_v2 = Gauge(
    "containers_state_health_v2",
    "Container healthyness; gauge value for \"healthy\" is 1, 4 for \"unhealthy\" and 2 if health check is not specified",
    [*container_id_name_labels],
    namespace=namespace,
    registry=registry
)


def collect_containers_metrics():
    d = docker.from_env()
    containers = d.containers.list(all=True)
    for container in containers:
        state = d.api.inspect_container(container.id)["State"]
        containers_state_status.labels(
            id=container.id,
            name=container.name
            ).state(state["Status"])
        health_state = "unchecked"
        if "Health" in state:
            health_state = state["Health"]["Status"]
        containers_state_health.labels(
            id=container.id,
            name=container.name
            ).state(health_state)
        health_state_gauge_value = None
        match health_state:
            case "healthy":
                health_state_gauge_value = 1
            case "unchecked":
                health_state_gauge_value = 2
            case "unhealthy":
                health_state_gauge_value = 4
        containers_state_health_v2.labels(
            id=container.id,
            name=container.name
            ).set(health_state_gauge_value)

def main():
    exporter_version.info({"version": "0.1.1"})

    collect_containers_metrics()
    print(generate_latest(registry).decode(), end="")


if __name__ == "__main__":
    main()
