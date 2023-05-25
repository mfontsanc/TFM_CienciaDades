from shiny import App, ui
from communities import community_server, community_ui
from community_detail import community_detail_ui, community_detail_server
from clinical_trials import clinical_trials_ui, clinical_trials_server


app_ui = ui.page_fluid(
    ui.navset_tab_card(
        ui.nav(
            "Communitats", community_ui("community")
        ),
        ui.nav(
            "Communitats en detall", community_detail_ui("community_detail")
        ),
        ui.nav(
            "Estudis clínics", clinical_trials_ui("clinical_trials_details")
        ),
        id="tfm_tabset",
    ),
)


def server(input, output, session):
    community_server("community")
    community_detail_server("community_detail")
    clinical_trials_server("clinical_trials_details")


app = App(app_ui, server) 
