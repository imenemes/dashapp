import plotly.express as px
from dash.dependencies import Output, Input

from wordcloud import WordCloud
import base64
from io import BytesIO

from dashcard import *




# Layout section: Bootstrap (https://hackerthemes.com/bootstrap-cheatsheet/)
# ************************************************************************
app.layout = dbc.Container([

    dbc.Row([
        dbc.Col([card_titre], xs=12, sm=12, md=12, lg=12, xl=12),
        dbc.Col([card_graphique], xs=12, sm=12, md=12, lg=12, xl=12),
        dbc.Col([card_pie], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([card_hist], xs=12, sm=12, md=12, lg=6, xl=6),
        dbc.Col([card_img], xs=12, sm=12, md=12, lg=12, xl=12),
    ], align='center'),
])


# Callback section: connecting the components
# ************************************************************************
# Line chart - Single

@app.callback(
    Output('line-fig2', 'figure'),
    Input('my-dpdn2', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['nom_type'].isin(stock_slctd)]
    figln2 = px.pie(dff, names='nom_type', hole=.5)
    return figln2


# Histogram
@app.callback(
    Output('my-hist', 'figure'),
    Input('my-checklist', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['mot'].isin(stock_slctd)]
    fighist = px.histogram(dff, x='mot')
    return fighist


@app.callback(
    Output('line', 'figure'),
    Input('menu', 'value')
)
def update_graph(stock_slctd):
    dff = df[df['nom_type'].isin(stock_slctd)]
    dfm = dff.groupby(['nom_type', 'date']).size().reset_index(name='count')
    figln2 = px.line(dfm, x='date', y='count', color='nom_type')
    return figln2


@app.callback(
    dash.dependencies.Output('output-container-date-picker-range', 'children'),
    [dash.dependencies.Input('my-date-picker-range', 'start_date'),
     dash.dependencies.Input('my-date-picker-range', 'end_date')])

def update_output(start_date, end_date):
    string_prefix = 'vous avez choisi: '
    if start_date is not None:
        start_date_object = date.fromisoformat(start_date)
        start_date_string = start_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'début de période: ' + start_date_string + ' | '
    if end_date is not None:
        end_date_object = date.fromisoformat(end_date)
        end_date_string = end_date_object.strftime('%B %d, %Y')
        string_prefix = string_prefix + 'fin de période: ' + end_date_string
    if len(string_prefix) == len('vous avez choisi: '):
        return 'choisissez une date'
    else:
        return string_prefix

def plot_wordcloud(data):
    d = {mot: n
        for mot in data['mot']
        for n in data['haineux']}
    wc = WordCloud(background_color='black', width=800, height=380)
    wc.fit_words(d)
    return wc.to_image()

@app.callback(
    Output('image_wc', 'src'),
    Input('image_wc', 'id'))
def make_image(b):
    dfm = df.groupby('mot').count().reset_index()
    dfm = dfm[['mot','haineux']]
    img = BytesIO()
    plot_wordcloud(data=dfm).save(img, format='PNG')
    return 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())


if __name__ == '__main__':
    app.run_server(debug=True, port=3500)
