#***********************************************************************
# ESTA APLICACIÓN AYUDA A OBTENER INFORMACION REFERENTE A TU CUOTA DE
# NAVEGACIÓN POR DATOS MOVILES, A COMPRAR TUS PAQUETES DE DATOS Y A
# OBTENER OTRO TIPO DE INFORMACION DESDE LA CONSOLA DE WINDOWS. LA MISMA
# NO TIENE UN CARACTER COMERCIAL, ES DE CÓDIGO LIBRE. LOS COMANDOS
# DE ACCESO SON:
#
# Guardar tus credenciales para acceder a tus datos desde mi.cubacel.net
# > cuota_datos perfil -uss [NUMEROTELF] -pss [CONTRASEÑA]
#
# Obtiene la información de la cuenta
# > cuota_datos perfil -i
#
# Obtiene cuánto le queda de datos nacionales y fecha de vencimiento
# > cuota_datos cuota -nac
#
# Obtiene cuánto le queda de datos 3g y fecha de vencimiento
# > cuota_datos cuota -umts
#
# Obtiene cuánto le queda de datos 4g y fecha de vencimiento
# > cuota_datos cuota -lte
#
# Obtiene cuánto le queda de datos de todo los tipos (nacional, 3g y 4g)
# > cuota_datos cuota -t
#
# Compra un paquete de datos de 400mb
# > cuota_datos comprar -umts 400mb
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
import pickle

#obtiene los datos guardados de formato pickle
def get_data():
    with open('data.pickle', 'rb') as pickled_file:
        restored_data = pickle.load(pickled_file)
        username = restored_data["username"]
        password = restored_data["password"]
        ret = {
            "username": username,
            "password": password
        }
    return ret

#Guarda los datos en formato pickle
def save_data(username, password):
    data = {
        'username': username,
        'password': password
    }
    pickle_file = open('data.pickle', 'wb')
    pickle.dump(data, pickle_file)
    pickle_file.close()

def conection_very_data(username, password):
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

def conection_pay_data(username, password):
    """
    :param username: Número de teléfono registrado en la plataforma de mi.cubacel.net
    :param password: Contraseña registrada en la plataforma de mi.cubacel.net
    :return: Interpretación de BeautifulSoup del código fuente de la pagina para comprar datos moviles
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
    r5 = requests.get("https://mi.cubacel.net/primary/_-iiVGcd3i", verify=False, cookies=r3.cookies)
    soup = BeautifulSoup(r5.text, "html.parser")
    return soup

def conection_confirm_pay(username, password, link):
    """
    :param username: Número de teléfono registrado en la plataforma de mi.cubacel.net
    :param password: Contraseña registrada en la plataforma de mi.cubacel.net
    :return: Interpretación de BeautifulSoup del código fuente de la página para confirmar la comprar de datos móviles
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
    r5 = requests.get(link, verify=False, cookies=r3.cookies)
    soup = BeautifulSoup(r5.text.encode("utf8"), "html.parser")
    link_conf = "https://mi.cubacel.net" + soup.find("a", {"class": "offerPresentationProductBuyLink_msdp"}).attrs.get("href")
    r6 = requests.get(link_conf, verify=False, cookies=r3.cookies) #esta peticion confirma la compra
    soup = BeautifulSoup(r6.text.encode("utf8"), "html.parser")
    with open('index.html', 'wb') as file:
        file.write(bytes(r6.text,"utf-8"))
    file.close()
    print(soup.find("div", { "class": "products_purchase_details_block" }).find_all("p")[1].getText())
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

def get_compra_paquete_3g(soup, tipo):
    """
    :param soup: Interpretación de BeautifulSoup de la pagina de promocion
    :param tipo: Tipo de datos a contratar: 400mb, 600mb, 1gb, 2.5gb o 4gb
    :return: Retorna el mensaje que devuelve mi.cubacel.net
    """
    block = soup.find_all("div", {"class": "offerPresentationProductRows_msdp"})
    if tipo.lower() == "400mb":
        compra_pak = block[2].find_all("div", {"class": "product_block"})[0]
    elif tipo.lower() == "600mb":
        compra_pak = block[2].find_all("div", {"class": "product_block"})[1]
    elif tipo.lower() == "1gb":
        compra_pak = block[2].find_all("div", {"class": "product_block"})[2]
    elif tipo.lower() == "2.5gb":
        compra_pak = block[2].find_all("div", {"class": "product_block"})[3]
    elif tipo.lower() == "4gb":
        compra_pak = block[2].find_all("div", {"class": "product_block"})[4]
    else:
        print("Error en tipo de paquete")
        return
    print("")
    print("Descripción: " + compra_pak.find("div", {"class": "product_desc"}).find_all("span")[0].getText())
    print("Precio: " + compra_pak.find("div", {"class": "product_desc"}).find_all("span")[1].getText())
    print("")
    opc = input("Está seguro de querer comprar este paquete de datos s[Si] / n[No]: ")
    if opc == "s" or opc.lower() == "si":
        print("")
        print("Comprando datos ...")
        link = "https://mi.cubacel.net" + compra_pak.find_all("a", {"class": "offerPresentationProductBuyLink_msdp"})[
            1].attrs.get("href", None)
        username = get_data()["username"]
        password = get_data()["password"]
        conection_confirm_pay(username, password, link)
        print("")
        print("Información de cuenta:")
        username = get_data()["username"]
        password = get_data()["password"]
        soup = conection_very_data(username, password)
        get_info(soup)

