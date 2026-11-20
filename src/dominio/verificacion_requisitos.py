from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class VerificacionRequisitos:
    numero_intento: int
    fecha: datetime
    exitosa: bool
    detalle_resultado: str

    def __post_init__(self) -> None:
        if self.numero_intento < 1:
            raise ValueError("El número de intento de verificación debe ser mayor o igual a 1.")
        detalle = self.detalle_resultado.strip() if self.detalle_resultado else ""
        if not detalle:
            raise ValueError("El detalle del resultado de la verificación es obligatorio.")
        object.__setattr__(self, "detalle_resultado", detalle)
