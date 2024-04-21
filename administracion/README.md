# SportApp - Endpoint Adminsitración

## GET - Health Check
*Endpoint:* `/administracion/health-check`

*Responses:*
- `200`: Servicio activo


## GET - Obtener planes
*Endpoint:* `/administracion/plan`

*Headers:*
- `Authorization`: Token tipo Bearer de autorización 

*Responses:*
- `200`: Lista de planes
- `401`: Token inválido
- `401`: Token expirado
- `403`: No se encontró el header de autorización
- `403`: El header de autorización no tiene un formato correcto

## POST - Obtener plan por id
*Endpoint:* `/administracion/plan/:idPlan:`

*Path Parameters:*
- `idPlan`: Id del plan a consultar

*Headers:*
- `Authorization`: Token tipo Bearer de autorización

*Responses:*
- `200`: Información del plan
- `401`: Token inválido
- `401`: Token expirado
- `403`: No se encontró el header de autorización
- `403`: El header de autorización no tiene un formato correcto

