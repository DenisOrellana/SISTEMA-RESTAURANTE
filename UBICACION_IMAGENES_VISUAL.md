# 🎨 UBICACIÓN DE IMÁGENES EN LA INTERFAZ

## Estructura Visual del Sistema de Gestión de Restaurante

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                                                                 │
│  🔲 Sistema de Gestión de Restaurante                                    [🟡][🟡][❌]
│  ┌──────────────────────────────────────────────────────────────────────────────┤
│  │ 🍽️ RESTAURANTE                                          [🏠] Platillos/Bebidas
│  │ ──────────────────────────────────────────────────────────────────────────────│
│  │ Control de Mesas                                                             │
│  │ Catálogo de Menú          [═══════════════════════════════════════════════] │ Orden Actual
│  │ Confirmación de Orden     │                                            📋 Orden Actual
│  │ Historial y Control       │ PLATILLOS / BEBIDAS                           ──────────────
│  │ Configuración             │ ────────────────────────────────────────────  │ Sin artículos
│  │                           │                                            │ │
│  │                           │ ┌─ PLATILLOS ─ BEBIDAS ──┐               │ │
│  │                           │ │                        │               │ │
│  │                           │ ┌────────────────────┐   │               │ │
│  │                           │ │  [ENTRADAS]       │   │               │ │
│  │                           │ ├────────────────────┤   │               │ │
│  │                           │ │                    │   │               │ │
│  │                           │ │ ┌──────────────┐   │   │               │ │
│  │                           │ │ │              │   │   │               │ │
│  │                           │ │ │ [alitas.jpg] │◄──┘   │               │ │
│  │                           │ │ │              │       │               │ │
│  │                           │ │ └──────────────┘       │               │ │
│  │                           │ │ Alitas Picantes       │               │ │
│  │                           │ │ Alitas crujientes...  │               │ │
│  │                           │ │ $8.99        [➕]     │               │ │
│  │                           │ │                       │               │ │
│  │                           │ ├────────────────────┐   │ Total: $0.00  │
│  │                           │ │                    │   │               │
│  │                           │ │ ┌──────────────┐   │   │ Mesa:        │
│  │                           │ │ │              │   │   │ Comensales:  │
│  │                           │ │ │[camarones.j] │   │   │               │
│  │                           │ │ │              │   │   │ ✓ Confirmar  │
│  │                           │ │ └──────────────┘   │   │              │
│  │                           │ │ Camarones Empa...  │   │ 🗑️ Limpiar   │
│  │                           │ │ Camarones frescos.. │   │              │
│  │                           │ │ $12.50       [➕]   │   │              │
│  │                           │ │                   │   │              │
│  │                           │ └────────────────────┘   │              │
│  │                           │                         │
│  │                           └─────────────────────────┘
│  │
│  │ COLUMNA IZQUIERDA    │        COLUMNA CENTRAL (Scrollable)    │ COLUMNA DERECHA
│  │ - Navegación         │        - Platillos en 3 categorías     │ - Vista previa
│  │ - Enlaces            │        - Bebidas en 2 columnas         │ - Carrito
│  └──────────────────────────────────────────────────────────────────────────────┘
```

---

## 📸 Asignación de Imágenes por Categoría

### 🥗 ENTRADAS (Columna 1)

```
┌─────────────────────────────────────┐
│         ENTRADAS                    │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │                                 │ │
│ │  imagenes/alitas.jpg            │ │  ← Alitas Picantes ($8.99)
│ │  [Foto de alitas crujientes]    │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│ Alitas Picantes                     │
│ Alitas crujientes con salsa pi...   │
│ $8.99                       [➕]    │
│                                     │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │                                 │ │
│ │  imagenes/camarones.jpg         │ │  ← Camarones Empanizados ($12.50)
│ │  [Foto de camarones]            │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│ Camarones Empanizados              │
│ Camarones frescos empanizados...   │
│ $12.50                      [➕]    │
│                                     │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │                                 │ │
│ │  imagenes/tabla quesos.jpg      │ │  ← Tabla de Quesos ($14.99)
│ │  [Foto de tabla de quesos]      │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│ Tabla de Quesos                     │
│ Selección de quesos artesanales..   │
│ $14.99                      [➕]    │
│                                     │
└─────────────────────────────────────┘
```

### 🍖 FUERTE (Columna 2)

```
┌─────────────────────────────────────┐
│         FUERTE                      │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │                                 │ │
│ │  imagenes/filete mignon.jpg     │ │  ← Filete Mignon ($24.99)
│ │  [Foto de filete]               │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│ Filete Mignon                       │
│ Filete de res de 250g con...        │
│ $24.99                      [➕]    │
│                                     │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │                                 │ │
│ │  imagenes/pechuga rellena.jpg   │ │  ← Pechuga Rellena ($16.50)
│ │  [Foto de pechuga]              │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│ Pechuga Rellena                     │
│ Pechuga de pollo rellena de...      │
│ $16.50                      [➕]    │
│                                     │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │                                 │ │
│ │  imagenes/pasta alfredo.jpg     │ │  ← Pasta Alfredo ($14.99)
│ │  [Foto de pasta]                │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│ Pasta Alfredo                       │
│ Pasta fresca con salsa cremosa...   │
│ $14.99                      [➕]    │
│                                     │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │                                 │ │
│ │ imagenes/Salmon a la mant..jpg  │ │  ← Salmón a la Mantequilla ($22.99)
│ │  [Foto de salmón]               │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│ Salmón a la Mantequilla             │
│ Salmón fresco con salsa de vino...  │
│ $22.99                      [➕]    │
│                                     │
└─────────────────────────────────────┘
```

### 🍰 POSTRE (Columna 3)

```
┌─────────────────────────────────────┐
│         POSTRE                      │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │                                 │ │
│ │  imagenes/browni.jpg            │ │  ← Brownie de Chocolate ($7.99)
│ │  [Foto de brownie]              │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│ Brownie de Chocolate                │
│ Brownie casero con helado de...     │
│ $7.99                       [➕]    │
│                                     │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │                                 │ │
│ │  imagenes/napolitano.jpg        │ │  ← Flan Napolitano ($6.99)
│ │  [Foto de flan]                 │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│ Flan Napolitano                     │
│ Flan casero con caramelo crujiente  │
│ $6.99                       [➕]    │
│                                     │
├─────────────────────────────────────┤
│ ┌─────────────────────────────────┐ │
│ │                                 │ │
│ │  imagenes/cheesecake.jpg        │ │  ← Cheesecake Clásico ($9.50)
│ │  [Foto de cheesecake]           │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│ Cheesecake Clásico                  │
│ Cheesecake de Nueva York con...     │
│ $9.50                       [➕]    │
│                                     │
└─────────────────────────────────────┘
```

### 🍹 BEBIDAS (Pestaña 2 - Formato 2 Columnas)

```
┌────────────────────────┬────────────────────────┐
│   COLUMNA 1            │   COLUMNA 2            │
├────────────────────────┼────────────────────────┤
│ ┌──────────────────┐   │ ┌──────────────────┐   │
│ │                  │   │ │                  │   │
│ │agua mineral.jpg  │   │ │  refresco.jpg    │   │
│ │[Agua mineral]    │   │ │[Refresco]        │   │
│ │                  │   │ │                  │   │
│ └──────────────────┘   │ └──────────────────┘   │
│ Agua Mineral           │ Refresco               │
│ Botella de agua...     │ Refresco surtido...    │
│ $2.50         [➕]     │ $3.00         [➕]     │
│                        │                        │
├────────────────────────┼────────────────────────┤
│ ┌──────────────────┐   │ ┌──────────────────┐   │
│ │                  │   │ │                  │   │
│ │jugo natural.jpg  │   │ │  vino.jpg        │   │
│ │[Jugo]            │   │ │[Vino]            │   │
│ │                  │   │ │                  │   │
│ └──────────────────┘   │ └──────────────────┘   │
│ Jugo Natural           │ Vino Tinto             │
│ Jugo recién exprimido..│ Vino tinto reserva..   │
│ $5.99         [➕]     │ $22.99        [➕]     │
│                        │                        │
├────────────────────────┼────────────────────────┤
│ ┌──────────────────┐   │                        │
│ │                  │   │                        │
│ │ cerveza.jpg      │   │                        │
│ │[Cerveza]         │   │                        │
│ │                  │   │                        │
│ └──────────────────┘   │                        │
│ Cerveza Premium        │                        │
│ Cerveza artesanal...   │                        │
│ $4.99         [➕]     │                        │
│                        │                        │
└────────────────────────┴────────────────────────┘
```

---

## 📊 Resumen de Ubicaciones

| Ubicación | Categoría | Productos | Imágenes |
|-----------|-----------|-----------|----------|
| Pestaña 1 - Columna 1 | ENTRADAS | 3 | alitas.jpg, camarones.jpg, tabla quesos.jpg |
| Pestaña 1 - Columna 2 | FUERTE | 4 | filete mignon.jpg, pechuga rellena.jpg, pasta alfredo.jpg, Salmon a la mantequilla.jpg |
| Pestaña 1 - Columna 3 | POSTRE | 3 | browni.jpg, napolitano.jpg, cheesecake.jpg |
| Pestaña 2 - Grid 2col | BEBIDAS | 5 | agua mineral.jpg, refresco.jpg, jugo natural.jpg, vino.jpg, cerveza.jpg |
| **TOTAL** | **4 Secciones** | **15 Productos** | **15 Imágenes ✅** |

---

## ✨ Características de Visualización

- ✅ Altura de imagen: 150 píxeles
- ✅ Ancho máximo: 220 píxeles
- ✅ Redimensionamiento: Proporcional (LANCZOS)
- ✅ Fondo naranja (#FF9F43) si no se carga imagen
- ✅ Fallback: Emoji 📷 si hay error
- ✅ Scroll vertical en platillos y bebidas

---

**Diagrama visual - Generado el 2026-07-06**
