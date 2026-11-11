# Vista física: diagrama de despliegue

Muestra dónde se ejecuta cada contenedor de la vista de procesos y por qué red viaja cada conexión.

Para: ingenieros de infraestructura (Área de Sistemas).

## 1. Presentación principal

Diagrama C4 de despliegue: [../diagramas/04-fisica.puml](../diagramas/04-fisica.puml).

## 2. Catálogo de elementos

| Nodo | Contenedores que aloja | Características | Conexiones |
|---|---|---|---|
| Navegador o celular | Aplicación web (ejecutándose en el navegador) | Equipo del usuario, fuera de la Universidad | Servidor web y Proveedor de identidad institucional (HTTPS, internet) |
| Servidor web [Ubuntu, Nginx] | Aplicación web (archivos estáticos) | Sirve la interfaz y hace de proxy inverso hacia la API; único nodo expuesto a internet | Navegadores (HTTPS) y API de prácticas (HTTPS, red interna) |
| Servidor de aplicaciones [Ubuntu, Docker] | API de prácticas, Worker de integración | Cada contenedor se reinicia por separado | Bróker (AMQP), Base de datos (SQL), Repositorio de documentos, SIA (HTTPS), correo (SMTP) y proveedor de identidad |
| Servidor de mensajería [Ubuntu] | Bróker de mensajes | Colas persistentes: los mensajes sobreviven a un reinicio | API y Worker (AMQP, red interna) |
| Servidor de base de datos [Ubuntu, PostgreSQL] | Base de datos | Solo accesible desde la red interna | API y Worker (SQL) |
| Almacenamiento institucional | Repositorio de documentos | Servidor de archivos con respaldo y política de no borrado | API (HTTPS, red interna) |

Todos los nodos, salvo el navegador, están en el centro de datos de la Universidad.

## 3. Justificación

- **RT-01:** todos los nodos del sistema están en la infraestructura de la Universidad; no hay nube pública. Esto también descarta las colas y bases de datos gestionadas (ADR-003, ADR-009).
- **RT-04 y RN-05:** Ubuntu, Nginx, Docker, PostgreSQL y RabbitMQ son software libre (supuesto S-09: están en el catálogo institucional).
- **EAC-02, PA-04 y ADR-003:** el bróker tiene nodo propio y colas persistentes; si el SIA o el worker caen, ninguna postulación se pierde.
- **RN-01:** la Base de datos con datos personales solo es accesible por la red interna, y solo el Servidor web queda expuesto.
- **RN-02 y ADR-009:** las actas viven en el almacenamiento institucional, separado de la base de datos y con política de no borrado.
- **RT-02 y RT-03:** el SIA y el proveedor de identidad se alcanzan por la red institucional, por sus servicios.

## 4. Comportamiento

- [CU-01](../diagramas/secuencias/cu01-postularse.puml) cruza nodos: navegador → Servidor web → Servidor de aplicaciones → Servidor de mensajería → Servidor de aplicaciones (worker) → SIA.
- [CU-07](../diagramas/secuencias/cu07-evaluar-practicante.puml) entra desde el navegador del supervisor, fuera de la Universidad, por el único nodo expuesto.

## 5. Vistas relacionadas

- [Procesos](02-procesos.md): cada contenedor de esa vista aparece en un nodo de esta.
- [Contexto](../contexto.md): cada sistema externo aparece con su protocolo.
