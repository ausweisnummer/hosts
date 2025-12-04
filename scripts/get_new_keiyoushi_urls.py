#!/usr/bin/env python3

import json
import os
import re

from pathlib import Path
from urllib.request import urlretrieve

keiyoushi_filename = "index.json"
hosts_filename = "hosts-porn"
out_filename = "new-addresses.txt"

# Descarga de archivos necesarios.
if not Path(keiyoushi_filename).exists():
    print("Descargando una copia de index.json...")
    urlretrieve(
        "https://raw.githubusercontent.com/keiyoushi/extensions/refs/heads"
        "/repo/index.json",
        keiyoushi_filename,
    )

if not Path(hosts_filename).exists():
    print("Descargando una copia de hosts-porn...")
    urlretrieve(
        "https://raw.githubusercontent.com/ausweisnummer/hosts/refs/heads"
        "/main/hosts-porn",
        hosts_filename,
    )

# Obtención de la lista de sitios NSFW mencionados en index.json.
try:
    with open(keiyoushi_filename, "r") as f:
        ext_list = json.load(f)

    nsfw_site_list = []

    for dict in ext_list:
        nsfw_dict_code = dict.get("nsfw", None)

        if nsfw_dict_code == 1:
            dict_sources = dict.get("sources")

            for source_dict in dict_sources:
                sites_in_dict = source_dict["baseUrl"].split()

                for site in sites_in_dict:
                    new_site = re.sub(r"#,|https://|http://", "", site)
                    new_site = re.sub(r"/(?!.*/).*", "", new_site)

                    if new_site not in nsfw_site_list:
                        nsfw_site_list.append(new_site)
except FileNotFoundError:
    print(f"No se encontró el archivo {keiyoushi_filename}.")
except OSError as os_err:
    print(
        "Se produjo un error del sistema al abrir el archivo"
        f" {keiyoushi_filename}"
        f"\nError encontrado: {os_err}."
    )

# Obtención de la lista de sitios del archivo hosts-porn.
try:
    with open(hosts_filename, "r") as f:
        hosts = f.readlines()

    hosts = [line.strip() for line in hosts if "127.0.0.1" in line]
    hosts = [line.replace("127.0.0.1 ", "") for line in hosts]
except FileNotFoundError:
    print(f"No se encontró el archivo {hosts_filename}.")
except OSError as os_err:
    print(
        "Se produjo un error del sistema al abrir el archivo"
        f" {hosts_filename}"
        f"\nError encontrado: {os_err}."
    )

# Comparación con los contenidos de la lista nsfw_site_list.
# La idea es encontrar aquellas direcciones que no están
# incluidas en el filtro al momento de ejecutar este
# programa y obtener un archivo con dichas direcciones, de
# manera que ya estén listas para insertar en hosts-porn.
try:
    with open(out_filename, "w") as out:
        for site in nsfw_site_list:
            if site not in hosts:
                out.write("127.0.0.1 " + site)
                out.write("\n")
except FileNotFoundError:
    print("No existe el directorio donde se quiere crear el archivo" f" {out_filename}")
except OSError as os_err:
    print(
        f"Se produjo un error del sistema al crear el archivo {out_filename}"
        f"\nError encontrado: {os_err}."
    )

try:
    os.remove(keiyoushi_filename)
    os.remove(hosts_filename)
except OSError as os_err:
    print(
        "Se produjo un error del sistema al borrar uno de los archivos"
        f" {out_filename}"
        f"\nError encontrado: {os_err}."
    )
