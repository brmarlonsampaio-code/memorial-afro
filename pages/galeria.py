import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import json

dash.register_page(__name__, path="/galeria", title="Galeria de Mídia")

with open("data/pontos_memoria.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

pontos = DATA["pontos"]

layout = dbc.Container([
    html.H2("🎞️ Galeria de Memória", 
            className="mb-2", style={"color": "#D4AF37", "fontFamily": "Merriweather"}),
    html.P("Imagens, vídeos e registros visuais do patrimônio afro-brasileiro.", 
           className="text-muted mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id="filtro-galeria",
                options=[{"label": p["nome"], "value": p["id"]} for p in pontos],
                placeholder="Filtrar por ponto específico...",
                className="mb-4",
                style={"color": "#000"}
            )
        ], width=12, lg=4)
    ]),

    html.Div(id="galeria-conteudo")
], fluid=True)

@callback(
    Output("galeria-conteudo", "children"),
    Input("filtro-galeria", "value")
)
def update_galeria(ponto_id):
    filtrados = [p for p in pontos if (not ponto_id or p["id"] == ponto_id)]

    cards = []
    for p in filtrados:
        if p.get("imagem"):
            cards.append(dbc.Col([
                dbc.Card([
                    dbc.CardImg(src=p["imagem"], top=True, style={"height": "250px", "objectFit": "cover"}),
                    dbc.CardBody([
                        html.H5(p["nome"], className="card-title", style={"color": "#D4AF37"}),
                        html.P(p["categoria_label"], className="card-text small text-muted"),
                        html.P(f"{p['cidade']}, {p['uf']}", className="card-text small")
                    ])
                ], style={"backgroundColor": "#1a1a2e", "border": "1px solid #D4AF37", "height": "100%"})
            ], width=12, md=6, lg=4, className="mb-4"))

        if p.get("video"):
            cards.append(dbc.Col([
                dbc.Card([
                    html.Div([
                        html.Iframe(
                            src=p["video"],
                            style={"width": "100%", "height": "250px", "border": "none"}
                        )
                    ]),
                    dbc.CardBody([
                        html.H5(f"📹 {p['nome']}", className="card-title", style={"color": "#D4AF37"}),
                        html.P("Registro em vídeo", className="card-text small text-muted")
                    ])
                ], style={"backgroundColor": "#1a1a2e", "border": "1px solid #D4AF37", "height": "100%"})
            ], width=12, md=6, lg=4, className="mb-4"))

    if not cards:
        return html.Div([
            html.H4("Nenhuma mídia disponível", className="text-center text-muted mt-5"),
            html.P("Selecione outro filtro.", className="text-center text-muted")
        ])

    return dbc.Row(cards)
