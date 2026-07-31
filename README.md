# 🌍 Memória Afro-Brasileira — Dashboard de Patrimônio e Diáspora

Dashboard interativo de mapeamento e documentação do patrimônio cultural, histórico e arqueológico de matriz africana no Brasil.

## Funcionalidades

- 🗺️ **Mapa Interativo** — Pontos geolocalizados com filtros por categoria, estado e período
- 🎞️ **Galeria de Mídia** — Imagens e vídeos dos pontos de memória
- 📚 **Biblioteca de Documentos** — Legislação, dossiês, planos de salvaguarda e bases de dados
- 📊 **Estatísticas em tempo real** — Contadores dinâmicos conforme filtros

## Categorias Mapeadas

| Categoria | Cor |
|-----------|-----|
| Quilombos / Territórios | 🟢 Verde |
| Terreiros de Matriz Africana | 🟣 Roxo |
| Monumentos Históricos | 🟡 Dourado |
| Sítios Arqueológicos | 🔴 Vermelho |
| Bens Culturais Imateriais | 🟠 Laranja |
| Memoriais | ⚫ Cinza |
| Portos de Desembarque | 🔵 Azul |

## Fontes de Dados

- [IPHAN — Patrimônio de Matriz Africana](https://www.gov.br/iphan/pt-br/assuntos/publicacoes-patrimonio-de-matriz-africana)
- [INCRA — Territórios Quilombolas](https://acervofundiario.incra.gov.br/)
- [UNESCO — Cais do Valongo](https://whc.unesco.org/en/list/1548)
- [Slave Voyages Database](https://www.slavevoyages.org/)
- [Fundação Cultural Palmares](https://www.palmares.gov.br/)

## Deploy no Render

1. Fork este repositório
2. Crie um Web Service no [Render](https://render.com)
3. Conecte seu repositório — o `render.yaml` será detectado automaticamente

Ou deploy manual:
```bash
pip install -r requirements.txt
gunicorn app:server
```

## Desenvolvimento Local

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Acesse em `http://localhost:1000`

## Como Contribuir

1. Adicione novos pontos em `data/pontos_memoria.json`
2. Inclua imagens/vídeos de domínio público ou com licença Creative Commons
3. Envie um Pull Request!

## Licença

MIT — Dados e imagens pertencem às respectivas fontes.
