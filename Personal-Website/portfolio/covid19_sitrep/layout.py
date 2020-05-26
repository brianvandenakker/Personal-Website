import os
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import datetime as dt

covid_data = pd.read_csv(os.path.join(os.path.dirname(__file__), "data/covid_country_level_data.csv"))
covid_data.drop(columns = ['m1_wildcard', 'stringency_index','legacy_stringency_index_for_display', 'legacy_stringency_index', 'age_percent_0_to_14',
                           'age_percent_15_to_64'], inplace = True)

layout = html.Div([

    html.H1(['Interact with the charts below to see how COVID-19 and State Responses are affecting the world'], style={'text-align':'center', 'font-size':'20px', 'font-family':'sans-serif'}),


    html.Div([
        dcc.Markdown(id = 'date_display', style={'text-align':'center', 'font-weight':'bold', 'font-size':'30px', 'font-family':'sans-serif'}),
        html.P("Use Slider to Adjust the Date", style={'text-align': 'right', 'margin-right': '18px', 'font-size': '14px', 'font-family': 'sans-serif'}),
        dcc.Slider(id = 'date_slider', min=min(covid_data['day_of_year'])+9,
                    max=max(covid_data['day_of_year']), value=max(covid_data['day_of_year'])-1,
                    marks = {
                        min(covid_data['day_of_year'])+9: {'label': str((dt.datetime(2020, 1, 1) + dt.timedelta(min(covid_data['day_of_year'])+8)).strftime("%b %d, %Y"))},
                    }),
    ]),

    html.Div([

    html.Div([
        html.Div([
            dcc.Dropdown(id="variable_selector",
                options =  [{'label': 'Confirmed Cases', 'value': 'confirmed_cases'},
                            {'label': 'Confirmed Deaths', 'value': 'confirmed_deaths'},
                            {'label': 'School Closing', 'value': 'c1_school_closing'},
                            {'label': 'Restrict Gatherings', 'value': 'c4_restrictions_on_gatherings'},
                            {'label': 'Workplace Closing', 'value': 'c2_workplace_closing'},
                            {'label': 'Stay at Home Requirements', 'value': 'c6_stay_at_home_requirements' },
                            {'label': 'Public Events Cancelled', 'value': 'c3_cancel_public_events'},
                            {'label': 'Public Transportation Closed', 'value': 'c5_close_public_transport'},
                            {'label': 'Public Information Campaigns', 'value': 'h1_public_information_campaigns'},
                            {'label': 'Restrictions on Internal Movement', 'value': 'c7_restrictions_on_internal_movement'},
                            {'label': 'International Travel Controls', 'value': 'c8_international_travel_controls'},
                            {'label': 'Fiscal Measures', 'value': 'e3_fiscal_measures'},
                            {'label': 'Testing Policy', 'value':'h2_testing_policy'},
                            {'label': 'Contact Tracing', 'value': 'h3_contact_tracing'},
                            {'label': 'Emergency Investment in Health Care', 'value': 'h4_emergency_investment_in_health_care'},
                            {'label': 'Investment in Vaccines', 'value': 'h5_investment_in_vaccines'},
                            {'label': 'Income Support', 'value': 'e1_income_support'},
                            {'label': 'Debt Contract Relief', 'value': 'e2_debt_contract_relief'},
                            {'label': 'Recieving International Support', 'value': 'e4_international_support'},
                            {'label': 'Stringency Index', 'value': 'stringency_index_for_display'},
                            {'label': 'Hospital Beds per Million', 'value': 'hospital_beds_per_million'},
                            {'label': 'Population Density', 'value': 'people_per_sq_km'},
                            {'label': 'GDP per Capita', 'value': 'gdp_percap'},
                            {'label': 'Population', 'value': 'population_millions'},
                            {'label': 'Percent 65 and Older', 'value': 'age_percent_65_UP'},
                            {'label': 'Percent Smoking', 'value': 'percent_smoking_prev'},
                            {'label': 'COVID19 Related Deaths per Million', 'value': 'deaths_per_million'},
                            {'label': 'COVID19 Confirmed Cases per Million', 'value': 'cases_per_million'},
                            {'label': 'Estimated Spare Hospital Beds per Million', 'value': 'spare_beds_per_million'}],
                value = 'confirmed_deaths', placeholder = "Select a Metric to Observe"
                )], style = {'width': '60%', 'display':'inline-block'}),

                html.Div([dcc.Dropdown(id="line_selector",
                    options = [{'label': 'Confirmed Cases', 'value': 'confirmed_cases'},
                               {'label': 'Confirmed Deaths', 'value': 'confirmed_deaths'},
                               {'label': 'Deaths per Million', 'value': 'deaths_per_million'},
                               {'label': 'Confirmed Cases per Million', 'value': 'cases_per_million'},
                               {'label': 'Moving Average, % change in Deaths', 'value': 'ma_percent_change_deaths_per_million'},
                               {'label': 'Moving Average, % change in new Cases', 'value': 'ma_percent_change_cases_per_million'},
                               {'label': 'Estimated Spare Hospital Beds per Million', 'value': 'spare_beds_per_million'}],
                               value = 'confirmed_deaths', placeholder = "Select a Metric to Observe")], style = {'width':'20%', 'display':'inline-block'}),

                html.Div([dcc.Dropdown(id="country_selector",
                    options = [{'label': f"{value}", 'value':f"{value}"} for value in covid_data['country_name'].unique()],
                               multi=True, placeholder = "Select Specific Countries")
                               ], style = {'width':'20%' , 'display':'inline-block'})

    ]),

    html.Div([
        dcc.Graph(id='map')
        ],style={'width':'60%',  'display':'inline-block'}),

    html.Div([
        dcc.Graph(id = 'growth')
        ],style={'width':'40%', 'display':'inline-block'})

    ]),

    html.Div([
    dcc.Markdown(id="covid_stats")
    ], style={'text-align':'center', 'font-family':'sans-serif'}),

    html.Div([
        html.P(["Created by: Brian VandenAkker"], style= {'text-align': 'left','font-size': '10px', 'display':'inline-block', 'width':'20%'}),
        html.P(["Primary Data Source: Thomas Hale, Sam Webster, Anna Petherick, Toby Phillips, and Beatriz Kira.(2020). Oxford COVID-19 Government Response Tracker. Blavatnik School of Government."], style = {'text-align': 'right','font-size': '10px', 'display':'inline-block', 'width':'70%'})
],style = {'text-align': 'center'}
)])
