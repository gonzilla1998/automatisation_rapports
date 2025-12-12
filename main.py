from docxtpl import DocxTemplate
from docx2pdf import convert
from data import csv_to_summary
from graphs import export_graphs



folder_path = r"C:\pyprojects\VEB_report_automation\Data\Cleaned"
output_folder = r"C:\pyprojects\VEB_report_automation\Data"
summary_stats=csv_to_summary(folder_path,output_folder)
export_graphs(folder_path, output_folder)


#template
template = DocxTemplate("WZC ... - Meetcampagne.docx")


#Variables
name_project ="test"
bouwjaar = "1956"
number_verdiepingen = "3"
ventilatie_type = "D"
gebruik_uren= "09u30 – 19u30"

#rooms and their different specifications
rooms={"rooms_1" : {"name":"test",
                    "luchtgroep_locatie":"",
                    "ventilatie_type":ventilatie_type,
                    "regeling":"",
                    "debiet":"",
                    "gebruik_uren":gebruik_uren,
                    "gemiddelde_CO2":"",
                    "minimum_CO2":"",
                    "maximum_CO2":"",
                    "CO2_under_900":"",
                    "CO2_under_1200":"",
                    },
       "rooms_2": {"name": "",
                   "luchtgroep_locatie": "",
                   "ventilatie_type": ventilatie_type,
                   "regeling": "",
                   "debiet": "",
                   "gebruik_uren": gebruik_uren,
                   "gemiddelde_CO2": "",
                   "minimum_CO2": "",
                   "maximum_CO2": "",
                   "CO2_under_900": "",
                   "CO2_under_1200": "",
                    },
        "rooms_3" : {"name":"",
                    "luchtgroep_locatie":"",
                    "ventilatie_type":ventilatie_type,
                    "regeling":"",
                    "debiet":"",
                    "gebruik_uren": gebruik_uren,
                    "gemiddelde_CO2":"",
                    "minimum_CO2":"",
                    "maximum_CO2":"",
                    "CO2_under_900":"",
                    "CO2_under_1200":"",
                    },
        "rooms_4" : {"name":"",
                    "luchtgroep_locatie":"",
                    "ventilatie_type":ventilatie_type,
                    "regeling":"",
                    "debiet":"",
                    "gebruik_uren": gebruik_uren,
                    "gemiddelde_CO2":"",
                    "minimum_CO2":"",
                    "maximum_CO2":"",
                    "CO2_under_900":"",
                    "CO2_under_1200":"",
                    },
        "rooms_5" : {"name":"",
                    "luchtgroep_locatie":"",
                    "ventilatie_type":ventilatie_type,
                    "regeling":"",
                    "debiet":"",
                    "gebruik_uren": gebruik_uren,
                    "gemiddelde_CO2":"",
                    "minimum_CO2":"",
                    "maximum_CO2":"",
                    "CO2_under_900":"",
                    "CO2_under_1200":"",
                    },

}



#lien entre les données et les noms mis sur word
context = {
    "site_name": "Zaventem",
    "bouwjaar": bouwjaar,
    "verdiepingen": number_verdiepingen,
    "ventilatie_type": ventilatie_type,
    #room 1
    "1_name": rooms["rooms_1"]["name"],
    "1_luchtgroep_locatie": rooms["rooms_1"]["luchtgroep_locatie"],
    "1_ventilatie_type": rooms["rooms_1"]["ventilatie_type"],
    "1_regeling": rooms["rooms_1"]["regeling"],
    "1_debiet": rooms["rooms_1"]["debiet"],
    "1_gebruik_uren": rooms["rooms_1"]["gebruik_uren"],
    "1_gemiddelde_CO2": rooms["rooms_1"]["gemiddelde_CO2"],
    "1_minimum_CO2": rooms["rooms_1"]["minimum_CO2"],
    "1_maximum_CO2": rooms["rooms_1"]["maximum_CO2"],
    "1_CO2_under_900": rooms["rooms_1"]["CO2_under_900"],
    "1_CO2_under_1200": rooms["rooms_1"]["CO2_under_1200"],



    "room_2": rooms["rooms_2"],
    "room_3": rooms["rooms_3"],
    "room_4": rooms["rooms_4"],
    "room_5": rooms["rooms_5"]

}

# Rendre le document
template.render(context)

# Sauvegarder en Word
output_docx = f"WZC {name_project} - Meetcampagne.docx"
template.save(output_docx)