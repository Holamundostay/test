# 🚀 Guía Rápida de Inicio

## Inicio en 5 Minutos

### 1️⃣ **Preparar el Ambiente**

```bash
# Instalar dependencias del backend
cd backend
pip install -r requirements.txt

# Instalar dependencias del frontend (en otra terminal)
cd frontend
npm install
```

### 2️⃣ **Ejecutar Backend**

```bash
cd backend
python -m uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Debería ver:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### 3️⃣ **Ejecutar Frontend**

```bash
cd frontend
npm run dev
```

Debería ver algo como:
```
  VITE v4.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### 4️⃣ **Abre en el navegador**

Ve a: **http://localhost:5173**

---

## 👤 Usuarios de Prueba

Selecciona cualquiera de estos usuarios:

| Usuario | Nombre | Rol | Contraseña |
|---------|--------|-----|-----------|
| maria | María García | Enfermera | (sin contraseña) |
| carlos | Carlos López | Enfermera | (sin contraseña) |
| ana | Ana Martínez | Supervisor | (sin contraseña) |
| admin | Administrador | Admin | (sin contraseña) |

---

## ✅ Checklist de Funcionalidad

Después de iniciar, prueba esto para confirmar que todo funciona:

- [ ] Puedo ver la pantalla de login con usuarios
- [ ] Puedo iniciar sesión haciendo clic en un usuario
- [ ] Veo 5 artículos en el inventario inicial
- [ ] Puedo ajustar la cantidad de un artículo
- [ ] Puedo agregar un artículo nuevo
- [ ] Puedo realizar un conteo
- [ ] Puedo ver los reportes

---

## 🐳 Con Docker (Alternativa)

Si tienes Docker instalado:

```bash
docker-compose up -d
```

Luego abre:
- Frontend: http://localhost:5173
- API docs: http://localhost:8000/docs

---

## 🔧 Solución Rápida de Problemas

| Problema | Solución |
|----------|----------|
| "No puedo conectar al backend" | Verifica que esté corriendo en puerto 8000 |
| "Node no encontrado" | Instala Node.js desde nodejs.org |
| "Python no encontrado" | Instala Python 3.10+ desde python.org |
| "Base de datos vacía" | Reinicia el servidor, se crea automáticamente |
| "Puerto 8000 en uso" | Cambia a otro puerto: `--port 8001` |

---

## 📊 Base de Datos

Se crea automáticamente como `backend/inventory.db`

Para ver/editar directamente:
```bash
# Instalar SQLite Browser (opcional)
# Luego abrir backend/inventory.db
```

---

## 🎯 Próximos Pasos

1. **Agregar más materiales** - Ve a la pestaña "Agregar artículo"
2. **Realizar conteos** - Usa "Realizar conteo" para cada material
3. **Ver reportes** - Analiza en la pestaña "Reportes"
4. **Gestionar usuarios** - Personaliza los 4 usuarios de prueba

---

## 📱 Navegación Rápida

- **📦 Inventario** - Ver todos los materiales y ajustar cantidades
- **➕ Agregar** - Crear nuevos materiales
- **📋 Conteos** - Registrar conteos físicos
- **📊 Reportes** - Ver histórico y auditoría

---

## 💡 Consejos

- 📝 Agrega notas en los conteos para rastrear discrepancias
- 👤 Cada usuario queda registrado automáticamente
- 🔍 Usa filtros en reportes para buscar rápidamente
- 🎨 Los colores indican el estado: 🔴 faltan, 🟢 sobra, ⚫ exacto

---

**¿Listo?** ¡Abre http://localhost:5173 y comienza! 🎉
