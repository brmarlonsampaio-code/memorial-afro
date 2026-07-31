import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import json

dash.register_page(__name__, path="/documentos", title="Documentos e Fontes")

with open("data/pontos_memoria.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

documentos = DATA["documentos_gerais"]
pontos = DATA["pontos"]

TIPOS = {
    "dossie": "Dossiê",
    "legislacao": "Legislação",
    "plano": "Plano de Salvaguarda",
    "base_dados": "Base de Dados",
    "livro": "Livro/Publicação"
}

layout = dbc.Container([
    html.H2("Documentos e Fontes de Pesquisa", 
            className="mb-2", style={"color": "#1B3A5C", "fontFamily": "Merriweather"}),
    html.P("Legislação, dossiês, planos de salvaguarda e bases de dados.", 
           className="text-muted mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="filtro-tipo",
                options=[{"label": v, "value": k} for k, v in TIPOS.items()],
                placeholder="Filtrar por tipo...",
                multi=True,
                className="mb-3",
                style={"color": "#000"}
            )
        ], width=12, lg=3),
        dbc.Col([
            dcc.Dropdown(
                id="filtro-doc-ponto",
                options=[{"label": p["nome"], "value": p["id"]} for p in pontos if p.get("documentos")],
                placeholder="Filtrar por ponto...",
                className="mb-3",
                style={"color": "#000"}
            )
        ], width=12, lg=3)
    ]),

    html.Div(id="lista-documentos"),

    html.Hr(style={"borderColor": "#1B3A5C", "margin": "3rem 0"}),

    html.H4("Links Úteis", className="mb-3", style={"color": "#1B3A5C"}),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("IPHAN - Patrimônio de Matriz Africana", className="card-title"),
                    html.P("Publicações e dossiês do IPHAN.", className="card-text small"),
                    html.A("Acessar →", href="https://www.gov.br/iphan/pt-br/assuntos/publicacoes-patrimonio-de-matriz-africana", 
                           target="_blank", className="btn btn-outline-secondary btn-sm", style={"color": "#1B3A5C", "borderColor": "#1B3A5C"})
                ])
            ], style={"backgroundColor": "#F7F8FA", "border": "1px solid #D9DEE4"}, className="mb-3")
        ], width=12, md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("INCRA - Territórios Quilombolas", className="card-title"),
                    html.P("Dados espaciais sobre territórios quilombolas.", className="card-text small"),
                    html.A("Acessar →", href="https://acervofundiario.incra.gov.br/", 
                           target="_blank", className="btn btn-outline-secondary btn-sm", style={"color": "#1B3A5C", "borderColor": "#1B3A5C"})
                ])
            ], style={"backgroundColor": "#F7F8FA", "border": "1px solid #D9DEE4"}, className="mb-3")
        ], width=12, md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Slave Voyages Database", className="card-title"),
                    html.P("Base de dados sobre o tráfico transatlântico.", className="card-text small"),
                    html.A("Acessar →", href="https://www.slavevoyages.org/", 
                           target="_blank", className="btn btn-outline-secondary btn-sm", style={"color": "#1B3A5C", "borderColor": "#1B3A5C"})
                ])
            ], style={"backgroundColor": "#F7F8FA", "border": "1px solid #D9DEE4"}, className="mb-3")
        ], width=12, md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Fundação Cultural Palmares", className="card-title"),
                    html.P("Certificação e políticas para comunidades quilombolas.", className="card-text small"),
                    html.A("Acessar →", href="https://www.palmares.gov.br/", 
                           target="_blank", className="btn btn-outline-secondary btn-sm", style={"color": "#1B3A5C", "borderColor": "#1B3A5C"})
                ])
            ], style={"backgroundColor": "#F7F8FA", "border": "1px solid #D9DEE4"}, className="mb-3")
        ], width=12, md=6),
    ])
], fluid=True)

@callback(
    Output("lista-documentos", "children"),
    Input("filtro-tipo", "value"),
    Input("filtro-doc-ponto", "value")
)
def update_docs(tipos, ponto_id):
    docs = documentos.copy()

    if tipos:
        docs = [d for d in docs if d["tipo"] in tipos]

    if ponto_id:
        ponto = next((p for p in pontos if p["id"] == ponto_id), None)
        if ponto and ponto.get("documentos"):
            docs_ponto = [{
                "titulo": d,
                "autor": "Documento do ponto",
                "ano": "",
                "tipo": "documento_ponto",
                "url": "#",
                "descricao": f"Documento relacionado a {ponto['nome']}"
            } for d in ponto["documentos"]]
            docs = docs_ponto + docs

    if not docs:
        return html.P("Nenhum documento encontrado.", className="text-muted")

    return dbc.Accordion([
        dbc.AccordionItem([
            html.P(d.get("descricao", ""), className="text-muted small"),
            html.P([html.Strong("Autor: "), d.get("autor", "Desconhecido")], className="small"),
            html.P([html.Strong("Ano: "), d.get("ano", "N/D")], className="small"),
            html.A("Acessar documento", href=d.get("url", "#"), target="_blank", 
                   className="btn btn-outline-secondary btn-sm mt-2",
                   style={"color": "#1B3A5C", "borderColor": "#1B3A5C"})
        ], title=f"{TIPOS.get(d['tipo'], 'Documento')} — {d['titulo']}", 
        style={"backgroundColor": "#F7F8FA", "color": "#2B2B2B"})
        for d in docs
    ], start_collapsed=True, style={"backgroundColor": "#F7F8FA"})
