# ADR-002: Consultar el SIA solo mediante un adaptador detrás del puerto ConsultaAcademica

## Estado

Aceptado — 2026-11-09

## Contexto

En la postulación (CU-01) el sistema debe verificar los requisitos académicos del estudiante contra el SIA (S-02). La restricción RT-03 prohíbe conectarse directamente a la base de datos del SIA: solo se pueden usar los servicios que el SIA expone para otros sistemas. Además existe el riesgo de que esos servicios no existan o fallen con frecuencia (R-02), y OB-01 depende de que los datos académicos no se retranscriban a mano.

## Alternativas consideradas

- **A) Conexión directa a la base de datos del SIA.** Rápida y sin depender de servicios. **Descartada por RT-03**: ata el sistema a la estructura interna del SIA y evade sus controles.
- **B) Llamar a los servicios del SIA desde cada caso de uso.** Directo, pero cada caso de uso tendría su propio código HTTP y su propio manejo de fallas; si el SIA cambia su servicio, hay que tocar varios módulos.
- **C) Un puerto `ConsultaAcademica` en la capa de aplicación y un único adaptador que llama a los servicios del SIA.** Los casos de uso solo conocen el puerto.

## Decisión

Se elige **C**. Cumple RT-03 y deja el contacto con el SIA en un solo lugar. Si R-02 se materializa y el SIA no ofrece servicios, se escribe un segundo adaptador que lee una exportación periódica acordada con el administrador del SIA, sin tocar los casos de uso.

## Consecuencias

**Positivas**
- Un cambio en el servicio del SIA toca solo el adaptador.
- Los casos de uso se prueban con un adaptador falso, sin depender del SIA.
- Deja preparado el plan B de R-02 (exportación periódica).

**Negativas y costos aceptados**
- Se depende del contrato del servicio del SIA, que este equipo no controla; hay que pactarlo con su administrador.
- Los datos académicos que se usan son una copia del momento de la consulta; si el SIA los corrige después, el sistema no se entera solo.

**Riesgos asumidos**
- El servicio del SIA puede no existir (R-02). Mitigación: confirmarlo en la primera semana (S-09) y, si no existe, usar el adaptador de exportación.
- Las fallas del SIA en plena postulación se resuelven en el [ADR-003](ADR-003-broker-mensajes.md).

**Vistas que modifica:** [contexto](../contexto.md) (SIA como sistema externo), [procesos](../vistas/02-procesos.md) y [desarrollo](../vistas/03-desarrollo.md) (Adaptador SIA).
