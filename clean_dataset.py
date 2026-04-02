"""
Nettoyage du dataset Dataset_complet_Meteo.xlsx
------------------------------------------------
Probleme: Excel a converti des valeurs numeriques en dates.
Ex: 21.9 (°C) -> 21 septembre 2026 -> 2026-09-21

Formule de recuperation: valeur = jour + mois / 10
Ex: 2026-09-21 -> 21 + 9/10 = 21.9

Colonnes supprimees: id, sunrise, sunset (inutiles)
"""

import pandas as pd
import numpy as np

INPUT_FILE = "data/Dataset_complet_Meteo.xlsx"
OUTPUT_FILE = "data/Dataset_complet_Meteo_clean.xlsx"

# Colonnes numeriques corrompues par Excel (nombres -> dates)
CORRUPTED_COLS = [
    "temperature_2m_max",
    "temperature_2m_min",
    "temperature_2m_mean",
    "apparent_temperature_max",
    "apparent_temperature_min",
    "apparent_temperature_mean",
    "wind_speed_10m_max",
    "wind_gusts_10m_max",
    "shortwave_radiation_sum",
]

# Plages de valeurs raisonnables pour validation (Cameroun)
VALID_RANGES = {
    "temperature_2m_max": (15, 50),
    "temperature_2m_min": (5, 35),
    "temperature_2m_mean": (10, 45),
    "apparent_temperature_max": (15, 55),
    "apparent_temperature_min": (5, 35),
    "apparent_temperature_mean": (10, 45),
    "wind_speed_10m_max": (0, 80),
    "wind_gusts_10m_max": (0, 120),
    "shortwave_radiation_sum": (0, 40),
}

# Colonnes a supprimer (inutiles pour l'import)
DROP_COLS = ["id", "sunrise", "sunset"]


def recover_from_datetime(val):
    """Recupere la valeur numerique d'un datetime corrompu.
    Excel a lu '21.9' comme '21 septembre' -> 2026-09-21.
    Formule inverse: jour + mois / 10.
    """
    if hasattr(val, "day") and hasattr(val, "month"):
        return val.day + val.month / 10
    return None


def fix_column(series, col_name):
    """Corrige une colonne corrompue: datetime -> float, str -> float."""
    fixed = pd.Series(index=series.index, dtype=float)
    n_recovered = 0
    n_parsed = 0
    n_failed = 0

    for i, val in series.items():
        if pd.isna(val):
            fixed[i] = np.nan
        elif hasattr(val, "day"):
            # Datetime corrompu -> recuperer le nombre
            fixed[i] = recover_from_datetime(val)
            n_recovered += 1
        else:
            # String ou nombre -> convertir en float
            try:
                fixed[i] = float(val)
                n_parsed += 1
            except (ValueError, TypeError):
                fixed[i] = np.nan
                n_failed += 1

    # Validation des plages
    lo, hi = VALID_RANGES.get(col_name, (None, None))
    if lo is not None:
        out_of_range = ((fixed < lo) | (fixed > hi)) & fixed.notna()
        n_out = out_of_range.sum()
        if n_out > 0:
            print(f"  ATTENTION: {n_out} valeurs hors plage [{lo}, {hi}]")
            fixed[out_of_range] = np.nan

    print(f"  {col_name}: {n_recovered} datetime recuperes, {n_parsed} str ok, {n_failed} echecs")
    return fixed


def main():
    print(f"Lecture de {INPUT_FILE}...")
    df = pd.read_excel(INPUT_FILE)
    print(f"  {len(df)} lignes, {len(df.columns)} colonnes\n")

    # Supprimer les colonnes inutiles
    cols_to_drop = [c for c in DROP_COLS if c in df.columns]
    if cols_to_drop:
        df.drop(columns=cols_to_drop, inplace=True)
        print(f"Colonnes supprimees: {cols_to_drop}\n")

    # Corriger les colonnes corrompues
    print("Correction des colonnes corrompues:")
    for col in CORRUPTED_COLS:
        if col in df.columns:
            df[col] = fix_column(df[col], col)

    # Convertir 'time' en date propre
    if "time" in df.columns:
        df["time"] = pd.to_datetime(df["time"]).dt.date

    # Stats finales
    print(f"\nResultat final:")
    print(f"  Lignes: {len(df)}")
    print(f"  Colonnes: {len(df.columns)}")
    print(f"  Colonnes: {list(df.columns)}")

    # Verifier qu'il n'y a plus de datetime dans les colonnes numeriques
    for col in CORRUPTED_COLS:
        if col in df.columns:
            assert df[col].dtype in [np.float64, np.float32, float], \
                f"{col} n'est pas float: {df[col].dtype}"

    print(f"\nNulls par colonne:")
    nulls = df.isnull().sum()
    for col in nulls[nulls > 0].index:
        print(f"  {col}: {nulls[col]} ({nulls[col]/len(df)*100:.1f}%)")

    print(f"\nSauvegarde dans {OUTPUT_FILE}...")
    df.to_excel(OUTPUT_FILE, index=False)
    print("Termine!")


if __name__ == "__main__":
    main()
