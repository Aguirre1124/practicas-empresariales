# ADR-006: Registrar las acciones relevantes en una bitácora de auditoría de solo inserción

## Estado

Aceptado — 2026-11-09

## Contexto

- CU-10 (aprobar el acta) es primario por seguridad: debe quedar registrado quién aprobó el acta y cuándo (OB-06, S-06).
- EAC-03 exige que cada intento de acceso rechazado quede registrado en menos de 1 minuto, con fecha, hora y dirección de origen.
- PA-03 pide decidir qué eventos se registran, dónde y por cuánto tiempo.
- RN-01 exige poder demostrar quién accedió a datos personales.
- OB-06 pide entregar el consolidado de cualquier periodo a auditoría en máximo 1 día hábil.

## Alternativas consideradas

- **A) Usar los registros técnicos (logs) del servidor.** No requiere nada nuevo. Pero se rotan y se borran, mezclan errores técnicos con acciones de negocio y no se pueden consultar por práctica.
- **B) Columnas de auditoría en cada tabla (creado por, modificado por, fecha).** Simple. Pero solo guardan el último cambio: se pierde el historial de quién aprobó antes y los intentos rechazados no tienen dónde quedar.
- **C) Una bitácora propia en la base de datos, de solo inserción: cada evento con quién, qué, cuándo, desde dónde y sobre qué práctica.** El usuario de la aplicación no tiene permiso para modificar ni borrar registros de esa tabla.

## Decisión

Se elige **C**. Es la única que guarda el historial completo (CU-10, OB-06) y los intentos rechazados (EAC-03). Se registran: aprobaciones y rechazos del acta, cambios de estado de la práctica, cambios de reglas de programa, accesos a datos personales e intentos de acceso rechazados. Se conserva el mismo tiempo que la tabla de retención define para las actas ([ADR-009](ADR-009-persistencia.md)).

## Consecuencias

**Positivas**
- Se puede reconstruir quién hizo qué en cualquier práctica (OB-06, RN-01).
- La aprobación del acta queda trazable sin firma digital certificada (S-06).
- La mesa de ayuda puede ver por qué un usuario no pudo hacer algo.

**Negativas y costos aceptados**
- La tabla crece todo el tiempo y no se puede depurar mientras dure la retención.
- Cada caso de uso debe acordarse de registrar sus eventos; si alguien lo olvida, el evento no existe. Se mitiga con un módulo de auditoría común.
- Cada acción hace una escritura extra en la base de datos.

**Riesgos asumidos**
- Un administrador de la base de datos podría alterar la tabla. Mitigación: permisos separados y respaldos que el Área de Sistemas conserva aparte.

**Vistas que modifica:** [lógica](../vistas/01-logica.md) (EventoBitacora), [desarrollo](../vistas/03-desarrollo.md) (Módulo Auditoría) y la secuencia de [CU-10](../diagramas/secuencias/cu10-aprobar-acta.puml).
