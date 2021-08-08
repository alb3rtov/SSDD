# Proyect url 
https://github.com/alb3rtov/ssdd

# Proyect members
- Alberto Vázquez Martínez <Alberto.Vazquez1@alu.uclm.es>
- Alvaro Ramos Cobacho <Alvaro.Ramos4@alu.uclm.es>

# Directorios
- El "slice" se encuentra en la raíz del proyecto ([icegauntlet.ice](https://github.com/alb3rtov/SSDD/blob/L1/icegauntlet.ice))
- Directorio "src": contiene los archivos de python del cliente y servidor
- Directorio "config": contiene los archivos de configuración de ZeroC Ice
- Directorio "maps": contiene los mapas (archivos .json), que los clientes subiran.
- Directorio "icegauntlet": contiene un fork de los ficheros del juego ICEGauntlet.

# Ejecución:
En la raíz del repositorio existen una serie de scripts en bash para la ejecución del servidor y cliente.
- run_map_server.sh: Arranca el servidor de mapas y de juego. En nuestro caso, hemos decidido implementar un solo servidor que será el de mapas y el de juego. **Importante ejecutar primero este script antes del run_game_server, ya que este crea los dos proxies**.<br>
```bash
  ./run_map_server.sh <Proxy servivio de autenticacion>
```
- run_game_server.sh: Imprime por pantalla el proxy de servicio de juego. En este caso, no es necesario pasarle como argumento el servicio de proxy de autenticación.
```bash
  ./run_game_server.sh
```
- upload_map.sh: Ejecuta una instancia del cliente para subir un mapa al servidor de mapas.
```bash
  ./upload_map.sh <Proxy servicio de mapas> <token> <ruta archivo mapa (.JSON)>
```
- delete_map.sh: Ejecuta una instancia del cliente para borrar un mapa del servidor de mapas.
```bash
  ./upload_map.sh <Proxy servicio de mapas> <token> <nombre mapa>
```
- get_new_token : Ejecuta una instancia del cliente para autenticarse en el servidor de autenticación. Devuelve el token del usuario.
```bash
  ./get_new_token <Usuario> <Constraseña> <Proxy servicio autenticacion>
```
- run_game.sh : Muestra un menú para ejecutar el juego local, y para conseguir una room del servicio de juego.
```bash
  ./run_game.sh <Proxy servicio juego>
```
- change_pass.sh : Script para cambiar la contraseña del usuario.
```bash
  ./change_pass.sh <Proxy servicio autenticacion>
```

   <!-- ### Ejemplo método getRoom
   El método getRoom elige un mapa aleatorio. Muestra por pantalla los mapas disponibles localmente.
   ![Alt Text](https://i.imgur.com/93l7eN8.gif) -->
