"""
Raspador de Preços — Mercado Livre
====================================
INSTALAÇÃO:
  pip install requests beautifulsoup4

COMO USAR:
  python raspador_precos.py
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
from time import sleep

# ── Configurações ──────────────────────────────────────────────────────────────

ARQUIVO_HISTORICO = "historico_precos.json"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "pt-BR,pt;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# ── Produtos para monitorar ────────────────────────────────────────────────────
# Edite essa lista com seus produtos e preços-alvo!

PRODUTOS = [
    {
        "nome": "Teclado Mecânico",
        "busca": "teclado mecânico gamer",
        "preco_alvo": 200.00,
    },
    {
        "nome": "Mouse Gamer",
        "busca": "mouse gamer sem fio",
        "preco_alvo": 150.00,
    },
    {
        "nome": "Headset",
        "busca": "headset ",
        "preco_alvo": 180.00,
    },
]

# ── Busca no Mercado Livre ─────────────────────────────────────────────────────

def buscar_preco_mercadolivre(termo_busca: str) -> dict | None:
    """Busca o primeiro resultado no Mercado Livre e retorna título, preço e link."""

    termo_formatado = termo_busca.replace(" ", "-")
    url = f"https://lista.mercadolivre.com.br/{termo_formatado}"

    try:
        resposta = requests.get(url, headers=HEADERS, timeout=15)
        resposta.raise_for_status()
        soup = BeautifulSoup(resposta.text, "html.parser")

        # ── Estratégia 1: seletores novos do ML (2025) ────────────────────────
        items = soup.select("li.ui-search-layout__item")

        for item in items:
            # Título — tenta vários seletores possíveis
            titulo = None
            for sel in ["h2.poly-box", "h2", ".poly-component__title", "a[title]"]:
                elem = item.select_one(sel)
                if elem:
                    titulo = elem.get_text(strip=True) or elem.get("title", "")
                    if titulo:
                        break

            # Preço — tenta extrair o valor monetário
            preco = None

            # Tenta seletor de fração (parte inteira do preço)
            fracao = item.select_one(".andes-money-amount__fraction")
            if fracao:
                centavos_elem = item.select_one(".andes-money-amount__cents")
                preco_str = fracao.get_text(strip=True).replace(".", "").replace(",", "")
                centavos  = centavos_elem.get_text(strip=True) if centavos_elem else "00"
                try:
                    preco = float(f"{preco_str}.{centavos[:2]}")
                except ValueError:
                    pass

            # Fallback: procura qualquer texto com padrão R$ X.XXX,XX
            if not preco:
                import re
                texto = item.get_text()
                match = re.search(r'R\$\s*([\d\.]+),(\d{2})', texto)
                if match:
                    inteiro   = match.group(1).replace(".", "")
                    centavos2 = match.group(2)
                    try:
                        preco = float(f"{inteiro}.{centavos2}")
                    except ValueError:
                        pass

            # Link do produto
            link_elem = item.select_one("a.poly-component__title, a[href*='MLB']")
            link = link_elem["href"] if link_elem else url

            # Só retorna se tiver pelo menos o preço
            if preco and preco > 0:
                return {
                    "titulo": titulo or "Produto encontrado",
                    "preco":  preco,
                    "link":   link,
                }

        # ── Estratégia 2: procura qualquer preço na página ────────────────────
        import re
        matches = re.findall(r'R\$\s*([\d\.]+),(\d{2})', resposta.text)
        if matches:
            inteiro, centavos = matches[0]
            preco = float(f"{inteiro.replace('.', '')}.{centavos}")
            # Pega o primeiro título que encontrar
            titulo_elem = soup.select_one("h2")
            titulo = titulo_elem.get_text(strip=True) if titulo_elem else "Produto encontrado"
            return {"titulo": titulo, "preco": preco, "link": url}

        print(f"  Nenhum produto encontrado para '{termo_busca}'")
        return None

    except requests.exceptions.Timeout:
        print(f"  Tempo limite excedido")
        return None
    except requests.exceptions.ConnectionError:
        print(f"  Sem conexão com a internet")
        return None
    except Exception as e:
        print(f"  Erro: {e}")
        return None


# ── Histórico ──────────────────────────────────────────────────────────────────

def carregar_historico() -> dict:
    if os.path.exists(ARQUIVO_HISTORICO):
        with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_historico(historico: dict) -> None:
    with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(historico, f, ensure_ascii=False, indent=2)

def registrar_preco(historico: dict, nome: str, dados: dict) -> dict:
    if nome not in historico:
        historico[nome] = []
    historico[nome].append({
        "data":   datetime.now().strftime("%Y-%m-%d %H:%M"),
        "preco":  dados["preco"],
        "titulo": dados["titulo"],
        "link":   dados["link"],
    })
    return historico

def calcular_variacao(historico: dict, nome: str) -> float | None:
    registros = historico.get(nome, [])
    if len(registros) < 2:
        return None
    preco_inicial = registros[0]["preco"]
    preco_atual   = registros[-1]["preco"]
    return round(((preco_atual - preco_inicial) / preco_inicial) * 100, 2)


# ── Relatório e alertas ────────────────────────────────────────────────────────

def verificar_alertas(produto: dict, preco_atual: float) -> None:
    if preco_atual <= produto["preco_alvo"]:
        print("\n" + "!" * 60)
        print(f"  ALERTA: {produto['nome']} atingiu seu preco-alvo!")
        print(f"  Preco atual: R$ {preco_atual:.2f}  |  Alvo: R$ {produto['preco_alvo']:.2f}")
        print(f"  Economia:    R$ {produto['preco_alvo'] - preco_atual:.2f}")
        print("!" * 60)

def exibir_relatorio(historico: dict) -> None:
    print("\n" + "=" * 60)
    print("  RELATORIO DE PRECOS")
    print("=" * 60)
    for nome, registros in historico.items():
        if not registros:
            continue
        ultimo   = registros[-1]
        variacao = calcular_variacao(historico, nome)
        print(f"\n{nome}")
        print(f"  Preco atual:  R$ {ultimo['preco']:.2f}")
        print(f"  Produto:      {ultimo['titulo'][:58]}")
        print(f"  Ultima busca: {ultimo['data']}")
        if variacao is not None:
            sinal = "v" if variacao < 0 else "^"
            print(f"  Variacao:     {sinal} {abs(variacao):.1f}% desde o inicio")
        print(f"  Link:         {ultimo['link'][:65]}")
    print("\n" + "=" * 60)


# ── Principal ──────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  RASPADOR DE PRECOS — Mercado Livre")
    print("=" * 60)
    print(f"  Monitorando {len(PRODUTOS)} produto(s)...")
    print("=" * 60)

    historico = carregar_historico()

    for i, produto in enumerate(PRODUTOS, 1):
        print(f"\n[{i}/{len(PRODUTOS)}] Buscando: {produto['nome']}...")
        resultado = buscar_preco_mercadolivre(produto["busca"])

        if resultado:
            print(f"  Preco:   R$ {resultado['preco']:.2f}")
            print(f"  Produto: {resultado['titulo'][:55]}")
            verificar_alertas(produto, resultado["preco"])
            historico = registrar_preco(historico, produto["nome"], resultado)
        else:
            print(f"  Nao foi possivel buscar agora.")

        if i < len(PRODUTOS):
            sleep(2)

    salvar_historico(historico)
    print(f"\nHistorico salvo em '{ARQUIVO_HISTORICO}'")
    exibir_relatorio(historico)
    print("\nDica: rode todo dia para acompanhar a variacao de precos!")

if __name__ == "__main__":
    main()