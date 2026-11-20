# AGENTS.md: Sistema de Gestión de Prácticas Empresariales

## Fuentes de verdad

- `docs/arquitectura.md`: mapa de la arquitectura (visión, drivers, ADR, vistas y glosario).
- `docs/drivers.md`, sección 1: catálogo de casos de uso. Es la lista de funcionalidades del sistema.
- `specs/`: una carpeta por caso de uso del catálogo, con el mismo número
  (`CU-01` → `specs/001-postularse/`), con `spec.md`, `plan.md`, `tasks.md` y `validacion.md`.
  La columna "Se especifica en" del catálogo enlaza cada caso de uso con su carpeta.
- Si el código contradice una especificación, gana la especificación.
- Si la especificación parece incorrecta o incompleta: detenerse y preguntar. No suponer.

## Arquitectura

- Estructura general: monolito modular (ver `docs/adr/ADR-001-estructura-general.md`).
- Organización interna del código: Clean Architecture (ver `docs/adr/ADR-001-estructura-general.md` y `docs/vistas/03-desarrollo.md`).
- Regla de dependencia: `dominio/` no importa nada de `aplicacion/` ni de `infraestructura/`; `aplicacion/` solo importa de `dominio/`.
- Puertos: definidos como `Protocol` en `aplicacion/puertos/` (ver `docs/adr/ADR-002-integracion-sia.md` y `docs/vistas/03-desarrollo.md`).
- Persistencia: PostgreSQL y almacenamiento institucional sin borrado (ver `docs/adr/ADR-009-persistencia.md`). En esta etapa, adaptadores en memoria.
- No se usa ninguna tecnología, librería o componente que no esté en un ADR o en el plan de la funcionalidad.

## Convenciones de código

- Lenguaje: Python 3.14.
- Una clase por archivo.
- Sin archivos `__init__.py` (paquetes de espacio de nombres).
- DTO en la entrada y en la salida de los casos de uso.
- Nombres de clases, atributos y métodos según el glosario (sección 10 de `docs/arquitectura.md`).

## Forma de trabajar

- Una fase o una tarea por sesión.
- Ejecutar solo lo que pide el prompt de la fase indicada; no adelantar fases.
- Implementar una sola tarea de `tasks.md` a la vez.
- Al terminar: listar los archivos creados o cambiados, marcar la tarea y detenerse.
- No inventar requisitos: lo que no esté en los documentos se marca con
  `[NECESITA ACLARACIÓN: <pregunta>]` en `spec.md` o se pregunta.
- No modificar archivos de `docs/` salvo que la persona lo pida.
