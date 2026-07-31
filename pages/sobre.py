import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/sobre", title="Sobre")

layout = dbc.Container([
    html.H2("Sobre o Projeto", className="mb-4", style={"color": "#1B3A5C", "fontFamily": "Merriweather"}),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Memória Afro-Brasileira", className="card-title", style={"color": "#1B3A5C"}),
                    html.P([
                        "Este projeto é uma plataforma digital de mapeamento e documentação do ",
                        html.Strong("patrimônio cultural, histórico e arqueológico"),
                        " de matriz africana no Brasil."
                    ]),
                    html.P([
                        "A plataforma reúne dados de fontes oficiais como ",
                        html.A("IPHAN", href="https://www.gov.br/iphan", target="_blank"),
                        ", ",
                        html.A("INCRA", href="https://www.gov.br/incra", target="_blank"),
                        ", ",
                        html.A("UNESCO", href="https://whc.unesco.org", target="_blank"),
                        " e ",
                        html.A("Slave Voyages Database", href="https://www.slavevoyages.org/", target="_blank"),
                        ", além de documentos de pesquisa, imagens e vídeos."
                    ]),
                    html.Hr(style={"borderColor": "#1B3A5C"}),
                    html.H5("Categorias Mapeadas", style={"color": "#1B3A5C"}),
                    html.Ul([
                        html.Li([html.Strong("Quilombos e Territórios"), " — Comunidades remanescentes de quilombos"]),
                        html.Li([html.Strong("Terreiros de Matriz Africana"), " — Ilês de Candomblé e lugares sagrados"]),
                        html.Li([html.Strong("Monumentos Históricos"), " — Locais de resistência cultural"]),
                        html.Li([html.Strong("Sítios Arqueológicos"), " — Cais do Valongo, navios negreiros"]),
                        html.Li([html.Strong("Bens Culturais Imateriais"), " — Capoeira, Samba, Maracatu, Jongo"]),
                        html.Li([html.Strong("Portos de Desembarque"), " — Principais portos do tráfico transatlântico"]),
                        html.Li([html.Strong("Memoriais"), " — Cemitérios e espaços de memória"]),
                    ]),
                    html.Hr(style={"borderColor": "#1B3A5C"}),
                    html.H5("Tecnologias", style={"color": "#1B3A5C"}),
                    html.P("Desenvolvido com Python, Dash, Plotly, Bootstrap e dados abertos governamentais."),
                ])
            ], style={"backgroundColor": "#F7F8FA", "border": "1px solid #D9DEE4"})
        ], width=12, lg=8),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Estatísticas", style={"color": "#1B3A5C"}),
                    html.Hr(style={"borderColor": "#1B3A5C"}),
                    html.Div([
                        html.H3("15+", className="text-center", style={"color": "#1B3A5C"}),
                        html.P("Pontos mapeados", className="text-center text-muted")
                    ], className="mb-3"),
                    html.Div([
                        html.H3("7", className="text-center", style={"color": "#1B3A5C"}),
                        html.P("Categorias", className="text-center text-muted")
                    ], className="mb-3"),
                    html.Div([
                        html.H3("10+", className="text-center", style={"color": "#1B3A5C"}),
                        html.P("Documentos catalogados", className="text-center text-muted")
                    ], className="mb-3"),
                    html.Hr(style={"borderColor": "#1B3A5C"}),
                    html.H6("Contribua", style={"color": "#1B3A5C"}),
                    html.P("Envie sugestões de novos pontos via GitHub Issues.", className="small text-muted")
                ])
            ], style={"backgroundColor": "#F7F8FA", "border": "1px solid #D9DEE4"})
        ], width=12, lg=4)
    ])
], fluid=True)
