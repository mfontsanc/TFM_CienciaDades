from shiny import ui, module, reactive, render
import requests
import plotly.express as px
from shinywidgets import output_widget, register_widget
import pandas as pd
from communities import HEADERS
from community_detail import get_list_communities, get_list_clinical_trials
import plotly
import random
import plotly.graph_objs as go


API_URL_CT = "http://127.0.0.1:5000/tfm-collaboration-network/v1/NetworkCollaboration/get_clinical_trial"

def get_clinical_trials(ct_id):
    """
        Method to get the data of a specific clinical trial.

        Parameters:
           ct_id (str): Identifier of the clinical trial

        Returns:
            Dataframe: dataframe containing the data of the clinical trial, by calling the application.
    """
    params = {
        "id": ct_id 
    }
    r=requests.post(url = API_URL_CT, headers = HEADERS, json = params)
    
    return r.json()

# Preload the list of clinical trials per community.
clinical_trials_per_communities = get_list_clinical_trials()

@module.ui
def clinical_trials_ui():
    return ui.page_fluid(
        ui.panel_title("Estudis clínics"),

        ui.br(),
        ui.row(
            ui.column(6, ui.h6("Llistat de les comunitats generades a partir dels estudis clínics:")),
            ui.column(6, ui.h6("Llistat d'estudis clínics involucrats en aquesta comunitat:")),
        ),
        ui.row(
            ui.column(6,ui.input_selectize("comunitats", " ", 
                                           get_list_communities(), multiple=False)),  
            ui.column(6,ui.input_selectize("clinical_trials", " ", 
                                           {"N/A": 0}, multiple=False)),        
        ), 

        ui.row(
            ui.column(6, ui.output_table("clinical_trial_details")),
            ui.column(6,
                ui.navset_tab_card(
                    ui.nav("Criteris d'eligibilitat", ui.output_table("criteris")),
                    ui.nav("Intervencions i/o condicions", ui.output_table("intervencions")),
                    ui.nav("Resultats", ui.output_table("resultats")),
                ),
            ),
        ),
        ui.br(),
        ui.row(
            ui.column(6, ui.h6("Núvol de paraules clau de l'estudi clínic:")),
            ui.column(6, ui.h6("Localitzacions on es realitza l'estudi clínic:")),
        ),
        ui.row(
            ui.column(6,output_widget("wordcloud")),
            ui.column(6,output_widget("ct_map")),
        ),
)

