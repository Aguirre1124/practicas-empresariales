from typing import Protocol

from dominio.evento_bitacora import EventoBitacora


class RepositorioBitacora(Protocol):
    def registrar(self, evento: EventoBitacora) -> None: ...

    def listar(self) -> list[EventoBitacora]: ...
