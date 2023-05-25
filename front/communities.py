from shiny import ui, module
import requests
import plotly.express as px
from shinywidgets import output_widget, register_widget
import pandas as pd
from pathlib import Path


API_URL = "http://127.0.0.1:5000/tfm-collaboration-network/v1/NetworkCollaboration/get_communities"
HEADERS = {
    "accept": "application/json",
    "Content-Type": "application/json",
}

def get_communities():
    """
        Method to retrieve all the communities of the database.

        Parameters:
            None

        Returns:
            Dataframe with all communities.
    """
    r=requests.post(url = API_URL, headers = HEADERS)
    
    return r.json()

def get_pie_ct_comm():
    """
        Method to get the number of clinical trials in a community and not in a community.

        Parameters:
            None

        Returns:
            Dataframe: Number of clinical trials per type (in/out of a community).
    """
    total_ct_orphans = [x for x in clinical_trials_communities if x[1] == -1]
    total_ct_community = [x for x in clinical_trials_communities if x[1] != -1]

    ct_bool = [['orphan', len(total_ct_orphans)], ['community', len(total_ct_community)]]
    return pd.DataFrame(ct_bool, columns =['type', 'num'])

def get_line_comm_number():
    """
        Method to get the number of clinical trials per community.

        Parameters:
            None

        Returns:
            Dataframe: Number of clinical trials per community.
    """
    comm_number = {}
    communities = list(set([x[1] for x in clinical_trials_communities if x[1] != -1]))

    for community in communities:
        number = len([x[0] for x in clinical_trials_communities if x[1] == community])

        if not comm_number.get(number):
            comm_number[number] = 0
        comm_number[number] += 1

    return pd.DataFrame(list(comm_number.items()), columns =['number_ct', 'number_comm'])

def get_similarities():
    """
        Method to get the number of similar clinical trials per clinical trials not in a community.

        Parameters:
            None

        Returns:
            Dataframe: Number of similar clinical trials.
    """
    filepath = Path(__file__).parent / "data/ct_no_community.csv"
    df = pd.read_csv(filepath, sep=';')
    df_sim = df['Similarity'].value_counts().to_frame().reset_index()
    return df_sim[1: len(df_sim)]
        
# Variables to load the data once the application starts.
clinical_trials_communities = get_communities()
df_ct_comm = get_pie_ct_comm()
df_comm_numb = get_line_comm_number()
ct_no_communities = get_similarities()

@module.ui
def community_ui():
    return ui.page_fluid(
        ui.panel_title("Resultats de la creació de les comunitats a partir dels estudis clínics"),

        ui.div("Per tal de crear les comunitats a partir dels estudis clínics, s'ha tingut en compte una sèrie de criteris: el tipus d'observació i/o intervenció, la condició de salut que s'està estudiant, i les paraules clau."),
        ui.div("La gran majoria d'estudis clínics no es troben dins d'una comunitat."),
        ui.br(),
        
        ui.layout_sidebar(
            ui.panel_sidebar("Estudis clínics amb o sense comunitat:", output_widget("pie")),
            
            ui.panel_main("Relació del nombre de comunitats amb el nombre d'estudis clínics dins de la comunitat:", output_widget("line")),
        ),

        ui.br(),
        ui.h6("Estudis clínics sense comunitat"),
        ui.div("Hi ha un total de 5,952 estudis clínics que no tenen cap altre estudi clínic similar. Per tant, hi ha 661 estudis clínics que tot i tenir altres estudis clínics similars, no s'han agrupat en cap comunitat."),
        output_widget("histogram"),

        ui.div("Perquè aquests estudis clínics no es troba en cap comunitat?")
)

@module.server
def community_server(input, output, session):
    pie_labels = ["Sense comunitat", "En una comunitat"]
    pie_chart = px.pie(df_ct_comm, values='num', names=pie_labels, color_discrete_sequence=px.colors.sequential.RdBu,
               labels={"num": "Número d'estudis clínics"})
    
    line_chart = px.scatter(df_comm_numb, x="number_ct", y="number_comm",
                            labels={"number_ct": "Número d'estudis clínics", "number_comm": "Número de comunitats"},
                            color_discrete_sequence=['rgb(178,24,43)'],
                            template="simple_white")
    
    histogram_chart = px.bar(ct_no_communities, y="Similarity", x='index', 
                             labels={"index": "Número d'estudis clínics similars", "Similarity": "Número d'estudis clínics"},
                             color_discrete_sequence=["rgb(103,0,31)"],
                             template="simple_white")

    register_widget("pie", pie_chart)
    register_widget("line", line_chart)
    register_widget("histogram", histogram_chart)
    