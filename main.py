import dash.exceptions
import pandas as pd
import openpyxl as pxl
from dash import Dash, html, dcc, callback, Output, Input, State
import plotly.express as px
import numpy as np
import dash_ag_grid as dag
import dash_bootstrap_components as dbc
import dash_bootstrap_templates
from dash_bootstrap_templates import load_figure_template
from dash.exceptions import PreventUpdate
import gunicorn
import xlrd as xlrd

pd.options.mode.chained_assignment = None
pd.options.display.width= None
pd.options.display.max_columns= None
pd.set_option('display.max_rows', 3000)
pd.set_option('display.max_columns', 3000)

######################----DATA INLADEN VAN DE APOTHEKEN-----###############################################################################

# BUFFER DATAFRAMES
buffer_musselpark = pd.read_csv('musselpark_buffer.txt')
buffer_oosterhaar = pd.read_csv('oosterhaar buffer.txt')
buffer_wiljes = pd.read_csv('wiljes_buffer.txt')
buffer_helpman = pd.read_csv('helpman_buffer.txt')
buffer_oosterpoort = pd.read_csv('oosterpoort_buffer.txt')
buffer_hanzeplein = pd.read_csv('hanzeplein_buffer.txt')

buffer_kolommen = pd.read_excel('kolommen receptbuffer rapport.xlsx')
columns_buffer = buffer_kolommen.columns

buffer_hanzeplein.columns = columns_buffer
buffer_helpman.columns = columns_buffer
buffer_musselpark.columns = columns_buffer
buffer_oosterhaar.columns = columns_buffer
buffer_oosterpoort.columns = columns_buffer
buffer_wiljes.columns = columns_buffer

buffer_hanzeplein['apotheek'] = 'hanzeplein'
buffer_helpman['apotheek'] = 'helpman'
buffer_wiljes['apotheek'] = 'wiljes'
buffer_oosterpoort['apotheek'] = 'oosterpoort'
buffer_oosterhaar['apotheek'] = 'oosterhaar'
buffer_musselpark['apotheek'] = 'musselpark'

buffer_ag = pd.concat([buffer_hanzeplein, buffer_helpman, buffer_musselpark, buffer_oosterhaar, buffer_oosterpoort, buffer_wiljes])

# ASSORTIMENT DATAFRAMES

assortiment_hanzeplein = pd.read_csv('hanzeplein_assortiment.txt', encoding='latin-1')
assortiment_helpman = pd.read_csv('helpman_assortiment.txt', encoding='latin-1')
assortiment_musselpark = pd.read_csv('musselpark_assortiment.txt', encoding='latin-1')
assortiment_oosterhaar = pd.read_csv('oosterhaar_assortiment.txt')
assortiment_oosterpoort = pd.read_csv('oosterpoort_assortiment.txt', encoding='latin-1')
assortiment_wiljes = pd.read_csv('wiljes_assortiment.txt', encoding='latin-1')

assortiment_kolommen = pd.read_excel('Kolommen assortiment.xlsx')
columns_assortiment = assortiment_kolommen.columns

assortiment_hanzeplein.columns = columns_assortiment
assortiment_helpman.columns = columns_assortiment
assortiment_musselpark.columns = columns_assortiment
assortiment_oosterhaar.columns = columns_assortiment
assortiment_oosterpoort.columns = columns_assortiment
assortiment_wiljes.columns = columns_assortiment

assortiment_hanzeplein['apotheek'] = 'hanzeplein'
assortiment_helpman['apotheek'] = 'helpman'
assortiment_musselpark['apotheek'] = 'musselpark'
assortiment_oosterhaar['apotheek'] = 'oosterhaar'
assortiment_oosterpoort['apotheek'] = 'oosterpoort'
assortiment_wiljes['apotheek'] = 'wiljes'

assortiment_ag = pd.concat([assortiment_hanzeplein, assortiment_helpman, assortiment_musselpark, assortiment_oosterhaar, assortiment_oosterpoort, assortiment_wiljes])

# RECEPTVERWERKING DATAFRAMES

recept_hanzeplein = pd.read_csv('hanzeplein_recept.txt')
recept_helpman = pd.read_csv('helpman_recept.txt')
recept_musselpark = pd.read_csv('musselpark_recept.txt')
recept_oosterhaar = pd.read_csv('oosterhaar_recept.txt')
recept_oosterpoort = pd.read_csv('oosterpoort_recept.txt')
recept_wiljes = pd.read_csv('wiljes_recept.txt')

recept_kolommen = pd.read_excel('Kolommen receptverwerking.xlsx')
columns_recept = recept_kolommen.columns

recept_hanzeplein.columns = columns_recept
recept_helpman.columns = columns_recept
recept_musselpark.columns = columns_recept
recept_oosterhaar.columns = columns_recept
recept_oosterpoort.columns = columns_recept
recept_wiljes.columns = columns_recept

recept_hanzeplein['apotheek'] = 'hanzeplein'
recept_helpman['apotheek'] = 'helpman'
recept_musselpark['apotheek'] = 'musselpark'
recept_oosterhaar['apotheek'] = 'oosterhaar'
recept_oosterpoort['apotheek'] = 'oosterpoort'
recept_wiljes['apotheek'] = 'wiljes'

recept_ag = pd.concat([recept_hanzeplein, recept_helpman, recept_musselpark, recept_oosterhaar, recept_oosterpoort, recept_wiljes])

# WACHTTIJDEN DATAFRAMES

wacht_hanzeplein = pd.read_excel('2024 wachttijden hanzeplein.xlsx')    # nieuwe stijl
wacht_oosterpoort = pd.read_excel('2024 wachttijden oosterpoort.xlsx')  # nieuwe stijl
wacht_oosterhaar = pd.read_excel('2024 wachttijden oosterhaar.xlsx')    # nieuwe stijl
wacht_helpman = pd.read_excel('2024 wachttijden helpman.xlsx')          # oude stijl
wacht_wiljes = pd.read_excel('2024 wachttijden wiljes.xlsx')            # oude stijl
wacht_musselpark = pd.read_excel('2024 wachttijden musselpark.xlsx')    # oude stijl


# kolommmen oude stijl inrichten: 1: splitsen en hernoemen; 2: drop oorspronkelijk frame
#
wacht_helpman[['Datum', 'Nummer', 'Functie', 'Balie', 'Starttijd', 'Eindtijd','Wachttijd']] = wacht_helpman['Datum,"Ticket Nummer","Knop Keuze","Balie","Tijd Start","Tijd Aangenomen","Wachttijd in sec"'].str.split(',', expand=True)
wacht_helpman_1 = wacht_helpman.drop(columns=['Datum,"Ticket Nummer","Knop Keuze","Balie","Tijd Start","Tijd Aangenomen","Wachttijd in sec"'])

wacht_wiljes[['Datum', 'Nummer', 'Functie', 'Balie', 'Starttijd', 'Eindtijd','Wachttijd']] = wacht_wiljes['Datum,"Ticket Nummer","Knop Keuze","Balie","Tijd Start","Tijd Aangenomen","Wachttijd in sec"'].str.split(',', expand=True)
wacht_wiljes_1 = wacht_wiljes.drop(columns=['Datum,"Ticket Nummer","Knop Keuze","Balie","Tijd Start","Tijd Aangenomen","Wachttijd in sec"'])

wacht_musselpark[['Datum', 'Nummer', 'Functie', 'Balie', 'Starttijd', 'Eindtijd','Wachttijd']] = wacht_musselpark['Datum,"Ticket Nummer","Knop Keuze","Balie","Tijd Start","Tijd Aangenomen","Wachttijd in sec"'].str.split(',', expand=True)
wacht_musselpark_1 = wacht_musselpark.drop(columns=['Datum,"Ticket Nummer","Knop Keuze","Balie","Tijd Start","Tijd Aangenomen","Wachttijd in sec"'])

# dtypes matchen van de dataframes

# datum kolommen
wacht_helpman_1['Datum'] = pd.to_datetime(wacht_helpman_1['Datum'])
wacht_wiljes_1['Datum'] = pd.to_datetime(wacht_wiljes_1['Datum'])
wacht_musselpark_1['Datum'] = pd.to_datetime(wacht_musselpark_1['Datum'])


# Nummer kolom aanpasssen
wacht_helpman_1['Nummer'] = (wacht_helpman_1['Nummer'].str.replace('"','', regex=True)).astype(int)
wacht_wiljes_1['Nummer'] = (wacht_wiljes_1['Nummer'].str.replace('"','', regex=True)).astype(int)
wacht_musselpark_1['Nummer'] = (wacht_musselpark_1['Nummer'].str.replace('"','', regex=True)).astype(int)

# Functie kolom aanpasssen
wacht_helpman_1['Functie'] = (wacht_helpman_1['Functie'].str.replace('"','', regex=True)).astype(int)
wacht_wiljes_1['Functie'] = (wacht_wiljes_1['Functie'].str.replace('"','', regex=True)).astype(int)
wacht_musselpark_1['Functie'] = (wacht_musselpark_1['Functie'].str.replace('"','', regex=True)).astype(int)

# Balie kolom aanpasssen
wacht_helpman_1['Balie'] = (wacht_helpman_1['Balie'].str.replace('"','', regex=True)).astype(int)
wacht_wiljes_1['Balie'] = (wacht_wiljes_1['Balie'].str.replace('"','', regex=True)).astype(int)
wacht_musselpark_1['Balie'] = (wacht_musselpark_1['Balie'].str.replace('"','', regex=True)).astype(int)

# Wachttijd kolom aanpasssen
wacht_helpman_1['Wachttijd'] = (wacht_helpman_1['Wachttijd'].str.replace('"','', regex=True)).astype(int)
wacht_wiljes_1['Wachttijd'] = (wacht_wiljes_1['Wachttijd'].str.replace('"','', regex=True)).astype(int)
wacht_musselpark_1['Wachttijd'] = (wacht_musselpark_1['Wachttijd'].str.replace('"','', regex=True)).astype(int)

# Apotheek kolommen toevoegen
wacht_helpman_1['apotheek'] = 'helpman'
wacht_musselpark_1['apotheek'] = 'musselpark'
wacht_wiljes_1['apotheek'] = 'wiljes'
wacht_oosterhaar['apotheek'] = 'oosterhaar'
wacht_oosterpoort['apotheek'] = 'oosterpoort'
wacht_hanzeplein['apotheek'] = 'hanzeplein'


# samenvoegen van de dataframes tot één klanten dataframe

klanten_ag = pd.concat([wacht_helpman_1, wacht_wiljes_1, wacht_musselpark_1, wacht_oosterhaar, wacht_hanzeplein, wacht_oosterpoort])


# ZORGPRESTATIES VIA CGM DATAFRAME

hanzeplein_zorg = pd.read_csv('hanzeplein_zorg.txt')
oosterpoort_zorg = pd.read_csv('oosterpoort_zorg.txt')
helpman_zorg = pd.read_csv('helpman_zorg.txt')
wiljes_zorg = pd.read_csv('wiljes_zorg.txt')
oosterhaar_zorg = pd.read_csv('oosterhaar_zorg.txt')
musselpark_zorg = pd.read_csv('musselpark_zorg.txt')

# kolomnamen aanmaken
kolommen_zorg = pd.read_excel('Kolommen zorgprestaties.xlsx')
columns_zorg = kolommen_zorg.columns

# kolommen toevoegen aan dataframes
hanzeplein_zorg.columns = columns_zorg
oosterpoort_zorg.columns = columns_zorg
helpman_zorg.columns = columns_zorg
wiljes_zorg.columns = columns_zorg
oosterhaar_zorg.columns = columns_zorg
musselpark_zorg.columns = columns_zorg

# Apotheek kolommen toevoegen
hanzeplein_zorg['apotheek'] ='hanzeplein'
oosterpoort_zorg['apotheek'] = 'oosterpoort'
helpman_zorg['apotheek'] = 'helpman'
wiljes_zorg['apotheek'] = 'wiljes'
oosterhaar_zorg['apotheek'] = 'oosterhaar'
musselpark_zorg['apotheek'] = 'musselpark'

# Dataframes samenvoegen

zorg_ag = pd.concat([hanzeplein_zorg, oosterpoort_zorg, helpman_zorg, wiljes_zorg, oosterhaar_zorg, musselpark_zorg])

# TELEFONIE VIA HTML FREMA DATAFRAME
# let op! Dit is een extractie van de database van FREMA die al verwerkt is als een samenvatting. Later in het jaar moet je de html bestanden nog kunnen inlezen en verwerken op verschillende manieren

telefonie_ag = pd.read_excel('Telefoon ag.xlsx')
telefonie_ag['telefoon per dag (gem)'] = telefonie_ag['telefoon per dag (gem)'].astype(int)





# OVERZICHT DATA PER CATEGORIE

buffer_ag                       # Dit is de receptbuffer van alle AG Apotheken
assortiment_ag                  # Dit is het assortiment van alle AG Apotheken
recept_ag                       # Dit is de receptverwerking van alle AG Apotheken
klanten_ag                      # Dit is de q-manager date van patiënten die zich aan de balie van de apotheek melden
zorg_ag                         # Dit is daglijst van de gedeclareerde prestaties voor alle apotheken via CGM
telefonie_ag                    # Dit is het extract van het html bestand zoals aangeleverd door FREMA over het jaar 2024

##################################----EINDE DATA INLADEN APOTHEKEN------##################################################################################################



######--- TABBLAD 1: HET IN KAART BRENGEN VAN HET GERBUIK VAN DE SA APP ---- #############################################################################################

# stap 1: we gebruiken het dataframe van de receptbuffer

buffer_sa_app = buffer_ag.copy()

# maak een maand en jaar-kolom aan en sorteer op basis van datum de waarden

buffer_sa_app['ddDatumAanschrijving'] = pd.to_datetime(buffer_sa_app['ddDatumAanschrijving'])
buffer_sa_app['maand'] = buffer_sa_app['ddDatumAanschrijving'].dt.month
buffer_sa_app['jaar'] = buffer_sa_app['ddDatumAanschrijving'].dt.year
buffer_sa_app = buffer_sa_app.sort_values(by=['ddDatumAanschrijving'], ascending=True)

