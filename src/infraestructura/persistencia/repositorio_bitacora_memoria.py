from dominio.evento_bitacora import EventoBitacora


class RepositorioBitacoraMemoria:
    def __init__(self) -> None:
        self._eventos: list[EventoBitacora] = []

    def registrar(self, evento: EventoBitacora) -> None:
        self._eventos.append(evento)

    def listar(self) -> list[EventoBitacora]:
        return list(self._eventos)
