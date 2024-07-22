import datetime
import pydantic

from . import base_source
from . import clients


class Process(
    pydantic.BaseModel,
):
    pid: int
    name: str
    cmdline: str
    status: str
    username: str
    cpu_pct: float
    memory_pct: float
    create_time: datetime.datetime


class ProcessSource(
    base_source.BaseSource,
):
    name = 'processes'

    def __init__(
        self,
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)

        self.process_client = clients.process.Client()

    @property
    def model(
        self,
    ):
        return Process

    def get_data(
        self,
    ):
        return [
            Process(
                pid=proc.pid,
                name=proc.name,
                cmdline=proc.cmdline or '',
                status=proc.status,
                username=proc.username,
                cpu_pct=proc.cpu_pct or 0.0,
                memory_pct=proc.memory_pct or 0.0,
                create_time=proc.create_time,
            )
            for proc in self.process_client.get_processes()
        ]
