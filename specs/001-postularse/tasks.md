# Tareas: 001 Postularse a la práctica empresarial

## Capa de dominio

- [x] T-01 Definir `EstadoPostulacion` y los estados considerados en trámite
      Archivos: `src/dominio/estado_postulacion.py`
      Escenarios: 1, 2, 3, 4, 6
      Depende de: ninguna

- [x] T-02 Crear entidad `Programa`
      Archivos: `src/dominio/programa.py`
      Escenarios: 1, 2, 4, 6
      Depende de: ninguna

- [x] T-03 Crear entidad `ReglaPractica` con evaluación de porcentaje mínimo de créditos y matrícula activa
      Archivos: `src/dominio/regla_practica.py`
      Escenarios: 1, 2, 4, 6
      Depende de: T-02

- [x] T-04 Crear entidad `Estudiante` vinculada a su `Programa`
      Archivos: `src/dominio/estudiante.py`
      Escenarios: 1, 2, 3, 4, 5, 6
      Depende de: T-02

- [x] T-05 Crear entidad `Empresa` con validación de nombre obligatorio y formato válido de NIT
      Archivos: `src/dominio/empresa.py`
      Escenarios: 1, 2, 4, 5, 6
      Depende de: ninguna

- [x] T-06 Crear entidad `SupervisorEmpresa` con validación de nombre y correo obligatorios
      Archivos: `src/dominio/supervisor_empresa.py`
      Escenarios: 1, 2, 4, 5, 6
      Depende de: T-05

- [x] T-07 Crear entidad `VerificacionRequisitos` para registrar cada intento de consulta al SIA
      Archivos: `src/dominio/verificacion_requisitos.py`
      Escenarios: 1, 2, 6
      Depende de: ninguna

- [x] T-08 Crear entidad `Postulacion` con sus reglas de transición de estado y registro de verificaciones
      Archivos: `src/dominio/postulacion.py`
      Escenarios: 1, 2, 3, 4, 6
      Depende de: T-01, T-03, T-04, T-05, T-06, T-07

- [x] T-09 Crear entidad inmutable `EventoBitacora` para auditoría de solo inserción
      Archivos: `src/dominio/evento_bitacora.py`
      Escenarios: 1, 2
      Depende de: ninguna

## Capa de aplicación (puertos y casos de uso)

- [x] T-10 Definir puerto `RepositorioPostulaciones`
      Archivos: `src/aplicacion/puertos/repositorio_postulaciones.py`
      Escenarios: 1, 2, 3, 4, 6
      Depende de: T-08

- [x] T-11 Definir puerto `RepositorioReglasPractica`
      Archivos: `src/aplicacion/puertos/repositorio_reglas_practica.py`
      Escenarios: 1, 2, 4, 6
      Depende de: T-03

- [x] T-12 Definir puerto de solo inserción `RepositorioBitacora`
      Archivos: `src/aplicacion/puertos/repositorio_bitacora.py`
      Escenarios: 1, 2
      Depende de: T-09

- [x] T-13 Crear DTO `DatosAcademicosDTO` con los datos devueltos por la consulta académica
      Archivos: `src/aplicacion/postulaciones/datos_academicos_dto.py`
      Escenarios: 1, 2, 6
      Depende de: ninguna

- [x] T-14 Definir puerto `ConsultaAcademica` hacia los servicios del SIA
      Archivos: `src/aplicacion/puertos/consulta_academica.py`
      Escenarios: 1, 2, 6
      Depende de: T-13

- [ ] T-15 Definir puerto `PublicadorMensajes` para encolar y reencolar verificaciones pendientes
      Archivos: `src/aplicacion/puertos/publicador_mensajes.py`
      Escenarios: 1, 2, 6
      Depende de: ninguna

- [ ] T-16 Definir puerto `Notificador` para el envío de resultados por correo al estudiante
      Archivos: `src/aplicacion/puertos/notificador.py`
      Escenarios: 1, 2
      Depende de: ninguna

- [ ] T-17 Implementar componente `RegistrarEventoBitacora` del Módulo Auditoría
      Archivos: `src/aplicacion/auditoria/registrar_evento_bitacora.py`
      Escenarios: 1, 2
      Depende de: T-09, T-12

