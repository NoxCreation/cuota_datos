#***********************************************************************
# ESTA APLICACIÓN AYUDA A OBTENER INFORMACION REFERENTE A TU CUOTA DE
# NAVEGACIÓN POR DATOS MOVILES DESDE LA CONSOLA DE WINDOWS. LA MISMA
# NO TIENE UN CARACTER COMERCIAL, ES DE CÓDIGO LIBRE. LOS COMANDOS
# DE ACCESO SON:
#
# Guardar tus credenciales para acceder a tus datos desde mi.cubacel.net
# > cuota_datos perfil -u <NUMEROTELF> -p <CONTRASEÑA>
#
# Obtiene la información de la cuenta
# > cuota_datos perfil -i
#
# Obtiene cuánto le queda de datos nacionales y fecha de vencimiento
# > cuota_datos cuota -n
#
# Obtiene cuánto le queda de datos 3g y fecha de vencimiento
# > cuota_datos cuota -3
#
# Obtiene cuánto le queda de datos 4g y fecha de vencimiento
# > cuota_datos cuota -4
#
# Obtiene cuánto le queda de datos de todo los tipos (nacional, 3g y 4g)
# > cuota_datos cuota -a
#
# Descargar código fuente: https://github.com/JosueCarballo/cuota_datos
# Licencia: Este código queda libererado bajo licencia GNP-GPL v3 de la Free Software Fundation y versiones posteriores.
#***********************************************************************

import json

import requests
import urllib3
from bs4 import BeautifulSoup

import sys
import argparse
from textwrap import dedent

def get_data():
    f = open('data.js', 'r')
    return json.loads(f.read())

def conection(username, password):
    """
    :param username: Número de teléfono registrado en la plataforma de mi.cubacel.net
    :param password: Contraseña registrada en la plataforma de mi.cubacel.net
    :return: Interpretación de BeautifulSoup del código fuente de la pagina de datos del perfil
    """
    urllib3.disable_warnings()
    r2 = requests.get("https://mi.cubacel.net:8443/login/images/cimg/86.jpg", verify=False,
                      cookies=requests.session().cookies, stream=True)
    data = {
        "language": "es_ES",
        "username": username,
        "password": password,
        "uword": "every"
    }
    r3 = requests.post("https://mi.cubacel.net:8443/login/Login", data=data, verify=False, cookies=r2.cookies)
    r5 = requests.get("https://mi.cubacel.net/primary/_-ijqJlSHh", verify=False, cookies=r3.cookies)
    soup = BeautifulSoup(r5.text, "html.parser")
    return soup

def get_info(soup):
    """
    :param soup: Valor resultante de la interpretación de BeautifulSoup del código fuente
    """
    saldo = soup.find_all("span", {"class":"cvalue"})[0].find("span", {"class": "mbcHlightValue_msdp"}).getText()
    num_telf = soup.find_all("span", {"class":"cvalue"})[1].getText()
    vence = soup.find_all("span", {"class":"cvalue"})[2].getText()
    print("")
    print("Número de Telf: " + num_telf)
    print("Saldo: " + saldo)
    print("Vencimiento: " + vence)

def get_info_nac(soup):
    """
    :param soup: Valor resultante de la interpretación de BeautifulSoup del código fuente
    """
    block = soup.find_all("div", {"class": "ac_block"})
    datos_nacional = soup.find("div", {"id": "myStat_bonusDataN"}).attrs.get("data-text", None) + " " + soup.find("div",{"id": "myStat_bonusDataN"}).attrs.get("data-info", None)
    expire_datos_nacional = block[0].find("div", {"class": "col2"}).find("div", "expires_date").getText() + " " + block[0].find("div", {"class": "col2"}).find("div", "expires_hours").getText()
    print("")
    print("Cuota: " + datos_nacional)
    print("Vence: " + expire_datos_nacional)

def get_info_dato4g(soup):
    """
    :param soup: Valor resultante de la interpretación de BeautifulSoup del código fuente
    """
    block = soup.find_all("div", {"class": "ac_block"})
    datos_4g = soup.find("div", {"id": "myStat_30012"}).attrs.get("data-text", None) + " " + soup.find("div", {
        "id": "myStat_30012"}).attrs.get("data-info", None)
    expire_datos_4g = block[1].find("div", {"class": "col2"}).find("div", "expires_date").getText() + " " + block[
        0].find("div", {"class": "col2"}).find("div", "expires_hours").getText()
    print("")
    print("Cuota: " + datos_4g)
    print("Vence: " + expire_datos_4g)

def get_info_dato3g(soup):
    """
    :param soup: Valor resultante de la interpretación de BeautifulSoup del código fuente
    """
    block = soup.find_all("div", {"class": "ac_block"})
    datos_3g = soup.find("div", {"id": "myStat_3001"}).attrs.get("data-text", None) + " " + soup.find("div", {
        "id": "myStat_3001"}).attrs.get("data-info", None)
    expire_datos_3g = block[2].find("div", {"class": "col2"}).find("div", "expires_date").getText() + " " + block[
        0].find("div", {"class": "col2"}).find("div", "expires_hours").getText()
    print("")
    print("Cuota: " + datos_3g)
    print("Vence: " + expire_datos_3g)

