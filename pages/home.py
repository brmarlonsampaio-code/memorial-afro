import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", title="Memória Afro-Brasileira")

def secao_card(icone, titulo, descricao, href):
    return dbc.Col([
        dbc.Card(
            dbc.CardBody([
                html.Div(icone, style={"fontSize": "2rem"}, className="mb-2"),
                html.H5(titulo, style={"color": "#D4AF37", "fontFamily": "Merriweather"}),
                html.P(descricao, className="text-muted small"),
                dbc.Button("Acessar", href=href, color="warning", outline=True, size="sm")
            ]),
            style={"backgroundColor": "#1a1a2e", "border": "1px solid #D4AF37", "height": "100%"}
        )
    ], width=12, sm=6, lg=3, className="mb-4")

layout = dbc.Container([
    html.Div([
        html.H1("🌍 Memória Afro-Brasileira",
                className="mb-3",
                style={"color": "#D4AF37", "fontFamily": "Merriweather", "fontWeight": "700"}),
        html.P(
            "Uma plataforma digital de mapeamento e documentação do patrimônio cultural, "
            "histórico e arqueológico de matriz africana no Brasil.",
            className="text-light mb-4",
            style={"maxWidth": "700px", "fontSize": "1.1rem"}
        ),
    ], className="text-center py-5"),

    dbc.Row([
        secao_card("🗺️", "Mapa", "Explore os pontos de memória, patrimônio e resistência negra em todo o país.", "/mapa"),
        secao_card("🎞️", "Galeria", "Imagens e vídeos documentando lugares e manifestações culturais.", "/galeria"),
        secao_card("📚", "Documentos", "Fontes, registros e materiais de pesquisa catalogados.", "/documentos"),
        secao_card("ℹ️", "Sobre", "Conheça o projeto, suas fontes e metodologia.", "/sobre"),
    ], className="justify-content-center")
], fluid=True)
