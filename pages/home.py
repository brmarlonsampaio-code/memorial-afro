import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/", title="Memória Afro-Brasileira")

def secao_card(icone_classe, titulo, descricao, href):
    return dbc.Col([
        dbc.Card(
            dbc.CardBody([
                html.I(className=f"{icone_classe} mb-2", style={"fontSize": "1.6rem", "color": "#1B3A5C"}),
                html.H5(titulo, style={"color": "#1B3A5C", "fontFamily": "Merriweather"}),
                html.P(descricao, className="text-muted small"),
                dbc.Button("Acessar", href=href, outline=True, size="sm",
                           style={"color": "#1B3A5C", "borderColor": "#1B3A5C"})
            ]),
            style={"backgroundColor": "#F7F8FA", "border": "1px solid #D9DEE4", "height": "100%"}
        )
    ], width=12, sm=6, lg=3, className="mb-4")

layout = dbc.Container([
    html.Div([
        html.H1("Memória Afro-Brasileira",
                className="mb-3",
                style={"color": "#1B3A5C", "fontFamily": "Merriweather", "fontWeight": "700"}),
        html.P(
            "Uma plataforma digital de mapeamento e documentação do patrimônio cultural, "
            "histórico e arqueológico de matriz africana no Brasil.",
            className="mb-4",
            style={"maxWidth": "700px", "fontSize": "1.1rem", "color": "#2B2B2B", "margin": "0 auto"}
        ),
    ], className="text-center py-5"),

    dbc.Row([
        secao_card("fa-solid fa-map-location-dot", "Mapa", "Explore os pontos de memória, patrimônio e resistência negra em todo o país.", "/mapa"),
        secao_card("fa-solid fa-photo-film", "Galeria", "Imagens e vídeos documentando lugares e manifestações culturais.", "/galeria"),
        secao_card("fa-solid fa-book", "Documentos", "Fontes, registros e materiais de pesquisa catalogados.", "/documentos"),
        secao_card("fa-solid fa-circle-info", "Sobre", "Conheça o projeto, suas fontes e metodologia.", "/sobre"),
    ], className="justify-content-center")
], fluid=True)
