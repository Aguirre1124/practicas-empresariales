# Vista de procesos: diagrama de contenedores

Muestra qué se ejecuta por separado y cómo se comunica. En C4 un contenedor no es Docker: es cualquier cosa que se ejecuta o guarda datos por separado.

Para: integradores del sistema.

## 1. Presentación principal

Diagrama C4 de nivel 2: [../diagramas/02-procesos.puml](../diagramas/02-procesos.puml).

## 2. Catálogo de elementos

| Elemento | Responsabilidad | Tecnología | Se comunica con |
|---|---|---|---|
| Aplicación web | Interfaz de todos los usuarios, también desde el celular | Angular (catálogo, RT-04) | Proveedor de identidad institucional (OpenID Connect) y API de prácticas (JSON / HTTPS) |
| API de prácticas | Reglas del negocio: postulación, seguimiento, evaluación, actas y reglas. Responde sin esperar al SIA | Python, monolito modular (ADR-001) | Aplicación web, Proveedor de identidad institucional, Base de datos (SQL), Repositorio de documentos y Bróker de mensajes (AMQP) |
| Bróker de mensajes | Guarda las verificaciones pendientes y los correos por enviar hasta que el worker los procese | RabbitMQ, colas persistentes (ADR-003) | API de prácticas (publica) y Worker de integración (entrega) |
| Worker de integración | Verifica requisitos con el SIA, envía correos y recordatorios (CU-08); reintenta con espera creciente si fallan | Python, mismo código de la API con otro punto de entrada (ADR-003) | Bróker de mensajes, SIA (HTTPS / REST), Servicio de correo institucional (SMTP) y Base de datos (SQL) |
| Base de datos | Prácticas, reglas, enlaces de acceso y bitácora de auditoría | PostgreSQL (ADR-009) | API de prácticas y Worker de integración (SQL) |
| Repositorio de documentos | Actas en PDF y evidencias, sin borrado durante la retención | Almacenamiento institucional de archivos (ADR-009) | API de prácticas (HTTPS) |

## 3. Justificación

- **PA-01 y ADR-001:** una sola API, monolito modular, porque la carga es baja (S-03).
- **EAC-02, PA-04 y ADR-003:** el bróker y el worker están separados de la API. La API guarda la postulación y responde; el worker es el único que espera al SIA y al correo, y reintenta.
- **RT-03 y ADR-002:** solo el Worker de integración habla con el SIA, y lo hace por sus servicios REST.
- **RT-02, PA-02 y ADR-004:** la aplicación web redirige al proveedor de identidad y la API valida el token; el sistema no guarda contraseñas.
- **RT-04, RN-05 y ADR-009:** PostgreSQL y RabbitMQ son software libre y del catálogo institucional (supuesto S-09 por confirmar).
- **RN-01:** toda la comunicación con el usuario va cifrada (HTTPS) y la Base de datos con datos personales solo la usan la API y el worker, nunca el navegador.
- **RN-02 y ADR-009:** las actas van a un repositorio aparte con política de no borrado.
- **CU-01 y CU-09:** son los dos casos que usan más contenedores: CU-01 cruza la API, el bróker, el worker y el SIA; CU-09 cruza la API y el Repositorio de documentos.

## 4. Comportamiento

- [CU-01 Postularse](../diagramas/secuencias/cu01-postularse.puml): muestra que la API responde antes de que el SIA conteste, y los reintentos del worker cuando el SIA no responde (EAC-02).
- [CU-09 Generar el acta](../diagramas/secuencias/cu09-generar-acta.puml): la API genera el PDF y lo guarda en el Repositorio de documentos.

## 5. Vistas relacionadas

- [Contexto](../contexto.md): de dónde vienen las personas y los sistemas externos.
- [Física](04-fisica.md): en qué servidor corre cada contenedor.
- [Desarrollo](03-desarrollo.md): cómo está organizada por dentro la API de prácticas.