@module.server
def clinical_trials_server(input, output, session):
    
    @reactive.Effect()
    @reactive.event(input.comunitats)
    def _():
        # When a new community is selected, this function is called.
        community_id = input.comunitats()
        # Get the list of clinical trial of a specific community.
        community = "Comunitat " + community_id
        result = clinical_trials_per_communities[community]
        result.sort()
        ui.update_selectize(id="clinical_trials", choices=result, selected=result[0])

        # Reload the tables.
        ui.output_table("clinical_trial_details")
        ui.output_table("criteris")
        ui.output_table("intervencions")
        ui.output_table("resultats")
    
    @output
    @render.table
    def clinical_trial_details():
        # Reload the table with the details of the selected clinical trial.
        clinical_trial_id = input.clinical_trials()

        if len(clinical_trial_id) > 4:
            # Call the application to retrieve the information from the database.
            data_ct = get_clinical_trials(clinical_trial_id)

            ct_properties = ["Títol", "Descripció", "Objectiu", "Fase", "Data inici", "Data últim participant", "Data finalització",
                            "Comunitat", "Número de participants", "Estat participació"]

            ct_data_properties = []
            for prop in ct_properties:
                ct_data_properties.append([prop, data_ct.get(prop)])

            # Dataframe used to generate the table.
            df = pd.DataFrame(ct_data_properties, columns=["",clinical_trial_id])

            # Creation of the wordcloud.
            leng = len(data_ct.get("Paraules clau"))
            colors = [plotly.colors.PLOTLY_SCALES['Viridis'][random.randrange(1, 17)][1] for i in range(leng)]
            weights = [random.randint(12, 25) for i in range(leng)]

            y_ = [x/100 for x in random.sample(range(100), leng)]
            x_ = [x/100 for x in random.sample(range(100), leng)]
            data = go.Scatter(x=x_, y=y_,
                              mode='text',
                              text=data_ct.get("Paraules clau"),
                              marker={'opacity': 0.3},
                              textfont={'size': weights, 'color': colors})
            layout = go.Layout({'xaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                                'yaxis': {'showgrid': False, 'showticklabels': False, 'zeroline': False},
                                'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)',})
            wordcloud = go.Figure(data=[data], layout=layout)

            register_widget("wordcloud", wordcloud)

            # Creation of the location map.
            coordinates = []
            for col in data_ct['Col·laboradors']:
                ord_name = col['Nom de organització'] if col.get('Nom de organització') else "N/A"
                coordinates.append([col["Latitud"], col["Longitud"], ord_name, col['Ciutat'], col['País']])

            if len(coordinates)>0:
                df_col = pd.DataFrame(coordinates, columns=['latitude', 'longitude', 'name', 'city', 'country'])
            else:
                color = "#FFFFFF"
                df_col = pd.DataFrame([[0, 0, '', 'N/A', 'N/A']], columns=['latitude', 'longitude', 'name', 'city', 'country'])

            map_chart = px.scatter_geo(df_col, lat="latitude", lon="longitude",
                        color="country",
                        hover_name="city", 
                        hover_data={'latitude':False, 'longitude':False,
                                    "country":True, "name":True},
                        projection="natural earth",
                        labels={"city": "Ciutat", "country": "País", "name": "Nom del col·laborador"})
            
            register_widget("ct_map", map_chart)

            return (
                df.style.set_table_attributes(
                    'class="dataframe shiny-table table w-auto"'
                )
                .format(
                    {
                        "mpg": "{0:0.1f}",
                        "disp": "{0:0.1f}",
                        "drat": "{0:0.2f}",
                        "wt": "{0:0.3f}",
                        "qsec": "{0:0.2f}",
                    }
                )
                .set_table_styles(
                    [dict(selector="th", props=[("text-align", "center")])]
                ).hide_index()
            )
    
    @output
    @render.table
    def criteris():
        # Reload the criteria tab when a new clinical trial is selected.
        clinical_trial_id = input.clinical_trials()

        if len(clinical_trial_id) > 4:
            # Get the data from the database
            data_ct = get_clinical_trials(clinical_trial_id)

            # Prepare the data as dataframe to be shown as a table.
            ct_data_properties = data_ct.get("Criteris eligibilitat")

            df = pd.DataFrame(ct_data_properties, columns=[""])
            
            return (
                df.style.set_table_attributes(
                    'class="dataframe shiny-table table w-auto"'
                )
                .format(
                    {
                        "mpg": "{0:0.1f}",
                        "disp": "{0:0.1f}",
                        "drat": "{0:0.2f}",
                        "wt": "{0:0.3f}",
                        "qsec": "{0:0.2f}",
                    }
                )
                .set_table_styles(
                    [dict(selector="th", props=[("text-align", "center")])]
                ).hide_index()
            )
    
    @output
    @render.table
    def intervencions():
        # Reload the interventions tab when a new clinical trial is selected.
        clinical_trial_id = input.clinical_trials()

        if len(clinical_trial_id) > 4:
            # Get the data from the database
            data_ct = get_clinical_trials(clinical_trial_id)

            # Prepare the data as dataframe.
            ct_data_properties = [["", x, ""] for x in data_ct.get("Condicions")]
            ct_data_properties[0] = ["Condicions: ", ct_data_properties[0][1], ct_data_properties[0][2]]
            ct_data_properties.append(["", "", ""])

            ct_int = [[x.get("Nom intervenció"), x.get("Descripció"), x.get("Tipus intervenció")] for x in data_ct.get("Intervencions")]
            if len(ct_int)>0:
                ct_data_properties.append(["Nom de la intervenció", "Descripció", "Tipus d'intervenció"])
                ct_data_properties = ct_data_properties + ct_int

            df = pd.DataFrame(ct_data_properties, columns=["", "", ""])
            
            return (
                df.style.set_table_attributes(
                    'class="dataframe shiny-table table w-auto"'
                )
                .format(
                    {
                        "mpg": "{0:0.1f}",
                        "disp": "{0:0.1f}",
                        "drat": "{0:0.2f}",
                        "wt": "{0:0.3f}",
                        "qsec": "{0:0.2f}",
                    }
                )
                .set_table_styles(
                    [dict(selector="th", props=[("text-align", "center")])]
                ).hide_index()
            )
    @output
    @render.table
    def resultats():
        # Reload the results tab when a new clinical trial is selected.
        clinical_trial_id = input.clinical_trials()

        if len(clinical_trial_id) > 4:
            # Get the data from database
            data_ct = get_clinical_trials(clinical_trial_id)

            # Prepare the data to be shown in a table.
            ct_data_res = data_ct.get("Resultat")
            ct_data_properties = []
            ct_data_properties.append(["Nom: ", ct_data_res.get("Nom")])
            ct_data_properties.append(["Descripció: ", ct_data_res.get("Descripció")])
            ct_data_properties.append(["Temps: ", ct_data_res.get("Descripció")])

            df = pd.DataFrame(ct_data_properties, columns=["", "Resultats"])
            
            return (
                df.style.set_table_attributes(
                    'class="dataframe shiny-table table w-auto"'
                )
                .format(
                    {
                        "mpg": "{0:0.1f}",
                        "disp": "{0:0.1f}",
                        "drat": "{0:0.2f}",
                        "wt": "{0:0.3f}",
                        "qsec": "{0:0.2f}",
                    }
                )
                .set_table_styles(
                    [dict(selector="th", props=[("text-align", "center")])]
                ).hide_index()
            )
    