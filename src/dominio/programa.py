from dataclasses import dataclass


@dataclass(frozen=True)
class Programa:
    nombre: str

    def __post_init__(self) -> None:
        nombre_limpio = self.nombre.strip() if self.nombre else ""
        if not nombre_limpio:
            raise ValueError("El nombre del programa académico es obligatorio.")
        object.__setattr__(self, "nombre", nombre_limpio)
