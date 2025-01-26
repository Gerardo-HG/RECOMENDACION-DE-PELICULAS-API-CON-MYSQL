# API de Recomendación de Películas

Este proyecto es una API de recomendación de películas que permite a los usuarios registrar sus datos, gestionar su lista de películas favoritas y recibir recomendaciones personalizadas basadas en sus preferencias.

## Características

- **Creación de Usuarios**: Los usuarios pueden registrarse proporcionando su información básica.
- **Gestión de Películas**: Los administradores pueden agregar, editar y eliminar películas.
- **Recomendaciones Personalizadas**: La API genera recomendaciones de películas basadas en las preferencias de los usuarios.
- **Consulta de Películas Recomendadas**: Los usuarios pueden obtener una lista de películas recomendadas según su historial y gustos.

## Tecnologías Utilizadas

- **FastAPI**: Framework de Python para crear la API.
- **SQLAlchemy**: ORM para la gestión de la base de datos.
- **Pydantic**: Para la validación de datos de entrada y salida.
- **Uvicorn**: Servidor ASGI para ejecutar la API.
- **MySQL**: Base de datos relacional utilizada para almacenar los datos de usuarios y películas.

## Instalación

### Prerequisitos

- Python 3.8 o superior
- MySQL (debe tener instalado MySQL en su máquina o usar una instancia en la nube)
- Herramienta de terminal para interactuar con MySQL

### Pasos para la instalación

1. Clona este repositorio en tu máquina local:
   
   ```
   git clone https://github.com/usuario/https://github.com/Gerardo-HG/RECOMENDACION-DE-PELICULAS-API-CON-MYSQL.git
    ```


3. Navega al directorio del proyecto
   
   ```
     cd "directorio_proyecto"
   ```

4. Crea un entorno virtual

   ```
     python3 -m venv venv    
   ```

5. Activa el entorno virtual
   
   . En Windows:
   
       ```
         .\venv\Scripts\activate
        ```

   . En macOS/Linux:

         ```
          source venv/bin/activate
         ```

6. Instalas dependencias
   
       ```
        pip install -r requirements.txt
       ```

7. Configura la base de datos MySQL
    . Accede a MySQL a través de la terminal:

       ```
         mysql -u root -p
       ```

     . Crea la base de datos para la API

         ```
            CREATE DATABASE peliculas_recomendaciones;
         ```

      . Crea el usuario y dale acceso a la base de datos

        ```
          CREATE USER 'usuario_api'@'localhost' IDENTIFIED BY 'tu_contraseña';
          GRANT ALL PRIVILEGES ON peliculas_recomendaciones.* TO 'usuario_api'@'localhost';
          FLUSH PRIVILEGES;
         ```

8. Configura la conexión a la base de datos en el archivo config.py:
       . Actualiza las credenciales de conexión a MySQL en tu archivo de configuración.

          ```
           DATABASE_URL = "mysql+mysqlconnector://usuario_api:tu_contraseña@localhost/peliculas_recomendaciones"
          ```

9. Ejecuta las migraciones para crear las tablas en la base de datos:

        ```
          alembic updrade head
        ```


10. Ejecuta el servidor de desarrollo:
 
         ```
        uvicorn main:app --reload
         ```
   
       La API estará disponible en http://127.0.0.1:8000.
     
