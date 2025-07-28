import xml.etree.ElementTree as ET
import pandas as pd
import os

def transform_xml():
    xml_path = "/opt/airflow/data/PrixCarburants_instantane.xml"
    output_path = "/opt/airflow/data/clean.csv"

    tree = ET.parse(xml_path)
    root = tree.getroot()

    rows = []
    for pdv in root.findall("pdv"):
        station_id = pdv.attrib.get("id")
        lat = pdv.attrib.get("latitude")
        lon = pdv.attrib.get("longitude")
        cp = pdv.attrib.get("cp")
        ville = pdv.findtext("ville", default="Inconnu")

        for prix in pdv.findall("prix"):
            carburant = prix.attrib.get("nom")
            valeur = prix.attrib.get("valeur")
            date = prix.attrib.get("maj")

            rows.append({
                "station_id": station_id,
                "latitude": lat,
                "longitude": lon,
                "code_postal": cp,
                "ville": ville,
                "carburant": carburant,
                "prix": float(valeur) / 100,
                "date_maj": date
            })

    df = pd.DataFrame(rows)
    df["date_maj"] = pd.to_datetime(df["date_maj"])
    df.to_csv(output_path, index=False)
    print("✅ Données transformées sauvegardées dans", output_path)
