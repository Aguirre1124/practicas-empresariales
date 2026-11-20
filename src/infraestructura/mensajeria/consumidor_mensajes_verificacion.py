from aplicacion.postulaciones.respuesta_postulacion_dto import RespuestaPostulacionDTO
from aplicacion.postulaciones.verificar_requisitos_postulacion import (
    VerificarRequisitosPostulacion,
)
from infraestructura.mensajeria.publicador_mensajes_memoria import (
    PublicadorMensajesMemoria,
)


class ConsumidorMensajesVerificacion:
    def __init__(
        self,
        cola: PublicadorMensajesMemoria,
        verificar_requisitos: VerificarRequisitosPostulacion,
    ) -> None:
        self._cola = cola
        self._verificar_requisitos = verificar_requisitos

    def procesar_siguiente(self) -> RespuestaPostulacionDTO | None:
        mensaje = self._cola.tomar_siguiente()
        if mensaje is None:
            return None
        id_postulacion, _espera_segundos = mensaje
        return self._verificar_requisitos.ejecutar(id_postulacion=id_postulacion)

    def procesar_lote(self, max_iteraciones: int = 100) -> list[RespuestaPostulacionDTO]:
        resultados: list[RespuestaPostulacionDTO] = []
        for _ in range(max_iteraciones):
            resultado = self.procesar_siguiente()
            if resultado is None:
                break
            resultados.append(resultado)
        return resultados
