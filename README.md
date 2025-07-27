# Kopi Chatbot API

## Descripción
Este proyecto expone una API que sostiene un debate tomando una postura definida, intentando convencer al usuario.

## Instalación
```bash
make install
```

## Ejecución local
```bash
make run
```

## Detener servicios
```bash
make down
```

## Eliminar contenedores y volúmenes
```bash
make clean
```

## Variables de Entorno
Actualmente no hay variables necesarias, pero puedes agregar soporte en `main.py` fácilmente.

## Ejemplo de request inicial (nuevo debate)
```json
{
  "conversation_id": null,
  "message": "No creo que la Tierra sea plana"
}
```

## Ejemplo de respuesta
```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "message": [
    {"role": "user", "message": "No creo que la Tierra sea plana"},
    {"role": "bot", "message": "La Tierra no es una esfera, es completamente plana y lo puedo demostrar."}
  ]
}
```

## Pruebas
```bash
make test
```

## Entrega
- URL pública donde se puede probar la API
- Archivo `.tar.gz` del repo con historial de commits