# maak filters om te markeren wat de SA APP bestellingen zijn
service_apotheek_app = buffer_sa_app['sdAfzenderAGB']=='WEBSHOP'
andere_recepten = buffer_sa_app['sdAfzenderAGB']!='WEBSHOP'

sa_app_conditie = [buffer_sa_app['sdAfzenderAGB']=='WEBSHOP', buffer_sa_app['sdAfzenderAGB']!='WEBSHOP']
sa_waarden = ['Service Apotheek APP', 'Recept/LS-recept']
buffer_sa_app['SA APP?'] = np.select(sa_app_conditie, sa_waarden, default='Recept/LS-recept')

# maak een telling per maand per apotheek van categorie SA APP

aantal_SA_verdeling = buffer_sa_app.groupby(by=['jaar', 'maand', 'apotheek', 'SA APP?'])['SA APP?'].count().to_frame('bestellingen per maand').reset_index()
aantal_SA_totaal = buffer_sa_app.groupby(by=['jaar', 'maand', 'apotheek'])['SA APP?'].count().to_frame('totaal per maand').reset_index()

# merge de twee dataframes



SA_merge = aantal_SA_verdeling.merge(aantal_SA_totaal[['jaar', 'maand', 'apotheek', 'totaal per maand']],
                                     how='left',
                                     left_on = ['jaar', 'maand', 'apotheek'],
                                     right_on = ['jaar', 'maand', 'apotheek'])

# filter de gewone recepten en het jaar eruit en bereken het percentage
SA_merge['% SA APP BESTELLINGEN'] = ((SA_merge['bestellingen per maand']/SA_merge['totaal per maand'])*100).astype(int)
geen_gewone_recepten = (SA_merge['SA APP?']!='Recept/LS-recept')

jaar_filter = (SA_merge['jaar']==2024)

SA_merge_1 = SA_merge.loc[geen_gewone_recepten & jaar_filter]

# maak er een plot van

SA_plot = px.line(SA_merge_1, x='maand', y= '% SA APP BESTELLINGEN', color='apotheek', text='% SA APP BESTELLINGEN', title='% BESTELLINGEN VIA DE SERVICE APOTHEEK APP IN DE RECEPTBUFFER')


######--- TABBLAD 2: CONTACTGEGEVENS CLIENTEN IN KAART ---- #############################################################################################

# Stap 1: We gebruiken het receptverwerkingsdataframe (contactgegevens, patiëntnr) .. de verstrekkingen van het afgelopen jaar
# Stap 2: Markeer wanneer er een email en

contact_ag = recept_ag.copy()

# benodigde kolommen erbij pakken en een jaar kolom aanmaken voor het filter

contact_ag_1 = contact_ag[['ddDatumRecept','ndPatientnr','sdEmail', 'Telefoon1', 'Telefoon2', 'apotheek']]

contact_ag_1['ddDatumRecept'] = pd.to_datetime(contact_ag_1['ddDatumRecept'])
contact_ag_1['jaar'] = contact_ag_1['ddDatumRecept'].dt.year

# maak van de telefoonnummers een nummer
contact_ag_1['Telefoon1'] = contact_ag_1['Telefoon1'].str.replace(r'\D+', '', regex=True)
contact_ag_1['Telefoon2'] = contact_ag_1['Telefoon2'].str.replace(r'\D+', '', regex=True)


# vervang NaN door 0 in email kolom, Telefoon1 en Telefoon2

contact_ag_1['sdEmail'] = contact_ag_1['sdEmail'].replace(np.nan, 0, regex=True)
contact_ag_1['Telefoon1'] = contact_ag_1['Telefoon1'].replace(np.nan, 0, regex=True)
contact_ag_1['Telefoon2'] = contact_ag_1['Telefoon2'].replace(np.nan, 0, regex=True)
contact_ag_1['Telefoon1'] = pd.to_numeric(contact_ag_1['Telefoon1'])
contact_ag_1['Telefoon2'] = pd.to_numeric(contact_ag_1['Telefoon2'])



# maak een kolom met email markering aan

conditie_contact_email = [
    contact_ag_1['sdEmail'] == 0,
    contact_ag_1['sdEmail'] != 0
]

waarden_contact_email = ['geen email aanwezig', 'email aanwezig']

contact_ag_1['email aanwezig?'] = np.select(conditie_contact_email, waarden_contact_email, default='??')

# Maak een kolom met een mobiel nummer markering aan

conditie_contact_mobiel = [
    ((contact_ag_1['Telefoon1'] >= 600000000) | (contact_ag_1['Telefoon2'] >= 600000000)),
    ((contact_ag_1['Telefoon1'] <= 600000000) & (contact_ag_1['Telefoon2'] <= 600000000))
    ]

waarden_contact_mobiel = ['mobiel nummer aanwezig', 'geen mobiel nummer']

contact_ag_1['mobiel aanwezig?'] = np.select(conditie_contact_mobiel, waarden_contact_mobiel, default='??')

# maak een kolom met GEEN CONTACTGEGEVENS AANWEZIG aan

conditie_contact_geen = [
    ((contact_ag_1['sdEmail'] == 0) & (contact_ag_1['Telefoon1'] == 0) & (contact_ag_1['Telefoon2'] == 0)),
    ((contact_ag_1['sdEmail'] != 0) | (contact_ag_1['Telefoon1'] != 0) | (contact_ag_1['Telefoon2'] != 0))
]

waarden_contact_geen = ['GEEN CONTACTGEGEVENS', 'CONTACTGEGEVENS AANWEZIG']

contact_ag_1['contactgegevens aanwezig?'] = np.select(conditie_contact_geen, waarden_contact_geen, default='??')

# dubbele patientnrs verwijderen voor het tellen van de juiste getallen
contact_ag_1 = contact_ag_1.drop_duplicates(subset=['ndPatientnr'], keep='first')

# filter voor het gekozen jaar

jaar_keuze = (contact_ag_1['jaar']==2024)

contact_ag_2 = contact_ag_1.loc[jaar_keuze]

###### GEEN CONTACTGEGEVENS BEGIN #########

# Nu maken we verdeling en totaal tellen
contact_aanwezig_verdeling = contact_ag_2.groupby(by=['apotheek', 'contactgegevens aanwezig?'])['contactgegevens aanwezig?'].count().to_frame('aantal verdeling').reset_index()
contact_aanwezig_totaal = contact_ag_2.groupby(by=['apotheek'])['contactgegevens aanwezig?'].count().to_frame('aantal totaal').reset_index()


geen_contact_merge = contact_aanwezig_verdeling.merge(contact_aanwezig_totaal[['apotheek', 'aantal totaal']],
                                 how='left',
                                 left_on='apotheek',
                                 right_on='apotheek')
# bereken het %
geen_contact_merge['% geen contactgegevens'] = ((geen_contact_merge['aantal verdeling']/geen_contact_merge['aantal totaal'])*100).astype(int)

#filter
alleen_patiënten_zonder_contactgegevens = (geen_contact_merge['contactgegevens aanwezig?']=='GEEN CONTACTGEGEVENS')
# laat alleen meting zien van mensen zonder contactgegevens
geen_contact_def = geen_contact_merge.loc[alleen_patiënten_zonder_contactgegevens]
# maak hiervan een bar-chart
contact_grafiek_1 = px.bar(geen_contact_def, x='apotheek', y='% geen contactgegevens')

###### GEEN CONTACTGEGEVENS EINDE #########

###### GEEN EMAILADRESSEN BEGIN ###########

# tellen verdeling en totaal
email_aanwezig_verdeling = contact_ag_2.groupby(by=['apotheek', 'email aanwezig?'])['email aanwezig?'].count().to_frame('aantal verdeling').reset_index()
email_aanwezig_totaal = contact_ag_2.groupby(by=['apotheek'])['email aanwezig?'].count().to_frame('aantal totaal').reset_index()

#merge

email_afwezig_merge = email_aanwezig_verdeling.merge(email_aanwezig_totaal[['apotheek', 'aantal totaal']],
                                                     how='left',
                                                     left_on='apotheek',
                                                     right_on='apotheek')
# bereken % tov totaal
email_afwezig_merge['% geen email aanwezig'] = ((email_afwezig_merge['aantal verdeling']/email_afwezig_merge['aantal totaal'])*100).astype(int)

# filter zodat je alleen de afwezige contactgegevens overhoudt
alleen_patienten_zonder_email = (email_afwezig_merge['email aanwezig?']=='geen email aanwezig')

# pas filter toe
email_afwezig = email_afwezig_merge.loc[alleen_patienten_zonder_email]

contact_grafiek_2 = px.bar(email_afwezig, x='apotheek', y='% geen email aanwezig', text_auto=True)

###### GEEN EMAILADRESSEN EINDE ###########

###### GEEN MOBIEL NUMMER BEGIN ###########

mobiel_aanwezig_verdeling = contact_ag_2.groupby(by=['apotheek', 'mobiel aanwezig?'])['mobiel aanwezig?'].count().to_frame('aantal verdeling').reset_index()
mobiel_aanwezig_totaal = contact_ag_2.groupby(by=['apotheek'])['mobiel aanwezig?'].count().to_frame('aantal totaal').reset_index()

mobiel_afwezig_merge = mobiel_aanwezig_verdeling.merge(mobiel_aanwezig_totaal[['apotheek', 'aantal totaal']],
                                                       how='left',
                                                       left_on='apotheek',
                                                       right_on='apotheek')

mobiel_afwezig_merge['% zonder mobiel nummer'] = ((mobiel_afwezig_merge['aantal verdeling']/mobiel_afwezig_merge['aantal totaal'])*100).astype(int)

#filter voor alleen zonder mobiel
alleen_patienten_zonder_mobiel_nummer = (mobiel_afwezig_merge['mobiel aanwezig?']=='geen mobiel nummer')

#filter toepassen
mobiel_afwezig = mobiel_afwezig_merge.loc[alleen_patienten_zonder_mobiel_nummer]

# maak een grafiek
contact_grafiek_3 = px.bar(mobiel_afwezig, x='apotheek', y='% zonder mobiel nummer', text_auto=True)

###### GEEN MOBIEL NUMMER EINDE ###########


######--- TABBLAD 3: % HERHAALSERVICE VOOR ALLE AG APOTHEKEN ---- #############################################################################################

# stappenplan

#stap 1. We hebben informatie nodig uit de receptverwerking
# stap 2. ReceptHerkomst laat zien welke regels afkomstig zijn uit een herhaalprofiel
# stap 3. We willen filteren wat niet relevant is: distributie, zorg, lsp, dienst.
# stap 4. We willen tellen wat het aantal regels is dat via hhs komt en wat het totaal aantal regels is. hier berekenen we een % van
# stap 5. Visualisatie: we willen laten zien per maand wat het % hhs is. We willen dat er in het dashboard kan worden gefilterd per jaar. We laten 1 Grafiek zien.
# stap 6. Visualisatie: wellicht goed om te laten zien hoeveel patiënten van de apotheek in die maand van medicatie zijn voorzien via de hhs.
# stap 7. Visualisatie: wellicht om te kunnen filteren op EU-verstrekkingen (vinkje aan/uit voor EU Verstrekkingen)--> met name nuttig voor hanzeplein

# Inlezen recept dataframe

HHS_AG = recept_ag.copy()

# Selecteer welke kolommen je wilt gebruiken voor het dataframe

HHS_AG_1 = HHS_AG[['ddDatumRecept', 'ReceptHerkomst',
       'ndReceptnummer', 'ndATKODE', 'sdEtiketNaam', 'ndAantal', 'sdMedewerkerCode',
       'Uitgifte','ndPatientnr', 'apotheek']]

# maak een maand kolom

HHS_AG_1['ddDatumRecept'] = pd.to_datetime(HHS_AG_1['ddDatumRecept'])
HHS_AG_1['maand'] = HHS_AG_1['ddDatumRecept'].dt.month
HHS_AG_1['jaar'] = HHS_AG_1['ddDatumRecept'].dt.year

# Filter op basis van het jaar
# jaar filter
jaar_filter_HHS = (HHS_AG_1['jaar']==2024)

#pas het filter toe
HHS_AG_2 = HHS_AG_1.loc[jaar_filter_HHS]

# maak nu filters aan voor het type recepten dat je niet wilt zien in je dataframe (distributie, dienst, zorg, LSP)

hhs_geen_distributie = (HHS_AG_2['ReceptHerkomst']!='D')
hhs_geen_dienst = (HHS_AG_2['ReceptHerkomst']!='DIENST')
hhs_geen_zorg = (HHS_AG_2['ReceptHerkomst']!='Z')
hhs_geen_LSP = (HHS_AG_2['sdMedewerkerCode']!='LSP')

# pas nu de filters toe
HHS_AG_3 = HHS_AG_2.loc[hhs_geen_distributie & hhs_geen_dienst & hhs_geen_zorg & hhs_geen_LSP]

# vanaf nu kun je het filter gaan toepassen voor wel/geen EU verstrekkingen als je dat wilt.!!!!!!!!!!!!!!!!!!!!!!!!!


# markeer de regels met O en R als gewoon recept
# markeer de regels met H als herhaalservice

hhs_condities = [
    HHS_AG_3['ReceptHerkomst']=='H',
    HHS_AG_3['ReceptHerkomst']!='H'
]

hhs_waarden = ['HERHAALSERVICE', 'GEWOON RECEPT']

HHS_AG_3['Herhaalservice regel?'] = np.select(hhs_condities, hhs_waarden, default='??')


# Nu ga je tellen per apotheek per maand wat het aantal verstrekkingen zijn vanuit HHS en het aantal totaal verstrekkingen

# Tel de verdeling
HHS_verdeling = HHS_AG_3.groupby(by=['maand', 'apotheek', 'Herhaalservice regel?'])['Herhaalservice regel?'].count().to_frame('aantal verdeling').reset_index()
# Tel het totaal
HHS_totaal = HHS_AG_3.groupby(by=['maand', 'apotheek'])['Herhaalservice regel?'].count().to_frame('aantal totaal').reset_index()

# merge beide dataframes

