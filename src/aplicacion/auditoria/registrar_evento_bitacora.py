from datetime import datetime, timezone

from aplicacion.puertos.repositorio_bitacora import RepositorioBitacora
from dominio.evento_bitacora import EventoBitacora


class RegistrarEventoBitacora:
    def __init__(self, repositorio_bitacora: RepositorioBitacora) -> None:
        self._repositorio_bitacora = repositorio_bitacora

    def ejecutar(
        self,
        usuario: str,
        accion: str,
        direccion_origen: str,
        detalle: str,
        id_referencia: str = "",
    ) -> EventoBitacora:
        evento = EventoBitacora(
            fecha_hora=datetime.now(timezone.utc),
            usuario=usuario,
            accion=accion,
            direccion_origen=direccion_origen,
            detalle=detalle,
            id_referencia=id_referencia,
        )
        self._repositorio_bitacora.registrar(evento)
        return evento
