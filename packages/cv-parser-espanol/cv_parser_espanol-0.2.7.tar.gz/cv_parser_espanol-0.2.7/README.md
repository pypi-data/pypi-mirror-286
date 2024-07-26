# CV Parser Español

`cv_parser_espanol` es un paquete de python que te permite leer un CV en los siguientes formatos (PDF, DOCX, TXT) y desglosarlo en diferentes secciones: 
1. Nombre
2. Direccion
3. Telefono
4. Educacion
5. Experiencia Laboral
6. Skills

## Instalacion
Puedes instalarlo utilizando pip

```bash
pip install cv-parser-espanol
```

## Modo de uso
Si tienes que convertir un pdf puedes primero utilizar el extractor de pdf a texto (pasando el archivo como bytes)
```python
import cv_parser_espanol
text= pdf_to_text(file_bytes)
cv = parse_cv(text)
```

Si el archivo que tienes es un docx o un pdf pero no tienes los bytes puedes utilizar directamete la funcion extract_text

