# Daily Goals Challenge 🎯

Una aplicación móvil gamificada para registrar y hacer seguimiento de tus metas diarias. ¡Mantén tu racha, gana puntos y no dejes que pasen 24 horas sin completar tus objetivos!

## 📋 Características

- **Gestión de Categorías**: Organiza tus metas en diferentes categorías personalizadas
- **Metas Personalizables**: Crea metas con diferentes valores de puntos y asígnalas a días específicos
- **Sistema de Puntos**: Gana puntos cada vez que completas una meta
- **Racha (Streak)**: Mantén tu racha completando todas las metas diariamente
- **Reinicio Automático**: Si pasan 24 horas sin completar todas las metas, pierdes tu racha y puntos
- **Calendario Semanal**: Visualiza tu progreso en un calendario de 7 días
- **Material Design**: Interfaz moderna y atractiva con KivyMD
- **Base de Datos Local**: Todos tus datos se guardan localmente en tu dispositivo

## 📦 Generar APK con GitHub Actions (Recomendado)

### Paso 1: Crear repositorio en GitHub
1. Ve a https://github.com/new
2. Nombre: `daily-goals-app` (o el que prefieras)
3. Puede ser público (2000 min/mes gratis) o privado (500 min/mes)

### Paso 2: Subir tu código
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/daily-goals-app.git
git push -u origin main
```

### Paso 3: Esperar la compilación automática
- Ve a la pestaña **"Actions"** en tu repositorio de GitHub
- Verás un workflow corriendo llamado "Build Android APK"
- Espera 15-20 minutos (GitHub compila en sus servidores)
- Cuando termine (✅ verde), haz clic en el workflow
- En "Artifacts" descarga **DailyGoals-APK.zip**

### Paso 4: Instalar en tu celular
1. Descomprime el ZIP y transfiere el APK a tu celular
2. En tu celular: Ajustes → Seguridad → Habilitar "Orígenes desconocidos"
3. Abre el APK y presiona "Instalar"

## 🚀 Testing en PC (Desarrollo)

1. **Instalar Python 3.8 o superior**

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**:
```bash
python main.py
```

### Para Compilar APK (Android)

#### Opción 1: Usando Buildozer en Linux/WSL (Recomendado)

1. **Instalar Buildozer** (requiere Linux o WSL en Windows):
```bash
# Instalar dependencias del sistema (Ubuntu/Debian)
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Instalar Buildozer
pip3 install buildozer cython==0.29.33
```

2. **Compilar el APK**:
```bash
# Primera vez (puede tardar bastante)
buildozer -v android debug

# El APK estará en: bin/dailygoals-1.0-arm64-v8a_armeabi-v7a-debug.apk
```

3. **Instalar en tu celular**:
- Transfiere el archivo APK a tu teléfono
- Habilita "Instalar desde fuentes desconocidas" en Configuración
- Instala el APK

#### Opción 2: Usando Google Colab (Más Fácil para Windows)

1. **Abre este notebook de Google Colab**: [Kivy Android Build](https://colab.research.google.com/)

2. **Sube tus archivos** al Colab:
   - `main.py`
   - `database.py`
   - `game_logic.py`
   - `buildozer.spec`

3. **Ejecuta estas celdas en Colab**:
```python
# Instalar buildozer
!pip install buildozer cython==0.29.33

# Instalar dependencias del sistema
!sudo apt update
!sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# Compilar
!buildozer -v android debug

