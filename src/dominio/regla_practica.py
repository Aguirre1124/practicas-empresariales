from dataclasses import dataclass

from dominio.programa import Programa


@dataclass(frozen=True)
class ReglaPractica:
    programa: Programa
    periodo_vigencia: str
    porcentaje_creditos_minimo: float = 80.0
    matricula_activa_requerida: bool = True
    horas_minimas: int = 480
    plazo_evaluacion_dias: int = 15

    def __post_init__(self) -> None:
        periodo = self.periodo_vigencia.strip() if self.periodo_vigencia else ""
        if not periodo:
            raise ValueError("El periodo de vigencia de la regla es obligatorio.")
        if not (0 < self.porcentaje_creditos_minimo <= 100):
            raise ValueError("El porcentaje mínimo de créditos debe estar entre 0 y 100.")
        if self.horas_minimas <= 0:
            raise ValueError("Las horas mínimas deben ser mayores a cero.")
        if self.plazo_evaluacion_dias <= 0:
            raise ValueError("El plazo de evaluación debe ser mayor a cero.")
        object.__setattr__(self, "periodo_vigencia", periodo)

    def evaluar_requisitos(
        self,
        porcentaje_creditos_aprobados: float,
        matricula_activa: bool,
    ) -> list[str]:
        incumplimientos: list[str] = []
        if porcentaje_creditos_aprobados < self.porcentaje_creditos_minimo:
            incumplimientos.append(
                f"No alcanza el mínimo de {self.porcentaje_creditos_minimo:g}% de créditos aprobados "
                f"(tiene {porcentaje_creditos_aprobados:g}%)."
            )
        if self.matricula_activa_requerida and not matricula_activa:
            incumplimientos.append("No tiene matrícula activa en el periodo académico vigente.")
        return incumplimientos
