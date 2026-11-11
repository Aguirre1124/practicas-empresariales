# ADR-004: Autenticar a los usuarios institucionales con el inicio de sesión único y autorizar por rol

## Estado

Aceptado — 2026-11-09

## Contexto

- RT-02 obliga a autenticar a estudiantes, docentes asesores y personal con la cuenta institucional (inicio de sesión único). El sistema no puede guardar contraseñas.
- PA-02 pide decidir cómo se controlan los permisos de cinco roles: estudiante, docente asesor, director de programa, supervisor y administrador.
- RN-01 (Ley 1581) exige que cada rol vea solo los datos personales que le corresponden.
- CU-10 necesita saber con certeza quién aprueba el acta.

Esta decisión cubre a los usuarios institucionales. El acceso del supervisor de empresa, que no tiene cuenta institucional, se decide en el [ADR-005](ADR-005-enlace-supervisor.md).

## Alternativas consideradas

- **A) Usuarios y contraseñas propios del sistema.** **Descartada por RT-02.**
- **B) Inicio de sesión único con el proveedor de identidad institucional y roles tomados solo del proveedor.** No se guarda nada de identidad. Pero el proveedor institucional no sabe quién es docente asesor de qué práctica ni quién dirige qué programa.
- **C) Inicio de sesión único con el proveedor institucional (OpenID Connect o SAML, según lo que ofrezca) y roles asignados dentro del sistema.** El proveedor dice quién es la persona; el sistema guarda qué rol tiene y sobre qué programa o práctica.

## Decisión

Se elige **C**. La autenticación la impone RT-02, así que la única decisión real es dónde viven los roles. Se guardan en el sistema porque los permisos dependen de datos que solo el sistema conoce (qué prácticas asesora cada docente), y eso permite cumplir RN-01 con permisos por práctica y no solo por tipo de usuario.

## Consecuencias

**Positivas**
- El sistema no guarda contraseñas (RT-02).
- Los permisos se pueden revisar por práctica: un docente asesor solo ve sus practicantes (RN-01).
- Cada acción queda ligada a una identidad institucional, lo que alimenta la bitácora del [ADR-006](ADR-006-bitacora-auditoria.md) (CU-10).

**Negativas y costos aceptados**
- Si el proveedor de identidad institucional cae, nadie con cuenta institucional puede entrar.
- Alguien tiene que asignar los roles en el sistema (directores y docentes asesores); es una tarea manual al inicio de cada periodo.
- El protocolo exacto (OpenID Connect o SAML) depende de lo que ofrezca la Universidad; el adaptador se escribe cuando se confirme.

**Riesgos asumidos**
- Que el proveedor institucional no permita registrar este sistema como cliente. Mitigación: validarlo con el administrador del SIA en la primera semana (S-09).

**Vistas que modifica:** [contexto](../contexto.md) (proveedor de identidad), [procesos](../vistas/02-procesos.md) y [desarrollo](../vistas/03-desarrollo.md) (Adaptador de identidad y control de acceso).
