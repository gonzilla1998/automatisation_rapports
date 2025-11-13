from docxtpl import DocxTemplate
from docx2pdf import convert

#template
template = DocxTemplate("WZC ... - Meetcampagne.docx")


#Variables
name_project ="test"
bouwjaar = "1956"
number_verdiepingen = "3"
ventilatie_type = "D"
gebruikuren= "09u30 – 19u30"

#rooms and their different specifications
rooms={"rooms_1" : {"name":"",
                    "luchtgroep_locatie":"",
                    "ventilatie_type":ventilatie_type,
                    "regeling":"",
                    "debiet":"",
                    "gebruikuren":gebruikuren,
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
                   "gebruikuren": gebruikuren,
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
                    "gebruikuren": gebruikuren,
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
                    "gebruikuren": gebruikuren,
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
                    "gebruikuren": gebruikuren,
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
    "room_1": rooms["rooms_1"],
    "room_2": rooms["rooms_2"],
    "room_3": rooms["rooms_3"],
    "room_4": rooms["rooms_4"],
    "room_5": rooms["rooms_5"],
    "ventilatie_type":ventilatie_type

}

# Rendre le document
template.render(context)

# Sauvegarder en Word
output_docx = f"WZC {name_project} - Meetcampagne.docx"
template.save(output_docx)