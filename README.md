# PSYS - API de E-commerce

Una API RESTful simple para una aplicación de e-commerce construida con Django y Django REST Framework (DRF). Permite gestionar productos, ventas, usuarios y autenticación JWT.

## Características

- **Gestión de Productos**: CRUD completo de productos con filtros avanzados (nombre, precio, stock, en_stock), búsqueda y ordenamiento. Incluye endpoint `/prods` para listar todos los productos sin paginación. Restricción única en combinación nombre+marca+modelo. Caché en vistas de lista para mejor rendimiento.
- **Ventas**: Creación de ventas con validación de stock y tipo de pago, disminución automática de stock en bulk de manera atómica. Cálculo automático de precios y subtotales. Listas con total de ventas agregado. Permisos basados en roles (Admin ve todas, Administrador_tienda ve propias + vendedores, Vendedor ve propias).
- **Usuarios**: CRUD de usuarios con permisos basados en grupos (Admin, Administrador_tienda, Vendedor). Autenticación y autorización con JWT personalizado que incluye datos de usuario y roles.
- **Permisos y Roles**: Sistema de control de acceso basado en grupos Django. Diferentes niveles de acceso para operaciones CRUD según rol del usuario.
- **Validaciones y Manejo de Errores**: Validaciones robustas para stock, tipos de pago y datos de entrada. Excepciones personalizadas para stock insuficiente, tipo de pago inválido y producto no encontrado. Logging de errores para debugging.
- **Documentación API**: Documentación automática con DRF Spectacular (Swagger/ReDoc).
- **Paginación**: Soporte para paginación en listas grandes, configurable por parámetro.
- **Filtros Avanzados**: Filtros en productos (nombre, precio, stock, en_stock) y ventas (ID venta, usuario, tipo pago, fecha de creación).
- **CORS**: Configurado para desarrollo local (http://localhost:5173).
- **Cache**: Caché en memoria para vistas de lista de productos.
- **Tests**: Suite completa de tests unitarios e integración cubriendo modelos, serializadores, vistas y autenticación.

## Permisos y Roles

La API utiliza un sistema de permisos basado en grupos Django para controlar el acceso:

- **Admin**: Acceso completo a todas las operaciones (usuarios, productos, ventas).
- **Administrador_tienda**: Puede gestionar usuarios y productos, ver ventas propias y de vendedores.
- **Vendedor**: Solo puede crear y ver sus propias ventas.

Los permisos se verifican en cada endpoint según el rol del usuario autenticado.

## Validaciones y Manejo de Errores

- **Stock Insuficiente**: Se valida antes de crear ventas. Lanza `InsufficientStockError` si no hay suficiente stock.
- **Tipo de Pago Inválido**: Solo se permiten: Efectivo, Tarjeta credito, Tarjeta debito, Transferencia.
- **Producto No Encontrado**: Manejo personalizado para productos inexistentes.
- **Producto Duplicado**: Restricción única en nombre + marca + modelo.
- **Errores de Autenticación**: Tokens JWT inválidos o expirados.
- **Logging**: Todos los errores se registran para debugging.

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

  - `GET /api/v1.0/products/`: Listar productos paginados (filtros: `?in_stock=true`, `?name=valor`, `?price__gt=10`, `?stock__lt=5`, `?search=nombre`, `?ordering=price`)
  - `GET /api/v1.0/prods/`: Listar todos los productos sin paginación (para clientes)
  - `POST /api/v1.0/products/`: Crear producto (requiere Admin o Administrador_tienda)
  - `GET /api/v1.0/products/{id}/`: Detalle de producto
  - `PUT/PATCH /api/v1.0/products/{id}/`: Actualizar producto (requiere Admin o Administrador_tienda)
  - `DELETE /api/v1.0/products/{id}/`: Eliminar producto (requiere Admin o Administrador_tienda)

- **Ventas**:

  - `GET /api/v1.0/sells/`: Listar ventas con total de ventas agregado (autenticado; filtros: `?sell_id=uuid`, `?user=username`, `?type_pay=Efectivo`, `?created_at__range=2023-01-01,2023-12-31`; permisos basados en roles)
  - `POST /api/v1.0/sells/`: Crear venta (autenticado, valida stock y tipo de pago, disminuye stock automáticamente)
  - `GET /api/v1.0/sells/{id}/`: Detalle de venta

- **Usuarios**:

  - `GET /api/v1.0/users/`: Listar usuarios (requiere Admin o Administrador_tienda)
  - `POST /api/v1.0/users/`: Crear usuario (requiere Admin o Administrador_tienda)
  - `GET /api/v1.0/users/{id}/`: Detalle de usuario
  - `PUT/PATCH /api/v1.0/users/{id}/`: Actualizar usuario (requiere Admin o Administrador_tienda)
  - `DELETE /api/v1.0/users/{id}/`: Eliminar usuario (requiere Admin o Administrador_tienda)

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

3. **Listar Productos con Filtro (solo en stock)**:
   ```bash
   curl -X GET "http://localhost:8000/api/v1.0/products/?in_stock=true&ordering=price"
   ```

4. **Listar Todos los Productos (sin paginación)**:
   ```bash
   curl -X GET "http://localhost:8000/api/v1.0/prods/"
   ```

5. **Listar Ventas con Filtros**:
   ```bash
   curl -X GET "http://localhost:8000/api/v1.0/sells/?type_pay=Efectivo" \
        -H "Authorization: Bearer <tu-token>"
   ```

6. **Respuesta de Error (Stock Insuficiente)**:
   ```json
   {
     "error": "Insuficient stock for product Producto X: requested 5, available 2."
   }
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

Desarrollado usando Django y DRF.
