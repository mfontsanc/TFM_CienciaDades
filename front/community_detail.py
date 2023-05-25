from shiny import ui, module, reactive, render
from communities import get_communities, HEADERS
from shinywidgets import output_widget, register_widget
import matplotlib.pyplot as plt
from plotly.offline import plot

import requests
import networkx as nx
import igviz as ig
import plotly.express as px
import pandas as pd

API_URL_DETAIL = "http://127.0.0.1:5000/tfm-collaboration-network/v1/NetworkCollaboration/get_communities_detail"
API_URL_COLLAB = "http://127.0.0.1:5000/tfm-collaboration-network/v1/NetworkCollaboration/get_collaborators"

def get_communities_details(community_id):
    """
        Method to retrieve the properties of each clinical trial of the community.

        Parameters:
            community_id (str): Identifier of the community

        Returns:
            Dataframe: dataframe with the data of the community.
    """
    community_id = community_id.replace("Comunitat ", "")
    params = {
        "community_id": community_id 
    }
    r=requests.post(url = API_URL_DETAIL, headers = HEADERS, json = params)
    
    return r.json()

def get_collaborators(community_id):
    """
        Method to retrieve the list of collaborator from the database of a specific community.

        Parameters:
            community_id (str): Identifier of the community.

        Returns:
            Dataframe: dataframe with the sponsors of the community.
    """
    community_id = community_id.replace("Comunitat ", "")
    params = {
        "community_id": community_id 
    }
    r=requests.post(url = API_URL_COLLAB, headers = HEADERS, json = params)
    
    return r.json()


def get_list_communities():    
    """
        Method to retrieve the list of communities.

        Parameters:
            None

        Returns:
            List: list of communities as strings.
    """
        
    all_community = ["Comunitat " + str(x[1]) for x in clinical_trials_communities if x[1] != -1]

    all_community = list(set(all_community))
    all_community.sort()

    return all_community

def get_list_clinical_trials():  
    """
        Method to retrieve the list of clinical trials per community.

        Parameters:
            None

        Returns:
            Dict: dictionary containing per each community the list of clinical trials.
    """

    all_community = [["Comunitat " + str(x[1]), x[0]] for x in clinical_trials_communities if x[1] != -1]
    clinical_trials_community = {}

    for community in all_community:
        key = community[0]
        value = community[1]

        if not clinical_trials_community.get(key):
            clinical_trials_community[key] = [""]
        clinical_trials_community[key].append(value)

    return clinical_trials_community

clinical_trials_communities = get_communities()
clinical_trials_per_communities = get_list_clinical_trials()


@module.ui
def community_detail_ui():
    return ui.page_fluid(
        ui.panel_title("Comunitats generades a partir dels estudis clínics"),
        
        ui.div("Llistat de les comunitats generades a partir dels estudis clínics."),
        ui.input_selectize(id="comunitats", label="  ", choices=get_list_communities(), multiple=False),    

        ui.layout_sidebar(        
            ui.panel_sidebar("Relació dels estudis clínics i els objectius, intervencions o observacions i paraules clau.", output_widget("network_graph")),    
            ui.panel_main("Mapa de localitzacions de tots els estudis clínics de la comunitat.", output_widget("map_chart"))
        ),

        ui.br(),
        ui.div("Llistat d'estudis clínics involucrats en aquesta comunitat."),
        ui.input_selectize("clinical_trials", "  ", {"N/A": 0}, multiple=False),
        
        ui.row(
            ui.column(4, ui.output_table("result_clinical_trials")),
            ui.column(8, ui.output_table("result_investigators")),
        ),
)

@module.server
def community_detail_server(input, output, session):

    @reactive.Effect()
    @reactive.event(input.comunitats)
    def _():
        # When a new community is selected, this function is called.
        community_id = input.comunitats()

        # Create the widget of the graph.
        data = get_communities_details(community_id)
        data_no_properties = [["Estudi clínic: " + x[0], x[2], x[1]] for x in data]
        df_graph = pd.DataFrame(data_no_properties, columns=['target', 'source', 'property_name'])

        graph = nx.Graph()
        graph = nx.from_pandas_edgelist(df_graph, "target", "source", ["property_name"])
        
        network_graph = ig.plot(graph, title="", layout="circular", highlight_neighbours_on_hover=True, colorscale="Viridis",
                                edge_text=["property_name"])

        register_widget("network_graph", network_graph)

        # Create the widget of the map with the locations of all clinical trials.
        data_collabs = get_collaborators(community_id)
        data_location = data_collabs['collaborators']

        coordinates = [(x[1], x[2], x[4], x[5], x[3], x[0]) for x in data_location]
        df = pd.DataFrame(coordinates, columns=['latitude', 'longitude', 'city', 'country', 
                                                'collaborator_name', 'clinical_trial_id'])

        map_chart = px.scatter_geo(df, lat="latitude", lon="longitude",
                     color="country", 
                     hover_name="city", 
                     hover_data={'latitude':False, 'longitude':False,
                                 "country":True, "collaborator_name":True, "clinical_trial_id":True},
                     projection="natural earth",
                     labels={"city": "Ciutat", "country": "País", "collaborator_name": "Nom del col·laborador",
                             "clinical_trial_id": "Estudi clínic"})
        
        register_widget("map_chart", map_chart)

        result = clinical_trials_per_communities[community_id]
        result.sort()
        result.insert(0, "All")
        ui.update_selectize(id="clinical_trials", choices=result, selected=community_id)
        ui.output_table("result_clinical_trials")
        ui.output_table("result_investigators")


    @output
    @render.table
    def result_investigators():        
        # Reload the table with the investigators of the community or a clinical trials.
        clinical_trial_id = input.clinical_trials()
        community_id = input.comunitats()
        data_collabs = get_collaborators(community_id)
        data_investigators = data_collabs['principal_investigator']

        if len(clinical_trial_id) > 4:
            investigators = [[x[1], x[2], x[3]] for x in data_investigators if x[0] == clinical_trial_id]
        else:
            investigators = [[x[1], x[2], x[3]] for x in data_investigators]

        return_investigators = []
        for investigator in investigators:
            name = investigator[0]
            role = investigator[1]
            affiliation = investigator[2]

            repeated = [x for x in return_investigators if x[0]==name and x[1]==role and x[2]==affiliation]
            if len(repeated)==0:
                return_investigators.append(investigator)

        return_investigators.sort()
        df = pd.DataFrame(return_investigators, columns=['Nom de l\'investigador', 'Rol', 'Organització afiliada'])
        
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
    def result_clinical_trials(): 
        # Reload the table with the sponsors of the community or a clinical trials.
        clinical_trial_id = input.clinical_trials()
        community_id = input.comunitats()
        data_collabs = get_collaborators(community_id)
        data_sponsors = data_collabs['sponsors']

        if len(clinical_trial_id) > 4:
            sponsors = [x[1] for x in data_sponsors if x[0] == clinical_trial_id]
        else:
            sponsors = [x[1] for x in data_sponsors]

        sponsors = list(set(sponsors))
        sponsors.sort()
        df = pd.DataFrame(sponsors, columns=['Patrocinadors'])
        
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
