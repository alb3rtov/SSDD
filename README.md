# Proyect url 
https://github.com/alb3rtov/ssdd

# Proyect members
- Alberto Vázquez Martínez <Alberto.Vazquez1@alu.uclm.es>
- Alvaro Ramos Cobacho <Alvaro.Ramos4@alu.uclm.es>

# Directorios
- El "slice" se encuentra en la raíz del proyecto (slice.ice)
- Directorio "src": contiene los archivos de python
- Directorio "config": contiene los archivos de configuración de ZeroC Ice
- Directorio "maps": contiene los mapas (archivos .json), que los clientes subiran.
- Directorio "icegauntlet": contiene los ficheros del juego ICEGauntlet.

# Ejecución:
En la raíz del repositorio existen una serie de scripts en bash para la ejecución del servidor y cliente.
- run_server.sh: Arranca el servidor de mapas y de juego. En nuestro caso, hemos decidido implementar un solo servidor que será el de mapas y el de juego. <br>
```bash
  ./run_server.sh <Proxy servivio de autenticacion>
```
- upload_map.sh: Ejecuta un cliente para subir un mapa al servidor de mapas.
```bash
  ./upload_map.sh <Proxy servicio de mapas> <token> <ruta archivo mapa (.JSON)>
```
- get_new_token : Ejecuta una instancia del cliente para autenticarse en el servidor de autenticación. Devuelve el token del usuario.
```bash
  ./get_new_token <Usuario> <Constraseña> <Proxy servicio autenticacion>
```

- run_game.sh : Muestra un menú para ejecutar el juego local, y para conseguir una room del servicio de juego.
```bash
  ./run_game.sh <Proxy servicio juego>
```
   ### Ejemplo método getRoom
   El método getRoom elige un mapa aleatorio. Muestra por pantalla los mapas disponibles localmente.
   
   ![Alt Text](https://i.imgur.com/93l7eN8.gif)
