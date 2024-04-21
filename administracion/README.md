# SportApp - Endpoint Adminsitración

## GET - Health Check
*Endpoint:* `/deporte/health-check`

*Responses:*
- `200`: Servicio activo

*Headers:*
- `Authorization`: Token tipo Bearer de autorización

*Responses:*
- `200`: Información del plan
- `401`: Token inválido
- `401`: Token expirado
- `403`: No se encontró el header de autorización
- `403`: El header de autorización no tiene un formato correcto

