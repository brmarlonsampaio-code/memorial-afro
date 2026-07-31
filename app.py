from dash import Dash, html, dcc, Input, Output, page_container
import dash_bootstrap_components as dbc

app = Dash(
    __name__,
    title="Memória Afro-Brasileira",
    use_pages=True,
    update_title="Carregando...",
    external_stylesheets=[
        dbc.themes.LITERA,
        "https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700&family=Open+Sans:wght@400;600&display=swap"
    ],
    suppress_callback_exceptions=True,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
)

navbar = dbc.Navbar(
    dbc.Container([
        html.A(
            dbc.Row([
                dbc.Col(html.I(className="fa-solid fa-globe-africa", style={"fontSize": "1.3rem", "color": "#1B3A5C"})),
                dbc.Col(dbc.NavbarBrand("Memória Afro-Brasileira", className="ms-2", 
                         style={"fontFamily": "Merriweather", "fontWeight": "700", "color": "#2B2B2B"})),
            ], align="center", className="g-0"),
            href="/",
            style={"textDecoration": "none"}
        ),
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Mapa", href="/mapa", style={"color": "#1B3A5C", "fontWeight": "600"})),
            dbc.NavItem(dbc.NavLink("Galeria", href="/galeria", style={"color": "#1B3A5C", "fontWeight": "600"})),
            dbc.NavItem(dbc.NavLink("Documentos", href="/documentos", style={"color": "#1B3A5C", "fontWeight": "600"})),
            dbc.NavItem(dbc.NavLink("Sobre", href="/sobre", style={"color": "#1B3A5C", "fontWeight": "600"})),
        ], className="ms-auto", navbar=True)
    ], fluid=True),
    color="#FFFFFF",
    dark=False,
    className="mb-4",
    style={"borderBottom": "1px solid #1B3A5C"}
)

app.layout = dbc.Container([
    dcc.Location(id="url"),
    navbar,
    html.Div(page_container, className="mt-3 pb-5")
], fluid=True, style={"minHeight": "100vh", "backgroundColor": "#FFFFFF"})

server = app.server

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=1000)
