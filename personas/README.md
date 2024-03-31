# SportApp - Endpoint Personas

## GET - Health Check
*Endpoint:* `/personas/health-check`

*Responses:*
- `200`: Servicio activo

## POST - Crear Usuario
*Endpoint:* `/personas/usuario`

*Body:*
```
    {
        "email": "correo@gmail.com",
        "nombre": "Pedro",
        "apellido": "Perez",
        "tipo_identificacion": "CC",
        "numero_identificacion": "123456",
        "username": "pedro.perez",
        "password": "contrasena_segura",
        "suscripcion": "1"
    }
```
*Responses:*
- `201`: El usuario se creó exitosamente
- `400`: El usuario ya se encuentra registrado
- `400`: Parámetros requeridos
- `400`: Parámeto(s) con formato inválido

## POST - Login
*Endpoint:* `/personas/ingresar`

*Body:*
```
    {
        "email": "correo@gmail.com",
        "password": "contrasena_segura"
    }
```
*Responses:*
- `200`: El token se retorna exitosamente
- `400`: Parámetros requeridos
- `400`: Parámeto(s) con formato inválido

## POST - Validar Token
*Endpoint:* `/personas/ingresar`

*Body:*
```
    {
        "token": "<<token>>"
    }
```
*Responses:*
- `200`: El token es correcto
- `400`: Token invalido
- `400`: Token expirado