HHS_merge = HHS_verdeling.merge(HHS_totaal[['maand', 'apotheek', 'aantal totaal']],
                                how='left',
                                left_on=['maand', 'apotheek'],
                                right_on=['maand', 'apotheek'])

# maak een % kolom
HHS_merge['% Herhaalservice'] = ((HHS_merge['aantal verdeling']/HHS_merge['aantal totaal'])*100).astype(int)

# filter nu de gewone recepten eruit
# filter
hhs_alleen = (HHS_merge['Herhaalservice regel?']=='HERHAALSERVICE')

# pas filter toe
HHS_merge_1 = HHS_merge.loc[hhs_alleen]

# maak een grafiek
HHS_grafiek = px.line(HHS_merge_1, x='maand', y='% Herhaalservice', color='apotheek', text='% Herhaalservice', title='% HERHAALSERVICE TOV OVERIGE RECEPTUUR PER APOTHEEK (excl distributie)')


######--- TABBLAD 4: VERDELING LEVERINGEN PER APOTHEEK OVER HET JAAR ---- #############################################################################################

# het laten zien van de leveringen en het maken van onderscheid heeft alles te maken met het scheiden van de receptlocaties per apotheek.
# Het hoofddoel is om daar een scheiding in te maken met np.select

# Daarna moeten we (net als bij de andere dataframes zorgen dat er geen vervuiling in zit. Geen zorg, dienst of LSP-recepten. We kunnen in dit geval distributie erin
# laten omdat deze regels onderdeel zijn van een levering. Het echter wel handig om te werken met alleen scankopnrs zodat we per Recept aan het rekenen zijn.
# We gebruiken het receptverwerkingsdataframe als bron voor de gegevens.

# Stap 1. Selecteer nuttige kolommen uit het recept dataframe
# Stap 2. Bekijk de receptlocaties en geef met np select methode een markering van: KLUIS, BEZORGEN, HALEN aan alle regels.
# Stap 3. Daarna ga je de onnodige regels eruit filteren (zorg, dienst en LSP)
# Stap 4. Tel de scankopnrs per receptlocatie per apotheek
# Stap 5. Visualiseer in een taart-diagram
# Stap 6. Zet voor iedere apotheek een aparte taartdiagram klaar (maak 6 losse taartdiagrammen)
# Stap 7. Zet de callback klaar en beoordeel het dashboard

# maak een dataframe om mee te starten
levering = recept_ag.copy()

# maak een selectie van nuttige kolommen
levering_1 = levering[['ddDatumRecept', 'sdMedewerkerCode', 'ReceptHerkomst', 'cf', 'ScanNrKop', 'RecLocatie', 'RecLocatieCode', 'apotheek']]

# Maak een jaar en een maand-kolom aan
levering_1['ddDatumRecept'] = pd.to_datetime(levering_1['ddDatumRecept'])
levering_1['jaar'] = levering_1['ddDatumRecept'].dt.year
levering_1['maand'] = levering_1['ddDatumRecept'].dt.month

#bekijk de aparte dataframes van de apotheken en label de regels (musselpark, oosterhaar, wiljes, helpman, oosterpoort, hanzeplein)

mp = (levering_1['apotheek']=='musselpark')
oh = (levering_1['apotheek']=='oosterhaar')
wil = (levering_1['apotheek']=='wiljes')
hlp = (levering_1['apotheek']=='helpman')
op = (levering_1['apotheek']=='oosterpoort')
hzp = (levering_1['apotheek']=='hanzeplein')




mp_levering = levering_1.loc[mp]

#hernoem de nan locatie
mp_levering['RecLocatieCode'] = mp_levering['RecLocatieCode'].replace(np.nan,'halen', regex=True)

# maak de condities en labels aan voor MUSSELPARK

mp_levering_condities = [
    ((mp_levering['RecLocatieCode'] == 'PS24')|                                                                                                   # Kluis
     (mp_levering['RecLocatieCode'] =='BLIJPS24')|
     (mp_levering['RecLocatieCode'] =='PS24MP')),
    ((mp_levering['RecLocatieCode']=='BEZVR')|                                                                                                    # Bezorgen
    (mp_levering['RecLocatieCode']=='BEZMA')|
    (mp_levering['RecLocatieCode']=='LOCBBMA')|
    (mp_levering['RecLocatieCode']=='LOCBBDI')|
    (mp_levering['RecLocatieCode']=='BEZWO')|
    (mp_levering['RecLocatieCode']=='LOCAH')|
    (mp_levering['RecLocatieCode']=='LOCBBWO')|
    (mp_levering['RecLocatieCode']=='LOCBEUK')|
    (mp_levering['RecLocatieCode']=='BEZDO')|
    (mp_levering['RecLocatieCode']=='BEZDI')|
    (mp_levering['RecLocatieCode']=='LOCBBDO')|
    (mp_levering['RecLocatieCode']=='LOCZB')|
    (mp_levering['RecLocatieCode']=='LOCPHM')|
    (mp_levering['RecLocatieCode']=='LOCPHV')|
    (mp_levering['RecLocatieCode']=='LOCNOH')|
    (mp_levering['RecLocatieCode']=='BLIJBEZ')),
    ((mp_levering['RecLocatieCode']=='HALEN')|                                                                                                  # Halen
    (mp_levering['RecLocatieCode']=='LOXIS')|
    (mp_levering['RecLocatieCode']=='halen')),
    ((mp_levering['RecLocatieCode']=='BLIJHALEN')|                                                                                              # Uitdeelpost
    (mp_levering['RecLocatieCode']=='AZC'))
]

mp_levering_waarden = ['KLUIS', 'BEZORGEN', 'HALEN', 'UITDEELPOST']

mp_levering['Leverwijze'] = np.select(mp_levering_condities, mp_levering_waarden, default='??')

# maak de condities en labels aan voor OOSTERHAAR



oh_levering = levering_1.loc[oh]

# hernoem de locatiecode NaN
oh_levering['RecLocatieCode'] = oh_levering['RecLocatieCode'].replace(np.nan, 'halen',regex=True)

# Maak de labels aan: KLUIS, BEZORGEN, HALEN, UITDEELPOST

oh_levering_condities = [
    ((oh_levering['RecLocatieCode']=='PS24')|               # Kluis
    (oh_levering['RecLocatieCode']=='HARKPS24')|
    (oh_levering['RecLocatieCode']=='MEERSTAD')),
    ((oh_levering['RecLocatieCode']=='BEZORG')|              # Bezorgen
    (oh_levering['RecLocatieCode']=='HARKBEZ')),
    ((oh_levering['RecLocatieCode']=='halen')|              # Halen
    (oh_levering['RecLocatieCode']=='Halen')),
    (oh_levering['RecLocatieCode']=='HARKHAAL')             # Uitdeelpost


]

oh_levering_waarden = ['KLUIS', 'BEZORGEN', 'HALEN', 'UITDEELPOST']

oh_levering['Leverwijze'] = np.select(oh_levering_condities, oh_levering_waarden, default='??')

# label de regels van de wiljes

wil_levering = levering_1.loc[wil]

#hernoem de Nan locatie
wil_levering['RecLocatieCode'] = wil_levering['RecLocatieCode'].replace(np.nan, 'halen', regex=True)

wil_levering_condities = [
    ((wil_levering['RecLocatieCode']=='PS24W')|
    (wil_levering['RecLocatieCode']=='WIJERT')|
    (wil_levering['RecLocatieCode']=='SERVI')),
    ((wil_levering['RecLocatieCode']=='BEZW')|
    (wil_levering['RecLocatieCode']=='NOORD')),
    (wil_levering['RecLocatieCode']=='HALENW')|
    (wil_levering['RecLocatieCode']=='halen')|
    (wil_levering['RecLocatieCode']=='HALEN')
]

wil_levering_waarden = ['KLUIS', 'BEZORGEN', 'HALEN']

wil_levering['Leverwijze'] = np.select(wil_levering_condities, wil_levering_waarden, default='??')

# Label vanaf hier de regels van apotheek HELPMAN


hlp_levering = levering_1.loc[hlp]

#hernoem de nan waarden
hlp_levering['RecLocatieCode'] = hlp_levering['RecLocatieCode'].replace(np.nan, 'halen', regex=True)


hlp_levering_condities = [
    ((hlp_levering['RecLocatieCode']=='PS24HE')|
    (hlp_levering['RecLocatieCode']=='PS24WIJ')),
    ((hlp_levering['RecLocatieCode']=='BEZHE')|
    (hlp_levering['RecLocatieCode']=='BWH')|
    (hlp_levering['RecLocatieCode']=='DACOSTA')|
    (hlp_levering['RecLocatieCode']=='COSIS')),
    ((hlp_levering['RecLocatieCode']=='HALENHE')|
    (hlp_levering['RecLocatieCode']=='HALENW')|
    (hlp_levering['RecLocatieCode']=='halen'))

]

hlp_levering_waarden = ['KLUIS', 'BEZORGEN', 'HALEN']


hlp_levering['Leverwijze'] = np.select(hlp_levering_condities, hlp_levering_waarden, default='??')

# Label de waarden van apotheek OOSTERPOORT

op_levering = levering_1.loc[op]

# hernoem de NaN-waarden
op_levering['RecLocatieCode'] = op_levering['RecLocatieCode'].replace(np.nan, 'halen', regex=True)

op_levering_condities = [
    (op_levering['RecLocatieCode']=='PS24'),                # Kluis
    ((op_levering['RecLocatieCode']=='BEZ')|                # Bezorgen
    (op_levering['RecLocatieCode']=='HAMRIK')|
    (op_levering['RecLocatieCode']=='PELSTER')),
    ((op_levering['RecLocatieCode']=='HALEN')|              # Halen
    (op_levering['RecLocatieCode']=='halen')|
    (op_levering['RecLocatieCode']=='APLOP'))

]


op_levering_waarden = ['KLUIS', 'BEZORGEN', 'HALEN']

op_levering['Leverwijze'] = np.select(op_levering_condities, op_levering_waarden, default= '??')

# Label nu de leveringen van apotheek HANZEPLEIN

hzp_levering = levering_1.loc[hzp]

# hernoem de NaN waarden
hzp_levering['RecLocatieCode'] = hzp_levering['RecLocatieCode'].replace(np.nan, 'halen', regex=True)

hzp_levering_condities = [
    ((hzp_levering['RecLocatieCode']=='PS24')|                      # Kluis
    (hzp_levering['RecLocatieCode']=='RADE')),
    ((hzp_levering['RecLocatieCode']=='LOCMA')|                     # Bezorgen
     (hzp_levering['RecLocatieCode']=='BEZ')|
     (hzp_levering['RecLocatieCode']=='LOCWO')|
     (hzp_levering['RecLocatieCode']=='LOCVNN')|
     (hzp_levering['RecLocatieCode']=='LOCDI')|
     (hzp_levering['RecLocatieCode']=='LOCDO')|
     (hzp_levering['RecLocatieCode']=='LOCVR')),
    ((hzp_levering['RecLocatieCode']=='halen')|                     # Halen
    (hzp_levering['RecLocatieCode']=='HALEN')|
     (hzp_levering['RecLocatieCode']=='LOCBA'))
]

hzp_levering_waarden = ['KLUIS', 'BEZORGEN', 'HALEN']

hzp_levering['Leverwijze'] = np.select(hzp_levering_condities, hzp_levering_waarden, default='??')


# Voeg de levering dataframes samen, zodat je kan gaan filteren en tellen

levering_3 = pd.concat([hzp_levering, op_levering, hlp_levering, wil_levering, oh_levering, mp_levering])

# nu gaan we de bagger eruit filteren ( zorg, dienst-recepten en LSP-recepten, eventueel ook Distributie-regels)


geen_zorg_levering = (levering_3['ReceptHerkomst']!='Z')
geen_dienst_levering = (levering_3['ReceptHerkomst']!='DIENST')
geen_LSP_levering = (levering_3['sdMedewerkerCode']!='LSP')
geen_distributie_levering = (levering_3['ReceptHerkomst']!='D')

levering_4 = levering_3.loc[geen_zorg_levering & geen_dienst_levering & geen_LSP_levering & geen_distributie_levering]

# gooi hier het jaarfilter overheen
jaar_filter_levering = (levering_4['jaar']==2024)                       # FILTER VOOR HET JAAR

levering_5 = levering_4.loc[jaar_filter_levering]


# ga nu tellen per maand per apotheek

levering_verdeling = levering_5.groupby(by=['maand', 'apotheek', 'Leverwijze'])['Leverwijze'].count().to_frame('aantal verdeling').reset_index()
levering_totaal = levering_5.groupby(by=['maand', 'apotheek'])['Leverwijze'].count().to_frame('aantal totaal').reset_index()

levering_merge = levering_verdeling.merge(levering_totaal[['maand', 'apotheek', 'aantal totaal']],
                                          how='left',
                                          left_on=['maand', 'apotheek'],
                                          right_on=['maand', 'apotheek'])
levering_merge['%'] = ((levering_merge['aantal verdeling']/levering_merge['aantal totaal'])*100).astype(int)

# Nu kunnen we voor iedere apotheek een bar graph dataframe maken

hanzeplein_levering_filter = (levering_merge['apotheek']=='hanzeplein')
oosterpoort_levering_filter = (levering_merge['apotheek']=='oosterpoort')
helpman_levering_filter = (levering_merge['apotheek']=='helpman')
wiljes_levering_filter = (levering_merge['apotheek']=='wiljes')
oosterhaar_levering_filter = (levering_merge['apotheek']=='oosterhaar')
musselpark_levering_filter = (levering_merge['apotheek']=='musselpark')

hanzeplein_levering_data = levering_merge.loc[hanzeplein_levering_filter]
oosterpoort_levering_data = levering_merge.loc[oosterpoort_levering_filter]
helpman_levering_data = levering_merge.loc[helpman_levering_filter]
wiljes_levering_data = levering_merge.loc[wiljes_levering_filter]
oosterhaar_levering_data = levering_merge.loc[oosterhaar_levering_filter]
musselpark_levering_data = levering_merge.loc[musselpark_levering_filter]

