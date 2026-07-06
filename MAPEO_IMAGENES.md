# 📸 Mapeo de Imágenes - Sistema de Gestión de Restaurante

## Cambios Realizados

### ✅ Actualizaciones del Código

Se han realizado los siguientes cambios al archivo `restaurante_app.py`:

1. **Agregados imports necesarios:**
   - `from PIL import Image, ImageTk` - Para cargar y mostrar imágenes
   - `import os` - Para verificar existencia de archivos

2. **Asignación de imágenes a productos:**
   - Se actualizó la función `obtener_productos()` con las rutas correctas de imágenes
   - Se implementó la carga de imágenes en la clase `TarjetaProducto`
   - Se agregó manejo de errores para imágenes faltantes (fallback a emoji 📷)

---

## 🍽️ PLATILLOS / ENTRADAS

| ID | Producto | Descripción | Precio | Imagen |
|---|----------|-------------|--------|--------|
| 1 | **Alitas Picantes** | Alitas crujientes con salsa picante casera | $8.99 | `imagenes/alitas.jpg` ✅ |
| 2 | **Camarones Empanizados** | Camarones frescos empanizados al horno | $12.50 | `imagenes/camarones.jpg` ✅ |
| 3 | **Tabla de Quesos** | Selección de quesos artesanales importados | $14.99 | `imagenes/tabla quesos.jpg` ✅ |

---

## 🥩 PLATILLOS / FUERTE (Platos Principales)

| ID | Producto | Descripción | Precio | Imagen |
|---|----------|-------------|--------|--------|
| 4 | **Filete Mignon** | Filete de res de 250g con champiñones | $24.99 | `imagenes/filete mignon.jpg` ✅ |
| 5 | **Pechuga Rellena** | Pechuga de pollo rellena de jamón y queso | $16.50 | `imagenes/pechuga rellena.jpg` ✅ |
| 6 | **Pasta Alfredo** | Pasta fresca con salsa cremosa de champiñones | $14.99 | `imagenes/pasta alfredo.jpg` ✅ |
| 7 | **Salmón a la Mantequilla** | Salmón fresco con salsa de vino blanco | $22.99 | `imagenes/Salmon a la mantequilla.jpg` ✅ |

---

## 🍰 PLATILLOS / POSTRE

| ID | Producto | Descripción | Precio | Imagen |
|---|----------|-------------|--------|--------|
| 8 | **Brownie de Chocolate** | Brownie casero con helado de vainilla | $7.99 | `imagenes/browni.jpg` ✅ |
| 9 | **Flan Napolitano** | Flan casero con caramelo crujiente | $6.99 | `imagenes/napolitano.jpg` ✅ |
| 10 | **Cheesecake Clásico** | Cheesecake de Nueva York con frutos rojos | $9.50 | `imagenes/cheesecake.jpg` ✅ |

---

## 🍹 BEBIDAS

| ID | Producto | Descripción | Precio | Imagen |
|---|----------|-------------|--------|--------|
| 11 | **Agua Mineral** | Botella de agua mineral 500ml | $2.50 | `imagenes/agua mineral.jpg` ✅ |
| 12 | **Refresco** | Refresco surtido 330ml | $3.00 | `imagenes/refresco.jpg` ✅ |
| 13 | **Jugo Natural** | Jugo recién exprimido de frutas frescas | $5.99 | `imagenes/jugo natural.jpg` ✅ |
| 14 | **Vino Tinto** | Vino tinto reserva 2019 | $22.99 | `imagenes/vino.jpg` ✅ |
| 15 | **Cerveza Premium** | Cerveza artesanal local 355ml | $4.99 | `imagenes/cerveza.jpg` ✅ |

---

## 📁 Archivos de Imagen Disponibles

La carpeta `imagenes/` contiene los siguientes archivos:

```
imagenes/
├── agua mineral.jpg        ✅ Producto 11
├── alitas.jpg              ✅ Producto 1
├── browni.jpg              ✅ Producto 8
├── camarones.jpg           ✅ Producto 2
├── cerveza.jpg             ✅ Producto 15
├── cheesecake.jpg          ✅ Producto 10
├── filete mignon.jpg       ✅ Producto 4
├── jugo natural.jpg        ✅ Producto 13
├── napolitano.jpg          ✅ Producto 9
├── pasta alfredo.jpg       ✅ Producto 6
├── pechuga rellena.jpg     ✅ Producto 5
├── refresco.jpg            ✅ Producto 12
├── Salmon a la mantequilla.jpg  ✅ Producto 7
├── tabla quesos.jpg        ✅ Producto 3
└── vino.jpg                ✅ Producto 14
```

**Total: 15 imágenes asignadas a 15 productos ✅**

---

## 🔧 Cómo Funciona

### En la Interfaz Gráfica:
1. Cada tarjeta de producto ahora carga la imagen correcta
2. Las imágenes se redimensionan automáticamente a 220x150 píxeles
3. Si una imagen no existe o hay error, se muestra un emoji 📷 como fallback
4. Las imágenes se cargan desde la carpeta `imagenes/` relativa al programa

### En el Código:
- La clase `TarjetaProducto` utiliza PIL (Pillow) para:
  - Abrir la imagen
  - Redimensionarla manteniendo proporción
  - Convertirla a PhotoImage para Tkinter
  - Mostrarla en la tarjeta del producto

---

## ✨ Características Implementadas

- ✅ Carga automática de imágenes para cada producto
- ✅ Redimensionamiento proporcional de imágenes
- ✅ Manejo de errores con fallback a emoji
- ✅ Interfaz visual mejorada con imágenes reales
- ✅ Compatibilidad con la captura de interfaz proporcionada

---

## 📝 Notas

- Las rutas de imágenes son relativas a la carpeta raíz del proyecto
- Asegúrate de que la carpeta `imagenes/` esté en el mismo directorio que `restaurante_app.py`
- Las imágenes se mantienen en memoria mientras la aplicación está en uso
- No se modificaron otros componentes de la aplicación

---

**Última actualización: 2026-07-06**