def get_compra_paquete_4g(soup, tipo):
    """
    :param soup: Interpretación de BeautifulSoup de la pagina de promocion
    :param tipo: Tipo de datos a contratar: 6.5gb o 10gb
    :return: Retorna el mensaje que devuelve mi.cubacel.net
    """
    block = soup.find_all("div", {"class": "offerPresentationProductRows_msdp"})
    if tipo.lower() == "6.5gb":
        compra_pak = block[1].find_all("div", {"class": "product_block"})[0]
    elif tipo.lower() == "10gb":
        compra_pak = block[1].find_all("div", {"class": "product_block"})[1]
    else:
        print("Error en tipo de paquete")
        return
    print("")
    print("Descripción: " + compra_pak.find("div", {"class": "product_desc"}).find_all("span")[0].getText())
    print("Precio: " + compra_pak.find("div", {"class": "product_desc"}).find_all("span")[1].getText())
    print("")
    opc = input("Está seguro de querer comprar este paquete de datos s[Si] / n[No]: ")
    if opc == "s" or opc.lower() == "si":
        print("")
        print("Comprando datos ...")
        link = "https://mi.cubacel.net" + compra_pak.find_all("a", {"class": "offerPresentationProductBuyLink_msdp"})[
            1].attrs.get("href", None)
        username = get_data()["username"]
        password = get_data()["password"]
        conection_confirm_pay(username, password, link)
        print("")
        print("Información de cuenta:")
        username = get_data()["username"]
        password = get_data()["password"]
        soup = conection_very_data(username, password)
        get_info(soup)

#Muestra información de este script
def sobre_func(args):
    print("**********************************************")
    print("|            Cuota Datos v0.2                |")
    print("|                                            |")
    print("|   Para conocer el estado de tus datos      |")
    print("|        Para comprar algún paquete          |")
    print("|           Para conocer tu saldo            |")
    print("|                                            |")
    print("|  Desarrollador: Ing. Josué Carballo Baños  |")
    print("|      Licencia: GNU-GPL v3 Open Source      |")
    print("|                                            |")
    print("|                 GitHub                     |")
    print("|https://github.com/JosueCarballo/cuota_datos|")
    print("|                                            |")
    print("**********************************************")

#Funcion que trata los argumentos de cuota
def cuota_func(args):
    if args.nacional:
        try:
            username = get_data()["username"]
            password = get_data()["password"]
            print("Buscando datos. Espere unos segundos...")
            soup = conection_very_data(username, password)
            get_info_nac(soup)
        except:
            print("")
            print("No se ha podido acceder a sus datos de cuota. Puede que no tenga conexión o que sus credenciales esten incorrectas.")
    elif args.dato4g:
        try:
            username = get_data()["username"]
            password = get_data()["password"]
            print("Buscando datos. Espere unos segundos...")
            soup = conection_very_data(username, password)
            get_info_dato4g(soup)
        except:
            print("")
            print("No se ha podido acceder a sus datos de cuota. Puede que no tenga conexión o que sus credenciales esten incorrectas.")
    elif args.dato3g:
        try:
            username = get_data()["username"]
            password = get_data()["password"]
            print("Buscando datos. Espere unos segundos...")
            soup = conection_very_data(username, password)
            get_info_dato3g(soup)
        except:
            print("")
            print("No se ha podido acceder a sus datos de cuota. Puede que no tenga conexión o que sus credenciales esten incorrectas.")
    elif args.todo:
        try:
            username = get_data()["username"]
            password = get_data()["password"]
            print("Buscando datos. Espere unos segundos...")
            soup = conection_very_data(username, password)
            get_info_todo(soup)
        except:
            print("")
            print("No se ha podido acceder a sus datos de cuota. Puede que no tenga conexión o que sus credenciales esten incorrectas.")

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
        soup = conection_very_data(username, password)
        get_info(soup)
        return None

    if args.username != None and args.password != None:
        save_data(args.username, args.password)
        print("Se ha guardado sus datos de perfil correctamente.")
    else:
        print("Debe usar los argumentos -uss [USERNAME] -pss [PASSWORD]")