- [ ] T-18 Implementar componente `ObtenerReglaVigente` del Módulo Reglas
      Archivos: `src/aplicacion/reglas/obtener_regla_vigente.py`
      Escenarios: 1, 2, 4, 6
      Depende de: T-03, T-11

- [ ] T-19 Crear DTO de entrada `SolicitudPostulacionDTO`
      Archivos: `src/aplicacion/postulaciones/solicitud_postulacion_dto.py`
      Escenarios: 1, 2, 3, 4, 5, 6
      Depende de: ninguna

- [ ] T-20 Crear DTO de salida `RespuestaPostulacionDTO`
      Archivos: `src/aplicacion/postulaciones/respuesta_postulacion_dto.py`
      Escenarios: 1, 2, 3, 4, 5, 6
      Depende de: ninguna

- [ ] T-21 Implementar caso de uso `PostularsePractica` (control de duplicados, validación de empresa, guardado pendiente y confirmación rápida)
      Archivos: `src/aplicacion/postulaciones/postularse_practica.py`
      Escenarios: 1, 2, 3, 4, 5, 6
      Depende de: T-08, T-10, T-15, T-17, T-18, T-19, T-20

- [ ] T-22 Implementar caso de uso `VerificarRequisitosPostulacion` (consulta al SIA, evaluación de reglas, manejo de fallas con reintento, bitácora y notificación)
      Archivos: `src/aplicacion/postulaciones/verificar_requisitos_postulacion.py`
      Escenarios: 1, 2, 6
      Depende de: T-08, T-10, T-14, T-15, T-16, T-17

## Capa de infraestructura y composición

- [ ] T-23 Implementar adaptador en memoria `RepositorioPostulacionesMemoria`
      Archivos: `src/infraestructura/persistencia/repositorio_postulaciones_memoria.py`
      Escenarios: 1, 2, 3, 4, 6
      Depende de: T-10

- [ ] T-24 Implementar adaptador en memoria `RepositorioReglasPracticaMemoria`
      Archivos: `src/infraestructura/persistencia/repositorio_reglas_practica_memoria.py`
      Escenarios: 1, 2, 4, 6
      Depende de: T-11

- [ ] T-25 Implementar adaptador en memoria de solo inserción `RepositorioBitacoraMemoria`
      Archivos: `src/infraestructura/persistencia/repositorio_bitacora_memoria.py`
      Escenarios: 1, 2
      Depende de: T-12

- [ ] T-26 Implementar adaptador `PublicadorMensajesMemoria` con cola persistente simulada y espera creciente
      Archivos: `src/infraestructura/mensajeria/publicador_mensajes_memoria.py`
      Escenarios: 1, 2, 6
      Depende de: T-15

- [ ] T-27 Implementar adaptador `ConsumidorMensajesVerificacion` del worker
      Archivos: `src/infraestructura/mensajeria/consumidor_mensajes_verificacion.py`
      Escenarios: 1, 2, 6
      Depende de: T-22, T-26

- [ ] T-28 Implementar adaptador `AdaptadorSIAMemoria` con simulación de respuesta académica y falla de tiempo límite de 5 s (`EAC-02`)
      Archivos: `src/infraestructura/sia/adaptador_sia_memoria.py`
      Escenarios: 1, 2, 6
      Depende de: T-14

- [ ] T-29 Implementar adaptador `AdaptadorCorreoMemoria` para notificaciones al estudiante
      Archivos: `src/infraestructura/notificaciones/adaptador_correo_memoria.py`
      Escenarios: 1, 2
      Depende de: T-16

- [ ] T-30 Implementar raíz de composición `ContenedorPostulaciones`
      Archivos: `src/infraestructura/composicion/contenedor_postulaciones.py`
      Escenarios: 1, 2, 3, 4, 5, 6
      Depende de: T-21, T-22, T-23, T-24, T-25, T-26, T-27, T-28, T-29

## Validación

- [ ] T-31 Validar los escenarios de `spec.md` y la regla de dependencia en `validacion.md`
      Archivos: `specs/001-postularse/validacion.md`
      Escenarios: 1, 2, 3, 4, 5, 6
      Depende de: T-30
