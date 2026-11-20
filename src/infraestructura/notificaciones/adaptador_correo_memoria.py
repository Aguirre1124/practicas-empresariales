class AdaptadorCorreoMemoria:
    def __init__(self) -> None:
        self.correos_enviados: list[dict[str, str]] = []

    def enviar_correo(
        self,
        destinatario: str,
        asunto: str,
        mensaje: str,
    ) -> None:
        self.correos_enviados.append(
            {
                "destinatario": destinatario,
                "asunto": asunto,
                "mensaje": mensaje,
            }
        )
