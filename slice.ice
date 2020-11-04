module IceGauntlet {
	//Interfaz de autenticación
	interface Authentication {
		//Método para cambiar contraseña
		void changePassword (string user, string currentPassHash, string newPassHash) throws Unauthorized;
		
		//Método para obtener token de autorización
		void getNewToken (string user, string passwordHash) throws Unauthorized;

		//Método para comprobar si el token es válido
		bool isValid (string token);
	};

	//Interfaz de gestión de mapas
	interface MapManaging {
		
	};
};
