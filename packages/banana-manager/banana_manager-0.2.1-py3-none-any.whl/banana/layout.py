from dash import dcc, html
from dash_ag_grid import AgGrid


layout = html.Div(
    [
        dcc.Location(id="banana--location"),
        html.Div(id="banana--menu", className="left-section"),
        html.Div(
            html.Div(
                [
                    html.H1(id="banana--table-title", className="table-title"),
                    AgGrid(
                        id="banana--table",
                        defaultColDef={
                            "filter": True,
                            "sortable": True,
                            "editable": True,
                        },
                        dashGridOptions={"pagination": True},
                        style={"height": "calc(100vh - 85px)", "overflow": "auto"},
                    ),
                ],
                className="content",
            ),
            className="right-section",
        ),
    ],
    className="container",
)
