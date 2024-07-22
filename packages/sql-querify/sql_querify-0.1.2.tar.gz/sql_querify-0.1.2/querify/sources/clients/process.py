import datetime
import psutil
import pydantic
import typing


class OpenFile(
    pydantic.BaseModel,
):
    path: str
    fd: int


class Process(
    pydantic.BaseModel,
):
    pid: int
    name: str
    cmdline: str | None
    status: str
    username: str
    cpu_pct: float | None
    memory_pct: float | None
    open_files: list[OpenFile]
    create_time: datetime.datetime | None


class Client:
    @staticmethod
    def get_processes() -> typing.Iterator[Process]:
        for proc in psutil.process_iter(
            [
                'pid',
                'name',
                'cmdline',
                'status',
                'username',
                'cpu_percent',
                'memory_percent',
                'open_files',
                'create_time',
            ]
        ):
            status = proc.info['status']

            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else None

            try:
                cpu_percent = proc.cpu_percent()
            except psutil.AccessDenied:
                cpu_percent = None
            except psutil.ZombieProcess:
                cpu_percent = None
                status = 'zombie'

            try:
                open_files = [
                    OpenFile(
                        path=open_file.path,
                        fd=open_file.fd,
                    )
                    for open_file in proc.open_files()
                ]
            except (psutil.AccessDenied, psutil.ZombieProcess):
                open_files = []

            yield Process(
                pid=proc.info['pid'],
                name=proc.info['name'],
                cmdline=cmdline,
                status=status,
                username=proc.info['username'],
                cpu_pct=cpu_percent,
                memory_pct=proc.info['memory_percent'],
                open_files=open_files,
                create_time=datetime.datetime.fromtimestamp(float(proc.info['create_time'])),
            )
