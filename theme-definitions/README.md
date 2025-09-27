# Theme Definitions

Este directorio contiene definiciones de temas en formato YAML para ThemeWeaver. Estas definiciones permiten crear temas completos sin necesidad de especificar todos los parámetros en la línea de comandos.

## Uso

Para generar un tema a partir de un archivo YAML, usa el siguiente comando:

```bash
pixi run generate nombre-tema --from-yaml /ruta/al/archivo.yaml
```

Donde:
- `nombre-tema` es el nombre que se usará para el directorio del tema
- `--from-yaml` especifica la ruta al archivo YAML con la definición del tema

## Estructura del archivo YAML

Los archivos YAML de definición de temas tienen la siguiente estructura:

```yaml
nombre-tema:
  overwrite: true|false                # Opcional, sobreescribir si existe
  variants: [dark, light]              # Opcional, variantes a generar
  display-name: "Nombre del Tema"      # Opcional, nombre para mostrar
  description: "Descripción del tema"  # Opcional, descripción
  author: "Autor del tema"             # Opcional, autor
  tags: [tag1, tag2, tag3]             # Opcional, etiquetas
  colors:                              # Obligatorio, 6 colores base
    - "#color1"  # Primary
    - "#color2"  # Secondary
    - "#color3"  # Error
    - "#color4"  # Success
    - "#color5"  # Warning
    - "#color6"  # Special
  syntax-format:                       # Opcional, formato de sintaxis
    normal: none|bold|italic|bold+italic
    keyword: none|bold|italic|bold+italic
    magic: none|bold|italic|bold+italic
    builtin: none|bold|italic|bold+italic
    definition: none|bold|italic|bold+italic
    comment: none|bold|italic|bold+italic
    string: none|bold|italic|bold+italic
    number: none|bold|italic|bold+italic
    instance: none|bold|italic|bold+italic
  syntax-colors:                       # Opcional, colores de sintaxis
    dark:                              # Para variante oscura
      - "#B0"
      - "#B1"
      - "#B2"
      # ... hasta 16 colores
    light:                             # Para variante clara
      - "#B0"
      - "#B1"
      - "#B2"
      # ... hasta 16 colores
```

## Ejemplo

```yaml
mi-tema:
  overwrite: true
  variants: [dark, light]
  display-name: "Mi Tema"
  description: "Un tema personalizado"
  author: "Mi Nombre"
  tags: [oscuro, alto-contraste, minimalista]
  colors:
    - "#1e1e2e"  # Primary
    - "#b4befe"  # Secondary
    - "#f38ba8"  # Error
    - "#a6e3a1"  # Success
    - "#fab387"  # Warning
    - "#eba0ac"  # Special
  syntax-format:
    normal: none
    keyword: bold
    magic: bold
    builtin: none
    definition: none
    comment: italic
    string: none
    number: none
    instance: italic
  syntax-colors:
    dark:
      - "#181926"  # B0
      - "#1e1e2e"  # B1
      - "#89b4fa"  # B2
      - "#cdd6f4"  # B3
      - "#181926"  # B4
      - "#a6e3a1"  # B5
      - "#f38ba8"  # B6
      - "#cdd6f4"  # B7
      - "#f38ba8"  # B8
      - "#94e2d5"  # B9
      - "#89b4fa"  # B10
      - "#a6e3a1"  # B11
      - "#7f849c"  # B12
      - "#f9e2af"  # B13
      - "#cba6f7"  # B14
      - "#cdd6f4"  # B15
    light:
      - "#e6e9ef"  # B0
      - "#eff1f5"  # B1
      - "#1e66f5"  # B2
      - "#4c4f69"  # B3
      - "#e6e9ef"  # B4
      - "#40a02b"  # B5
      - "#d20f39"  # B6
      - "#4c4f69"  # B7
      - "#d20f39"  # B8
      - "#179299"  # B9
      - "#1e66f5"  # B10
      - "#40a02b"  # B11
      - "#9ca0b0"  # B12
      - "#df8e1d"  # B13
      - "#8839ef"  # B14
      - "#4c4f69"  # B15
```

## Notas

- Para los colores de sintaxis, puedes proporcionar 1 color (para auto-generación) o 16 colores (para una paleta personalizada).
- Si no se especifican colores de sintaxis, se generarán automáticamente a partir de los colores del grupo.
- Si no se especifican variantes, se generarán ambas (dark y light).
- El nombre del tema en el archivo YAML puede ser diferente del nombre usado en la línea de comandos. El nombre de la línea de comandos tiene prioridad.
