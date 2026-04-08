import os
import time
import requests
import pandas as pd
from datetime import datetime
from playwright.sync_api import sync_playwright

PASTA_EDITAIS = "editais"
os.makedirs(PASTA_EDITAIS, exist_ok=True)

TOKEN = "8154559594:AAF8JFztQIJS65SZ3bTuf2EcXFS7vBHI8zA"
CHAT_ID = "5229401010"

URL = "https://www.pciconcursos.com.br/concursos/norte/"


# ================= FUNÇÕES =================

def calcular_urgencia(data_str):
    try:
        data_final = datetime.strptime(data_str, "%d/%m/%Y")
        dias = (data_final - datetime.now()).days
        return "URGENTE" if dias <= 3 else "NÃO URGENTE"
    except:
        return "NÃO DEFINIDO"


def extrair_salario(texto):
    if "R$" in texto:
        try:
            return "R$" + texto.split("R$")[-1].split("\n")[0].strip()
        except:
            return "Não informado"
    return "Não informado"


def tratar_cargos(texto):
    cargos = [c.strip() for c in texto.split("\n") if c.strip()]

    if len(cargos) > 3:
        return "Diversos"

    return ", ".join(cargos) if cargos else "Não informado"


def encontrar_pdf(page):
    links = page.locator("a")

    for i in range(links.count()):
        href = links.nth(i).get_attribute("href")

        if href and ".pdf" in href:
            if not href.startswith("http"):
                href = "https://www.pciconcursos.com.br" + href
            return href

    return None


def baixar_pdf(url, nome):
    try:
        r = requests.get(url, timeout=15)

        if r.status_code == 200:
            nome = nome.replace("/", "").replace("\\", "")
            caminho = os.path.join(PASTA_EDITAIS, f"{nome}.pdf")

            with open(caminho, "wb") as f:
                f.write(r.content)

            return caminho
    except:
        pass

    return "Não encontrado"


# ================= TELEGRAM =================

def enviar_mensagem(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})


def montar_mensagem(dados):
    msg = "Concursos do Amazonas\n\n"

    for d in dados:
        msg += f"{d['Concurso']}\n"
        msg += f"{d['Salário']}\n"
        msg += f"{d['Cargos']}\n"
        msg += f"{d['Data Final']}\n"
        msg += f"{d['Alerta']}\n"
        msg += f"{d['Link']}\n\n"

    return msg


# ================= MAIN =================

def main():
    dados = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print("Abrindo site...")

        for tentativa in range(3):
            try:
                print(f"Tentativa {tentativa+1}...")
                page.goto(URL, timeout=60000, wait_until="domcontentloaded")
                break
            except:
                print("Falhou, tentando novamente...")
                time.sleep(3)

        page.wait_for_selector("div.na")

        concursos = page.locator("div.na")

        print(f"Total encontrado: {concursos.count()}")

        for i in range(concursos.count()):
            try:
                concurso = concursos.nth(i)
                estado = concurso.locator(".cc").inner_text()

                if estado != "AM":
                    continue

                titulo = concurso.locator("a").inner_text()
                link = concurso.locator("a").get_attribute("href")

                if not link.startswith("http"):
                    link = "https://www.pciconcursos.com.br" + link

                data_texto = concurso.locator(".ce span").inner_text()

                if "a" in data_texto:
                    data_texto = data_texto.split("a")[-1].strip()

                alerta = calcular_urgencia(data_texto)

                info = concurso.locator(".cd").inner_text()
                salario = extrair_salario(info)

                try:
                    cargos_texto = concurso.locator(".cd span").first.inner_text()
                except:
                    cargos_texto = ""

                cargos = tratar_cargos(cargos_texto)

                print(f"{titulo}")

                page.goto(link, timeout=60000, wait_until="domcontentloaded")
                page.wait_for_selector("body")

                pdf_link = encontrar_pdf(page)
                pdf = baixar_pdf(pdf_link, titulo) if pdf_link else "Não encontrado"

                dados.append({
                    "Concurso": titulo,
                    "Salário": salario,
                    "Cargos": cargos,
                    "Data Final": data_texto,
                    "Alerta": alerta,
                    "Link": link,
                    "PDF": pdf
                })

                page.go_back()
                page.wait_for_selector("div.na")

            except Exception as e:
                print("Erro:", e)
                continue

        browser.close()

    if dados:
        df = pd.DataFrame(dados)
        df.to_excel("concursos_amazonas.xlsx", index=False)
        print("Excel criado!")

        mensagem = montar_mensagem(dados)
        enviar_mensagem(mensagem)

        print("Enviado para Telegram!")


# 🔥 CORREÇÃO AQUI
if __name__ == "__main__":
    main()