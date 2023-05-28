# TFM_CienciaDades
TFM - Màster ciència de dades - Maria Font Sánchez

## Instal·lació

### Entorn de treball

#### Python
El llenguatge utilitzat per a l'execució del codi és Python versió 3.9. 

Hi ha dos opcions per a instal·lar Python i les llibreries necessàries:
1. Instal·lació manual de Python tal i com s'especifica a la web oficial: https://www.python.org/downloads/. I posterior instal·lació de les llibreries que hi ha indicades en el següent fitxer YAML: https://github.com/mfontsanc/TFM_CienciaDades/blob/main/env/python_3.9.yaml.
2. Crear un nou entorn des del navegador d'Anaconda i importar el fitxer YAML: https://github.com/mfontsanc/TFM_CienciaDades/blob/main/env/python_3.9.yaml, on durant la importació s'instal·laran totes les llibreries del fitxer.

#### Jupyter Notebook
Si s'ha importat el fitxer YAML en l'entorn de treball d'Anaconda, Jupyter Notebook ja estarà també instal·lat.

En cas contrari, es pot instal·lar tal i com s'especifica en la web oficial: https://jupyter.org/install#jupyter-notebook

#### Entorn de desenvolupament Python
L'aplicació Python s'ha desenvolupat fent ús de l'entorn de desenvolupament IntelliJ IDEA: https://www.jetbrains.com/es-es/idea/. Tot i així, hi ha d'altres entorns de desenvolupament Python que poden ser utilitzats també.

#### Entorn de desenvolupament Shiny
L'aplicació web amb Shiny i Python s'ha desenvolupat fent ús de l'entorn Visual Studio Code: https://code.visualstudio.com/, instal·lant l'extensió Shiny for Python: https://marketplace.visualstudio.com/items?itemName=Posit.shiny-python que permet executar l'aplicació de forma més ràpida.

#### Base de dades NoSQL
La base de dades basada en graf utilitzada és la versió gratuïta de GraphDB: https://graphdb.ontotext.com/.


## Inicialització de les aplicacions

Realitzar el clonat de la branca "main" del codi: https://github.com/mfontsanc/TFM_CienciaDades/tree/main

#### Base de dades NoSQL
Iniciar GraphDB i crear un nou repositori:
1. Crear el repositori tal i com s'especifica en la documentació oficial: https://graphdb.ontotext.com/documentation/10.0/creating-a-repository.html, on l'identificador del repositori sigui "clinical_trials" i sense modificar les opcions per defecte.
2. Crear el repositori des del fitxer: https://github.com/mfontsanc/TFM_CienciaDades/blob/main/env/clinical_trials-config.ttl 

#### Aplicació Python
L'aplicació Python desenvolupada per aquest TFM es troba ubicada en la carpeta "application": https://github.com/mfontsanc/TFM_CienciaDades/tree/main/application.

Per tal d'executar el projecte, cal obrir-ho des de l'IntelliJ (o qualsevol altre entorn de desenvolupament Python) i inicialitzar la classe wsgi.py ubicada dins de la carpeta "src/dev".

Es pot comprovar que l'aplicació s'ha inicialitzar correctament accedint a: http://127.0.0.1:5000 

#### Aplicació web Shiny
L'aplicació web desenvolupada per aquest TFM es troba ubicada en la carpeta "front": https://github.com/mfontsanc/TFM_CienciaDades/tree/main/front. 

Per tal d'executar el projecte es pot fer des del mateix entorn Visual Studio Code: https://shiny.rstudio.com/py/docs/running-debugging.html#running-in-visual-studio-code. 

#### Jupyter Notebooks
Obrir el Jupyter Notebook i el fitxer prinicpal anomenat "TFM_Maria Font Sánchez.ipynb": https://github.com/mfontsanc/TFM_CienciaDades/blob/main/TFM_Maria%20Font%20S%C3%A1nchez.ipynb 

Des d'aquest fitxer es pot accedir a la resta de Notebooks i executar el codi de l'aplicació Python i inserir les dades.