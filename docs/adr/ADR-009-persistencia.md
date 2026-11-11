# ADR-009: Guardar los datos en PostgreSQL y las actas en el almacenamiento institucional, sin borrado

## Estado

Aceptado — 2026-11-09

## Contexto

- RT-04 obliga a usar el motor de base de datos del catálogo institucional, y RT-01 a desplegar en la infraestructura de la Universidad.
- RN-05 descarta licencias comerciales de pago recurrente.
- RN-02 (Ley 594) obliga a conservar actas y evidencias según la tabla de retención documental: las actas aprobadas no se modifican ni se borran.
- RN-01 (Ley 1581) exige proteger los datos personales.

Supuesto: el catálogo institucional incluye PostgreSQL (se confirma con el Área de Sistemas, S-09).

## Alternativas consideradas

- **A) Todo en PostgreSQL, incluidos los PDF de las actas como binarios.** Un solo lugar que respaldar. Pero la base de datos crece con archivos que nunca cambian y los respaldos se vuelven lentos.
- **B) Base de datos como servicio en la nube.** Sin servidor que administrar. **Descartada por RT-01.**
- **C) Motor comercial (por ejemplo, Oracle o SQL Server).** **Descartada por RN-05**, salvo que la Universidad ya tenga la licencia en su catálogo.
- **D) PostgreSQL para los datos y el almacenamiento de archivos institucional para los PDF de las actas y las evidencias, con una política que impide borrarlos o sobrescribirlos durante la retención.**

## Decisión

Se elige **D**. El motor está prácticamente impuesto por RT-04 y RN-05; la decisión real es dónde viven los documentos. Se separan porque las actas tienen una regla de conservación propia (RN-02) que se aplica mejor sobre archivos que sobre filas de una base de datos.

## Consecuencias

**Positivas**
- Tecnología que el Área de Sistemas ya soporta (RT-04) y sin licencias (RN-05).
- Las actas aprobadas no se pueden alterar (RN-02).
- La base de datos se mantiene liviana y sus respaldos son rápidos.

**Negativas y costos aceptados**
- Hay dos cosas que respaldar y mantener coherentes: si se restaura la base de datos sin los archivos, quedan actas sin su PDF.
- La política de no borrado también impide corregir un acta aprobada por error: hay que emitir una nueva y anular la anterior.

**Riesgos asumidos**
- Que el almacenamiento institucional no permita políticas de retención. Mitigación: que el sistema solo tenga permiso de escribir, no de borrar.

**Vistas que modifica:** [procesos](../vistas/02-procesos.md) (PostgreSQL y repositorio de documentos) y [física](../vistas/04-fisica.md) (servidor de base de datos y almacenamiento institucional).
