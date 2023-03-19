import sqlite3
import nmap
import socket

sqlite_connection = sqlite3.connect('domains.db')
cursor = sqlite_connection.cursor()
sqlite_create_table_query = '''CREATE TABLE domains (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            domain TEXT NOT NULL,
                            http BOOL,
                            https BOOL);'''
try:
    cursor.execute(sqlite_create_table_query)
except:
    pass

sqlite_create_table_query = '''CREATE UNIQUE INDEX idx_domains_domain ON domains (domain);'''
try:
    cursor.execute(sqlite_create_table_query)
except:
    pass
sqlite_connection.commit()

nm = nmap.PortScanner()


def get_ip(domain) -> str:
    result_ip = None
    try:
        result_ip = str(socket.gethostbyname(domain))
    except:
        pass
    return result_ip

def nmap_scan(ip):
    return nm.scan(str(ip), arguments='-T5 -Pn -p 80,443')


with open('domains.txt') as f:
    lines = f.readlines()
    for domain in lines:
        domain = domain.strip()
        print(domain)
        ip = get_ip(domain)
        if not ip:
            pass
        result = nmap_scan(ip)

        if result['scan']:
            http = True if result['scan'][ip]['tcp'][80]['state'] == "open" else False
            https = True if result['scan'][ip]['tcp'][443]['state'] == "open" else False
            cursor.execute(
                "REPLACE INTO domains (domain, http, https) VALUES (?, ?, ?)",
                (domain, http, https))
            sqlite_connection.commit()
    f.close()
