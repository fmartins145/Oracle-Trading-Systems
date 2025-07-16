import streamlit as st
import requests
from bs4 import BeautifulSoup
from datetime import datetime

st.set_page_config(page_title="Sinais Forex USD - Tempo Real")

st.title("📈 Sinais Fundamentais Forex (USD) - Tempo Real")

url = "https://www.forexfactory.com/calendar"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

eventos = soup.find_all("tr", class_="calendar__row")

sinais = []

for evento in eventos:
    impacto = evento.find("td", class_="calendar__impact")
    if impacto and "High" in impacto.get("title", ""):
        moeda = evento.find("td", class_="calendar__currency").text.strip()
        horario = evento.find("td", class_="calendar__time").text.strip()
        nome = evento.find("td", class_="calendar__event").text.strip()
        atual = evento.find("td", class_="calendar__actual").text.strip()
        previsto = evento.find("td", class_="calendar__forecast").text.strip()

        if moeda == "USD":
            if atual and previsto and atual != "-" and previsto != "-":
                try:
                    atual_f = float(atual.replace('%', '').replace(',', ''))
                    previsto_f = float(previsto.replace('%', '').replace(',', ''))

                    direcao = "USD Forte 📈" if atual_f > previsto_f else "USD Fraco 📉"
                    acao = "Comprar USD (Ex: USDJPY, USDCAD)" if atual_f > previsto_f else "Vender USD (Ex: EURUSD, GBPUSD)"
                    tempo = "Gráfico recomendado: M15 a M30"

                    sinais.append({
                        "horario": horario,
                        "nome": nome,
                        "atual": atual,
                        "previsto": previsto,
                        "direcao": direcao,
                        "acao": acao,
                        "tempo": tempo
                    })
                except:
                    pass

if not sinais:
    st.info("Nenhum evento de alto impacto com USD encontrado hoje.")
else:
    for s in sinais:
        st.subheader(f"🕒 {s['horario']} - {s['nome']}")
        st.write(f"📊 Atual: {s['atual']} | Previsto: {s['previsto']}")
        st.success(f"📌 Direção: {s['direcao']}")
        st.warning(f"💰 Ação sugerida: {s['acao']}")
        st.info(s["tempo"])