# Descargar el APK
from google.colab import files
files.download('bin/dailygoals-1.0-arm64-v8a_armeabi-v7a-debug.apk')
```

#### Opción 3: Usar Python for Android (p4a) directamente

```bash
pip install python-for-android
p4a apk --private . --package=org.dailygoals.app --name "Daily Goals" --version 1.0 --bootstrap=sdl2 --requirements=python3,kivy
```

## 📱 Uso de la Aplicación

### 1. Primera Configuración

1. **Crear Categorías**:
   - Ve a "Gestionar Categorías"
   - Crea categorías como: "Salud", "Estudio", "Ejercicio", etc.

2. **Crear Metas**:
   - Ve a "Gestionar Metas"
   - Agrega metas a tus categorías
   - Asigna puntos a cada meta (ej: 10, 20, 50 puntos)

### 2. Uso Diario

1. **Completar Metas**:
   - Ve a "Completar Metas"
   - Marca cada meta que completes durante el día
   - Gana puntos por cada meta completada

2. **Mantener la Racha**:
   - Completa TODAS tus metas antes de que pasen 24 horas
   - Si completas todas las metas, tu racha aumenta 1 día
   - Si pasan 24 horas sin completar todas, ¡pierdes todo!

3. **Ver Progreso**:
   - La pantalla principal muestra tu racha actual y puntos
   - Ve a "Estadísticas" para ver tu mejor racha y más datos

## ⚠️ Reglas Importantes

- **Tienes 24 horas** desde tu última actividad para completar todas las metas
- Si **no completas TODAS las metas** en 24 horas, el juego se reinicia
- Cuando se reinicia: pierdes tu racha actual y todos tus puntos
- Tu **mejor racha** se guarda como récord
- Solo puedes completar cada meta **una vez por día**

## 🏗️ Estructura del Proyecto

```
daily-goals-challenge/
│
├── main.py              # Interfaz Kivy y pantallas
├── database.py          # Gestión de base de datos SQLite
├── game_logic.py        # Lógica del juego (rachas, puntos, reinicio)
├── buildozer.spec       # Configuración para compilar Android
├── requirements.txt     # Dependencias Python
└── README.md           # Este archivo
```

## 🔧 Solución de Problemas

### Error: "sqlite3 module not found"
SQLite3 viene incluido con Python, pero si tienes problemas:
```bash
pip install pysqlite3-binary
```

### Error en Buildozer: "SDK/NDK not found"
Buildozer descarga automáticamente el SDK/NDK en la primera compilación. Asegúrate de tener buena conexión a internet.

### La app se cierra al abrir en Android
Verifica los logs con:
```bash
buildozer android logcat
```

### Permisos de almacenamiento
La app necesita permisos de almacenamiento para guardar la base de datos. Ya están configurados en `buildozer.spec`.

## 🎮 Ejemplos de Uso

### Ejemplo 1: Rutina de Fitness
**Categorías**: Ejercicio, Nutrición, Descanso

**Metas**:
- Ejercicio: "30 min cardio" (20 pts), "Rutina de fuerza" (25 pts)
- Nutrición: "5 porciones de vegetales" (15 pts), "2L de agua" (10 pts)
- Descanso: "8 horas de sueño" (15 pts)

**Total diario**: 85 puntos posibles

### Ejemplo 2: Desarrollo Personal
**Categorías**: Aprendizaje, Productividad, Bienestar

**Metas**:
- Aprendizaje: "1 hora de estudio" (20 pts), "Leer 30 páginas" (15 pts)
- Productividad: "Completar 3 tareas importantes" (25 pts)
- Bienestar: "Meditar 10 min" (10 pts), "No redes sociales después 9pm" (15 pts)

**Total diario**: 85 puntos posibles

## 📊 Sistema de Puntos

- Puntos predeterminados: **10 puntos por meta**
- Puedes personalizar los puntos al crear cada meta
- Los puntos son acumulativos mientras mantengas tu racha
- Se pierden completamente si fallas en completar todas las metas en 24 horas

## 🔮 Características Futuras Posibles

- [ ] Notificaciones push recordando completar metas
- [ ] Gráficos de progreso semanal/mensual
- [ ] Metas semanales (no solo diarias)
- [ ] Compartir logros con amigos
- [ ] Temas y personalización de colores
- [ ] Recompensas desbloqueables con puntos

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso personal.

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Si encuentras bugs o tienes ideas para mejorar la app, no dudes en crear un issue o pull request.

## 📞 Soporte

Si tienes problemas o preguntas:
1. Revisa la sección de Solución de Problemas
2. Verifica que tengas todas las dependencias instaladas
3. Asegúrate de estar usando Python 3.8 o superior

---

**¡Disfruta alcanzando tus metas diarias! 🎯🔥**