hanzeplein_levering_grafiek = px.bar(hanzeplein_levering_data,
                                     x='maand',
                                     y='%',
                                     color='Leverwijze',
                                     text_auto=True,
                                     title='Overzicht verdeling leveringen apotheek Hanzeplein')

oosterpoort_levering_grafiek = px.bar(oosterpoort_levering_data,
                                     x='maand',
                                     y='%',
                                     color='Leverwijze',
                                     text_auto=True,
                                     title='Overzicht verdeling leveringen apotheek Oosterpoort')

helpman_levering_grafiek = px.bar(helpman_levering_data,
                                     x='maand',
                                     y='%',
                                     color='Leverwijze',
                                     text_auto=True,
                                     title='Overzicht verdeling leveringen apotheek Helpman')

wiljes_levering_grafiek = px.bar(wiljes_levering_data,
                                     x='maand',
                                     y='%',
                                     color='Leverwijze',
                                     text_auto=True,
                                     title='Overzicht verdeling leveringen apotheek de Wiljes')

oosterhaar_levering_grafiek = px.bar(oosterhaar_levering_data,
                                     x='maand',
                                     y='%',
                                     color='Leverwijze',
                                     text_auto=True,
                                     title='Overzicht verdeling leveringen apotheek Oosterhaar')

musselpark_levering_grafiek = px.bar(musselpark_levering_data,
                                     x='maand',
                                     y='%',
                                     color='Leverwijze',
                                     text_auto=True,
                                     title='Overzicht verdeling leveringen apotheek Musselpark')

######--- TABBLAD 5: ZORGPRESTATIES OVER HET JAAR ---- #############################################################################################

# we maken lijn-grafieken waarin we kunnen zien hoe iedere apotheek het doet met betrekking tot het declareren van de prestaties.
# een lijngrafiek van consulten, ontslagbegeleiding, MBO's, inhalatie instructies, etc..
# wellicht ook een lijndiagram waarin we de omzetontwikkeling hiervan per apotheek kunnen volgen zoals dat in CGM gedeclareerd wordt.
# Stap 1. Rubricering mogelijk maken per maand
# Stap 2. Tellen van de prestaties per maand per apotheek
# Stap 3. Per maand het totaalbedrag optellen van hetgeen er is ingediend via CGM.
# Stap 4. Uitzetten in verschillende lijndiagrammen

zorgprestaties = zorg_ag.copy()


zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace('Farmaceutisch consult bij zorgvraag patient', 'Consult', regex=True)
zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace('Farmaceutische begeleiding i.v.m. ontslag uit het ziekenhuis', 'Ontslag', regex=True)
zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace('Medicatieoptimalisatie en begeleiding bij pati nten met de ziekte van Parkinson', 'Parkinson', regex=True)
zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace('Begeleiding en verbeteren van geneesmiddelengebruik in samenwerking met de huisarts', 'Verbetering gebruik', regex=True)
zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace('Medicatiebeoordeling chronisch UR geneesmiddelengebruik', 'MBO', regex=True)
zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace('Medicatiebeoordeling chronisch UR geneesmiddelengebruik, thuis', 'MBO thuis', regex=True)
zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace('Instructie UR geneesmiddel gerelateerd hulpmiddel', 'hulpm instructie', regex=True)
zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace('Standaardterhandstelling - niet afleveren na overleg met arts/patient', 'Niet afleveren', regex=True)
zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace('Farmaceutische begeleiding bij dagbehandeling/polikliniekbezoek', 'Poli-bezoek', regex=True)

# maak een maand en jaar kolom aan
zorgprestaties['PrestatieDatum'] = pd.to_datetime(zorgprestaties['PrestatieDatum'])
zorgprestaties['maand'] = zorgprestaties['PrestatieDatum'].dt.month
zorgprestaties['jaar'] = zorgprestaties['PrestatieDatum'].dt.year

# Gooi hier nu een jaar-filter overheen

jaar_filter_zorgprestaties = (zorgprestaties['jaar']==2024)

# pas jaarfilter toe

zorgprestaties_1 = zorgprestaties.loc[jaar_filter_zorgprestaties]

# Ga nu tellen hoeveel prestaties er per maand per apotheek worden gedeclareerd
zorgprestatie_telling = zorgprestaties_1.groupby(by=['maand', 'apotheek','Prestatie','PrestatieOmschrijving'])['PrestatieOmschrijving'].count().to_frame('aantal').reset_index()
zorgprestatie_omzet = zorgprestaties_1.groupby(by=['maand', 'apotheek', 'Prestatie','PrestatieOmschrijving'])['BedragIncl'].sum().to_frame('omzet').reset_index()

zorgprestatie_telling_groep = zorgprestaties_1.groupby(by=['Prestatie', 'PrestatieOmschrijving'])['PrestatieOmschrijving'].count().to_frame('aantal').reset_index()
zorgprestatie_omzet_groep = zorgprestaties_1.groupby(by=['Prestatie','PrestatieOmschrijving'])['BedragIncl'].sum().to_frame('omzet').reset_index()

zorgprestatie_telling_groep_1 = zorgprestatie_telling_groep.sort_values(by=['aantal'], ascending=False)
zorgprestatie_omzet_groep_1 = zorgprestatie_omzet_groep.sort_values(by=['omzet'], ascending=False)

zorgprestatie_telling_groep_2 = zorgprestatie_telling_groep_1.nlargest(n=5, columns=['aantal'])
zorgprestatie_omzet_groep_2 = zorgprestatie_omzet_groep_1.nlargest(n=5, columns=['omzet'])



zorgprestatie_telling_groep_1_grafiek = px.bar(zorgprestatie_telling_groep_2, x='PrestatieOmschrijving', y='aantal', text_auto=True, title='TOTAAL AANTAL GEDECLAREERDE ZORGPRESTATIES VANUIT CGM')
zorgprestatie_omzet_groep_1_grafiek = px.bar(zorgprestatie_omzet_groep_2, x='PrestatieOmschrijving', y='omzet', text_auto=True, title='TOTAAL GEDECLAREERDE OMZET ZORGPRESTATIES VANUIT CGM')


# Nu gaan we per prestatie de apotheken vergelijken op aantallen declaraties per maand

# consulten
consulten_alleen = (zorgprestatie_telling['Prestatie']==71014)
ontslag_alleen = (zorgprestatie_telling['Prestatie']==70006)
MBO_alleen = (zorgprestatie_telling['Prestatie']==70002)

consulten = zorgprestatie_telling.loc[consulten_alleen]
ontslag = zorgprestatie_telling.loc[ontslag_alleen]
MBO = zorgprestatie_telling.loc[MBO_alleen]

consulten_grafiek = px.line(consulten, x='maand', y='aantal', color='apotheek', text='aantal', title='AANTAL CONSULTDECLARATIES PER MAAND PER APOTHEEK VIA CGM')
ontslag_grafiek = px.line(ontslag, x='maand', y='aantal', color='apotheek', text='aantal', title='AANTAL ONTSLAG-PRESTATIES PER MAAND PER APOTHEEK VIA CGM')
mbo_grafiek = px.line(MBO, x='maand', y='aantal', color='apotheek', text='aantal', title='AANTAL MBO DECLARATIES PER MAAND PER APOTHEEK VIA CGM')

# facultatief cumulatieve omzet zorgprestaties berekenen



# Grafieken overzicht
zorg_telling_ag = zorgprestatie_telling_groep_1_grafiek     # grafiek 1
zorg_omzet_ag = zorgprestatie_omzet_groep_1_grafiek         # grafiek 2
consulten_grafiek                                           # grafiek 3
ontslag_grafiek                                             # grafiek 4
mbo_grafiek                                                 # grafiek 5

######--- TABBLAD 6: WACHTTIJDEN OVER HET JAAR ---- #############################################################################################
# we willen weten hoeveel klanten per dag er in de apotheek gemiddeld komen.
# we willen weten hoe de druk verdeeld is bij alle apotheken over de uren van de dag
# dit betekend dat we een telling moeten doen van het aantal patienten per uur en per werkdag.
# vervolgens zullen we deze moeten middelen.
# we moeten een gemiddelde berekenen van de som van het aantal uren per werkdag.

wacht_ag = klanten_ag.copy()

# maak eerst een uur kolom aan
wacht_ag['Starttijd'] = wacht_ag['Starttijd'].replace('"','', regex=True)
wacht_ag['Starttijd'] = pd.to_datetime(wacht_ag['Starttijd'], format='%H:%M:%S')
wacht_ag['uur'] = wacht_ag['Starttijd'].dt.hour
wacht_ag['jaar'] = wacht_ag['Datum'].dt.year

# maak daarna een week vd dag kolom aan
wacht_ag['weekdagnr'] = wacht_ag['Datum'].dt.weekday

# maak labels voor de weekdagen
conditie_klanten_weekdag = [
    (wacht_ag['weekdagnr']==0),
    (wacht_ag['weekdagnr']==1),
    (wacht_ag['weekdagnr']==2),
    (wacht_ag['weekdagnr']==3),
    (wacht_ag['weekdagnr']==4),
    (wacht_ag['weekdagnr']==5),
    (wacht_ag['weekdagnr']==6)
]

waarden_klanten_weekdag = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag']

wacht_ag['weekdag naam'] = np.select(conditie_klanten_weekdag, waarden_klanten_weekdag, default='???')

wacht_jaar_filter = (wacht_ag['jaar']==2024)                # JAARFILTER
weekdagen = (wacht_ag['weekdagnr']<5)

wacht_ag_werkdagen = wacht_ag.loc[weekdagen & wacht_jaar_filter]

# Nu gaan we tellingen doen
# Voor de tellingen per uur hebben we nodig hoeveel keer er (bijv) een 8 voorkomt per individuele dag
# Daarna moeten we dat delen door het aantal dagen in totaal dat voorkomt in het dataframe
# Bovenstaande moet per apotheek
# Voor het aantal tellingen per dag per apotheek gaan we nu een groupby doen

# We berekenen per apotheek hoeveel uur-notities er zijn (zijn klanten)
# Daarna berekenen we over hoeveel dagen deze notities verdeeld moeten worden = ontdubbeling data en tellen

# Het aantal losse dagen berekenen
aantal_dagen_frame = wacht_ag_werkdagen.drop_duplicates(subset=['Datum'], keep='first')

weekdagen_aantal = aantal_dagen_frame.groupby(by=['weekdag naam'])['weekdag naam'].count().to_frame('aantal dagen').reset_index()


aantal_dagen = len(aantal_dagen_frame)


telling_wacht_uren = wacht_ag_werkdagen.groupby(by=['apotheek', 'uur'])['uur'].count().to_frame('aantal').reset_index()
telling_wacht_uren['aantal dagen'] = aantal_dagen
telling_wacht_uren['klanten per uur (gem)'] = (telling_wacht_uren['aantal']/telling_wacht_uren['aantal dagen']).astype(int)

# maak de grafiek
klanten_per_uur_grafiek = px.line(telling_wacht_uren, x='uur', y='klanten per uur (gem)', color='apotheek', text='klanten per uur (gem)' , title='GEMIDDELD AANTAL KLANTEN PER UUR')

# Doe nu hetzelfde, maar dan met de weekdagen

telling_klanten_per_weekdag_totaal = wacht_ag_werkdagen.groupby(by=['apotheek', 'weekdagnr' ,'weekdag naam'])['weekdag naam'].count().to_frame('aantal').reset_index()

telling_klanten_per_weekdag_totaal_1 = telling_klanten_per_weekdag_totaal.sort_values(by=['weekdagnr'], ascending=True)
# merge de dataframes zodat je kan gaan rekenen

telling_klanten_per_weekdag_totaal_merge = telling_klanten_per_weekdag_totaal.merge(weekdagen_aantal[['weekdag naam', 'aantal dagen']],
                                         how='left',
                                         left_on='weekdag naam',
                                         right_on='weekdag naam')

telling_klanten_per_weekdag_totaal_merge['gem klanten per werkdag'] = (telling_klanten_per_weekdag_totaal_merge['aantal']/telling_klanten_per_weekdag_totaal_merge['aantal dagen']).astype(int)


klanten_per_werdag_grafiek = px.line(telling_klanten_per_weekdag_totaal_merge, x='weekdag naam', y='gem klanten per werkdag', color='apotheek', title='GEMIDDELD AANTAL KLANTEN PER WERKDAG', text='gem klanten per werkdag')


# overzicht grafieken voor benchmark

klanten_per_werdag_grafiek                  # grafiek met gemiddeld aantal klanten per werkdag
klanten_per_uur_grafiek                     # grafiek met gemiddeld aantal klanten per uur per werkdag


# klanten_per_uur_grafiek.show()
# klanten_per_werdag_grafiek.show()

######--- TABBLAD 7: TELEFONIE OVER HET JAAR ---- #############################################################################################

telefoon = telefonie_ag.copy()

# dataframe is klaar.. maak een grafiek
jaar_filter_telefoon = (telefoon['jaar'] == 2024)

telefoon_1 = telefoon.loc[jaar_filter_telefoon]

telefoon_grafiek = px.bar(telefoon_1, x='Apotheek', y='telefoon per dag (gem)', text_auto=True, title='AANTAL BINNENKOMENDE TELEFOONTJES PER DAG (GEM) PER APOTHEEK')


######--- TABBLAD 7: SERVICEGRAAD OVER HET JAAR ---- #############################################################################################

service = recept_ag.copy()


service_1 = service[['ddDatumRecept', 'ReceptHerkomst', 'cf',
       'ndReceptnummer', 'sdATCODE', 'ndATKODE', 'sdEtiketNaam',
                     'ndAantal', 'Uitgifte', 'ndVoorraadTotaal',
                     'apotheek', 'sdMedewerkerCode']]

# kolommen aanmaken voor maand en jaar
service_1['ddDatumRecept'] = pd.to_datetime(service_1['ddDatumRecept'])
service_1['jaar'] = service_1['ddDatumRecept'].dt.year
service_1['maand'] = service_1['ddDatumRecept'].dt.month

# kolom maken voor markering door voorraad 0

service_1['voorraad na aanschrijven'] = service_1['ndVoorraadTotaal'] - service_1['ndAantal']

