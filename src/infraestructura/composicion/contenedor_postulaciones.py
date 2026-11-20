from aplicacion.auditoria.registrar_evento_bitacora import RegistrarEventoBitacora
from aplicacion.postulaciones.postularse_practica import PostularsePractica
from aplicacion.postulaciones.verificar_requisitos_postulacion import (
    VerificarRequisitosPostulacion,
)
from aplicacion.reglas.obtener_regla_vigente import ObtenerReglaVigente
from infraestructura.mensajeria.consumidor_mensajes_verificacion import (
    ConsumidorMensajesVerificacion,
)
from infraestructura.mensajeria.publicador_mensajes_memoria import (
    PublicadorMensajesMemoria,
)
from infraestructura.notificaciones.adaptador_correo_memoria import (
    AdaptadorCorreoMemoria,
)
from infraestructura.persistencia.repositorio_bitacora_memoria import (
    RepositorioBitacoraMemoria,
)
from infraestructura.persistencia.repositorio_postulaciones_memoria import (
    RepositorioPostulacionesMemoria,
)
from infraestructura.persistencia.repositorio_reglas_practica_memoria import (
    RepositorioReglasPracticaMemoria,
)
from infraestructura.sia.adaptador_sia_memoria import AdaptadorSIAMemoria


class ContenedorPostulaciones:
    def __init__(self) -> None:
        self.repositorio_postulaciones = RepositorioPostulacionesMemoria()
        self.repositorio_reglas = RepositorioReglasPracticaMemoria()
        self.repositorio_bitacora = RepositorioBitacoraMemoria()
        self.publicador_mensajes = PublicadorMensajesMemoria()
        self.adaptador_sia = AdaptadorSIAMemoria()
        self.adaptador_correo = AdaptadorCorreoMemoria()

        self.registrar_evento_bitacora = RegistrarEventoBitacora(
            repositorio_bitacora=self.repositorio_bitacora,
        )
        self.obtener_regla_vigente = ObtenerReglaVigente(
            repositorio_reglas=self.repositorio_reglas,
        )
        self.postularse_practica = PostularsePractica(
            repositorio_postulaciones=self.repositorio_postulaciones,
            obtener_regla_vigente=self.obtener_regla_vigente,
            publicador_mensajes=self.publicador_mensajes,
            registrar_evento_bitacora=self.registrar_evento_bitacora,
        )
        self.verificar_requisitos = VerificarRequisitosPostulacion(
            repositorio_postulaciones=self.repositorio_postulaciones,
            consulta_academica=self.adaptador_sia,
            publicador_mensajes=self.publicador_mensajes,
            notificador=self.adaptador_correo,
            registrar_evento_bitacora=self.registrar_evento_bitacora,
        )
        self.consumidor_verificacion = ConsumidorMensajesVerificacion(
            cola=self.publicador_mensajes,
            verificar_requisitos=self.verificar_requisitos,
        )
