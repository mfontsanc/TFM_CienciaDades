INSERT_DATA = """PREFIX tfm: <http://purl.org/net/TFM/communities#> 
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

INSERT DATA
{ GRAPH <http://purl.org/net/TFM/communities#> { 
%s
} }
"""

GET_CT_COM = """
PREFIX tfm: <http://purl.org/net/TFM/communities#>
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>
select DISTINCT ?ct_id ?comm_id where { 
    ?ct ocre:OCRE901005 ?ct_id_uri.
    ?ct_id_uri ocre:OCRE900242 ?ct_id.
    OPTIONAL{
        ?ct tfm:community_id ?comm_id.
    }
}
"""

GET_COMM_NAMES = """
PREFIX tfm: <http://purl.org/net/TFM/communities#>
select ?comm_id ?comm_name where { 
    ?comm_id tfm:community_name ?comm_name
}
"""

GET_CT_COMM_ID = """
PREFIX tfm: <http://purl.org/net/TFM/communities#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>
PREFIX ocre_protocol: <http://purl.org/net/OCRe/study_protocol.owl#>
select DISTINCT ?ct_id ?property_name ?object where { 
    {
        ?ct_id tfm:community_id %d ;
            ?property_study ?object.
        ?property_study rdfs:label ?property_name.
        FILTER(?property_study in (ocre:OCRE058000))
    }
    UNION
    {
        ?ct_id tfm:community_id %d ;
               ocre:OCRE900089 ?study_protocol.
        ?study_protocol ?property_protocol ?epoch.
        ?epoch ocre:OCRE900224 ?object.
        BIND("intervention" as ?property_name)
        FILTER(?property_protocol in (ocre_protocol:OCRE885707))
    }
    UNION
    {
        ?ct_id tfm:community_id %d ;
               ocre:OCRE900089 ?study_protocol.
        ?study_protocol ?property_protocol ?object.
        ?property_protocol rdfs:label ?property_name.
        FILTER(?property_protocol in (ocre:OCRE900086))
    }
    UNION    
    {
        ?ct_id tfm:community_id %d ;
            ?property_study ?object.
        BIND("keyword" as ?property_name)
        FILTER(?property_study in (ocre:OCRE900224))
    }
}
"""

GET_SPONSORS_COMM_ID = """
PREFIX tfm: <http://purl.org/net/TFM/communities#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>

select DISTINCT ?ct_id ?sponsor_name where { 
    ?ct_id tfm:community_id %d ;
        ?property_study ?sponsor.
    ?sponsor ocre:OCRE900224 ?sponsor_name
    FILTER(?property_study in(ocre:OCRE535519))
} 
"""

GET_PRINCIPAL_INVESTIGATOR_COMM_ID = """
PREFIX tfm: <http://purl.org/net/TFM/communities#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>

select DISTINCT ?ct_id ?investigator_name ?investigator_role ?investigator_affiliation where { 
    ?ct_id tfm:community_id %d ;
        ?property_study ?investigator.
    ?investigator ocre:OCRE900224 ?investigator_name;
                  ocre:OCRE900212 ?investigator_role;
                  ocre:OCRE900064 ?affiliation.
    ?affiliation ocre:OCRE900224 ?investigator_affiliation.
    FILTER(?property_study in(ocre:OCRE901006))
} 
"""

GET_LOCATION_COMM_ID = """
PREFIX tfm: <http://purl.org/net/TFM/communities#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>

select DISTINCT ?ct_id ?collaborator_name ?collaborator_city ?collaborator_country ?collaborator_zip where { 
    ?ct_id tfm:community_id %d ;
        ?property_study ?collaborator.
    ?collaborator ocre:OCRE400040 ?collaborator_city;
                  ocre:OCRE744000 ?collaborator_country;
                  ocre:OCRE885000 ?collaborator_zip.
    OPTIONAL{
        ?collaborator ocre:OCRE900224 ?collaborator_name.
    }
    FILTER(?property_study in(ocre:OCRE400076))
} 
"""

GET_CLINICAL_TRIAL_DATA_PROPERTIES = """
PREFIX tfm: <http://purl.org/net/TFM/communities#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>

select DISTINCT ?property_study ?object where { 
    {
        %s ?property_study ?object.
        FILTER(?property_study in(ocre:OCRE058000, ocre:OCRE189000, tfm:community_id, ocre:OCRE413000,
                ocre:OCRE900210, ocre:OCRE900211, ocre:OCRE900212, ocre:OCRE900213, ocre:OCRE900214,
                ocre:OCRE900237))
    }
    UNION
    {
        %s ?property_study ?design.
        ?design ocre:OCRE741000 ?phase.
        ?phase ocre:OCRE900224 ?object.
        FILTER(?property_study in (ocre:OCRE820850))
    }
    UNION
    {
        %s ?property_study ?recruitment.
        ?recruitment ocre:OCRE900224 ?object.
        FILTER(?property_study in (ocre:OCRE901007))
    }
} 
"""