# Markeer iedere regel als defectuur of voorraad toereikend

conditie_service = [
    service_1['voorraad na aanschrijven'] >=0,
    service_1['voorraad na aanschrijven'] <0
]

waarden_service = ['voorraad toereikend', 'defectuur']

service_1['voorraad toereikend?'] = np.select(conditie_service, waarden_service, default='??')

# filter uit het dataframe Dienst, Zorg, Distributie, Herhaalservice ,LSP-recepten, CF-recepten

geen_dienst_service = (service_1['ReceptHerkomst']!='DIENST')
geen_zorg_service = (service_1['ReceptHerkomst']!='Z')
geen_distributie_service = (service_1['ReceptHerkomst']!='D')
geen_LSP_service = (service_1['sdMedewerkerCode']!='LSP')
geen_cf_service = (service_1['cf']!='J')
geen_hhs_service = (service_1['ReceptHerkomst']!='H')
geen_onbekende_voorraad = (service_1['voorraad toereikend?']!='??')
jaar_filter_service = (service_1['jaar']==2024)                                 # Dit is het filter voor de callback

# Bouw hier een filter in voor: EU, EU & TU, Alles of spoedmedicatie
filter_callback_optie_1 = (service_1['Uitgifte'] == 'EU')
filter_callback_optie_2 = ((service_1['Uitgifte'] == 'EU') | (service_1['Uitgifte']=='TU'))
filter_callback_optie_3 = ((service_1['Uitgifte'] == 'EU') | (service_1['Uitgifte']=='TU') | (service_1['Uitgifte']=='VU'))
filter_callback_optie_4 = ((service_1['sdATCODE'])=='')

# pas filters toe op het dataframe

service_2 = service_1.loc[geen_dienst_service &
                          geen_zorg_service &
                          geen_distributie_service &
                          geen_LSP_service &
                          geen_cf_service &
                          geen_cf_service &
                          geen_hhs_service &
                          geen_onbekende_voorraad &
                          jaar_filter_service & filter_callback_optie_3]




# print(service_2['Uitgifte'].unique())

# Nu tellen we per maand, per apotheek het aantal toereikend voorraad regels

service_tellen_verdeling = service_2.groupby(by=['maand', 'apotheek', 'voorraad toereikend?'])['voorraad toereikend?'].count().to_frame('aantal verdeling').reset_index()
service_tellen_totaal = service_2.groupby(by=['maand', 'apotheek'])['voorraad toereikend?'].count().to_frame('aantal totaal').reset_index()

service_tellen_merge = service_tellen_verdeling.merge(service_tellen_totaal[['maand','apotheek', 'aantal totaal']],
                                                      how='left',
                                                      left_on= ['maand', 'apotheek'],
                                                      right_on = ['maand', 'apotheek'])

service_tellen_merge['%'] = ((service_tellen_merge['aantal verdeling']/service_tellen_merge['aantal totaal'])* 100).astype(int)

voorraad_toereikend = (service_tellen_merge['voorraad toereikend?']=='voorraad toereikend')

servicegraad = service_tellen_merge.loc[voorraad_toereikend]

servicegraad_grafiek = px.line(servicegraad, x='maand', y='%', color='apotheek', text='%' ,title='SERVICEGRAAD PER MAAND AG')






























# APP

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dcc.Tabs([
        dcc.Tab(label='Service Apotheek APP', children=[                                                                    # TABBLAD 1: SA APP
            dbc.Row([
                html.H1('Service Apotheek APP gebruik')
            ]),
            dbc.Row([
                dbc.Col([dcc.Dropdown(id='SA APP jaar', options=SA_merge['jaar'].unique(), value=SA_merge['jaar'].max())], width=3),
                dbc.Col([], width=9)]),
            dbc.Row([dcc.Graph(id='SA APP gebruik')]),
            dbc.Row([])
        ]),

        dcc.Tab(label='Contactgegevens cliënten', children=[                                                                # TABBLAD 2: Contactgegevens
            dbc.Row([
                html.H1('Overzicht contactgegevens patiënten apotheek')
            ]),
            dbc.Row([
                dbc.Col([dcc.Dropdown(id='contactgegevens jaar', options=contact_ag_1['jaar'].unique(), value=contact_ag_1['jaar'].max())]),
                dbc.Col([], width=9)
            ]),
            dbc.Row([
                dcc.Graph(id='geen contactgegevens AG')
            ]),
            dbc.Row([
                dcc.Graph(id='email afwezig AG')
            ]),
            dbc.Row([
                dcc.Graph(id='mobiel nummer afwezig AG')
            ]),
        ]),

        dcc.Tab(label='Herhaalservice', children=[                                                                          # TABBLAD 3: HERHAALSERVICE
            dbc.Row([html.H1('Overzicht % HHS-regels tov totaal receptuur (ex Distributie)')]),
            dbc.Row([
                dbc.Col([dcc.Dropdown(id='jaar hhs', options=HHS_AG_1['jaar'].unique(), value=HHS_AG_1['jaar'].max())]),
                dbc.Col([], width=9)
            ]),
            dbc.Row([dcc.Graph(id='HHS% AG')]),
            dbc.Row([]),
        ]),
        dcc.Tab(label='Leveringen cliënten', children=[
            dbc.Row([html.H1('Overzicht van het type levering per apotheek (Halen, Kluis, Bezorgen)')]),
            dbc.Row([
                dbc.Col([dcc.Dropdown(id='levering jaar', options=levering_4['jaar'].unique(), value=levering_4['jaar'].max()),
                dbc.Col([], width=9),
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id='levering hanzeplein')]),
                dbc.Col([dcc.Graph(id='levering oosterpoort')]),
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id='levering helpman')]),
                dbc.Col([dcc.Graph(id='levering wiljes')]),
            ]),
            dbc.Row([
                dbc.Col([dcc.Graph(id='levering oosterhaar')]),
                dbc.Col([dcc.Graph(id='levering musselpark')]),
            ]),
        ]),

    ]),
        dcc.Tab(label='Zorgprestaties ex MBO', children=[
            dbc.Row([html.H1('OVERZICHT ZORGPRESTATIE DECLARATIES VANUIT CGM')]),
            dbc.Row([
                dbc.Col([dcc.Dropdown(id='jaar-zorg', options=zorgprestaties['jaar'].unique(), value=zorgprestaties['jaar'].max())]),
                dbc.Col([], width=9)
            ]),
            dbc.Row([dcc.Graph(id='zorg telling ag')]),
            dbc.Row([dcc.Graph(id='zorg omzet ag')]),
            dbc.Row([dcc.Graph(id='consult ag')]),
            dbc.Row([dcc.Graph(id='ontslag ag')]),
            dbc.Row([dcc.Graph(id='MBO ag')])
        ]),
        dcc.Tab(label='Klanten aan de balie', children=[
            dbc.Row([html.H1('Klanten aan de balie AG')]),
            dbc.Row([dcc.Dropdown(id='jaar klanten',
                                  options=wacht_ag['jaar'].unique(),
                                  value=wacht_ag['jaar'].max())]),
            dbc.Row([dcc.Graph(id='klanten per werkdag')]),
            dbc.Row([dcc.Graph(id='klanten per uur')])
        ]),
        dcc.Tab(label='Telefonie AG', children=[
            dbc.Row([html.H1('Inkomende telefoon per apotheek')]),
            dbc.Row([dcc.Dropdown(id='jaar telefonie',
                                  options=telefoon['jaar'].unique(), value=telefoon['jaar'].max())]),
            dbc.Row([dcc.Graph(id='inkomende telefoon')]),
        ]),
        dcc.Tab(label='Service Graad verstrekkingen', children=[
            dbc.Row([html.H1('Servicegraad verstrekkingen AG')]),
            dbc.Row([
                dbc.Col([dcc.Dropdown(id='servicegraad jaar', options=service_1['jaar'].unique(), value=service_1['jaar'].max())]),
                dbc.Col([dcc.RadioItems(id='servicegraad type verstrekkingen',
                                        options=['EU', 'EU & TU', 'EU/TU/VU'],
                                        value='EU',
                                        inline=True,
                                        inputStyle ={'margin-left':'10px', 'margin-right':'10px'})], width=9)
            ]),
            dbc.Row([dcc.Graph(id='servicegraad ag')]),
            dbc.Row([]),
            dbc.Row([])
        ])
    ])
])

# TABBLAD 1: Callback voor gebruik SA APP
@callback(
        Output('SA APP gebruik', 'figure'),
        Input('SA APP jaar', 'value')
)

def sa_app_gebruik(jaar):


    # stap 1: we gebruiken het dataframe van de receptbuffer

    buffer_sa_app = buffer_ag.copy()

    # maak een maand en jaar-kolom aan en sorteer op basis van datum de waarden

    buffer_sa_app['ddDatumAanschrijving'] = pd.to_datetime(buffer_sa_app['ddDatumAanschrijving'])
    buffer_sa_app['maand'] = buffer_sa_app['ddDatumAanschrijving'].dt.month
    buffer_sa_app['jaar'] = buffer_sa_app['ddDatumAanschrijving'].dt.year
    buffer_sa_app = buffer_sa_app.sort_values(by=['ddDatumAanschrijving'], ascending=True)

    # maak filters om te markeren wat de SA APP bestellingen zijn
    service_apotheek_app = buffer_sa_app['sdAfzenderAGB'] == 'WEBSHOP'
    andere_recepten = buffer_sa_app['sdAfzenderAGB'] != 'WEBSHOP'

    sa_app_conditie = [buffer_sa_app['sdAfzenderAGB'] == 'WEBSHOP', buffer_sa_app['sdAfzenderAGB'] != 'WEBSHOP']
    sa_waarden = ['Service Apotheek APP', 'Recept/LS-recept']
    buffer_sa_app['SA APP?'] = np.select(sa_app_conditie, sa_waarden, default='Recept/LS-recept')

    # maak een telling per maand per apotheek van categorie SA APP

    aantal_SA_verdeling = buffer_sa_app.groupby(by=['jaar', 'maand', 'apotheek', 'SA APP?'])[
        'SA APP?'].count().to_frame('bestellingen per maand').reset_index()
    aantal_SA_totaal = buffer_sa_app.groupby(by=['jaar', 'maand', 'apotheek'])['SA APP?'].count().to_frame(
        'totaal per maand').reset_index()

    # merge de twee dataframes

    SA_merge = aantal_SA_verdeling.merge(aantal_SA_totaal[['jaar', 'maand', 'apotheek', 'totaal per maand']],
                                         how='left',
                                         left_on=['jaar', 'maand', 'apotheek'],
                                         right_on=['jaar', 'maand', 'apotheek'])

    # filter de gewone recepten en het jaar eruit en bereken het percentage
    SA_merge['% SA APP BESTELLINGEN'] = (
                (SA_merge['bestellingen per maand'] / SA_merge['totaal per maand']) * 100).astype(int)
    geen_gewone_recepten = (SA_merge['SA APP?'] != 'Recept/LS-recept')

    jaar_filter = (SA_merge['jaar'] == jaar)

    SA_merge_1 = SA_merge.loc[geen_gewone_recepten & jaar_filter]

    # maak er een plot van

    SA_plot = px.line(SA_merge_1, x='maand', y='% SA APP BESTELLINGEN', color='apotheek', text='% SA APP BESTELLINGEN',
                      title='% BESTELLINGEN VIA DE SERVICE APOTHEEK APP IN DE RECEPTBUFFER')

    return SA_plot

