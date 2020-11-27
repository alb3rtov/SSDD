# Proyect url 
https://github.com/alb3rtov/ssdd

# Proyect members
- Alberto Vázquez Martínez <Alberto.Vazquez1@alu.uclm.es>
- Alvaro Ramos Cobacho <Alvaro.Ramos4@alu.uclm.es>

# Directorios
- El "slice" se encuentra en la raíz del proyecto (slice.ice)
- Directorio "src": contiene los archivos de python
- Directorio "config": contiene los archivos de configuración de ZeroC Ice

# Ejecución:
En la raíz del repositorio existen una serie de scripts en bash para la ejecución del servidor y cliente.
- run_map_server.sh: Arranca el servidor de mapas y de juego. <br>
```bash
  ./run_map_server.sh <Proxy servivio de autenticacion>
```
- upload_map.sh: Ejecuta un cliente para subir un mapa al servidor de mapas.
```bash
  ./upload_map.sh <Proxy servicio de mapas> <token> <ruta archivo mapa (.JSON)>
```
