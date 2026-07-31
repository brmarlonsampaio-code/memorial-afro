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
    html.H2("🗺️ Mapa da Memória Afro-Brasileira", 
            className="mb-2", style={"color": "#D4AF37", "fontFamily": "Merriweather"}),
    html.P("Explore os pontos de memória, patrimônio e resistência negra no Brasil.", 
           className="text-muted mb-4"),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Filtros", className="card-title", style={"color": "#D4AF37"}),

                    html.Label("Categoria", className="fw-bold text-light"),
                    dcc.Dropdown(
                        id="filtro-categoria",
                        options=[{"label": v["label"], "value": k} for k, v in categorias.items()],
                        placeholder="Todas as categorias",
                        multi=True,
                        className="mb-3",
                        style={"color": "#000"}
                    ),

                    html.Label("Estado (UF)", className="fw-bold text-light"),
                    dcc.Dropdown(
                        id="filtro-uf",
                        options=[{"label": uf, "value": uf} for uf in sorted(df["uf"].unique())],
                        placeholder="Todos os estados",
                        multi=True,
                        className="mb-3",
                        style={"color": "#000"}
                    ),

                    html.Hr(style={"borderColor": "#D4AF37"}),

                    html.H6("Legenda", className="text-light"),
                    html.Div([
                        html.Div([
                            html.Span("⬤", style={"color": v["cor"], "marginRight": "8px", "fontSize": "1.2rem"}),
                            html.Span(v["label"], className="text-light small")
                        ], className="mb-1") for k, v in categorias.items()
                    ]),

                    html.Hr(style={"borderColor": "#D4AF37"}),

                    html.Div(id="info-ponto", children=[
                        html.P("Clique em um ponto no mapa para ver detalhes.", 
                               className="text-muted text-center")
                    ])
                ])
            ], style={"backgroundColor": "#1a1a2e", "border": "1px solid #D4AF37"})
        ], width=12, lg=3, className="mb-4"),

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Loading(
                        id="loading-mapa",
                        type="circle",
                        color="#D4AF37",
                        children=dcc.Graph(
                            id="mapa-memoria",
                            config={"displayModeBar": True, "scrollZoom": True},
                            style={"height": "75vh"}
                        )
                    )
                ])
            ], style={"backgroundColor": "#1a1a2e", "border": "1px solid #D4AF37"})
        ], width=12, lg=9)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="total-pontos", className="text-center", style={"color": "#D4AF37"})
                ])
            ], style={"backgroundColor": "#1a1a2e", "border": "1px solid #D4AF37"})
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="total-categorias", className="text-center", style={"color": "#D4AF37"})
                ])
            ], style={"backgroundColor": "#1a1a2e", "border": "1px solid #D4AF37"})
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(id="total-estados", className="text-center", style={"color": "#D4AF37"})
                ])
            ], style={"backgroundColor": "#1a1a2e", "border": "1px solid #D4AF37"})
        ], width=4),
    ], className="mt-4")
], fluid=True)

@callback(
    Output("mapa-memoria", "figure"),
    Output("info-ponto", "children"),
    Output("total-pontos", "children"),
    Output("total-categorias", "children"),
    Output("total-estados", "children"),
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

    if dff.empty:
        fig = go.Figure()
        fig.update_layout(
            mapbox_style="open-street-map",
            mapbox_center={"lat": -14.2, "lon": -51.9},
            mapbox_zoom=3,
            paper_bgcolor="#0f0f1a",
            plot_bgcolor="#0f0f1a",
            font_color="#F5F5DC",
            margin={"r":0,"t":0,"l":0,"b":0}
        )
        return fig, html.P("Nenhum ponto encontrado.", className="text-warning"), "0 pontos", "0 categorias", "0 estados"

    dff["cor"] = dff["categoria"].apply(lambda x: categorias.get(x, {}).get("cor", "#D4AF37"))

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
        paper_bgcolor="#0f0f1a",
        plot_bgcolor="#0f0f1a",
        font_color="#F5F5DC",
        legend=dict(
            bgcolor="rgba(26,26,46,0.9)",
            bordercolor="#D4AF37",
            borderwidth=1,
            font=dict(color="#F5F5DC")
        ),
        margin={"r":0,"t":0,"l":0,"b":0}
    )

    info = html.Div([
        html.P("Clique em um ponto no mapa para ver detalhes.", className="text-muted text-center")
    ])

    if click_data:
        ponto_nome = click_data["points"][0]["hovertext"]
        ponto = dff[dff["nome"] == ponto_nome].iloc[0]

        info = html.Div([
            html.H5(ponto["nome"], style={"color": "#D4AF37"}),
            html.P([html.Strong("Categoria: "), 
                    html.Span(ponto["categoria_label"], style={"color": ponto["cor"]})]),
            html.P([html.Strong("Local: "), f"{ponto['cidade']}, {ponto['uf']}"]),
            html.P([html.Strong("Período: "), ponto["periodo"]]),
            html.P(ponto["descricao"], className="small"),
            html.Hr(style={"borderColor": "#D4AF37"}),
            html.P([html.Strong("Fontes: "), ", ".join(ponto["fontes"])], className="small text-muted"),
        ])

    total_p = f"{len(dff)} ponto{'s' if len(dff) > 1 else ''}"
    total_c = f"{dff['categoria'].nunique()} categoria{'s' if dff['categoria'].nunique() > 1 else ''}"
    total_e = f"{dff['uf'].nunique()} estado{'s' if dff['uf'].nunique() > 1 else ''}"

    return fig, info, total_p, total_c, total_e
