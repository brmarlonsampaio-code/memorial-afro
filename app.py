from dash import Dash, html, dcc, Input, Output, page_container
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    title="Memória Afro-Brasileira",
    use_pages=True,
    update_title="Carregando...",
    external_stylesheets=[
        dbc.themes.DARKLY,
        "https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Open+Sans:wght@400;600&display=swap"
    ],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

navbar = dbc.Navbar(
    dbc.Container([
        html.A(
            dbc.Row([
                dbc.Col(html.Span("🌍", style={"fontSize": "1.5rem"})),
                dbc.Col(dbc.NavbarBrand("Memória Afro-Brasileira", className="ms-2", 
                         style={"fontFamily": "Merriweather", "fontWeight": "700", "color": "#F5F5DC"})),
            ], align="center", className="g-0"),
            href="/",
            style={"textDecoration": "none"}
        ),
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("🗺️ Mapa", href="/mapa")),
            dbc.NavItem(dbc.NavLink("🎞️ Galeria", href="/galeria")),
            dbc.NavItem(dbc.NavLink("📚 Documentos", href="/documentos")),
            dbc.NavItem(dbc.NavLink("ℹ️ Sobre", href="/sobre")),
        ], className="ms-auto", navbar=True)
    ], fluid=True),
    color="#1a1a2e",
    dark=True,
    className="mb-4 shadow",
    style={"borderBottom": "3px solid #D4AF37"}
)

app.layout = dbc.Container([
    dcc.Location(id="url"),
    navbar,
    html.Div(page_container, className="mt-3 pb-5")
], fluid=True, style={"minHeight": "100vh", "backgroundColor": "#0f0f1a"})

server = app.server

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1000)
