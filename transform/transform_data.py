import xml.etree.ElementTree as ET
import pandas as pd
import os
from config.config import RAW_DATA_PATH, CLEAN_DATA_PATH

def transform_xml():
    tree = ET.parse(RAW_DATA_PATH)
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
    df.dropna(subset=["prix"], inplace=True)
    df = df[df["prix"] > 0]
    df["date_maj"] = pd.to_datetime(df["date_maj"])
    df.to_csv(CLEAN_DATA_PATH, index=False)
    print("✅ Données transformées sauvegardées dans", CLEAN_DATA_PATH)
