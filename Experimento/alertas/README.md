# Usuarios

## Instrucciones para el despliegue
1. Descargar el repositorio
2. Ubicado en el directorio Experimento\usuarios Ejecutar el siguiente comando:
```docker-compose up --build -d```


## Instrucciones para la ejecución
1. Ejecutar la siguiente instrucción para probar el servicio de registro de usuarios
```curl --location 'http://localhost:3001/usuarios' \--header 'Content-Type: application/json' \--data '{"nombre":"Neztor", "apellido":"perez", "email":"neztor@uniandes.edu.co", "deportes_practica": "atletismo"}'```