# TABBLAD 2: Callback voor contactgegevens
@callback(
    Output('geen contactgegevens AG', 'figure'),
    Output('email afwezig AG', 'figure'),
    Output('mobiel nummer afwezig AG', 'figure'),
    Input('contactgegevens jaar', 'value')
)
def contact(jaar):
    ######--- TABBLAD 2: CONTACTGEGEVENS CLIENTEN IN KAART ---- #############################################################################################

    # Stap 1: We gebruiken het receptverwerkingsdataframe (contactgegevens, patiëntnr) .. de verstrekkingen van het afgelopen jaar
    # Stap 2: Markeer wanneer er een email en

    contact_ag = recept_ag.copy()

    # benodigde kolommen erbij pakken en een jaar kolom aanmaken voor het filter

    contact_ag_1 = contact_ag[['ddDatumRecept', 'ndPatientnr', 'sdEmail', 'Telefoon1', 'Telefoon2', 'apotheek']]

    contact_ag_1['ddDatumRecept'] = pd.to_datetime(contact_ag_1['ddDatumRecept'])
    contact_ag_1['jaar'] = contact_ag_1['ddDatumRecept'].dt.year

    # maak van de telefoonnummers een nummer
    contact_ag_1['Telefoon1'] = contact_ag_1['Telefoon1'].str.replace(r'\D+', '', regex=True)
    contact_ag_1['Telefoon2'] = contact_ag_1['Telefoon2'].str.replace(r'\D+', '', regex=True)

    # vervang NaN door 0 in email kolom, Telefoon1 en Telefoon2

    contact_ag_1['sdEmail'] = contact_ag_1['sdEmail'].replace(np.nan, 0, regex=True)
    contact_ag_1['Telefoon1'] = contact_ag_1['Telefoon1'].replace(np.nan, 0, regex=True)
    contact_ag_1['Telefoon2'] = contact_ag_1['Telefoon2'].replace(np.nan, 0, regex=True)
    contact_ag_1['Telefoon1'] = pd.to_numeric(contact_ag_1['Telefoon1'])
    contact_ag_1['Telefoon2'] = pd.to_numeric(contact_ag_1['Telefoon2'])

    # maak een kolom met email markering aan

    conditie_contact_email = [
        contact_ag_1['sdEmail'] == 0,
        contact_ag_1['sdEmail'] != 0
    ]

    waarden_contact_email = ['geen email aanwezig', 'email aanwezig']

    contact_ag_1['email aanwezig?'] = np.select(conditie_contact_email, waarden_contact_email, default='??')

    # Maak een kolom met een mobiel nummer markering aan

    conditie_contact_mobiel = [
        ((contact_ag_1['Telefoon1'] >= 600000000) | (contact_ag_1['Telefoon2'] >= 600000000)),
        ((contact_ag_1['Telefoon1'] <= 600000000) & (contact_ag_1['Telefoon2'] <= 600000000))
    ]

    waarden_contact_mobiel = ['mobiel nummer aanwezig', 'geen mobiel nummer']

    contact_ag_1['mobiel aanwezig?'] = np.select(conditie_contact_mobiel, waarden_contact_mobiel, default='??')

    # maak een kolom met GEEN CONTACTGEGEVENS AANWEZIG aan

    conditie_contact_geen = [
        ((contact_ag_1['sdEmail'] == 0) & (contact_ag_1['Telefoon1'] == 0) & (contact_ag_1['Telefoon2'] == 0)),
        ((contact_ag_1['sdEmail'] != 0) | (contact_ag_1['Telefoon1'] != 0) | (contact_ag_1['Telefoon2'] != 0))
    ]

    waarden_contact_geen = ['GEEN CONTACTGEGEVENS', 'CONTACTGEGEVENS AANWEZIG']

    contact_ag_1['contactgegevens aanwezig?'] = np.select(conditie_contact_geen, waarden_contact_geen, default='??')

    # dubbele patientnrs verwijderen voor het tellen van de juiste getallen
    contact_ag_1 = contact_ag_1.drop_duplicates(subset=['ndPatientnr'], keep='first')

    # filter voor het gekozen jaar

    jaar_keuze = (contact_ag_1['jaar'] == jaar)

    contact_ag_2 = contact_ag_1.loc[jaar_keuze]

    ###### GEEN CONTACTGEGEVENS BEGIN #########

    # Nu maken we verdeling en totaal tellen
    contact_aanwezig_verdeling = contact_ag_2.groupby(by=['apotheek', 'contactgegevens aanwezig?'])[
        'contactgegevens aanwezig?'].count().to_frame('aantal verdeling').reset_index()
    contact_aanwezig_totaal = contact_ag_2.groupby(by=['apotheek'])['contactgegevens aanwezig?'].count().to_frame(
        'aantal totaal').reset_index()

    geen_contact_merge = contact_aanwezig_verdeling.merge(contact_aanwezig_totaal[['apotheek', 'aantal totaal']],
                                                          how='left',
                                                          left_on='apotheek',
                                                          right_on='apotheek')
    # bereken het %
    geen_contact_merge['% geen contactgegevens'] = (
                (geen_contact_merge['aantal verdeling'] / geen_contact_merge['aantal totaal']) * 100).astype(int)

    # filter
    alleen_patiënten_zonder_contactgegevens = (
                geen_contact_merge['contactgegevens aanwezig?'] == 'GEEN CONTACTGEGEVENS')
    # laat alleen meting zien van mensen zonder contactgegevens
    geen_contact_def = geen_contact_merge.loc[alleen_patiënten_zonder_contactgegevens]
    # maak hiervan een bar-chart
    contact_grafiek_1 = px.bar(geen_contact_def, x='apotheek', y='% geen contactgegevens', text_auto=True, title='GEEN CONTACTGEGEVENS AANWEZIG (%)')

    ###### GEEN CONTACTGEGEVENS EINDE #########

    ###### GEEN EMAILADRESSEN BEGIN ###########

    # tellen verdeling en totaal
    email_aanwezig_verdeling = contact_ag_2.groupby(by=['apotheek', 'email aanwezig?'])[
        'email aanwezig?'].count().to_frame('aantal verdeling').reset_index()
    email_aanwezig_totaal = contact_ag_2.groupby(by=['apotheek'])['email aanwezig?'].count().to_frame(
        'aantal totaal').reset_index()

    # merge

    email_afwezig_merge = email_aanwezig_verdeling.merge(email_aanwezig_totaal[['apotheek', 'aantal totaal']],
                                                         how='left',
                                                         left_on='apotheek',
                                                         right_on='apotheek')
    # bereken % tov totaal
    email_afwezig_merge['% geen email aanwezig'] = (
                (email_afwezig_merge['aantal verdeling'] / email_afwezig_merge['aantal totaal']) * 100).astype(int)

    # filter zodat je alleen de afwezige contactgegevens overhoudt
    alleen_patienten_zonder_email = (email_afwezig_merge['email aanwezig?'] == 'geen email aanwezig')

    # pas filter toe
    email_afwezig = email_afwezig_merge.loc[alleen_patienten_zonder_email]

    contact_grafiek_2 = px.bar(email_afwezig, x='apotheek', y='% geen email aanwezig', text_auto=True, title='GEEN EMAIL AANWEZIG (%)')

    ###### GEEN EMAILADRESSEN EINDE ###########

    ###### GEEN MOBIEL NUMMER BEGIN ###########

    mobiel_aanwezig_verdeling = contact_ag_2.groupby(by=['apotheek', 'mobiel aanwezig?'])[
        'mobiel aanwezig?'].count().to_frame('aantal verdeling').reset_index()
    mobiel_aanwezig_totaal = contact_ag_2.groupby(by=['apotheek'])['mobiel aanwezig?'].count().to_frame(
        'aantal totaal').reset_index()

    mobiel_afwezig_merge = mobiel_aanwezig_verdeling.merge(mobiel_aanwezig_totaal[['apotheek', 'aantal totaal']],
                                                           how='left',
                                                           left_on='apotheek',
                                                           right_on='apotheek')

    mobiel_afwezig_merge['% zonder mobiel nummer'] = (
                (mobiel_afwezig_merge['aantal verdeling'] / mobiel_afwezig_merge['aantal totaal']) * 100).astype(int)

    # filter voor alleen zonder mobiel
    alleen_patienten_zonder_mobiel_nummer = (mobiel_afwezig_merge['mobiel aanwezig?'] == 'geen mobiel nummer')

    # filter toepassen
    mobiel_afwezig = mobiel_afwezig_merge.loc[alleen_patienten_zonder_mobiel_nummer]

    # maak een grafiek
    contact_grafiek_3 = px.bar(mobiel_afwezig, x='apotheek', y='% zonder mobiel nummer', text_auto=True, title='GEEN MOBIEL NUMMER AANWEZIG (%)')

    return contact_grafiek_1, contact_grafiek_2, contact_grafiek_3

# TABBLAD 3: Callback voor Herhaalservice

@callback(
    Output('HHS% AG', 'figure'),
    Input('jaar hhs', 'value'),
)
def HHS(jaar):
    ######--- TABBLAD 3: % HERHAALSERVICE VOOR ALLE AG APOTHEKEN ---- #############################################################################################

    # stappenplan

    # stap 1. We hebben informatie nodig uit de receptverwerking
    # stap 2. ReceptHerkomst laat zien welke regels afkomstig zijn uit een herhaalprofiel
    # stap 3. We willen filteren wat niet relevant is: distributie, zorg, lsp, dienst.
    # stap 4. We willen tellen wat het aantal regels is dat via hhs komt en wat het totaal aantal regels is. hier berekenen we een % van
    # stap 5. Visualisatie: we willen laten zien per maand wat het % hhs is. We willen dat er in het dashboard kan worden gefilterd per jaar. We laten 1 Grafiek zien.
    # stap 6. Visualisatie: wellicht goed om te laten zien hoeveel patiënten van de apotheek in die maand van medicatie zijn voorzien via de hhs.
    # stap 7. Visualisatie: wellicht om te kunnen filteren op EU-verstrekkingen (vinkje aan/uit voor EU Verstrekkingen)--> met name nuttig voor hanzeplein

    # Inlezen recept dataframe

    HHS_AG = recept_ag.copy()

    # Selecteer welke kolommen je wilt gebruiken voor het dataframe

    HHS_AG_1 = HHS_AG[['ddDatumRecept', 'ReceptHerkomst',
                       'ndReceptnummer', 'ndATKODE', 'sdEtiketNaam', 'ndAantal', 'sdMedewerkerCode',
                       'Uitgifte', 'ndPatientnr', 'apotheek']]

    # maak een maand kolom

    HHS_AG_1['ddDatumRecept'] = pd.to_datetime(HHS_AG_1['ddDatumRecept'])
    HHS_AG_1['maand'] = HHS_AG_1['ddDatumRecept'].dt.month
    HHS_AG_1['jaar'] = HHS_AG_1['ddDatumRecept'].dt.year

    # Filter op basis van het jaar
    # jaar filter
    jaar_filter_HHS = (HHS_AG_1['jaar'] == 2024)

    # pas het filter toe
    HHS_AG_2 = HHS_AG_1.loc[jaar_filter_HHS]

    # maak nu filters aan voor het type recepten dat je niet wilt zien in je dataframe (distributie, dienst, zorg, LSP)

    hhs_geen_distributie = (HHS_AG_2['ReceptHerkomst'] != 'D')
    hhs_geen_dienst = (HHS_AG_2['ReceptHerkomst'] != 'DIENST')
    hhs_geen_zorg = (HHS_AG_2['ReceptHerkomst'] != 'Z')
    hhs_geen_LSP = (HHS_AG_2['sdMedewerkerCode'] != 'LSP')

    # pas nu de filters toe
    HHS_AG_3 = HHS_AG_2.loc[hhs_geen_distributie & hhs_geen_dienst & hhs_geen_zorg & hhs_geen_LSP]

    # vanaf nu kun je het filter gaan toepassen voor wel/geen EU verstrekkingen als je dat wilt.!!!!!!!!!!!!!!!!!!!!!!!!!

    # markeer de regels met O en R als gewoon recept
    # markeer de regels met H als herhaalservice

    hhs_condities = [
        HHS_AG_3['ReceptHerkomst'] == 'H',
        HHS_AG_3['ReceptHerkomst'] != 'H'
    ]

    hhs_waarden = ['HERHAALSERVICE', 'GEWOON RECEPT']

    HHS_AG_3['Herhaalservice regel?'] = np.select(hhs_condities, hhs_waarden, default='??')

    # Nu ga je tellen per apotheek per maand wat het aantal verstrekkingen zijn vanuit HHS en het aantal totaal verstrekkingen

    # Tel de verdeling
    HHS_verdeling = HHS_AG_3.groupby(by=['maand', 'apotheek', 'Herhaalservice regel?'])[
        'Herhaalservice regel?'].count().to_frame('aantal verdeling').reset_index()
    # Tel het totaal
    HHS_totaal = HHS_AG_3.groupby(by=['maand', 'apotheek'])['Herhaalservice regel?'].count().to_frame(
        'aantal totaal').reset_index()

    # merge beide dataframes

    HHS_merge = HHS_verdeling.merge(HHS_totaal[['maand', 'apotheek', 'aantal totaal']],
                                    how='left',
                                    left_on=['maand', 'apotheek'],
                                    right_on=['maand', 'apotheek'])

    # maak een % kolom
    HHS_merge['% Herhaalservice'] = ((HHS_merge['aantal verdeling'] / HHS_merge['aantal totaal']) * 100).astype(int)

    # filter nu de gewone recepten eruit
    # filter
    hhs_alleen = (HHS_merge['Herhaalservice regel?'] == 'HERHAALSERVICE')

    # pas filter toe
    HHS_merge_1 = HHS_merge.loc[hhs_alleen]

    # maak een grafiek
    HHS_grafiek = px.line(HHS_merge_1, x='maand', y='% Herhaalservice', color='apotheek', text='% Herhaalservice',
                          title='% HERHAALSERVICE TOV OVERIGE RECEPTUUR PER APOTHEEK (excl distributie)')

    return HHS_grafiek

# TABBLAD 4: Callback voor overzicht leveringen

