# Contexto del sistema: Sistema de Gestión de Prácticas Empresariales

El contexto no es una vista de 4+1: es el marco que encuadra las cuatro vistas. Muestra el sistema como una caja negra, quién lo usa y con qué sistemas externos se comunica.

## 1. Presentación principal

Diagrama C4 de nivel 1: [diagramas/contexto.puml](diagramas/contexto.puml).

## 2. Catálogo de elementos

| Elemento | Tipo | Rol o responsabilidad | Interacción con el sistema |
|---|---|---|---|
| Estudiante | Persona | Se postula (CU-01), registra horas (CU-04) y consulta su trámite (CU-11) | Aplicación web (HTTPS), con la cuenta institucional |
| Docente asesor | Persona | Revisa horas y avance (CU-06) y aprueba el acta (CU-10) | Aplicación web (HTTPS), con la cuenta institucional |
| Director de programa | Persona | Aprueba postulaciones (CU-02), asigna docente asesor (CU-03), configura reglas (CU-12) y aprueba el acta (CU-10) | Aplicación web (HTTPS), con la cuenta institucional |
| Administrador del sistema | Persona | Asigna roles y ejecuta la migración inicial (CU-15) | Aplicación web (HTTPS), con la cuenta institucional |
| Supervisor de empresa | Persona externa | Valida horas (CU-05) y evalúa al practicante (CU-07) | Enlace de un solo uso recibido por correo (HTTPS), sin cuenta (RN-04) |
| Sistema de Gestión de Prácticas Empresariales | Sistema en alcance | Gestiona postulación, seguimiento, evaluación y acta final de las prácticas | Con todos los demás elementos |
| SIA | Sistema externo | Fuente de los datos académicos del estudiante; lo administra el administrador del SIA | Sus servicios de consulta (HTTPS / REST), nunca su base de datos (RT-03) |
| Proveedor de identidad institucional | Sistema externo | Autentica con la cuenta institucional (inicio de sesión único) | OpenID Connect sobre HTTPS (RT-02) |
| Servicio de correo institucional | Sistema externo | Entrega notificaciones, recordatorios y enlaces de evaluación | SMTP |

## 3. Justificación

- **Casos de uso primarios:** CU-01, CU-07, CU-09, CU-10 y CU-12 definen los actores del diagrama. CU-07 es el que trae al supervisor de empresa como persona externa.
- **RT-02 y ADR-004:** el proveedor de identidad aparece como sistema externo porque el sistema no guarda contraseñas.
- **RT-03 y ADR-002:** el SIA aparece aparte y la flecha indica sus servicios REST, no su base de datos.
- **RN-04 y ADR-005:** el supervisor no tiene cuenta. Entra con el enlace que le llega por el servicio de correo, por eso existe la flecha del correo hacia él.
- **PA-02:** el diagrama muestra las dos formas de acceso: cuenta institucional (cuatro personas internas) y enlace (supervisor).

## 4. Comportamiento

Aquí empiezan los escenarios (+1) de [drivers.md, sección 6](drivers.md#6-escenarios). Todos arrancan en una persona de este diagrama y cruzan el sistema hacia el SIA, el proveedor de identidad o el correo.

## 5. Vistas relacionadas

- [Procesos](vistas/02-procesos.md): qué contenedor habla con cada sistema externo.
- [Física](vistas/04-fisica.md): por qué red sale cada conexión.
