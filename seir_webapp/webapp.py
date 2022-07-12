from scipy.integrate import odeint
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output

colors={
    'TEXTCOLOR':'#b3d9ff',
    'BGCOLOR':'#000d1a'
}

app=Dash(__name__, title="SEIR Model", assets_folder="assets", external_stylesheets=[dbc.themes.SUPERHERO])

app.layout=html.Div(style={'padding':30},children=[
    html.Div([
        html.H1("SEIR MODEL", style={'text-align':'center'}),
        html.P([
            "This is simple simulation of epidemic based on SEIR model."
        ],style={'text-align':'center'})
    ], style={'color':colors['TEXTCOLOR']}),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H4("Clinical parameters", style={'text-align':'center'}),
                    html.Label("Duration of incubation period"),
                    dcc.Slider(id='incub_period',min=0, max=20, step=0.5, value=5, updatemode='drag', tooltip={'placement':'bottom','always_visible':False}, 
                        marks={
                                0:{'label':'0\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                5:{'label':'5\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                10:{'label':'10\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                15:{'label':'15\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                20:{'label':'20 days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}}
                        }),
                    html.Br(),
                    html.Label("Duration of mild infections"),
                    dcc.Slider(id='dur_mild_inf',min=0, max=20, step=1, value=6, updatemode='drag', tooltip={'placement':'bottom','always_visible':False}, 
                        marks={
                                0:{'label':'0\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                5:{'label':'5\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                10:{'label':'10\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                15:{'label':'15\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                20:{'label':'20 days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}}
                        }),
                    html.Br(),
                    html.Label("Percent of severe infections"),
                    dcc.Slider(id='frac_severe_inf',min=0, max=100, step=1, value=15, updatemode='drag', tooltip={'placement':'bottom','always_visible':False}, 
                        marks={
                                0:{'label':'0%','style':{'color':colors['TEXTCOLOR']}},
                                25:{'label':'25%','style':{'color':colors['TEXTCOLOR']}},
                                50:{'label':'50%','style':{'color':colors['TEXTCOLOR']}},
                                75:{'label':'75%','style':{'color':colors['TEXTCOLOR']}},
                                100:{'label':'100%','style':{'color':colors['TEXTCOLOR']}}
                        }),
                    html.Br(),
                    html.Label("Duration of severe infections"),
                    dcc.Slider(id='dur_severe_inf',min=0, max=10, step=1, value=6, updatemode='drag', tooltip={'placement':'bottom','always_visible':False}, 
                        marks={
                                0:{'label':'0\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                5:{'label':'5\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                10:{'label':'10 days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                        }),
                    html.Br(),
                    html.Label("Percent of critical infections"),
                    dcc.Slider(id='frac_crit_inf',min=0, max=100, step=1, value=5, updatemode='drag', tooltip={'placement':'bottom','always_visible':False}, 
                        marks={
                                0:{'label':'0%','style':{'color':colors['TEXTCOLOR']}},
                                25:{'label':'25%','style':{'color':colors['TEXTCOLOR']}},
                                50:{'label':'50%','style':{'color':colors['TEXTCOLOR']}},
                                75:{'label':'75%','style':{'color':colors['TEXTCOLOR']}},
                                100:{'label':'100%','style':{'color':colors['TEXTCOLOR']}}
                        }),
                    html.Br(),
                    html.Label("Duration of critical infections"),
                    dcc.Slider(id='dur_crit_inf',min=0, max=30, step=1, value=8, updatemode='drag', tooltip={'placement':'bottom','always_visible':False}, 
                        marks={
                                0:{'label':'0\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                10:{'label':'10\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                20:{'label':'20\n days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}},
                                30:{'label':'30 days','style':{'color':colors['TEXTCOLOR'],'white-space':'pre-wrap'}}
                        }),
                    html.Br(),
                    html.Label("Death rate for critical infections"),
                    dcc.Slider(id='frac_death',min=0, max=100, step=1, value=40, updatemode='drag', tooltip={'placement':'bottom','always_visible':False}, 
                        marks={
                                0:{'label':'0%','style':{'color':colors['TEXTCOLOR']}},
                                25:{'label':'25%','style':{'color':colors['TEXTCOLOR']}},
                                50:{'label':'50%','style':{'color':colors['TEXTCOLOR']}},
                                75:{'label':'75%','style':{'color':colors['TEXTCOLOR']}},
                                100:{'label':'100%','style':{'color':colors['TEXTCOLOR']}}
                        }),
                ],style={'padding':20,'flex':0.5}),
                html.Div([
                    html.H4("Transmission parameters", style={'text-align':'center'}),
                    html.Label("Mild infection"),
                    dcc.Slider(id='mild_tran',min=0, max=3, step=0.01, value=0.5, updatemode='drag', tooltip={'placement':'bottom','always_visible':False}, 
                        marks={
                                0:{'label':'0/day','style':{'color':colors['TEXTCOLOR']}},
                                1:{'label':'1/day','style':{'color':colors['TEXTCOLOR']}},
                                2:{'label':'2/day','style':{'color':colors['TEXTCOLOR']}},
                                3:{'label':'3/day','style':{'color':colors['TEXTCOLOR']}}
                        }),
                    html.Br(),
                    html.Label("Severe infection"),
                    dcc.Slider(id='severe_tran',min=0, max=3, step=0.01, value=0.1, updatemode='drag', tooltip={'placement':'bottom','always_visible':False}, 
                        marks={
                                0:{'label':'0/day','style':{'color':colors['TEXTCOLOR']}},
                                1:{'label':'1/day','style':{'color':colors['TEXTCOLOR']}},
                                2:{'label':'2/day','style':{'color':colors['TEXTCOLOR']}},
                                3:{'label':'3/day','style':{'color':colors['TEXTCOLOR']}}
                        }),
                    html.Br(),
                    html.Label("Critical infection"),
                    dcc.Slider(id='crit_tran',min=0, max=3, step=0.01, value=0.1, updatemode='drag', tooltip={'placement':'bottom','always_visible':False}, 
                        marks={
                                0:{'label':'0/day','style':{'color':colors['TEXTCOLOR']}},
                                1:{'label':'1/day','style':{'color':colors['TEXTCOLOR']}},
                                2:{'label':'2/day','style':{'color':colors['TEXTCOLOR']}},
                                3:{'label':'3/day','style':{'color':colors['TEXTCOLOR']}}
                        }),
                ],style={'padding':20,'flex':0.5}),
            ],style={'display':'flex', 'flex-direction':'row'}),
            html.Div([
                html.H4("Simulation Parameters"),
                html.Div([
                    html.Div([
                        html.Label("Population size: "), 
                        dcc.Input(id='pop_size', type = "number" , value = 1000),
                    ],style={'flex':0.5, 'padding':20}),
                    html.Div([
                        html.Label("Initial infected: "),
                        dcc.Input(id='init_inf', type = "number" , value = 1),
                    ],style={'flex':0.5, 'padding':20})
                ],style={'display':'flex', 'flex_direction':'row'}),
                html.Label("Simulation duration"),
                dcc.Slider(id='sim_dur',min=0, max=150, step=1, value=100, updatemode='drag', tooltip={'placement':'bottom','always_visible':False}, 
                    marks={
                            0:{'label':'0 days','style':{'color':colors['TEXTCOLOR']}},
                            50:{'label':'50 days','style':{'color':colors['TEXTCOLOR']}},
                            100:{'label':'100 days','style':{'color':colors['TEXTCOLOR']}},
                            150:{'label':'150 days','style':{'color':colors['TEXTCOLOR']}}
                    }),
            ],style={'padding':20})
        ],style={'flex':0.35, 'backgroundColor':'#001a35', 'color':colors['TEXTCOLOR'], 'height':'100%'}),
        html.Div([
                    dcc.Tabs(id='output_tabs', 
                            value='graph',
                            parent_className='custom-tabs',
                            className='custom-tabs-container',
                            children=[
                        dcc.Tab(label='Graph',
                                value='graph',
                                className='custom-tab',
                                selected_className='custom-tab--selected',
                                children=[
                                    html.H3(["Predicted Cases"], style={'color':colors['TEXTCOLOR'],'padding-left':20,'padding-top':20,'backgroundColor':'#001a33','text-align':'left'}),
                                    html.P(["Simulate the natural course of an epidemic in a single population without any interventions."],style={'color':colors['TEXTCOLOR'],'text-align':'left','padding-left':20}),
                                    dcc.Graph(id='graph', style={'backgroundColor':'#001a33','padding':20}),
                                    html.H3(["Output parameters"], style={'color':colors['TEXTCOLOR'],'padding-left':20,'padding-top':20,'backgroundColor':'#001a33','text-align':'left'}),
                                    html.Div(id='output_table', style={'padding-left':40, 'padding-bottom':20, 'padding-top':20})
                                ], 
                                style={'backgroundColor':'#001a33'},
                                selected_style={'backgroundColor':colors['TEXTCOLOR']}),
                        dcc.Tab(label='Model',
                                value='model',
                                className='custom-tab',
                                selected_className='custom-tab--selected',
                                children=[
                                    html.H3(["Model description"],style={'color':colors['TEXTCOLOR'],'padding-left':20,'padding-top':20,'text-align':'left'}),
                                    html.Div([
                                        html.Img(src='/assets/seirdmodel.png', style={'width':'50%', 'height':'50%'}),
                                        html.P([
                                            dcc.Markdown('''Susceptible ( $$S$$ ) individuals who become infected start out in an exposed class $$E$$, 
                                            where they are asymptomatic and do not transmit infection. The rate of progressing from the exposed stage to the infected stage $$I$$,
                                            where the individual is symptomatic and infectious, occurs at rate $$a$$. The clinical descriptions of diffrent stages of infection are given below.
                                            Infected individuals begin with *mild* infection ( $$I_{1}$$ ), from which they either recover, at rate $$\gamma_{1}$$, or progress 
                                            to *severe* infection ( $$I_{2}$$ ), at rate $$p_{1}$$. Severe infection resolves at rate $$\gamma_{2}$$ or progress to *critical* stage ( $$I_{3}$$ )
                                            at rate $$p_{2}$$. Individuals with critical infection recover at rate $$\gamma_{3}$$ or die at rate $$\mu$$. Recovered individuals are tracked by class $$R$$
                                            and are assumed to be protected from re-infection for life. Individuals may transmit the infection at any stage, though with difrent rates. The transmission rate in stage $$i$$ is described by $$\\beta_{i}$$.''',mathjax=True),
                                            html.A(["Read more"], href='https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology')
                                        ],style={'color':colors['TEXTCOLOR'], 'text-align':'justify','padding':20})
                                    ]),
                                    html.H3(["Equations"],style={'color':colors['TEXTCOLOR'],'padding-left':20,'padding-top':20,'text-align':'left'}),
                                    dcc.Markdown('''
                                    $$\dot{S} = -(\\beta_{1}I_{1} - \\beta_{2}I_{2} - \\beta_{3}I_{3})S$$\n
                                    $$\dot{E} = (\\beta_{1}I_{1} + \\beta_{2}I_{2} + \\beta_{3}I_{3})S - aE$$\n
                                    $$\dot{I_{1}} = aE - (\gamma_{1} + p_{1})I_{1}$$\n
                                    $$\dot{I_{2}} = p_{1}I_{1} - (\gamma_{2} + p_{2})I_{2}$$\n
                                    $$\dot{I_{3}} = p_{2}I_{2} - (\gamma_{3} + \mu)I_{3}$$\n
                                    $$\dot{R} = \gamma_{1}I_{1} + \gamma_{2}I_{2} + \gamma_{3}I_{3}$$\n
                                    $$\dot{D} = \mu I_{3}
                                    ''',mathjax=True, style={'color':colors['TEXTCOLOR']}),
                                    html.H3(["Variables"],style={'color':colors['TEXTCOLOR'],'padding-left':20,'padding-top':20,'text-align':'left'}),
                                    html.Div([
                                        html.Ul([
                                            html.Li([dcc.Markdown("$$S$$: Susceptible individuals", mathjax=True)]),
                                            html.Li([dcc.Markdown("$$E$$: Exposed individuals - infected but not yet infectious or symptomatic", mathjax=True)]),
                                            html.Li([dcc.Markdown("$$I_{i}$$: Infected individuals in severity class $$i$$. Severity increases with $$i$$ and we assume individuals must pass through all previous classes", mathjax=True),
                                            html.Div([
                                                html.Ul([
                                                    html.Li([dcc.Markdown("$$I_{1}$$: mild infection",mathjax=True)]),
                                                    html.Li([dcc.Markdown("$$I_{2}$$: severe infection",mathjax=True)]),
                                                    html.Li([dcc.Markdown("$$I_{3}$$: critical infection",mathjax=True)])
                                                ])
                                            ]),
                                            html.Li([dcc.Markdown("$$R$$: individuals who have rocovered from disease and are now immune", mathjax=True)]),
                                            html.Li([dcc.Markdown("$$D$$: Dead individuals", mathjax=True)]),
                                            ]),
                                        ],className='custom-list')
                                    ],style={'color':colors['TEXTCOLOR'], 'padding-left':20, 'text-align':'left'}),
                                    html.H3(["Parameters"],style={'color':colors['TEXTCOLOR'],'padding-left':20,'padding-top':20,'text-align':'left'}),
                                    html.Div([
                                        html.Ul([
                                            html.Li([dcc.Markdown("$$\\beta_{i}$$: rate at which infected individuals in class $$I_{i}$$ contact susceptibles and infect them", mathjax=True)]),
                                            html.Li([dcc.Markdown("$$a$$: rate of progression from the exposed to infected class", mathjax=True)]),
                                            html.Li([dcc.Markdown("$$\gamma_{i}$$: rate aat which infected individuals in class $$I_{i}$$ recover from disease and become immune", mathjax=True),
                                            html.Li([dcc.Markdown("$$p_{i}$$: rate at which infected individuals in class $$I_{i}$$ progress to class $$I_{i+1}$$", mathjax=True)]),
                                            html.Li([dcc.Markdown("$$\mu$$: deathe rate for individuals in the most severe stage of disease", mathjax=True)]),
                                            ]),
                                        ],className='custom-list'),
                                        html.P(["All rates are per day"], style={'padding-left':30})
                                    ],style={'color':colors['TEXTCOLOR'], 'padding-left':20, 'text-align':'left'}),
                                ],
                                style={'backgroundColor':'#001a33'},
                                selected_style={'backgroundColor':colors['TEXTCOLOR']})
                            ]),
                ],style={'flex':0.65}),
    ],style={'display':'flex', 'flex-direction':'row'})
])

@app.callback(
    Output('graph','figure'),
    Input('incub_period','value'),
    Input('dur_mild_inf','value'),
    Input('frac_severe_inf','value'),
    Input('dur_severe_inf','value'),
    Input('frac_crit_inf','value'),
    Input('dur_crit_inf','value'),
    Input('frac_death','value'),
    Input('mild_tran','value'),
    Input('severe_tran','value'),
    Input('crit_tran','value'),
    Input('pop_size','value'),
    Input('init_inf','value'),
    Input('sim_dur','value') 
)
def render_graph(incub_period,dur_mild_inf,frac_severe_inf,dur_severe_inf,frac_crit_inf,dur_crit_inf,frac_death,mild_tran,severe_tran,crit_tran,pop_size,init_inf,sim_dur):
    b1=round(mild_tran,3)
    b2=round(severe_tran,3)
    b3=round(crit_tran,3)
    a=round((1/incub_period),3)
    g1=round(((1/dur_mild_inf)*0.8),3)
    p1=round(((1/dur_mild_inf)-g1),3)
    p2=round((1/dur_severe_inf)*(frac_crit_inf/(frac_severe_inf+frac_crit_inf)),3)
    g2=round((1/dur_severe_inf)*(frac_severe_inf/(frac_severe_inf+frac_crit_inf)),3)
    u=round(((1/dur_crit_inf)*frac_death/100),3)
    g3=round(((1/dur_crit_inf)-u),3)
    S = [0 for x in range(sim_dur+1)]
    E = [0 for x in range(sim_dur+1)]
    I1 = [0 for x in range(sim_dur+1)]
    I2 = [0 for x in range(sim_dur+1)]
    I3 = [0 for x in range(sim_dur+1)]
    R = [0 for x in range(sim_dur+1)]
    D = [0 for x in range(sim_dur+1)]
    N = [0 for x in range(sim_dur+1)]
    N[0]=pop_size
    S[0]=pop_size-init_inf
    E[0]=init_inf
    for t in range(1,sim_dur+1):
        S[t]=(S[t-1]+(-(b1*I1[t-1]-b2*I2[t-1]-b3*I3[t-1])*S[t-1]/N[t-1]))
        E[t]=(E[t-1] + ((b1*I1[t-1]-b2*I2[t-1]-b3*I3[t-1])*S[t-1]/N[t-1] - a*E[t-1]))
        I1[t]=(I1[t-1] + ( a*E[t-1] - (g1+p1)*I1[t-1]))
        I2[t]=(I2[t-1] + (p1*I1[t-1] - (g2+p2)*I2[t-1]))
        I3[t]=(I3[t-1] + (p2*I2[t-1] - (g3+u)*I3[t-1]))
        R[t]=(R[t-1] + (g1*I1[t-1] + g2*I2[t-1] + g3*I3[t-1]))
        D[t]=(D[t-1] + (u*I3[t-1]))
        N[t]=(S[t]+E[t]+I1[t]+I2[t]+I3[t])

    fig= go.Figure()
    T=list(range(0,sim_dur+1))

    fig.add_trace(go.Scatter(x=T, y=S, name="Susceptible(S)")),
    fig.add_trace(go.Scatter(x=T, y=E, name="Exposed(E)")),
    fig.add_trace(go.Scatter(x=T, y=I1, name="Mild Infected(I1)")),
    fig.add_trace(go.Scatter(x=T, y=I2, name="Severe Infected(I2)")),
    fig.add_trace(go.Scatter(x=T, y=I3, name="Critical Infected(I3)")),
    fig.add_trace(go.Scatter(x=T, y=R, name="Recovered(R)")),
    fig.add_trace(go.Scatter(x=T, y=D, name="Death(D)"))

    fig.update_layout(
            yaxis={'title':'Population','gridcolor':'#00478e'},
            xaxis={'title':'Time','gridcolor':'#00478e'},
            paper_bgcolor='#001a33',
            plot_bgcolor='#001a33',
            font={'color':colors['TEXTCOLOR']},
            )
    fig.update_layout(transition_duration=100)

    return fig

@app.callback(
    Output('output_table','children'),
    Input('incub_period','value'),
    Input('dur_mild_inf','value'),
    Input('frac_severe_inf','value'),
    Input('dur_severe_inf','value'),
    Input('frac_crit_inf','value'),
    Input('dur_crit_inf','value'),
    Input('frac_death','value'),
    Input('mild_tran','value'),
    Input('severe_tran','value'),
    Input('crit_tran','value'),
    Input('pop_size','value'),
    Input('init_inf','value'),
    Input('sim_dur','value') 
)
def render_graph(incub_period,dur_mild_inf,frac_severe_inf,dur_severe_inf,frac_crit_inf,dur_crit_inf,frac_death,mild_tran,severe_tran,crit_tran,pop_size,init_inf,sim_dur):
    b1=round(mild_tran,3)
    b2=round(severe_tran,3)
    b3=round(crit_tran,3)
    a=round((1/incub_period),3)
    g1=round(((1/dur_mild_inf)*0.8),3)
    p1=round(((1/dur_mild_inf)-g1),3)
    p2=round((1/dur_severe_inf)*(frac_crit_inf/(frac_severe_inf+frac_crit_inf)),3)
    g2=round((1/dur_severe_inf)*(frac_severe_inf/(frac_severe_inf+frac_crit_inf)),3)
    u=round(((1/dur_crit_inf)*frac_death/100),3)
    g3=round(((1/dur_crit_inf)-u),3)
    return html.Div([
        html.Table(className='custom-table', children=[
            html.Thead([
                html.Tr([
                    html.Th(["Parameters"], scope='col'),
                    html.Th(["Value"],scope='col')
                ])
            ]),
            html.Tbody([
                html.Tr([
                    html.Td("b1*N"),
                    html.Td([b1])
                ]),
                html.Tr([
                    html.Td("b2*N"),
                    html.Td([b2])
                ]),
                html.Tr([
                    html.Td("b3*N"),
                    html.Td([b3])
                ]),
                html.Tr([
                    html.Td("a"),
                    html.Td([a])
                ]),
                html.Tr([
                    html.Td("g1"),
                    html.Td([g1])
                ]),
                html.Tr([
                    html.Td("g2"),
                    html.Td([g2])
                ]),
                html.Tr([
                    html.Td("g3"),
                    html.Td([g3])
                ]),
                html.Tr([
                    html.Td("p1"),
                    html.Td([p1])
                ]),
                html.Tr([
                    html.Td("p2"),
                    html.Td([p2])
                ]),
                html.Tr([
                    html.Td("u"),
                    html.Td([u])
                ]),
                html.Tr([
                    html.Td("N0"),
                    html.Td([pop_size])
                ]),
            ])
        ],style={'flex':0.25}),
        html.P([
            dcc.Markdown('''
            These parameters can be changed using input elements.
            Values in this table represent the current values chosen via sliders.\n
            **Note** that transmission rates are scaled by N, so that $$\\beta * N$$ is constant as $$N$$ changes''', mathjax=True)
        ], style={'flex':0.75, 'color':colors['TEXTCOLOR'], 'padding':20})
    ], style={'display':'flex', 'flex-direction':'row'})
if __name__ == '__main__':
    app.run_server(debug=True)