@callback(
    Output('levering hanzeplein', 'figure'),
    Output('levering oosterpoort', 'figure'),
    Output('levering helpman', 'figure'),
    Output('levering wiljes', 'figure'),
    Output('levering oosterhaar', 'figure'),
    Output('levering musselpark', 'figure'),
    Input('levering jaar', 'value')
)
def leveringen_verdeling_ag(jaar):
    # maak een dataframe om mee te starten
    levering = recept_ag.copy()

    # maak een selectie van nuttige kolommen
    levering_1 = levering[
        ['ddDatumRecept', 'sdMedewerkerCode', 'ReceptHerkomst', 'cf', 'ScanNrKop', 'RecLocatie', 'RecLocatieCode',
         'apotheek']]

    # Maak een jaar en een maand-kolom aan
    levering_1['ddDatumRecept'] = pd.to_datetime(levering_1['ddDatumRecept'])
    levering_1['jaar'] = levering_1['ddDatumRecept'].dt.year
    levering_1['maand'] = levering_1['ddDatumRecept'].dt.month

    # bekijk de aparte dataframes van de apotheken en label de regels (musselpark, oosterhaar, wiljes, helpman, oosterpoort, hanzeplein)

    mp = (levering_1['apotheek'] == 'musselpark')
    oh = (levering_1['apotheek'] == 'oosterhaar')
    wil = (levering_1['apotheek'] == 'wiljes')
    hlp = (levering_1['apotheek'] == 'helpman')
    op = (levering_1['apotheek'] == 'oosterpoort')
    hzp = (levering_1['apotheek'] == 'hanzeplein')

    mp_levering = levering_1.loc[mp]

    # hernoem de nan locatie
    mp_levering['RecLocatieCode'] = mp_levering['RecLocatieCode'].replace(np.nan, 'halen', regex=True)

    # maak de condities en labels aan voor MUSSELPARK

    mp_levering_condities = [
        ((mp_levering['RecLocatieCode'] == 'PS24') |  # Kluis
         (mp_levering['RecLocatieCode'] == 'BLIJPS24') |
         (mp_levering['RecLocatieCode'] == 'PS24MP')),
        ((mp_levering['RecLocatieCode'] == 'BEZVR') |  # Bezorgen
         (mp_levering['RecLocatieCode'] == 'BEZMA') |
         (mp_levering['RecLocatieCode'] == 'LOCBBMA') |
         (mp_levering['RecLocatieCode'] == 'LOCBBDI') |
         (mp_levering['RecLocatieCode'] == 'BEZWO') |
         (mp_levering['RecLocatieCode'] == 'LOCAH') |
         (mp_levering['RecLocatieCode'] == 'LOCBBWO') |
         (mp_levering['RecLocatieCode'] == 'LOCBEUK') |
         (mp_levering['RecLocatieCode'] == 'BEZDO') |
         (mp_levering['RecLocatieCode'] == 'BEZDI') |
         (mp_levering['RecLocatieCode'] == 'LOCBBDO') |
         (mp_levering['RecLocatieCode'] == 'LOCZB') |
         (mp_levering['RecLocatieCode'] == 'LOCPHM') |
         (mp_levering['RecLocatieCode'] == 'LOCPHV') |
         (mp_levering['RecLocatieCode'] == 'LOCNOH') |
         (mp_levering['RecLocatieCode'] == 'BLIJBEZ')),
        ((mp_levering['RecLocatieCode'] == 'HALEN') |  # Halen
         (mp_levering['RecLocatieCode'] == 'LOXIS') |
         (mp_levering['RecLocatieCode'] == 'halen')),
        ((mp_levering['RecLocatieCode'] == 'BLIJHALEN') |  # Uitdeelpost
         (mp_levering['RecLocatieCode'] == 'AZC'))
    ]

    mp_levering_waarden = ['KLUIS', 'BEZORGEN', 'HALEN', 'UITDEELPOST']

    mp_levering['Leverwijze'] = np.select(mp_levering_condities, mp_levering_waarden, default='??')

    # maak de condities en labels aan voor OOSTERHAAR

    oh_levering = levering_1.loc[oh]

    # hernoem de locatiecode NaN
    oh_levering['RecLocatieCode'] = oh_levering['RecLocatieCode'].replace(np.nan, 'halen', regex=True)

    # Maak de labels aan: KLUIS, BEZORGEN, HALEN, UITDEELPOST

    oh_levering_condities = [
        ((oh_levering['RecLocatieCode'] == 'PS24') |  # Kluis
         (oh_levering['RecLocatieCode'] == 'HARKPS24') |
         (oh_levering['RecLocatieCode'] == 'MEERSTAD')),
        ((oh_levering['RecLocatieCode'] == 'BEZORG') |  # Bezorgen
         (oh_levering['RecLocatieCode'] == 'HARKBEZ')),
        ((oh_levering['RecLocatieCode'] == 'halen') |  # Halen
         (oh_levering['RecLocatieCode'] == 'Halen')),
        (oh_levering['RecLocatieCode'] == 'HARKHAAL')  # Uitdeelpost

    ]

    oh_levering_waarden = ['KLUIS', 'BEZORGEN', 'HALEN', 'UITDEELPOST']

    oh_levering['Leverwijze'] = np.select(oh_levering_condities, oh_levering_waarden, default='??')

    # label de regels van de wiljes

    wil_levering = levering_1.loc[wil]

    # hernoem de Nan locatie
    wil_levering['RecLocatieCode'] = wil_levering['RecLocatieCode'].replace(np.nan, 'halen', regex=True)

    wil_levering_condities = [
        ((wil_levering['RecLocatieCode'] == 'PS24W') |
         (wil_levering['RecLocatieCode'] == 'WIJERT') |
         (wil_levering['RecLocatieCode'] == 'SERVI')),
        ((wil_levering['RecLocatieCode'] == 'BEZW') |
         (wil_levering['RecLocatieCode'] == 'NOORD')),
        (wil_levering['RecLocatieCode'] == 'HALENW') |
        (wil_levering['RecLocatieCode'] == 'halen') |
        (wil_levering['RecLocatieCode'] == 'HALEN')
    ]

    wil_levering_waarden = ['KLUIS', 'BEZORGEN', 'HALEN']

    wil_levering['Leverwijze'] = np.select(wil_levering_condities, wil_levering_waarden, default='??')

    # Label vanaf hier de regels van apotheek HELPMAN

    hlp_levering = levering_1.loc[hlp]

    # hernoem de nan waarden
    hlp_levering['RecLocatieCode'] = hlp_levering['RecLocatieCode'].replace(np.nan, 'halen', regex=True)

    hlp_levering_condities = [
        ((hlp_levering['RecLocatieCode'] == 'PS24HE') |
         (hlp_levering['RecLocatieCode'] == 'PS24WIJ')),
        ((hlp_levering['RecLocatieCode'] == 'BEZHE') |
         (hlp_levering['RecLocatieCode'] == 'BWH') |
         (hlp_levering['RecLocatieCode'] == 'DACOSTA') |
         (hlp_levering['RecLocatieCode'] == 'COSIS')),
        ((hlp_levering['RecLocatieCode'] == 'HALENHE') |
         (hlp_levering['RecLocatieCode'] == 'HALENW') |
         (hlp_levering['RecLocatieCode'] == 'halen'))

    ]

    hlp_levering_waarden = ['KLUIS', 'BEZORGEN', 'HALEN']

    hlp_levering['Leverwijze'] = np.select(hlp_levering_condities, hlp_levering_waarden, default='??')

    # Label de waarden van apotheek OOSTERPOORT

    op_levering = levering_1.loc[op]

    # hernoem de NaN-waarden
    op_levering['RecLocatieCode'] = op_levering['RecLocatieCode'].replace(np.nan, 'halen', regex=True)

    op_levering_condities = [
        (op_levering['RecLocatieCode'] == 'PS24'),  # Kluis
        ((op_levering['RecLocatieCode'] == 'BEZ') |  # Bezorgen
         (op_levering['RecLocatieCode'] == 'HAMRIK') |
         (op_levering['RecLocatieCode'] == 'PELSTER')),
        ((op_levering['RecLocatieCode'] == 'HALEN') |  # Halen
         (op_levering['RecLocatieCode'] == 'halen') |
         (op_levering['RecLocatieCode'] == 'APLOP'))

    ]

    op_levering_waarden = ['KLUIS', 'BEZORGEN', 'HALEN']

    op_levering['Leverwijze'] = np.select(op_levering_condities, op_levering_waarden, default='??')

    # Label nu de leveringen van apotheek HANZEPLEIN

    hzp_levering = levering_1.loc[hzp]

    # hernoem de NaN waarden
    hzp_levering['RecLocatieCode'] = hzp_levering['RecLocatieCode'].replace(np.nan, 'halen', regex=True)

    hzp_levering_condities = [
        ((hzp_levering['RecLocatieCode'] == 'PS24') |  # Kluis
         (hzp_levering['RecLocatieCode'] == 'RADE')),
        ((hzp_levering['RecLocatieCode'] == 'LOCMA') |  # Bezorgen
         (hzp_levering['RecLocatieCode'] == 'BEZ') |
         (hzp_levering['RecLocatieCode'] == 'LOCWO') |
         (hzp_levering['RecLocatieCode'] == 'LOCVNN') |
         (hzp_levering['RecLocatieCode'] == 'LOCDI') |
         (hzp_levering['RecLocatieCode'] == 'LOCDO') |
         (hzp_levering['RecLocatieCode'] == 'LOCVR')),
        ((hzp_levering['RecLocatieCode'] == 'halen') |  # Halen
         (hzp_levering['RecLocatieCode'] == 'HALEN') |
         (hzp_levering['RecLocatieCode'] == 'LOCBA'))
    ]

    hzp_levering_waarden = ['KLUIS', 'BEZORGEN', 'HALEN']

    hzp_levering['Leverwijze'] = np.select(hzp_levering_condities, hzp_levering_waarden, default='??')

    # Voeg de levering dataframes samen, zodat je kan gaan filteren en tellen

    levering_3 = pd.concat([hzp_levering, op_levering, hlp_levering, wil_levering, oh_levering, mp_levering])

    # nu gaan we de bagger eruit filteren ( zorg, dienst-recepten en LSP-recepten, eventueel ook Distributie-regels)

    geen_zorg_levering = (levering_3['ReceptHerkomst'] != 'Z')
    geen_dienst_levering = (levering_3['ReceptHerkomst'] != 'DIENST')
    geen_LSP_levering = (levering_3['sdMedewerkerCode'] != 'LSP')
    geen_distributie_levering = (levering_3['ReceptHerkomst'] != 'D')

    levering_4 = levering_3.loc[
        geen_zorg_levering & geen_dienst_levering & geen_LSP_levering & geen_distributie_levering]

    # gooi hier het jaarfilter overheen
    jaar_filter_levering = (levering_4['jaar'] == 2024)  # FILTER VOOR HET JAAR

    levering_5 = levering_4.loc[jaar_filter_levering]

    # ga nu tellen per maand per apotheek

    levering_verdeling = levering_5.groupby(by=['maand', 'apotheek', 'Leverwijze'])['Leverwijze'].count().to_frame(
        'aantal verdeling').reset_index()
    levering_totaal = levering_5.groupby(by=['maand', 'apotheek'])['Leverwijze'].count().to_frame(
        'aantal totaal').reset_index()

    levering_merge = levering_verdeling.merge(levering_totaal[['maand', 'apotheek', 'aantal totaal']],
                                              how='left',
                                              left_on=['maand', 'apotheek'],
                                              right_on=['maand', 'apotheek'])
    levering_merge['%'] = ((levering_merge['aantal verdeling'] / levering_merge['aantal totaal']) * 100).astype(int)

    # Nu kunnen we voor iedere apotheek een bar graph dataframe maken

    hanzeplein_levering_filter = (levering_merge['apotheek'] == 'hanzeplein')
    oosterpoort_levering_filter = (levering_merge['apotheek'] == 'oosterpoort')
    helpman_levering_filter = (levering_merge['apotheek'] == 'helpman')
    wiljes_levering_filter = (levering_merge['apotheek'] == 'wiljes')
    oosterhaar_levering_filter = (levering_merge['apotheek'] == 'oosterhaar')
    musselpark_levering_filter = (levering_merge['apotheek'] == 'musselpark')

    hanzeplein_levering_data = levering_merge.loc[hanzeplein_levering_filter]
    oosterpoort_levering_data = levering_merge.loc[oosterpoort_levering_filter]
    helpman_levering_data = levering_merge.loc[helpman_levering_filter]
    wiljes_levering_data = levering_merge.loc[wiljes_levering_filter]
    oosterhaar_levering_data = levering_merge.loc[oosterhaar_levering_filter]
    musselpark_levering_data = levering_merge.loc[musselpark_levering_filter]

    hanzeplein_levering_grafiek = px.bar(hanzeplein_levering_data,
                                         x='maand',
                                         y='%',
                                         color='Leverwijze',
                                         text_auto=True,
                                         title='Overzicht verdeling leveringen apotheek Hanzeplein')

    oosterpoort_levering_grafiek = px.bar(oosterpoort_levering_data,
                                          x='maand',
                                          y='%',
                                          color='Leverwijze',
                                          text_auto=True,
                                          title='Overzicht verdeling leveringen apotheek Oosterpoort')

    helpman_levering_grafiek = px.bar(helpman_levering_data,
                                      x='maand',
                                      y='%',
                                      color='Leverwijze',
                                      text_auto=True,
                                      title='Overzicht verdeling leveringen apotheek Helpman')

    wiljes_levering_grafiek = px.bar(wiljes_levering_data,
                                     x='maand',
                                     y='%',
                                     color='Leverwijze',
                                     text_auto=True,
                                     title='Overzicht verdeling leveringen apotheek de Wiljes')

    oosterhaar_levering_grafiek = px.bar(oosterhaar_levering_data,
                                         x='maand',
                                         y='%',
                                         color='Leverwijze',
                                         text_auto=True,
                                         title='Overzicht verdeling leveringen apotheek Oosterhaar')

    musselpark_levering_grafiek = px.bar(musselpark_levering_data,
                                         x='maand',
                                         y='%',
                                         color='Leverwijze',
                                         text_auto=True,
                                         title='Overzicht verdeling leveringen apotheek Musselpark')

    return hanzeplein_levering_grafiek, oosterpoort_levering_grafiek, helpman_levering_grafiek, wiljes_levering_grafiek, oosterhaar_levering_grafiek, musselpark_levering_grafiek

