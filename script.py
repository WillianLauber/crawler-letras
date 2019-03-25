from bs4 import BeautifulSoup 
import requests
import re
import csv

#criar arquivo
def salvar(lista):    
       
    with open('data/samba_enredo.csv', mode='w', newline='') as csvFile:
        fieldnames = ['escola', 'genero', 'ano', 'enredo', 'letra']
        writer = csv.DictWriter(csvFile, fieldnames=fieldnames, delimiter=";")
        writer.writeheader()
        for item in lista:
            writer.writerow({'escola': item[0], 'genero': item[1], 'ano': item[2], 'enredo':item[3], 'letra':item[4]})


#pegar as informações do samba enredo na pagina
def carregarInformacoes(pagina):
    try:
        page = requests.get(pagina)
        soup = BeautifulSoup(page.text, 'lxml')

      

        # formata titulo
        titulo = str(soup.find_all(class_ = 'cnt-head_title'))
        titulo = re.sub(r'[></]', ' ', titulo.split("h1")[1])

        #formata letra
        letra = []
        letra_temp = str(soup.find_all(class_ = 'cnt-letra p402_premium'))
        letra_temp = letra_temp.split("<p>")

        for i in range(1, len(letra_temp)):
            linha = letra_temp[i].replace("\"", "").replace("<br/>", ". ").replace(" </div>", "").replace("</p>", "").replace("]", "") + "."
            letra.append(linha)

        #retirar ano, nome da escola de samba e genero musical
        
        titulo = titulo.strip().split(" - ")
        escola = titulo.pop(0).strip()
       # titulo = titulo[0].split(" ")
        genero = titulo[0][:-4].strip()
        ano =  int(titulo[0][-4:])
        enredo = None
        if letra[1].startswith("Enredo: "):
            enredo = letra.pop(0).strip().split("Enredo: ")[1]
        letra = '\n'.join(letra)

        return [ escola, genero, ano, enredo, letra]
    except KeyboardInterrupt:
        print()
        print("Good bye")
    except :
        print("erro ao buscar informações do link: " + pagina)
        return [ None, None, None, None, None]
  
site = "https://www.letras.mus.br"

try:
    page = requests.get(site + "/sambas/")
    beautifulSoup = BeautifulSoup(page.text, 'lxml')

    # Pegar links de todos os samba enredos
    cnt = beautifulSoup.select('.cnt-list a')
    endpoints = []
    sambas = []
    for i in range(len(cnt)): 
        endpoints.append(cnt[i]["href"])
    endpoints.append(cnt[0]["href"])

    for endpoint in endpoints:
        sambas.append(carregarInformacoes(site + endpoint))

    salvar(sambas)
    
except KeyboardInterrupt:
    print()
    print("Good bye")
