import dash
from dash import html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import json
import pandas as pd

dash.register_page(__name__, path="/mapa", title="Mapa de Memória")

with open("data/pontos_memoria.json", "r", encoding="utf-8") as f:
    DATA = json.load(f)

df = pd.DataFrame(DATA["pontos"])
categorias = DATA["categorias"]

layout = dbc.Container([
    html.H2("Mapa da Memória Afro-Brasileira", 
            className="mb-2", style={"color": "#1B3A5C", "fontFamily": "Merriweather"}),
    html.P("Explore os pontos de memória, patrimônio e resistência negra no Brasil.", 
           className="text-muted mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filtros", className="card-title", style={"color": "#1B3A5C"}),

                    html.Label("Categoria", className="fw-bold", style={"color": "#1B3A5C"}),
                    dcc.Dropdown(
                        id="filtro-categoria",
                        options=[{"label": v["label"], "value": k} for k, v in categorias.items()],
                        placeholder="Todas as categorias",
                        multi=True,
                        className="mb-3",
                        style={"color": "#000"}
                    ),

                    html.Label("Estado (UF)", className="fw-bold", style={"color": "#1B3A5C"}),
                    dcc.Dropdown(
                        id="filtro-uf",
                        options=[{"label": uf, "value": uf} for uf in sorted(df["uf"].unique())],
                        placeholder="Todos os estados",
                        multi=True,
                        className="mb-3",
                        style={"color": "#000"}
                    ),

                    html.Hr(style={"borderColor": "#1B3A5C"}),

                    html.H6("Legenda", style={"color": "#1B3A5C"}),
                    html.Div([
                        html.Div([
                            html.Span("⬤", style={"color": v["cor"], "marginRight": "8px", "fontSize": "1.2rem"}),
                            html.Span(v["label"], className="small", style={"color": "#2B2B2B"})
                        ], className="mb-1") for k, v in categorias.items()
                    ]),

                    html.Hr(style={"borderColor": "#1B3A5C"}),

                    html.P("Clique em um ponto no mapa para ver detalhes, fotos, vídeos e documentos.",
                           className="text-muted text-center small")
                ])
            ], style={"backgroundColor": "#F7F8FA", "border": "1px solid #D9DEE4"})
        ], width=12, lg=3, className="mb-4"),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-mapa",
                        type="circle",
                        color="#1B3A5C",
                        children=dcc.Graph(
                            id="mapa-memoria",
                            config={"displayModeBar": True, "scrollZoom": True},
                            style={"height": "75vh"}
                        )
                    )
                ])
            ], style={"backgroundColor": "#F7F8FA", "border": "1px solid #D9DEE4"})
        ], width=12, lg=9)
    ]),

    dbc.Offcanvas(
        id="painel-detalhes",
        title=html.Span("Detalhes do ponto", style={"color": "#1B3A5C", "fontFamily": "Merriweather"}),
        placement="end",
        is_open=False,
        scrollable=True,
        style={"backgroundColor": "#F7F8FA", "borderLeft": "2px solid #1B3A5C", "width": "420px"},
        children=[]
    ),

    html.Div(id="rodape-mapa", className="mt-4")
], fluid=True)

def linha_estatisticas(total_p, total_c, total_e):
    def card(texto):
        return dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(texto, className="text-center", style={"color": "#1B3A5C"})
                ])
            ], style={"backgroundColor": "#F7F8FA", "border": "1px solid #D9DEE4"})
        ], width=4)

    return dbc.Row([card(total_p), card(total_c), card(total_e)])

def linha_midia(ponto):
    imagem_col = dbc.Col([
        dbc.Card([
            dbc.CardImg(src=ponto["imagem"], top=True, style={"maxHeight": "320px", "objectFit": "cover"})
            if ponto.get("imagem") else
            dbc.CardBody(html.P("Sem foto cadastrada para este ponto.", className="text-muted text-center mb-0"))
        ], style={"backgroundColor": "#F7F8FA", "border": "1px solid #D9DEE4", "height": "100%"})
    ], width=12, lg=6, className="mb-3 mb-lg-0")

    documentos = ponto.get("documentos") or []
    links = ponto.get("links") or []

    if documentos or links:
        conteudo_docs = []
        if documentos:
            conteudo_docs.append(html.Ul([html.Li(doc, className="small") for doc in documentos]))
        if links:
            conteudo_docs.append(html.Ul([
                html.Li(html.A(link["titulo"], href=link["url"], target="_blank"), className="small")
                for link in links
            ]))
    else:
        conteudo_docs = [html.P("Nenhum documento cadastrado para este ponto.", className="text-muted mb-0")]

    documentos_col = dbc.Col([
        dbc.Card([
            dbc.CardBody([
                html.H5(ponto["nome"], style={"color": "#1B3A5C", "fontFamily": "Merriweather"}),
                html.P(f"{ponto['cidade']}, {ponto['uf']}", className="text-muted small mb-3"),
                html.H6("Documentos e fontes", style={"color": "#1B3A5C"}),
                *conteudo_docs
            ])
        ], style={"backgroundColor": "#F7F8FA", "border": "1px solid #D9DEE4", "height": "100%"})
    ], width=12, lg=6)

    return dbc.Row([imagem_col, documentos_col])

