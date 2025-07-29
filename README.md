# Kopi Challenge – Chatbot API

Este proyecto es una API que permite simular un chatbot capaz de sostener un debate con una postura fija sobre cualquier tema proporcionado por el usuario. El bot responde de manera persuasiva, defiende su punto de vista y mantiene la coherencia a lo largo de múltiples intercambios.


### `POST /chat`

#### Request:
```json
{
  "conversation_id": null,
  "message": "Los fantasmas no existen"
}