def get_info_todo(soup):
    """
    :param soup: Valor resultante de la interpretación de BeautifulSoup del código fuente
    """
    block = soup.find_all("div", {"class": "ac_block"})
    datos_nacional = soup.find("div", {"id": "myStat_bonusDataN"}).attrs.get("data-text", None) + " " + soup.find("div", { "id": "myStat_bonusDataN"}).attrs.get(
        "data-info", None)
    expire_datos_nacional = block[0].find("div", {"class": "col2"}).find("div", "expires_date").getText() + " " + block[
        0].find("div", {"class": "col2"}).find("div", "expires_hours").getText()
    datos_4g = soup.find("div", {"id": "myStat_30012"}).attrs.get("data-text", None) + " " + soup.find("div", {
        "id": "myStat_30012"}).attrs.get("data-info", None)
    expire_datos_4g = block[1].find("div", {"class": "col2"}).find("div", "expires_date").getText() + " " + block[
        0].find("div", {"class": "col2"}).find("div", "expires_hours").getText()
    datos_3g = soup.find("div", {"id": "myStat_3001"}).attrs.get("data-text", None) + " " + soup.find("div", {
        "id": "myStat_3001"}).attrs.get("data-info", None)
    expire_datos_3g = block[2].find("div", {"class": "col2"}).find("div", "expires_date").getText() + " " + block[
        0].find("div", {"class": "col2"}).find("div", "expires_hours").getText()
    print("")
    print("Cuota Nacional: " + datos_nacional)
    print("Vence: " + expire_datos_nacional)
    print("")
    print("Cuota 3G: " + datos_3g)
    print("Vence: " + expire_datos_3g)
    print("")
    print("Cuota 4G: " + datos_4g)
    print("Vence: " + expire_datos_4g)


#Funcion que trata los argumentos de cuota
def cuota_func(args):
    # Todo: escoger las excepciones adecuadas para cada bloque try-except para cumplir con la PEP8
    try:
        username = get_data()["username"]
        password = get_data()["password"]
        print("Buscando datos. Espere unos segundos...")
        soup = conection(username, password)
    except:
        print("\nNo se ha podido acceder a sus datos de cuota. Puede que no tenga conexión o que sus credenciales estén incorrectas.")
    
    try:
        if args.nacional:
            get_info_nac(soup)
        elif args.dato4g:
            get_info_dato4g(soup)
        elif args.dato3g:
            get_info_dato3g(soup)
        elif args.todo:
            get_info_todo(soup)
    except:
        pass
        
#Funcion que trata los argumentos de perfil
def perfil_func(args):
    if args.username:
        username = args.username
    if args.password:
        password = args.password
    if args.info:
        username = get_data()["username"]
        password = get_data()["password"]
        print("Buscando datos. Espere unos segundos...")
        soup = conection(username, password)
        get_info(soup)
        return None
    f = open('data.js', 'wb')
    if args.username != None and args.password != None:
        data = {
            'username': username,
            'password': password
        }
        f.write(
            json.dumps(data).encode("utf8")
        )
        f.close()
        print("Se ha guardado sus datos de perfil correctamente.")
    else:
        print("Debe usar los argumentos -uss [USERNAME] -pss [PASSWORD]")

#Funcion principal de arranque
def main(args):
    parser = argparse.ArgumentParser(
        epilog=dedent("""\
        Subcommands:
            perfil
                -u --username: Para guardar su usuario
                -p --password: Para guardar la contraseña
                -i  --info: Retorna información de la cuenta

            cuota
                -n  --nacional: Devuelve la información de cuota nacional
                -4  --dato4g: Devuelve la información de cuota 4g
                -3  --dato3g: Devuelve la información de cuota 3g
                -a    --all: Devuelve todos los datos de cuota

        Usa -h para obtener más información
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )


    subparsers = parser.add_subparsers()

    cuota_parser = subparsers.add_parser('cuota')
    cuota_parser.set_defaults(func=cuota_func)
    cuota_parser.add_argument("-n", "--nacional",
        action="store_true",
        help="Devuelve la información de cuota nacional"
    )
    cuota_parser.add_argument("-4", "--dato4g",
        action="store_true",
        help="Devuelve la información de cuota 4g"
    )
    cuota_parser.add_argument("-3", "--dato3g",
        action="store_true",
        help="Devuelve la información de cuota 3g"
    )
    cuota_parser.add_argument("-a", "--all",
        action="store_true",
        help="Devuelve todos los datos de cuota de los datos móviles"
    )

    perfil_parser = subparsers.add_parser('perfil')
    perfil_parser.set_defaults(func=perfil_func)
    perfil_parser.add_argument("-u", "--username",
        nargs="?",
        help="Guarda el usuario"
    )
    perfil_parser.add_argument("-p", "--password",
       nargs="?",
       help="Guarda la contraseña"
    )
    perfil_parser.add_argument("-i", "--info",
       action="store_true",
       help="Retorna información de la cuenta"
    )

    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main(sys.argv[1:])


