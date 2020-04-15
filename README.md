Cuota Datos v0.2
==========
La aplicación Cuota Datos le permite la revisión y compra de tus datos móviles desde tu ordenador. El mismo ha sido creado en lenguaje Python. Una versión instalable para windows puede ser adquirida desde este enlace junto con una guía para el uso correcto de la aplicación.

https://my.pcloud.com/publink/show?code=XZuRIPkZ30T7h8lB9fp4wp4dtYtvUYDyK20V

## Ejecutar el Script
Para ejecutar el script tanto desde Windows o Linux debe posicionar la consola y ejecutar:

> python cuota_datos.py

Se mostrarán los posibles comandos a utilizar y que serán explicados posterioremente:
    sobre

    perfil
        -uss --username: Para guardar su usuario
        -pss --password: Para guardar la contraseña
        -i  --info: Retorna información de la cuenta

    cuota
        -nac  --nacional: Devuelve la información de cuota nacional
        -lte  --dato4g: Devuelve la información de cuota 4g
        -umts  --dato3g: Devuelve la información de cuota 3g
        -t    --todo: Devuelve todos los datos de cuota
 
    comprar
        -umts --datos3g: Para comprar un paquete de cuota 3g
            400mb
            600mb
            1g
            2.5g
            4g
        -lte  --datos4g: Para comprar un paquete de cuota 4g
            6.5gb
            10gb
            
## Información de desarrollo
Para conocer los datos de desarrollo de Cuota Datos debe escribir el comando:

> cuota_datos.py sobre

## Actualizar las credenciales

Este script usa los datos brindados por https://mi.cubacel.net/ , es por ello que antes de usarlo deberá tener una cuenta en dicha plataforma. Estos datos se guardan en un archivo binario .pickle en su máquina, por lo que no se envía a ningún servidor ajeno. Luego estas credenciales serán usadas  cada vez que desee conocer el estado de su cuota movil. Para ello deberá utilizar el comando:

> cuota_datos.py perfil -uss [NUMEROTELEFONO] -pss [CONTRASEÑA]

El comando perfil esta constituido por el argumento -uss ó --username que guardará el usuario con el que iniciará seción, en este caso la plataforma registra a los usuarios por su número de teléfono, es por ello que el valor correspondiente será el del teléfono con el que se registró en la plataforma y al cual se le gestionará su uso de datos móviles. A la vez, también está constituido por el argumento -pss ó --password que guardará la contraseña con la que se resgitró.

## Verificar información de mi cuenta

El comando perfil tiene asociado también el argumento -i ó --info que brinda detalles del número de teléfono, saldo de esta cuenta y fecha de vencimiento de la línea. Para poder tener acceso a la misma escribimos:

> cuota_datos.py perfil -i

## Verificar mi consumo de datos

La principal tarea del script está dado por determinar el consumo de sus datos móviles desde su ordenador. Este estado se obtiene mediante el comando **cuota** que tiene diferentes argumentos que ayudan a visualizar el estado de la cuenta:

**-nac ó --nacional** Este argumento se usa para conocer cuánto le queda y cuando vence su bono nacional.
**-umts ó --dato3g** Este argumento se usa para conocer cuánto le queda y cuando vence sus datos 3G.
**-lte ó --dato4g** Este argumento se usa para conocer cuánto le queda y cuando vence sus datos 4G.
**-t ó --todo** Este argumento visualiza todos los estados de cuota nacional, 3G y 4G y sus respectivos vencimientos.

Ejemplo:
> cuota_datos.py cuota -lte
    
    Buscando datos. Espere unos segundos...
    Cuota: 80.222 MB
    Vence: 25 días
    
##  Comprar paquete de datos
Desde Cuota Datos podemos realizar la cuota de datos móviles. Para ello deberán escribir los siguientes comandos:

> cuota_datos comprar -[TECNOLOGIA] [PLAN]

Sería:
**-umts [PLAN] ó --datos3g [PLAN]** Para comprar un plan de datos 3G
**-lte [PLAN] ó --datos4g [PLAN]** Para comprar un plan de datos 4G

El Plan para 3G: 400mb, 600mb, 1gb, 2.5gb, 4gb
El PLan para 4G: 6.5gb, 10gb

Ejemplo: Comprar un plan para 3G de 400mb

> cuota_datos comprar -umts 400mb

## Detalles técnicos

Quienes se han autenticado en la plataforma de mi.cubacel.net notarán que además de poner usuario y contraseña también deberán poner un valor captcha (https://mi.cubacel.net:8443/login/). Este script burla la escritura de un valor captcha para entrar y obtener los valores de estado de cuenta. Para ello podemos notar en el código javascript de la página de login, que este genera valores numéricos aleatorios de 1 a 190 y este es adicionado a una URL que carga en el servidor la imagen correspondiente. Teniendo en cuenta los valores de la cookie guardado a la hora de acceder a la página de login el sistema hace una correspondencia entre la petición de la imagen y el acceso. De esta forma lo que se hace es siempre hacer la misma petición de valor de imagen captcha para cuando se inicie seción no se pida al usuario introducirlo y conocer siempre cual será su valor.

## Usar script de forma automática en la consola

En el link (https://my.pcloud.com/publink/show?code=XZuRIPkZ30T7h8lB9fp4wp4dtYtvUYDyK20V) hay un descargable instalable y un PDF explicando el cómo deberá realizarse la misma y el uso natural por la consola de windows. Este repositorio también posee el script setup.py con el que desde la consola podrá realizar su propia compilación para su sistema operativo con el comando:

> python setup.py bdist_msi

## Cambios
**version 0.2**
    - Guardar credenciales en un archivo binario .pickle
    - Comprar paquete 3G y 4G
    - Mejoras en el instalador para Windows.

## Licencia

Este código queda libererado bajo licencia GNP-GPL v3 de la Free Software Fundation y versiones posteriores.
