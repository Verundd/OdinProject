import requests
import time
import socket
import ssl
import subprocess
import platform
import nmap
import json

def url_split(url):
    url_split = url.split("/")
    return url_split[2]

def time_session(url):
    start_time = time.time()
    r = requests.get(url)
    end_time = time.time()

    all_time = end_time - start_time

    return all_time

def params_dns(url):
    url_sp = url_split(url)

    try:
        ip_adresses = socket.gethostbyname_ex(url_sp)
        return ip_adresses
    except socket.gaierror as e:
        return (f"Ошибка: {e}")

def ssl_search(url):
    hostname = url_split(url)
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
        try:
            s.settimeout(5)  
            s.connect((hostname, 443))
            cert = s.getpeercert()
            cert_json = json.dumps(cert,indent=4)
            return cert_json
        except socket.timeout:
            return f"Ошибка получения SSL-сертификата для {hostname}"

def ping(url):

    host = url_split(url)

    parameter = '-n' if platform.system().lower() == 'windows' else '-c'
    result = subprocess.run(['ping', parameter, '1', host], stdout=subprocess.PIPE)
    res = result.returncode

    if res == 0:
        return f"Хост {host} доступен."
    else:
        return f"Хост {host} недоступен."

def scan_ports(url):


    host = url_split(url)

    scanner = nmap.PortScanner()

    scanner.scan(host, ports='21-443')

    ports_dict = {}

    for h in scanner.all_hosts():
        ports_dict[h] = {}
        for proto in scanner[h].all_protocols():
            ports_dict[h][proto] = {}
            for port in scanner[h][proto].keys():
                ports_dict[h][proto][port] = scanner[h][proto][port]['state']

    ports_json = json.dumps(ports_dict, indent=4)
    
    return ports_json


