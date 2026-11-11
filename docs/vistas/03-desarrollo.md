# Vista de desarrollo: componentes de la API de prácticas

Abre el contenedor principal, la API de prácticas, y muestra sus componentes organizados en las capas de Clean Architecture. El Worker de integración ejecuta el mismo código con otro punto de entrada (el Consumidor de mensajes), por eso sus adaptadores aparecen aquí.

Para: programadores.

## 1. Presentación principal

Diagrama C4 de nivel 3: [../diagramas/03-desarrollo.puml](../diagramas/03-desarrollo.puml).

## 2. Catálogo de elementos

| Componente | Capa | Responsabilidad | Depende de |
|---|---|---|---|
| Controlador REST | infraestructura (entrada) | Recibe las peticiones HTTP y las traduce a casos de uso | Adaptador de identidad y módulos de casos de uso |
| Adaptador de identidad | infraestructura (entrada) | Valida el token del proveedor institucional y carga el rol del usuario (ADR-004) | Proveedor de identidad institucional (HTTPS) |
| Consumidor de mensajes | infraestructura (entrada, Worker) | Toma mensajes del bróker y reintenta con espera creciente (ADR-003) | Módulo Postulaciones |
| Carga inicial | infraestructura (entrada) | Migración desde Excel (CU-15). **Pendiente, declarado como riesgo (PA-05)** | Módulo Postulaciones |
| Módulo Postulaciones | aplicación | CU-01 y CU-02: registra la postulación como pendiente, publica la verificación y procesa su resultado | Módulo Reglas, Puertos |
| Módulo Seguimiento | aplicación | CU-03 a CU-06, CU-11 y CU-13: asignación de docente asesor, horas y estado | Módulo Reglas, Puertos |
| Módulo Evaluación | aplicación | CU-07: evaluación del supervisor | Módulo Acceso externo, Puertos |
| Módulo Actas | aplicación | CU-09, CU-10 y CU-14: genera, aprueba y consolida actas (ADR-008) | Módulo Seguimiento, Módulo Evaluación, Puertos |
| Módulo Reglas | aplicación | CU-12: reglas por programa y periodo (ADR-007) | Módulo Auditoría, Puertos |
| Módulo Acceso externo | aplicación | Emite y valida enlaces de un solo uso (ADR-005) | Módulo Auditoría, Puertos |
| Módulo Auditoría | aplicación | Registra eventos en la bitácora (ADR-006) | Dominio, Puertos |
| Puertos | aplicación | Interfaces que definen los casos de uso: repositorios, ConsultaAcademica, PublicadorMensajes, Notificador, GeneradorActa y RepositorioDocumentos | Dominio |
| Dominio | dominio | Las entidades de la [vista lógica](01-logica.md) y sus reglas | Nada |
| Adaptador PostgreSQL | infraestructura (salida) | Implementa los puertos de repositorio (ADR-009) | Base de datos (SQL) |
| Publicador de mensajes | infraestructura (salida) | Implementa PublicadorMensajes (ADR-003) | Bróker de mensajes (AMQP) |
| Adaptador SIA | infraestructura (salida, Worker) | Implementa ConsultaAcademica sobre los servicios del SIA (ADR-002) | SIA (HTTPS / REST) |
| Adaptador de correo | infraestructura (salida, Worker) | Implementa Notificador | Servicio de correo institucional (SMTP) |
| Generador de PDF | infraestructura (salida) | Implementa GeneradorActa a partir de la plantilla (ADR-008) | Librería libre de HTML a PDF (RN-05) |
| Adaptador de documentos | infraestructura (salida) | Implementa RepositorioDocumentos (ADR-009) | Repositorio de documentos (HTTPS) |

### Vista de usos (sin ciclos)

Un módulo *usa* a otro si no funciona bien sin él. Todos los módulos usan el Dominio y registran en Auditoría.

| Módulo | Usa a |
|---|---|
| Módulo Actas | Módulo Seguimiento, Módulo Evaluación |
| Módulo Postulaciones | Módulo Reglas |
| Módulo Seguimiento | Módulo Reglas |
| Módulo Evaluación | Módulo Acceso externo |
| Módulo Reglas | Módulo Auditoría |
| Módulo Acceso externo | Módulo Auditoría |
| Módulo Auditoría | Dominio |

Los módulos se ordenan en niveles y cada uno solo usa a los de niveles inferiores, así que no hay ciclos:

1. Módulo Actas, Módulo Postulaciones
2. Módulo Seguimiento, Módulo Evaluación
3. Módulo Reglas, Módulo Acceso externo
4. Módulo Auditoría
5. Dominio

Ningún módulo de un nivel inferior usa a uno de un nivel superior.

**Regla de dependencia:** la infraestructura usa la aplicación (entrada) o implementa sus puertos (salida); la aplicación usa el dominio; el dominio no usa a nadie.

## 3. Justificación

- **PA-01 y ADR-001:** monolito modular, un módulo por grupo de casos de uso, con las capas de Clean Architecture.
- **EAC-01, CU-12 y ADR-007:** un programa nuevo se configura como dato en el Módulo Reglas. Si aparece un tipo de requisito nuevo se tocan solo el Módulo Reglas y el Adaptador SIA: 2 módulos, como pide la medida del escenario.
- **RT-03 y ADR-002:** el SIA queda aislado en el Adaptador SIA, detrás del puerto ConsultaAcademica.
- **RT-02, PA-02 y ADR-004:** el Adaptador de identidad es el único que habla con el proveedor institucional.
- **RN-04, EAC-03 y ADR-005:** el Módulo Acceso externo es la segunda forma de entrar, solo para el supervisor.
- **PA-03, CU-10 y ADR-006:** el Módulo Auditoría es común; ningún módulo escribe la bitácora por su cuenta.
- **PA-04 y ADR-003:** el Consumidor de mensajes centraliza los reintentos para el SIA y el correo.
- **RN-03 y ADR-008:** el Generador de PDF es un adaptador; la plantilla vive fuera del código.
- **RN-01:** el Adaptador de identidad carga el rol y cada módulo filtra por práctica.
- **PA-05:** la Carga inicial está dibujada para que no se olvide, pero queda pendiente y declarada como riesgo en [arquitectura.md](../arquitectura.md#7-decisiones-de-diseño).

## 4. Comportamiento

- [CU-01](../diagramas/secuencias/cu01-postularse.puml): Controlador REST → Módulo Postulaciones → Publicador de mensajes; luego Consumidor de mensajes → Adaptador SIA.
- [CU-07](../diagramas/secuencias/cu07-evaluar-practicante.puml): Módulo Evaluación → Módulo Acceso externo → Módulo Auditoría.
- [CU-09](../diagramas/secuencias/cu09-generar-acta.puml) y [CU-10](../diagramas/secuencias/cu10-aprobar-acta.puml): Módulo Actas → Generador de PDF y Adaptador de documentos.
- [CU-12](../diagramas/secuencias/cu12-configurar-reglas.puml): Módulo Reglas → Módulo Auditoría.

## 5. Vistas relacionadas

- [Procesos](02-procesos.md): es el interior del contenedor API de prácticas (y del Worker de integración).
- [Lógica](01-logica.md): el componente Dominio contiene esas entidades.
