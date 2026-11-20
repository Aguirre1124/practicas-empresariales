from typing import Protocol


class Notificador(Protocol):
    def enviar_correo(
        self,
        destinatario: str,
        asunto: str,
        mensaje: str,
    ) -> None: ...
