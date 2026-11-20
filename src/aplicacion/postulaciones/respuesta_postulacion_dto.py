from dataclasses import dataclass


@dataclass(frozen=True)
class RespuestaPostulacionDTO:
    aceptada: bool
    id_postulacion: str | None
    estado: str | None
    mensaje: str
    detalle_verificacion: str | None = None
