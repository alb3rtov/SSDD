module IceGauntlet {

	//Interfaz de autenticación
	interface Authentication {
		//Método para cambiar contraseña
		void changePassword (string user, string currentPassHash, string newPassHash) throws Unauthorized;
		
		//Método para obtener token de autorización
		void getNewToken (string user, string passwordHash) throws Unauthorized;

		//Método para comprobar si el token es válido
		bool isValid (string token) throws Unauthorized;
	};

	//Interfaz de gestión de mapas
	interface MapManaging {
		//Metodo publicar mapa
		void publish (string token, string roomData) throws Unauthorized, RoomAlreadyExists;
		//Metodo eliminar mapa
		void remove (string token, string roomName) throws Unauthorized, RoomNotExists;
	};

	//Interfaz de juego
	interface Game {
		//Metodo para obenter la room
		string getRoom() throws RoomNotExists;
	};
};
