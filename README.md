# SportApp

## Ejecutar ambiente local
Se deben subir todos los microservicios para probar el ambiente completo. Estas instrucciones se deben ejecutar desde el directorio raíz del proyecto
# Microservicio Usuarios
1. Construir la imagen de Docker
```
docker image build -f backend/usuarios/Dockerfile -t usuarios:1.0 .
```
2. Ejecutar la imagen de docker
```
docker run -p 5001:5001 -d usuarios:1.0  
```