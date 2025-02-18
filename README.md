# InseguirdadNL


Este repositorio tiene como objetivo visualizar la inseguridad en el estado de Nuevo León. A través de esta herramienta, se puede analizar:

- Qué municipio es el más inseguro.
- Qué lugares la gente considera más inseguros.
- Cómo el rol de género influye en la percepción de la inseguridad.

## Instalación

Para ejecutar este proyecto, primero instala las librerías necesarias con el siguiente comando:

```sh
pip install streamlit pandas plotly
```
## Automatización de la Base de Datos

En el futuro, si se desea automatizar la obtención de datos, se utilizará la API de ENSU (Encuesta Nacional de Seguridad Pública Urbana) proporcionada por el INEGI. Para ello, se seguirá el siguiente procedimiento:

1. **Obtener el Token de Acceso:** Es necesario registrarse en la plataforma del INEGI para obtener un token que permita el acceso a la API.
2. **Realizar una Solicitud a la API:** Una vez obtenido el token, se realizará un request a la API para obtener los datos actualizados.
3. **Integrar los Datos en la Aplicación:** Los datos obtenidos se integrarán a la aplicación para su visualización y análisis en tiempo real.

Con esta automatización, se garantizará que la información sobre la inseguridad en Nuevo León esté siempre actualizada y disponible para su consulta.
