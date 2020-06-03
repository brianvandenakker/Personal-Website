import os
import pandas as pd
import numpy as np
import datetime as dt
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate


covid_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "data/covid_country_level_data.csv"))
covid_data.drop(columns = ['m1_wildcard', 'stringency_index', 'age_percent_0_to_14',
                           'age_percent_15_to_64'], inplace = True)



def register_callbacks(dashapp):
    @dashapp.callback(
        Output(component_id='map', component_property='figure'),
        [Input(component_id='variable_selector', component_property='value'),
        Input(component_id='date_slider', component_property= 'value')],
    )
    def update_map(var_selected, date_selected):
        if var_selected is None:
            raise PreventUpdate

        df = covid_data[[var_selected, 'day_of_year', 'date', 'country_name']].query(f"day_of_year=={date_selected}")

        map = go.Figure(data=go.Choropleth(
            locations = df['country_name'],
            locationmode = 'country names',
            z = np.log(df[var_selected]),
            colorscale = 'Reds',
            marker_line_color = 'black',
            marker_line_width = 0.5,
            zmin=0,
            zmax=max(np.log(covid_data[var_selected])),
            text = df[var_selected],
            hoverinfo = 'location+text'
            ))
        map.update_layout(
            margin=dict(
            l=5,
            r=50,
            b=0,
            t=0,
            pad=2
            ),
            geo=dict(
                showframe = False,
                showcoastlines = True,
                projection_type = 'equirectangular',
            ))

        return map


    @dashapp.callback(
        Output(component_id='growth', component_property='figure'),
        [Input(component_id='line_selector', component_property='value'),
         Input(component_id='country_selector', component_property='value'),
         Input(component_id='date_slider', component_property= 'value')]
    )
    def update_graph(var_selected, country_selected, date_selected):
        if var_selected is None:
            raise PreventUpdate
        elif country_selected is None:
            if('death' in var_selected):
                df = covid_data[[var_selected, 'day_of_year', 'date', 'country_name',
                                'days_since_first_death']].query(f"days_since_first_death>0 & day_of_year <= {date_selected}")
                fig = px.line(df, x='days_since_first_death', y=var_selected, color='country_name',
                                line_shape='spline', render_mode='svg', hover_name='country_name',
                                )
                fig.update_layout(yaxis_type="log", showlegend=False, plot_bgcolor='white',
                                    margin=dict(
                                    l=0,
                                    r=50,
                                    b=50,
                                    t=0,
                                    pad=0
                                    )),
                fig.update_xaxes(title_text= 'Days Since First Death'),
                fig.update_yaxes(title_text = var_selected.replace('_', ' ').title())

            elif(var_selected == 'spare_beds_per_million'):
                df = covid_data[[var_selected, 'day_of_year', 'date', 'country_name',
                                'days_since_first_case']].query(f"days_since_first_case>0 & day_of_year <= {date_selected}")
                fig = px.line(df, x='days_since_first_case', y=var_selected, color='country_name',
                                line_shape='spline', render_mode='svg', hover_name='country_name',
                                )
                fig.update_layout(showlegend=False, plot_bgcolor='white',
                                    margin=dict(
                                    l=0,
                                    r=50,
                                    b=50,
                                    t=0,
                                    pad=0
                                    )),
                fig.update_xaxes(title_text= 'Days Since First Death'),
                if(min(df[var_selected]) < 0 ): val = 1.2
                else: val = -1.2
                fig.update_yaxes(range = [min(df[var_selected])*val, max(df[var_selected])*1.2], title_text = var_selected.replace('_', ' ').title())

            else:
                df = covid_data[[var_selected, 'day_of_year', 'date', 'country_name',
                                'days_since_first_case']].query(f"days_since_first_case>0 & day_of_year <= {date_selected}")
                fig = px.line(df, x='days_since_first_case', y=var_selected, color='country_name')
                fig.update_layout(yaxis_type="log", showlegend=False, plot_bgcolor='white',
                                    margin=dict(
                                    l=0,
                                    r=50,
                                    b=50,
                                    t=0,
                                    pad=0
                                    )),
                fig.update_xaxes(title_text= 'Days Since First Case'),
                fig.update_yaxes(title_text = var_selected.replace('_', ' ').title())

        else:
            if('death' in var_selected):

                df = covid_data[[var_selected, 'day_of_year', 'date', 'country_name',
                                'days_since_first_death']].query(f"days_since_first_death>0 & day_of_year <= {date_selected} & country_name == {country_selected}")
                try:
                    fig = px.line(df, x='days_since_first_death', y=var_selected, color='country_name',
                                    line_shape='spline', render_mode='svg', hover_name='country_name')
                    fig.update_layout(yaxis_type="log", showlegend=False, plot_bgcolor='white',
                                        margin=dict(
                                        l=0,
                                        r=50,
                                        b=50,
                                        t=0,
                                        pad=0
                                        )),
                    fig.update_xaxes(title_text= 'Days Since First Death'),
                    fig.update_yaxes(title_text = var_selected.replace('_', ' ').title())
                except:
                    df = covid_data[[var_selected, 'day_of_year', 'date', 'country_name',
                                    'days_since_first_death']].query(f"days_since_first_death>0 & day_of_year <= {date_selected}")
                    fig = px.line(df, x='days_since_first_death', y=var_selected, color='country_name',
                                    line_shape='spline', render_mode='svg', hover_name='country_name')
                    fig.update_layout(yaxis_type="log", showlegend=False, plot_bgcolor='white',
                                        margin=dict(
                                        l=0,
                                        r=50,
                                        b=50,
                                        t=0,
                                        pad=0
                                        )),
                    fig.update_xaxes(title_text= 'Days Since First Death'),
                    fig.update_yaxes(title_text = var_selected.replace('_', ' ').title())
            else:
                df = covid_data[[var_selected, 'day_of_year', 'date', 'country_name',
                                'days_since_first_case']].query(f"days_since_first_case>0 & day_of_year <= {date_selected} & country_name == {country_selected}")
                try:
                    if(var_selected == 'spare_beds_per_million'):
                        fig = px.line(df, x='days_since_first_case', y=var_selected, color='country_name',
                                        line_shape='spline', render_mode='svg', hover_name='country_name',
                                        )
                        fig.update_layout(showlegend=False, plot_bgcolor='white',
                                            margin=dict(
                                            l=0,
                                            r=50,
                                            b=50,
                                            t=0,
                                            pad=0
                                            )),
                        fig.update_xaxes(title_text= 'Days Since First Death'),
                        if(min(df[var_selected]) < 0 ): val = 1.2
                        else: val = -1.2
                        fig.update_yaxes(range = [min(df[var_selected])*val, max(df[var_selected])*1.2], title_text = var_selected.replace('_', ' ').title())
                    else:
                        fig = px.line(df, x='days_since_first_case', y=var_selected, color='country_name')
                        fig.update_layout(yaxis_type="log", showlegend=False, plot_bgcolor='white',
                                            margin=dict(
                                            l=0,
                                            r=50,
                                            b=50,
                                            t=0,
                                            pad=0
                                            )),
                        fig.update_xaxes(title_text= 'Days Since First Case'),
                        fig.update_yaxes(title_text = var_selected.replace('_', ' ').title())

                except:
                    if(var_selected == 'spare_beds_per_million'):
                        df = covid_data[[var_selected, 'day_of_year', 'date', 'country_name',
                                        'days_since_first_case']].query(f"days_since_first_case>0 & day_of_year <= {date_selected}")
                        fig = px.line(df, x='days_since_first_case', y=var_selected, color='country_name',
                                        line_shape='spline', render_mode='svg', hover_name='country_name',
                                        )
                        fig.update_layout(showlegend=False, plot_bgcolor='white',
                                            margin=dict(
                                            l=0,
                                            r=50,
                                            b=50,
                                            t=0,
                                            pad=0
                                            )),
                        fig.update_xaxes(title_text= 'Days Since First Death'),
                        if(min(df[var_selected]) < 0 ): val = 1.2
                        else: val = -1.2
                        fig.update_yaxes(range = [min(df[var_selected])*val, max(df[var_selected])*1.2], title_text = var_selected.replace('_', ' ').title())
                    else:
                        df = covid_data[[var_selected, 'day_of_year', 'date', 'country_name',
                                        'days_since_first_case']].query(f"days_since_first_case>0 & day_of_year <= {date_selected}")
                        fig = px.line(df, x='days_since_first_case', y=var_selected, color='country_name',
                                        line_shape='spline', render_mode='svg', hover_name='country_name')
                        fig.update_layout(yaxis_type="log", showlegend=False, plot_bgcolor='white',
                                            margin=dict(
                                            l=0,
                                            r=50,
                                            b=50,
                                            t=0,
                                            pad=0
                                            )),
                        fig.update_xaxes(title_text= 'Days Since First Case'),
                        fig.update_yaxes(title_text = var_selected.replace('_', ' ').title())


        return fig


    @dashapp.callback(
        Output(component_id='date_display', component_property='children'),
        [Input(component_id='date_slider', component_property= 'value')]
    )
    def display_date(date_selected):
        return (dt.datetime(2020, 1, 1) + dt.timedelta(date_selected - 1)).strftime("%B %d, %Y")


    @dashapp.callback(
        Output(component_id='covid_stats', component_property='children'),
        [Input(component_id='date_slider', component_property= 'value')]
    )
    def covid_stats(date_selected):
        df = covid_data[['day_of_year', 'date', 'country_name', 'confirmed_cases', 'confirmed_deaths',
                        'stringency_index_for_display', 'c1_school_closing', 'c2_workplace_closing', 'c6_stay_at_home_requirements']].query(f"day_of_year=={date_selected}")

        summary = f"""
        Global Statistics \n
        Confirmed Cases: { df['confirmed_cases'].sum():,} |
        Total Deaths: {np.sum(df['confirmed_deaths']):,} |
        Countries with workplace closings: {(np.count_nonzero(df['c2_workplace_closing']))} |
        Countries with state at home requirements: {sum(1 for i in df['c6_stay_at_home_requirements'] if i and pd.notnull(i))}
        """
        return summary