#Funcion que trata los argumentos de comprar
def compra_func(args):
    if args.datos3g:
        tipo = args.datos3g
        continuar = False
        if  tipo.lower() == "400mb" or \
            tipo.lower() == "600mb" or \
            tipo.lower() == "1gb" or \
            tipo.lower() == "2.5gb" or \
            tipo.lower() == "4gb":
            continuar = True
        if continuar:
            username = get_data()["username"]
            password = get_data()["password"]
            print("Buscando datos. Espere unos segundos...")
            soup = conection_pay_data(username, password)
            get_compra_paquete_3g(soup, tipo)
        else:
            print("Debe especificar un tipo de compra válida: 400mb, 600mb, 1gb, 2.5gb o 4gb")
    elif args.datos4g:
        tipo = args.datos4g
        continuar = False
        if tipo.lower() == "6.5gb" or \
           tipo.lower() == "10gb":
            continuar = True
        if continuar:
            username = get_data()["username"]
            password = get_data()["password"]
            print("Buscando datos. Espere unos segundos...")
            soup = conection_pay_data(username, password)
            get_compra_paquete_4g(soup, tipo)
        else:
            print("Debe especificar un tipo de compra válida: 400mb, 600mb, 1gb, 2.5gb o 4gb")
    else:
        is_3g = True
        print("Generación de transmisión de voz y datos")
        print("     0. 3g ó UMTS")
        print("     1. 4g ó LTE")
        print("     2. Ninguno")
        print("")
        opc = input("> Selecciona la generación de transmisión de voz y datos para la que desea realizar la compra: ")
        if opc == "0":
            print("Paquetes de datos:")
            print("     0. 400mb")
            print("     1. 600mb")
            print("     2. 1gb")
            print("     3. 2.5gb")
            print("     4. 4gb")
            print("     5. Ninguno")
            print("")
            opc = input("> Escriba el número del paquete que desea comprar: ")
            if opc == "0": tipo = "400mb"
            elif opc == "1": tipo = "600mb"
            elif opc == "2": tipo = "1gb"
            elif opc == "3": tipo = "2.5gb"
            elif opc == "4": tipo = "4gb"
            elif opc == "5": return
            else:
                print("No ha introducido una opción numérica válida.")
                return
            is_3g = True
        elif opc == "1":
            print("Paquetes de datos:")
            print("     0. 6.5gb")
            print("     1. 10gb")
            print("     2. Ninguno")
            print("")
            opc = input("> Escriba el número del paquete que desea comprar: ")
            if opc == "0": tipo = "6.5gb"
            elif opc == "1": tipo = "10gb"
            elif opc == "2": return
            else:
                print("No ha introducido una opción numérica válida.")
                return
            is_3g = False
        elif opc == "2": return
        else:
            print("No ha introducido una opción numérica válida.")
            return
        username = get_data()["username"]
        password = get_data()["password"]
        print("Buscando datos. Espere unos segundos...")
        soup = conection_pay_data(username, password)
        if is_3g:
            get_compra_paquete_3g(soup, tipo)
        else:
            get_compra_paquete_4g(soup, tipo)

#Funcion principal de arranque
def main(args):
    parser = argparse.ArgumentParser(
        epilog=dedent("""\
        Subcommands:
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

        Usa -h para obtener más información
        """),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )


    subparsers = parser.add_subparsers()

    #SOBRE
    sobre_parser = subparsers.add_parser('sobre')
    sobre_parser.set_defaults(func=sobre_func)

    #CUOTA
    cuota_parser = subparsers.add_parser('cuota')
    cuota_parser.set_defaults(func=cuota_func)
    cuota_parser.add_argument("-nac", "--nacional",
        action="store_true",
        help="Devuelve la información de cuota nacional"
    )
    cuota_parser.add_argument("-lte", "--dato4g",
        action="store_true",
        help="Devuelve la información de cuota 4g"
    )
    cuota_parser.add_argument("-umts", "--dato3g",
        action="store_true",
        help="Devuelve la información de cuota 3g"
    )
    cuota_parser.add_argument("-t", "--todo",
        action="store_true",
        help="Devuelve todos los datos de cuota de los datos moviles"
    )

    # PERFIL
    perfil_parser = subparsers.add_parser('perfil')
    perfil_parser.set_defaults(func=perfil_func)
    perfil_parser.add_argument("-uss", "--username",
        nargs="?",
        help="Guarda el usuario"
    )
    perfil_parser.add_argument("-pss", "--password",
       nargs="?",
       help="Guarda el password"
    )
    perfil_parser.add_argument("-i", "--info",
       action="store_true",
       help="Devuelve todos los datos de cuota"
    )

    # COMPRA
    comprar_parser = subparsers.add_parser('comprar')
    comprar_parser.set_defaults(func=compra_func)
    comprar_parser.add_argument("-umts", "--datos3g",
        nargs="?",
        help="Compra paquetes de datos 3G. Debe especificar 400mb, 600mb, 1gb, 2.5gb, 4gb."
    )
    comprar_parser.add_argument("-lte", "--datos4g",
        nargs="?",
        help="Guarda el password"
    )

    args = parser.parse_args()
    if 'func' in args:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main(sys.argv[1:])