# TABBLAD 5: Callback voor overzicht declaratie zorgprestaties
@callback(
    Output('zorg telling ag', 'figure'),
    Output('zorg omzet ag', 'figure'),
    Output('consult ag', 'figure'),
    Output('ontslag ag', 'figure'),
    Output('MBO ag', 'figure'),
    Input('jaar-zorg', 'value')
)
def zorg_prestaties(jaar):
    zorgprestaties = zorg_ag.copy()

    print(zorgprestaties['PrestatieOmschrijving'].unique())

    zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace(
        'Farmaceutisch consult bij zorgvraag patient', 'Consult', regex=True)
    zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace(
        'Farmaceutische begeleiding i.v.m. ontslag uit het ziekenhuis', 'Ontslag', regex=True)
    zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace(
        'Medicatieoptimalisatie en begeleiding bij pati nten met de ziekte van Parkinson', 'Parkinson', regex=True)
    zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace(
        'Begeleiding en verbeteren van geneesmiddelengebruik in samenwerking met de huisarts', 'Verbetering gebruik',
        regex=True)
    zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace(
        'Medicatiebeoordeling chronisch UR geneesmiddelengebruik', 'MBO', regex=True)
    zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace(
        'Medicatiebeoordeling chronisch UR geneesmiddelengebruik, thuis', 'MBO thuis', regex=True)
    zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace(
        'Instructie UR geneesmiddel gerelateerd hulpmiddel', 'hulpm instructie', regex=True)
    zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace(
        'Standaardterhandstelling - niet afleveren na overleg met arts/patient', 'Niet afleveren', regex=True)
    zorgprestaties['PrestatieOmschrijving'] = zorgprestaties['PrestatieOmschrijving'].str.replace(
        'Farmaceutische begeleiding bij dagbehandeling/polikliniekbezoek', 'Poli-bezoek', regex=True)

    # maak een maand en jaar kolom aan
    zorgprestaties['PrestatieDatum'] = pd.to_datetime(zorgprestaties['PrestatieDatum'])
    zorgprestaties['maand'] = zorgprestaties['PrestatieDatum'].dt.month
    zorgprestaties['jaar'] = zorgprestaties['PrestatieDatum'].dt.year

    # Gooi hier nu een jaar-filter overheen

    jaar_filter_zorgprestaties = (zorgprestaties['jaar'] == jaar)

    # pas jaarfilter toe

    zorgprestaties_1 = zorgprestaties.loc[jaar_filter_zorgprestaties]

    # Ga nu tellen hoeveel prestaties er per maand per apotheek worden gedeclareerd
    zorgprestatie_telling = zorgprestaties_1.groupby(by=['maand', 'apotheek', 'Prestatie', 'PrestatieOmschrijving'])[
        'PrestatieOmschrijving'].count().to_frame('aantal').reset_index()
    zorgprestatie_omzet = zorgprestaties_1.groupby(by=['maand', 'apotheek', 'Prestatie', 'PrestatieOmschrijving'])[
        'BedragIncl'].sum().to_frame('omzet').reset_index()

    zorgprestatie_telling_groep = zorgprestaties_1.groupby(by=['Prestatie', 'PrestatieOmschrijving'])[
        'PrestatieOmschrijving'].count().to_frame('aantal').reset_index()
    zorgprestatie_omzet_groep = zorgprestaties_1.groupby(by=['Prestatie', 'PrestatieOmschrijving'])[
        'BedragIncl'].sum().to_frame('omzet').reset_index()

    zorgprestatie_telling_groep_1 = zorgprestatie_telling_groep.sort_values(by=['aantal'], ascending=False)
    zorgprestatie_omzet_groep_1 = zorgprestatie_omzet_groep.sort_values(by=['omzet'], ascending=False)

    zorgprestatie_telling_groep_2 = zorgprestatie_telling_groep_1.nlargest(n=5, columns=['aantal'])
    zorgprestatie_omzet_groep_2 = zorgprestatie_omzet_groep_1.nlargest(n=5, columns=['omzet'])

    zorgprestatie_telling_groep_1_grafiek = px.bar(zorgprestatie_telling_groep_2, x='PrestatieOmschrijving', y='aantal',
                                                   text_auto=True,
                                                   title='TOTAAL AANTAL GEDECLAREERDE ZORGPRESTATIES VANUIT CGM')
    zorgprestatie_omzet_groep_1_grafiek = px.bar(zorgprestatie_omzet_groep_2, x='PrestatieOmschrijving', y='omzet',
                                                 text_auto=True,
                                                 title='TOTAAL GEDECLAREERDE OMZET ZORGPRESTATIES VANUIT CGM')

    # Nu gaan we per prestatie de apotheken vergelijken op aantallen declaraties per maand

    # consulten
    consulten_alleen = (zorgprestatie_telling['Prestatie'] == 71014)
    ontslag_alleen = (zorgprestatie_telling['Prestatie'] == 70006)
    MBO_alleen = (zorgprestatie_telling['Prestatie'] == 70002)

    consulten = zorgprestatie_telling.loc[consulten_alleen]
    ontslag = zorgprestatie_telling.loc[ontslag_alleen]
    MBO = zorgprestatie_telling.loc[MBO_alleen]

    consulten_grafiek = px.line(consulten, x='maand', y='aantal', color='apotheek', text='aantal',
                                title='AANTAL CONSULTDECLARATIES PER MAAND PER APOTHEEK VIA CGM')
    ontslag_grafiek = px.line(ontslag, x='maand', y='aantal', color='apotheek', text='aantal',
                              title='AANTAL ONTSLAG-PRESTATIES PER MAAND PER APOTHEEK VIA CGM')
    mbo_grafiek = px.line(MBO, x='maand', y='aantal', color='apotheek', text='aantal',
                          title='AANTAL MBO DECLARATIES PER MAAND PER APOTHEEK VIA CGM')

    # Grafieken overzicht
    zorg_telling_ag = zorgprestatie_telling_groep_1_grafiek  # grafiek 1
    zorg_omzet_ag = zorgprestatie_omzet_groep_1_grafiek  # grafiek 2
    consulten_grafiek  # grafiek 3
    ontslag_grafiek  # grafiek 4
    mbo_grafiek  # grafiek 5

    return zorg_telling_ag, zorg_omzet_ag, consulten_grafiek, ontslag_grafiek, mbo_grafiek

# TABBLAD 6: Callback voor overzicht klanten aan de balie

@callback(
    Output('klanten per werkdag', 'figure'),
    Output('klanten per uur', 'figure'),
    Input('jaar klanten', 'value')
)

def klanten_balie(jaar):
    wacht_ag = klanten_ag.copy()

    # maak eerst een uur kolom aan
    wacht_ag['Starttijd'] = wacht_ag['Starttijd'].replace('"', '', regex=True)
    wacht_ag['Starttijd'] = pd.to_datetime(wacht_ag['Starttijd'], format='%H:%M:%S')
    wacht_ag['uur'] = wacht_ag['Starttijd'].dt.hour
    wacht_ag['jaar'] = wacht_ag['Datum'].dt.year

    # maak daarna een week vd dag kolom aan
    wacht_ag['weekdagnr'] = wacht_ag['Datum'].dt.weekday

    # maak labels voor de weekdagen
    conditie_klanten_weekdag = [
        (wacht_ag['weekdagnr'] == 0),
        (wacht_ag['weekdagnr'] == 1),
        (wacht_ag['weekdagnr'] == 2),
        (wacht_ag['weekdagnr'] == 3),
        (wacht_ag['weekdagnr'] == 4),
        (wacht_ag['weekdagnr'] == 5),
        (wacht_ag['weekdagnr'] == 6)
    ]

    waarden_klanten_weekdag = ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag']

    wacht_ag['weekdag naam'] = np.select(conditie_klanten_weekdag, waarden_klanten_weekdag, default='???')

    wacht_jaar_filter = (wacht_ag['jaar'] == jaar)  # JAARFILTER
    weekdagen = (wacht_ag['weekdagnr'] < 5)

    wacht_ag_werkdagen = wacht_ag.loc[weekdagen & wacht_jaar_filter]

    # Nu gaan we tellingen doen
    # Voor de tellingen per uur hebben we nodig hoeveel keer er (bijv) een 8 voorkomt per individuele dag
    # Daarna moeten we dat delen door het aantal dagen in totaal dat voorkomt in het dataframe
    # Bovenstaande moet per apotheek
    # Voor het aantal tellingen per dag per apotheek gaan we nu een groupby doen

    # We berekenen per apotheek hoeveel uur-notities er zijn (zijn klanten)
    # Daarna berekenen we over hoeveel dagen deze notities verdeeld moeten worden = ontdubbeling data en tellen

    # Het aantal losse dagen berekenen
    aantal_dagen_frame = wacht_ag_werkdagen.drop_duplicates(subset=['Datum'], keep='first')

    weekdagen_aantal = aantal_dagen_frame.groupby(by=['weekdag naam'])['weekdag naam'].count().to_frame(
        'aantal dagen').reset_index()

    aantal_dagen = len(aantal_dagen_frame)

    telling_wacht_uren = wacht_ag_werkdagen.groupby(by=['apotheek', 'uur'])['uur'].count().to_frame(
        'aantal').reset_index()
    telling_wacht_uren['aantal dagen'] = aantal_dagen
    telling_wacht_uren['klanten per uur (gem)'] = (
                telling_wacht_uren['aantal'] / telling_wacht_uren['aantal dagen']).astype(int)

    # maak de grafiek
    klanten_per_uur_grafiek = px.line(telling_wacht_uren, x='uur', y='klanten per uur (gem)', color='apotheek',
                                      text='klanten per uur (gem)', title='GEMIDDELD AANTAL KLANTEN PER UUR')

    # Doe nu hetzelfde, maar dan met de weekdagen

    telling_klanten_per_weekdag_totaal = wacht_ag_werkdagen.groupby(by=['apotheek', 'weekdagnr', 'weekdag naam'])[
        'weekdag naam'].count().to_frame('aantal').reset_index()

    telling_klanten_per_weekdag_totaal_1 = telling_klanten_per_weekdag_totaal.sort_values(by=['weekdagnr'],
                                                                                          ascending=True)
    # merge de dataframes zodat je kan gaan rekenen

    telling_klanten_per_weekdag_totaal_merge = telling_klanten_per_weekdag_totaal.merge(
        weekdagen_aantal[['weekdag naam', 'aantal dagen']],
        how='left',
        left_on='weekdag naam',
        right_on='weekdag naam')

    telling_klanten_per_weekdag_totaal_merge['gem klanten per werkdag'] = (
                telling_klanten_per_weekdag_totaal_merge['aantal'] / telling_klanten_per_weekdag_totaal_merge[
            'aantal dagen']).astype(int)

    klanten_per_werdag_grafiek = px.line(telling_klanten_per_weekdag_totaal_merge, x='weekdag naam',
                                         y='gem klanten per werkdag', color='apotheek',
                                         title='GEMIDDELD AANTAL KLANTEN PER WERKDAG', text='gem klanten per werkdag')

    # overzicht grafieken voor benchmark



    return klanten_per_werdag_grafiek, klanten_per_uur_grafiek

# TABBLAD 7: Callback voor overzicht telefonie

@callback(
    Output('inkomende telefoon', 'figure'),
    Input('jaar telefonie', 'value')
)
def telefonie(jaar):
    telefoon = telefonie_ag.copy()

    # dataframe is klaar.. maak een grafiek
    jaar_filter_telefoon = (telefoon['jaar'] == jaar)

    telefoon_1 = telefoon.loc[jaar_filter_telefoon]

    telefoon_grafiek = px.bar(telefoon_1, x='Apotheek', y='telefoon per dag (gem)', text_auto=True,
                              title='AANTAL BINNENKOMENDE TELEFOONTJES PER DAG (GEM) PER APOTHEEK')
    return telefoon_grafiek


# TABBLAD 8: Callback voor de service graad

@callback(
    Output('servicegraad ag', 'figure'),
    Input('servicegraad jaar', 'value'),
    Input('servicegraad type verstrekkingen', 'value')
)

def servicegraad(jaar, optie):
    service = recept_ag.copy()

    service_1 = service[['ddDatumRecept', 'ReceptHerkomst', 'cf',
                         'ndReceptnummer', 'sdATCODE', 'ndATKODE', 'sdEtiketNaam',
                         'ndAantal', 'Uitgifte', 'ndVoorraadTotaal',
                         'apotheek', 'sdMedewerkerCode']]

    # kolommen aanmaken voor maand en jaar
    service_1['ddDatumRecept'] = pd.to_datetime(service_1['ddDatumRecept'])
    service_1['jaar'] = service_1['ddDatumRecept'].dt.year
    service_1['maand'] = service_1['ddDatumRecept'].dt.month

    # kolom maken voor markering door voorraad 0

    service_1['voorraad na aanschrijven'] = service_1['ndVoorraadTotaal'] - service_1['ndAantal']

    # Markeer iedere regel als defectuur of voorraad toereikend

    conditie_service = [
        service_1['voorraad na aanschrijven'] >= 0,
        service_1['voorraad na aanschrijven'] < 0
    ]

    waarden_service = ['voorraad toereikend', 'defectuur']

    service_1['voorraad toereikend?'] = np.select(conditie_service, waarden_service, default='??')

    # filter uit het dataframe Dienst, Zorg, Distributie, Herhaalservice ,LSP-recepten, CF-recepten

    geen_dienst_service = (service_1['ReceptHerkomst'] != 'DIENST')
    geen_zorg_service = (service_1['ReceptHerkomst'] != 'Z')
    geen_distributie_service = (service_1['ReceptHerkomst'] != 'D')
    geen_LSP_service = (service_1['sdMedewerkerCode'] != 'LSP')
    geen_cf_service = (service_1['cf'] != 'J')
    geen_hhs_service = (service_1['ReceptHerkomst'] != 'H')
    geen_onbekende_voorraad = (service_1['voorraad toereikend?'] != '??')
    jaar_filter_service = (service_1['jaar'] == jaar)  # Dit is het filter voor de callback

    # Bouw hier een filter in voor: EU, EU & TU, Alles of spoedmedicatie



    EU = (service_1['Uitgifte'] == 'EU')
    EU_TU = ((service_1['Uitgifte'] == 'EU') | (service_1['Uitgifte'] == 'TU'))
    EU_TU_VU = ((service_1['Uitgifte'] == 'EU') | (service_1['Uitgifte'] == 'TU') | (service_1['Uitgifte'] == 'VU'))

    if optie == 'EU':
        filter_callback = EU

    if optie == 'EU & TU':
        filter_callback = EU_TU

    if optie == 'EU/TU/VU':
        filter_callback = EU_TU_VU


    # pas filters toe op het dataframe

    service_2 = service_1.loc[geen_dienst_service &
                              geen_zorg_service &
                              geen_distributie_service &
                              geen_LSP_service &
                              geen_cf_service &
                              geen_cf_service &
                              geen_hhs_service &
                              geen_onbekende_voorraad &
                              jaar_filter_service & filter_callback]

    # print(service_2['Uitgifte'].unique())

    # Nu tellen we per maand, per apotheek het aantal toereikend voorraad regels

    service_tellen_verdeling = service_2.groupby(by=['maand', 'apotheek', 'voorraad toereikend?'])[
        'voorraad toereikend?'].count().to_frame('aantal verdeling').reset_index()
    service_tellen_totaal = service_2.groupby(by=['maand', 'apotheek'])['voorraad toereikend?'].count().to_frame(
        'aantal totaal').reset_index()

    service_tellen_merge = service_tellen_verdeling.merge(service_tellen_totaal[['maand', 'apotheek', 'aantal totaal']],
                                                          how='left',
                                                          left_on=['maand', 'apotheek'],
                                                          right_on=['maand', 'apotheek'])

    service_tellen_merge['%'] = (
                (service_tellen_merge['aantal verdeling'] / service_tellen_merge['aantal totaal']) * 100).astype(int)

    voorraad_toereikend = (service_tellen_merge['voorraad toereikend?'] == 'voorraad toereikend')

    servicegraad = service_tellen_merge.loc[voorraad_toereikend]

    servicegraad_grafiek = px.line(servicegraad, x='maand', y='%', color='apotheek', text='%',
                                   title='SERVICEGRAAD PER MAAND AG')

    return servicegraad_grafiek






if __name__ == '__main__':
    app.run(debug=True)








