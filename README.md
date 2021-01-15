# Encriptacion-caotica

Aplicación web de encriptación de imágenes RGB usando una combinación de los mapa de Henon y el mapa del gato de Arnold junto con una clave privada y una clave pública. Estas claves son generadas empleando el algoritmo de Diffie-Helmann.

<p align="center">
  <img src="imagenes/menu_principal.png">
</p>

## Instalar librerias
```
pip install -r requirements.txt
```

## Como ejecutar la aplicación

Para ejecutar la aplicación debe acceder a la ruta del repositorio mediante un terminal.

Ejecutar el comando 
````
python app.py
````

## Como encriptar una imagen

Si no dispone de un par de claves, <strong>debe generarlas</strong>.

<p align="center">
  <img src="imagenes/generacion_keys.png">
</p>

Una vez creadas las claves ya podremos encriptar la imagen.

Selecciona la imagen que desea encriptar y pulse encriptar.

<p align="center">
  <img src="imagenes/encriptar.png">
</p>

## Como desencriptar una imagen

El proceso para desencriptar una imagen es el mismo que el de encriptar.

Selecciona una imagen encriptada y pulse desencriptar.

<p align="center">
  <img src="imagenes/desencriptar.png">
</p>

<strong>Es importante que para desencriptar una imagen encriptada, se debe usar la misma clave que se usó para enciptarla. En caso de que no se use la misma clave, el proceso fallará.</strong>
