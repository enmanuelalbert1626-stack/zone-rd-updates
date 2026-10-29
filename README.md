# ZONE RD · Canal de actualizaciones

El control de versiones está en **Actions → Publicar actualización de ZONE RD → Run workflow**.

1. En **Releases → Draft a new release**, crea una etiqueta (por ejemplo `v1.0-r7`).
2. Adjunta un único archivo APK de ZONE RD y publica la release.
3. Abre el formulario de Actions, introduce esa etiqueta y escribe el mensaje.
4. Deja marcada **Obligatoria** para bloquear las versiones anteriores; desmárcala para ofrecer la actualización sin elevar el mínimo permitido.
5. Pulsa **Run workflow** y espera a que termine en verde.

El proceso obtiene la versión real del APK, calcula SHA-256 y tamaño y actualiza el archivo público de versiones. GitHub Pages puede tardar unos minutos en propagar un cambio. Cada APK debe tener un código Android superior al anterior y conservar el mismo paquete y firma. Nunca adjuntes la clave de firma al repositorio.

Los teléfonos necesitan instalar una vez la compilación 38 o posterior para incorporar el actualizador. Los APK anteriores sin actualizador no pueden recibir este mecanismo retroactivamente. La comprobación requiere Internet al abrir o volver al juego; las partidas siguen siendo OFFLINE o LAN.

Este repositorio y sus APK publicados son públicos. Solo los administradores autorizados pueden cambiar la política o ejecutar el formulario. El APK no contiene credenciales de GitHub. El alojamiento usa los servicios gratuitos de repositorios públicos de GitHub, sujetos a sus límites y condiciones; cada archivo de una release debe ser menor de 2 GiB.
