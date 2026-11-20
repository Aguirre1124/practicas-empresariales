from dataclasses import dataclass
import re


_PATRON_NIT = re.compile(r"^\d{6,12}(-\d)?$")


@dataclass(frozen=True)
class Empresa:
    nombre: str
    nit: str

    def __post_init__(self) -> None:
        nombre = self.nombre.strip() if self.nombre else ""
        nit = self.nit.strip() if self.nit else ""
        if not nombre:
            raise ValueError("El nombre de la empresa es obligatorio.")
        if not nit:
            raise ValueError("El NIT de la empresa es obligatorio.")
        if not _PATRON_NIT.match(nit):
            raise ValueError(
                f"El NIT '{nit}' no tiene un formato válido (use solo dígitos y opcionalmente guion con dígito de verificación)."
            )
        object.__setattr__(self, "nombre", nombre)
        object.__setattr__(self, "nit", nit)
