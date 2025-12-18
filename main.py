from docxtpl import DocxTemplate, InlineImage
from docx2pdf import convert
from data import csv_to_summary
from graphs_daily import export_graphs



folder_path = r"C:\pyprojects\VEB_report_automation\Data\Data_cleaned"
output_folder = r"C:\pyprojects\VEB_report_automation\Data"

#Create summary statistics and export graphs
loaded_names, summary_stats=csv_to_summary(folder_path,output_folder,separator_name=" ")
export_graphs(folder_path, output_folder,separator_name=" ")


#template
template = DocxTemplate("WZC ... - Meetcampagne.docx")


#Variables
name_project ="WZC Breugheldal"
bouwjaar = "1956"
number_verdiepingen = "drie"
ventilatie_type = "D"
gebruik_uren= "09u30 – 19u30"
luchtgroep_locatie= "kelder"
regeling= "07u00 – 22u00"

#rooms and their different specifications
rooms={"rooms_1" : {"name":summary_stats.loc[0,"Device"],
                    "luchtgroep_locatie":luchtgroep_locatie,
                    "ventilatie_type":ventilatie_type,
                    "regeling":regeling,
                    "debiet":"P: 750 m³/h - E: 375 m³/h",
                    "gebruik_uren":gebruik_uren,
                    "gemiddelde_CO2":f"{summary_stats.loc[0,"Mean_All"]:.0f} ppm" ,
                    "minimum_CO2":f"{summary_stats.loc[0,"Min_All"]:.0f} ppm",
                    "maximum_CO2":f"{summary_stats.loc[0,"Max_All"]:.0f} ppm",
                    "CO2_under_900":f"{summary_stats.loc[0,"Percent_Under_900_All"]:.0f} %" if summary_stats.loc[0,"Percent_Under_900_All"]== 100 else f"{summary_stats.loc[0,"Percent_Under_900_All"]:.1f} %",
                    "CO2_under_1200":f"{summary_stats.loc[0,"Percent_Under_1200_All"]:.0f} %" if summary_stats.loc[0,"Percent_Under_1200_All"]== 100 else f"{summary_stats.loc[0,"Percent_Under_1200_All"]:.1f} %",
                    "graph_meetcampagne":InlineImage(template, f"{summary_stats.loc[0,'Device']}_daily.png", width=4000000),
                    "graph_dagelijkse_concentratie":InlineImage(template,  f"{output_folder}\\Graphs\\{summary_stats.loc[0,'Device']}_hourly.png", width=5500000)
                    }
}



#lien entre les données et les noms mis sur word
context = {
    "site_name": name_project,
    "bouwjaar": bouwjaar,
    "verdiepingen": number_verdiepingen,
    "ventilatie_type": ventilatie_type,
    #room 1
    "name_1": rooms["rooms_1"]["name"],
    "luchtgroep_locatie_1": rooms["rooms_1"]["luchtgroep_locatie"],
    "ventilatie_type_1": rooms["rooms_1"]["ventilatie_type"],
    "regeling_1": rooms["rooms_1"]["regeling"],
    "debiet_1": rooms["rooms_1"]["debiet"],
    "gebruik_uren_1": rooms["rooms_1"]["gebruik_uren"],
    "gemiddelde_CO2_1": rooms["rooms_1"]["gemiddelde_CO2"],
    "minimum_CO2_1": rooms["rooms_1"]["minimum_CO2"],
    "maximum_CO2_1": rooms["rooms_1"]["maximum_CO2"],
    "CO2_under_900_1": rooms["rooms_1"]["CO2_under_900"],
    "CO2_under_1200_1": rooms["rooms_1"]["CO2_under_1200"],
    #"graph_meetcampagne_1": rooms["rooms_1"]["graph_meetcampagne"],
    "graph_dagelijkse_concentratie_1":rooms["rooms_1"]["graph_dagelijkse_concentratie"] ,

 

}

# Rendre le document
template.render(context)

# Sauvegarder en Word
output_docx = f"{name_project} - Meetcampagne.docx"
template.save(output_docx)