GET_CLINICAL_TRIAL_KEYWORDS = """
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>

select DISTINCT ?property_study ?object where { 
    %s ?property_study ?object.
    FILTER(?property_study in (ocre:OCRE900224))
}
"""

GET_CLINICAL_TRIAL_LOCATIONS = """
PREFIX tfm: <http://purl.org/net/TFM/communities#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>

select DISTINCT ?collaborator_name ?collaborator_city ?collaborator_country ?collaborator_zip where { 
    %s ?property_study ?collaborator.
    ?collaborator ocre:OCRE400040 ?collaborator_city;
                  ocre:OCRE744000 ?collaborator_country;
                  ocre:OCRE885000 ?collaborator_zip.
    OPTIONAL{
        ?collaborator ocre:OCRE900224 ?collaborator_name.
    }
    FILTER(?property_study in(ocre:OCRE400076))
} 
"""

GET_CLINICAL_TRIAL_INVESTIGATORS = """
PREFIX tfm: <http://purl.org/net/TFM/communities#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>

select DISTINCT ?investigator_name ?investigator_role ?investigator_affiliation ?affiliation_city ?affiliation_country 
where { 
    %s ?property_study ?investigator.
    ?investigator ocre:OCRE900224 ?investigator_name;
                  ocre:OCRE900212 ?investigator_role;
                  ocre:OCRE900064 ?affiliation.
    ?affiliation ocre:OCRE900224 ?investigator_affiliation.
    OPTIONAL{
        ?affiliation ocre:OCRE400040 ?affiliation_city;
                     ocre:OCRE744000 ?affiliation_country.
    }
    FILTER(?property_study in(ocre:OCRE901006))
} 
"""

GET_CLINICAL_TRIAL_SPONSORS = """
PREFIX tfm: <http://purl.org/net/TFM/communities#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>

select DISTINCT ?sponsor_name where { 
    %s ?property_study ?sponsor.
    ?sponsor ocre:OCRE900224 ?sponsor_name
    FILTER(?property_study in(ocre:OCRE535519))
} 
"""

GET_CLINICAL_TRIAL_RESULTS = """
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>

select DISTINCT ?property_study ?object where { 
    %s ocre:OCRE738000 ?output.
    ?output ?property_study ?object.
    FILTER(?property_study in (ocre:OCRE000021, ocre:OCRE900214, ocre:OCRE900224))
}
"""

GET_CLINICAL_TRIAL_CRITERIA = """
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>

select DISTINCT ?property_study ?object where { 
    {
        %s ocre:OCRE900089 ?output.
        ?output ?property_study ?criterias.
        ?criterias ocre:OCRE900214 ?object.
        FILTER NOT EXISTS{?criterias ocre:OCRE900224 ?label.}
        FILTER(?property_study in (ocre:OCRE693433))
    }
    UNION
    {
        %s ocre:OCRE900089 ?output.
        ?output ?property_study ?criterias.
        ?criterias ocre:OCRE900214 ?data;
                   ocre:OCRE900224 ?label.
        BIND(concat(?label, ": ", ?data) as ?object)
        FILTER(?property_study in (ocre:OCRE693433))
    }
}
"""

GET_CLINICAL_TRIAL_INTERVENTION = """
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>
PREFIX ocre_protocol: <http://purl.org/net/OCRe/study_protocol.owl#>

select DISTINCT ?name ?description ?type where { 
    {
        %s ocre:OCRE900089 ?output.
        ?output ?property_study ?intervention.
        ?intervention ocre:OCRE900214 ?description;
                      ocre:OCRE900224 ?name;
                      ocre:OCRE900218 ?type.
        FILTER(?property_study in (ocre_protocol:OCRE885707))
    }
}
"""

GET_CLINICAL_TRIAL_CONDITION = """
PREFIX ocre: <http://purl.org/net/OCRe/OCRe.owl#>
PREFIX ocre_protocol: <http://purl.org/net/OCRe/study_protocol.owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

select DISTINCT ?condition where { 
    {
        %s ocre:OCRE900089 ?study_protocol.
        ?study_protocol ?property_protocol ?condition.
        FILTER(?property_protocol in (ocre:OCRE900086))
    }
}
"""