# Zicão Store · Simulador de Compras

Simulador de parcelas no cartão (PagBank e PicPay, de 1x a 18x). Você digita quanto quer **receber à vista** e o app mostra quanto cobrar em cada parcela. O texto sai pronto pra colar no WhatsApp ou no Instagram.

**Online:** https://thiagogaldinozicao-source.github.io/maquininha

## Como funciona

```
total = valor_à_vista / (1 - taxa)
```

A maquininha desconta a taxa do total cobrado. Dividindo por `(1 - taxa)`, o que sobra depois do desconto é exatamente o valor à vista.
Exemplo: R$ 1.000 no PagBank 1x (4,99%) → cobra R$ 1.052,52.

## Estrutura

```
index.html             app inteiro (HTML + CSS + JS, sem dependências)
manifest.webmanifest   nome/ícones quando instalado na tela inicial
favicon.svg            ícone da aba do navegador
sw.js                  service worker (app abre sem internet)
icons/                 PNGs dos ícones (iPhone, Android, App Store)
icons/icon.svg         desenho-fonte do ícone
icons/gen.py           regenera todos os PNGs a partir do SVG
```

Não tem build, framework nem `npm install`: é um arquivo HTML estático.

## Rodar no computador

Precisa de um servidor local. Abrir o arquivo com duplo clique até funciona, mas a cópia de texto e o manifest podem falhar.

```bash
git clone https://github.com/thiagogaldinozicao-source/maquininha.git
cd maquininha
python3 -m http.server 8000
# abrir http://localhost:8000
```

Para testar no celular na mesma rede Wi-Fi, abra `http://IP-DO-PC:8000`.

## Publicar

O site é servido pelo **GitHub Pages** a partir da branch `main` (pasta raiz). Para publicar, basta dar push na `main`; o site atualiza em 1 a 2 minutos.

O HTML sempre busca a versão nova quando há internet. Se mudar ícones ou o manifest, aumente `VERSAO` no `sw.js` para limpar o cache antigo.

## Tarefas comuns

### Atualizar taxas

No `index.html`, procure o objeto `maquinas`. Cada linha é `[parcelas, taxa em %]`:

```js
pagbank: { ..., taxas: [[1,4.99],[2,5.83], ... ] }
```

Para adicionar outra maquininha, crie uma nova chave nesse objeto e um botão `.aba` com `id="aba-<chave>"`.

### Trocar o ícone

1. Edite o desenho em `icons/gen.py` (função `svg`).
2. Gere os ícones de novo (precisa de Python 3 com Playwright):
   ```bash
   pip install playwright && playwright install chromium
   python3 icons/gen.py
   ```
3. Aumente o `?v=N` nos links de ícone do `index.html` e do `manifest.webmanifest` (isso fura o cache).
4. No iPhone, apague o atalho e adicione de novo pelo Safari: Compartilhar → Adicionar à Tela de Início.

## Dados salvos

O app guarda só duas coisas no `localStorage` do navegador: a última maquininha usada (`zicao-maquina`) e o rodapé (`zicao-rodape`). Nada é enviado pra servidor nenhum.