@callback(
    Output("mapa-memoria", "figure"),
    Output("painel-detalhes", "children"),
    Output("painel-detalhes", "is_open"),
    Output("painel-detalhes", "title"),
    Output("rodape-mapa", "children"),
    Input("filtro-categoria", "value"),
    Input("filtro-uf", "value"),
    Input("mapa-memoria", "clickData")
)
def update_mapa(cats, ufs, click_data):
    dff = df.copy()
    if cats:
        dff = dff[dff["categoria"].isin(cats)]
    if ufs:
        dff = dff[dff["uf"].isin(ufs)]

    painel_titulo = html.Span("Detalhes do ponto", style={"color": "#1B3A5C", "fontFamily": "Merriweather"})

    if dff.empty:
        fig = go.Figure()
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_center={"lat": -14.2, "lon": -51.9},
            mapbox_zoom=3,
            paper_bgcolor="#FFFFFF",
            plot_bgcolor="#FFFFFF",
            font_color="#2B2B2B",
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        return fig, [], False, painel_titulo, linha_estatisticas("0 pontos", "0 categorias", "0 estados")

    dff["cor"] = dff["categoria"].apply(lambda x: categorias.get(x, {}).get("cor", "#1B3A5C"))

    fig = px.scatter_mapbox(
        dff,
        lat="lat",
        lon="lon",
        color="categoria_label",
        color_discrete_map={v["label"]: v["cor"] for k, v in categorias.items()},
        hover_name="nome",
        hover_data={"cidade": True, "uf": True, "periodo": True, "lat": False, "lon": False, "cor": False},
        zoom=3.5,
        center={"lat": -14.2, "lon": -51.9},
        height=700
    )

    fig.update_layout(
        mapbox_style="open-street-map",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font_color="#2B2B2B",
        showlegend=False,
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    painel_children = []
    painel_open = False
    ponto_clicado = None

    triggered_id = dash.callback_context.triggered[0]["prop_id"].split(".")[0] if dash.callback_context.triggered else None

    if click_data and triggered_id == "mapa-memoria":
        ponto_nome = click_data["points"][0]["hovertext"]
        pontos_encontrados = dff[dff["nome"] == ponto_nome]

        if not pontos_encontrados.empty:
            ponto = pontos_encontrados.iloc[0]
            ponto_clicado = ponto
            painel_titulo = html.Span(ponto["nome"], style={"color": "#1B3A5C", "fontFamily": "Merriweather"})
            painel_open = True

            blocos = [
                html.P([html.Strong("Categoria: "),
                        html.Span(ponto["categoria_label"], style={"color": ponto["cor"]})]),
                html.P([html.Strong("Local: "), f"{ponto['cidade']}, {ponto['uf']}"]),
                html.P([html.Strong("Período: "), ponto["periodo"]]),
                html.P(ponto["descricao"]),
            ]

            if ponto.get("imagem"):
                blocos.append(
                    html.Img(src=ponto["imagem"], className="img-fluid rounded mb-3",
                              style={"width": "100%", "border": "1px solid #D9DEE4"})
                )

            if ponto.get("video"):
                blocos.append(
                    html.Div(
                        html.Iframe(
                            src=ponto["video"],
                            style={"width": "100%", "height": "220px", "border": "none"},
                            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                        ),
                        className="mb-3"
                    )
                )

            blocos.append(html.Hr(style={"borderColor": "#1B3A5C"}))
            blocos.append(html.P([html.Strong("Fontes: "), ", ".join(ponto["fontes"])], className="small text-muted"))

            documentos = ponto.get("documentos") or []
            if len(documentos) > 0:
                blocos.append(html.H6("Documentos", className="mt-3", style={"color": "#1B3A5C"}))
                blocos.append(html.Ul([html.Li(doc, className="small") for doc in documentos]))

            links = ponto.get("links") or []
            if len(links) > 0:
                blocos.append(html.H6("Links", className="mt-3", style={"color": "#1B3A5C"}))
                blocos.append(html.Ul([
                    html.Li(html.A(link["titulo"], href=link["url"], target="_blank"), className="small")
                    for link in links
                ]))

            painel_children = blocos

    total_p = f"{len(dff)} ponto{'s' if len(dff) > 1 else ''}"
    total_c = f"{dff['categoria'].nunique()} categoria{'s' if dff['categoria'].nunique() > 1 else ''}"
    total_e = f"{dff['uf'].nunique()} estado{'s' if dff['uf'].nunique() > 1 else ''}"

    if ponto_clicado is not None:
        rodape = linha_midia(ponto_clicado)
    else:
        rodape = linha_estatisticas(total_p, total_c, total_e)

    return fig, painel_children, painel_open, painel_titulo, rodape
