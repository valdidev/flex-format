# FlexFormat

FlexFormat es una aplicación de escritorio con interfaz gráfica desarrollada en Python que permite convertir datos entre los formatos JSON, XML y YAML de manera sencilla y eficiente. La aplicación cuenta con un diseño moderno de tema oscuro, validación de entrada en tiempo real, y opciones para copiar el resultado al portapapeles o guardarlo en un archivo.

## Características
- **Conversión de formatos**: Convierte datos entre JSON, XML y YAML.
- **Validación en tiempo real**: Verifica la validez del formato de entrada mientras se escribe.
- **Interfaz gráfica intuitiva**: Diseño en tema oscuro con controles claros y tooltips para botones.
- **Funcionalidades adicionales**:
  - Copiar el resultado al portapapeles.
  - Guardar el resultado en un archivo.
- **Soporte de Unicode**: Maneja caracteres no-ASCII en todos los formatos.
- **Pantalla de inicio**: Muestra una splash screen al iniciar la aplicación.

## Requisitos
- **Python**: Versión 3.6 o superior.
- **Dependencias**:
  - `tkinter` (normalmente incluido con Python).
  - `PyYAML` (para manejar YAML).
- **Sistema operativo**: Compatible con Windows, macOS y Linux (probado en Windows con el ícono `flexformat.ico`).
- **Archivos adicionales**:
  - `flexformat.ico`: Ícono de la aplicación (requerido para Windows).

## Instalación
1. Clona o descarga el repositorio:
   ```bash
   git clone <URL-del-repositorio>
   cd flexformat
   ```
2. Instala las dependencias necesarias:
   ```bash
   pip install pyyaml
   ```
3. Asegúrate de que el archivo `flexformat.ico` esté en el directorio raíz (para Windows).
4. Ejecuta la aplicación:
   ```bash
   python main.py
   ```

## Estructura del Proyecto
```
flexformat/
├── converters/
│   ├── json_converter.py    # Funciones para parsear y convertir JSON
│   ├── xml_converter.py    # Funciones para parsear y convertir XML
│   ├── yaml_converter.py   # Funciones para parsear y convertir YAML
├── ui/
│   ├── format_converter.py  # Lógica de la interfaz gráfica principal
│   ├── splash_screen.py     # Lógica de la pantalla de inicio
│   ├── styles.py           # Configuración del tema oscuro
├── utils/
│   ├── file_operations.py  # Funciones para copiar y guardar archivos
│   ├── validation.py       # Funciones para validar entradas
├── main.py                 # Punto de entrada de la aplicación
├── flexformat.ico          # Ícono de la aplicación
└── README.md               # Documentación del proyecto
```

## Uso
1. **Iniciar la aplicación**:
   - Ejecuta `python main.py`.
   - Se mostrará una pantalla de inicio (splash screen) antes de cargar la interfaz principal.
2. **Interfaz principal**:
   - Selecciona el formato de entrada (JSON, XML o YAML) desde el primer menú desplegable.
   - Selecciona el formato de salida desde el segundo menú desplegable.
   - Escribe o pega el código en el área de texto de entrada (izquierda).
   - La validación se realiza automáticamente mientras escribes, mostrando un mensaje debajo del área de entrada (color azul para válido, rojo para errores).
3. **Convertir**:
   - Haz clic en el botón "Convertir" para transformar el código al formato de salida.
   - El resultado aparecerá en el área de texto de salida (derecha).
4. **Opciones adicionales**:
   - **Copiar al portapapeles**: Usa el botón con el ícono 📋.
   - **Guardar como archivo**: Usa el botón con el ícono 💾.
5. **Errores**:
   - Si el formato de entrada es inválido, el formato de salida es igual al de entrada, o no hay entrada, se mostrará un mensaje de error.

## Detalles Técnicos
- **Librerías utilizadas**:
  - `json` (estándar) para manejar JSON.
  - `xml.etree.ElementTree` y `xml.dom.minidom` (estándar) para XML.
  - `yaml` (PyYAML) para YAML.
  - `tkinter` para la interfaz gráfica.
- **Conversión**:
  - Los datos se parsean a un diccionario Python como formato intermedio.
  - Cada formato tiene funciones específicas para parsear (`parse`) y convertir (`convert`) en los módulos de `converters/`.
- **Interfaz**:
  - Tema oscuro personalizado definido en `ui/styles.py`.
  - Área de texto con fuente `Consolas` para mejor legibilidad.
  - Tooltips en los botones de copiar y guardar.
- **Validación**:
  - Implementada en `utils/validation.py`, verifica la entrada en tiempo real según el formato seleccionado.

## Contribuciones
Si deseas contribuir:
1. Crea un fork del repositorio.
2. Implementa tus cambios en una rama nueva.
3. Envía un pull request con una descripción clara de los cambios.

## Licencia
Este proyecto no especifica una licencia. Contacta al autor para más detalles.

## Notas
- La pantalla de inicio (`ui/splash_screen.py`) no se incluyó en los archivos proporcionados, pero se asume que existe y se ejecuta antes de la interfaz principal.
- Asegúrate de que `flexformat.ico` esté presente en el directorio raíz para evitar errores en Windows.
- La aplicación es sensible a errores en el formato de entrada; asegúrate de ingresar datos válidos para evitar excepciones.