# PSYS - API de E-commerce

Una API RESTful simple para una aplicación de e-commerce construida con Django y Django REST Framework (DRF). Permite gestionar productos, ventas, usuarios y autenticación JWT.

## Características

- **Gestión de Productos**: CRUD de productos con filtros por stock, búsqueda y ordenamiento.
- **Ventas**: Creación de ventas con validación de stock y cálculo automático de precios.
- **Usuarios**: Autenticación y autorización con JWT.
- **Documentación API**: Documentación automática con DRF Spectacular (Swagger/ReDoc).
- **Paginación**: Soporte para paginación en listas grandes.
- **Validaciones**: Validaciones robustas para stock, tipos de pago y datos de entrada.
- **Logging**: Logs de errores para debugging.
- **Tests**: Suite completa de tests unitarios e integración.

## Tecnologías Utilizadas

- **Backend**: Django 5.2.8, Django REST Framework 3.16.1
- **Autenticación**: JWT con django-rest-framework-simplejwt 5.5.1
- **Base de Datos**: SQLite (desarrollo); PostgreSQL recomendado para producción
- **Documentación**: DRF Spectacular
- **Testing**: Django Test Framework + DRF TestCase
- **Gestión de Dependencias**: uv

## Instalación

### Prerrequisitos

- Python 3.13+
- uv (gestor de paquetes)

### Pasos

1. **Clona el repositorio**:

   ```bash
   git clone <url-del-repositorio>
   cd psys
   ```

2. **Instala dependencias**:

   ```bash
   uv sync
   ```

3. **Configura variables de entorno** (opcional, crea `.env`):

   ```
   SECRET_KEY=tu-clave-secreta
   DEBUG=True
   ```

4. **Ejecuta migraciones**:

   ```bash
   cd backend
   uv run python manage.py migrate
   ```

5. **Crea un superusuario** (opcional):

   ```bash
   uv run python manage.py createsuperuser
   ```

6. **Ejecuta el servidor**:
   ```bash
   uv run python manage.py runserver
   ```

La API estará disponible en `http://localhost:8000/api/v1.0/`.

## Uso

### Endpoints Principales

- **Autenticación**:

  - `POST /api/v1.0/auth/token/`: Obtener token JWT
  - `POST /api/v1.0/auth/token/refresh/`: Refrescar token

- **Productos**:

  - `GET /api/v1.0/products/`: Listar productos (con filtros: `?in_stock=true`, `?search=nombre`, `?ordering=price`)
  - `POST /api/v1.0/products/`: Crear producto (requiere staff)
  - `GET /api/v1.0/products/{id}/`: Detalle de producto
  - `PUT/PATCH /api/v1.0/products/{id}/`: Actualizar producto (requiere staff)
  - `DELETE /api/v1.0/products/{id}/`: Eliminar producto (requiere staff)

- **Ventas**:

  - `GET /api/v1.0/sells/`: Listar ventas (autenticado)
  - `POST /api/v1.0/sells/`: Crear venta (autenticado, valida stock)
  - `GET /api/v1.0/sells/{id}/`: Detalle de venta

- **Usuarios**:

  - `GET /api/v1.0/users/`: Listar usuarios
  - `POST /api/v1.0/users/`: Crear usuario

- **Documentación**:
  - `GET /api/v1.0/schema/swagger-ui/`: Interfaz Swagger
  - `GET /api/v1.0/schema/redoc/`: Documentación ReDoc

### Ejemplo de Uso

1. **Obtener Token**:

   ```bash
   curl -X POST http://localhost:8000/api/v1.0/auth/token/ \
        -H "Content-Type: application/json" \
        -d '{"username": "tu-usuario", "password": "tu-contraseña"}'
   ```

2. **Crear una Venta**:
   ```bash
   curl -X POST http://localhost:8000/api/v1.0/sells/ \
        -H "Authorization: Bearer <tu-token>" \
        -H "Content-Type: application/json" \
        -d '{
          "type_pay": "Efectivo",
          "sells": [
            {"product": 1, "quantity": 2}
          ]
        }'
   ```

## Testing

Ejecuta los tests con:

```bash
cd backend
uv run python manage.py test
```

Los tests cubren:

- Modelos (ej. disminución de stock)
- Serializers (validaciones)
- Views (CRUD, permisos)
- Autenticación JWT

## Contribución

1. Fork el proyecto.
2. Crea una rama para tu feature: `git checkout -b feature/nueva-funcionalidad`.
3. Haz commits descriptivos.
4. Push a la rama: `git push origin feature/nueva-funcionalidad`.
5. Abre un Pull Request.

### Guías de Código

- Sigue PEP 8 para Python.
- Agrega docstrings a nuevas funciones/clases.
- Incluye tests para nuevas funcionalidades.
- Usa type hints donde sea posible.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más detalles.

## Contacto

Para preguntas o soporte, abre un issue en el repositorio o contacta al mantenedor.

---

Desarrollado usnado Django y DRF.
