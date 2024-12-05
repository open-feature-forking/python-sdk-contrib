import time

from testcontainers.core.container import DockerContainer
from testcontainers.core.waiting_utils import wait_container_is_ready, wait_for_logs

HEALTH_CHECK = 8014


class FlagdContainer(DockerContainer):
    def __init__(
        self,
        image: str = "ghcr.io/open-feature/flagd-testbed:v0.5.15",
        port: int = 8013,
        **kwargs,
    ) -> None:
        super().__init__(image, **kwargs)
        self.port = port
        self.with_exposed_ports(self.port, HEALTH_CHECK)

    def start(self) -> "FlagdContainer":
        super().start()
        self._checker(self.get_container_host_ip(), self.get_exposed_port(HEALTH_CHECK))
        return self

    @wait_container_is_ready(ConnectionError)
    def _checker(self, host: str, port: str) -> None:
        # First we wait for Flagd to say it's listening
        wait_for_logs(
            self,
            "listening",
            5,
        )

        time.sleep(1)
        # Second we use the GRPC health check endpoint
        # channel = grpc.insecure_channel(host + ":" + port)
        # health_stub = health_pb2_grpc.HealthStub(channel)
        #
        # def health_check_call(stub: health_pb2_grpc.HealthStub):
        #     request = health_pb2.HealthCheckRequest()
        #     resp = stub.Check(request)
        #     if resp.status == health_pb2.HealthCheckResponse.SERVING:
        #         return True
        #     elif resp.status == health_pb2.HealthCheckResponse.NOT_SERVING:
        #         return False
        #
        # # Should succeed
        # # Check health status every 1 second for 30 seconds
        # ok = False
        # for _ in range(30):
        #     try :
        #         ok = health_check_call(health_stub)
        #     except grpc.RpcError as e:
        #
        #         channel = grpc.insecure_channel(host + ":" + port)
        #         health_stub = health_pb2_grpc.HealthStub(channel)
        #         pass
        #     if ok is True:
        #         break
        #     time.sleep(1)
        #
        # if not ok:
        #     raise ConnectionError("flagD not ready in time")
