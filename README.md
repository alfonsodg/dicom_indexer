#Indexer Client



##Descripción
Cliente ligero que se conecta con base de datos de PACS local DCM4CHEE compatible y envía hacia el indexador central la metadata de los estudios radiológicos contenidos en el centro médico, convirtiéndolos a json y registrándolos por medio de un webservice.


##Arquitectura

###Base
* Python 2.7 o superior
* MySQL 5.6 o superior

###Dependiente de Python
* PyMySQL 0.7.11 o superior
* Requests 2.18.4 o superior


##Base de Datos
Este cliente indexador está soportado sobre la base de datos original de dcm4chee, solo agrega una nueva tabla **study_service** y un procedimiento almacenado **indexer_process** que permite grabar el último estudio registrado en la nueva tabla.
A partir de este punto, el cliente consulta (select) **study_service** y obtiene los últimos estudios a enviar al indexador.


##Estructura
```
indexer_client -> Directorio Raiz
    client.py -> Aplicación cliente, autoejecutable
    requirements.txt -> Archivo dependencias Python
    README.md -> Este documento (Guia uso / desarrollador)
    config.json -> Archivo de configuración
    server.json -> Archivo básico json que debe crearse o modificarse
    extras -> Directorio con archivos adicionales importantes
        add_indexer.sql -> Cambios en la base de datos PACS
        heading_indexer.sh -> Script bash para cron
    tests -> Directorio con pruebas de la aplicación
```

    
##Instalación

###Copiar / clonar el directorio en /srv
```
git clone https://alfonsodg@bitbucket.org/controlradiologico/dicom_indexer.git
```

###Verificar que se tenga instalado la arquitectura base (python y mysql)

###Instalar ENV
```
virtualenv venv
```

###Activar ENV
```
source venv/bin/activate
```

###Instalar requerimientos de la aplicación contenidos en requirements.txt
```
pip install -r requirements.txt
```

###Modificar config.json a discreción o dejarlo tal como está para instalación por defecto

###Crear o modificar server.json colocando el código del centro médico
```
    {
      "server": "000"
    }
```

###Agregar modificaciones SQL al MySQL del PACS, para esto basta con copiar el contenido dentro de **add_indexer.sql** dentro del mismo mysql o (desde el directorio dicom_indexer)
```
    mysql BASEDATOS_DCM4CHEE < extras/add_indexer.sql
```

###Para la primera carga ejecutar client.py con el parámetro initial (desde el directorio dicom_indexer)
```
python client.py initial
```


##Uso

* Para agregar más estudios al indexador basta con ejecutar
```
**python client.py** o simplemente ejecutar **./client.py**
```


##Crontab (Tareas Automatizadas)
Agregar en el cron con el comando **crontab -e**
```
    */5 * * * * /srv/dicom_indexer/extras/dicom_indexer.sh
```


##Estructura de Datos

###Formato JSON para INSERT (POST)
```
    {
      "patient_pk":"Clave primaria de paciente en tabla patient en pacsdb",
      "patient_id":"RUT de paciente",
      "patient_name":"Nombre de paciente",
      "study_pk":"Clave primaria de estudio en tabla study en pacsdb",
      "study_iuid":"Código único de estudio SUID",
      "study_datetime":"Fecha y hora de estudio",
      "study_description":"Descripción de la prueba",
      "study_modality":"Modalidad",
      "study_series":"Número de series",
      "study_instances":"Número de instancias",
      "center":"Código de PACS (centro médico) origen"
    }
```

##Configuración
Está contenido dentro del archivo **config.json**
```
    {
      "database": {
        "host": "IP o nombre del servidor",
        "port": "Puerto",
        "user": "Usuario asignado",
        "password": "Clave asignada",
        "name": "nombre de la base de datos"
      },
      "server": "No se usa, revisar: server.json",
      "key": "Llave de seguridad para acceso al webservice",
      "webservice_url": "URL del servicio web para insertar los registros en formato json"
    }
```