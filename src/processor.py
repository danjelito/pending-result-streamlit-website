import pandas as pd
import re
import io
from center_map import CenterMap


def load_files(files):
    """Reads multiple Excel files into a single concatenated DataFrame."""
    dataframes = []
    for file in files:
        df = pd.read_excel(file, skiprows=1) 
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True) if dataframes else None


def create_download_link(data):
    """Generates an Excel file for download from a dictionary of DataFrames."""
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        for sheet_name, df in data.items():
            if sheet_name == "Summary":
                df.to_excel(writer, sheet_name=sheet_name, index=True)
            else:
                df.to_excel(writer, sheet_name=sheet_name, index=False)
        writer.close()

    buffer.seek(0)  # Reset buffer position
    return buffer


def generate_report(df: pd.DataFrame) -> dict:
    """
    Generates a report from the given DataFrame by cleaning and transforming the data.

    The function performs the following steps:
    1. Renames columns to lowercase and replaces spaces with underscores.
    2. Drops columns and rows with all NaN values.
    3. Drops specific columns that are not needed for the report.
    4. Assigns new columns for time, date, center, teacher_clean, and area.
    5. Drops duplicate rows.
    6. Selects and renames specific columns for the final report.

    Args:
        df (pd.DataFrame): The input DataFrame containing the raw data.

    Returns:
        dict: A dictionary containing the cleaned and transformed data for each area,
              as well as unmapped data and the raw cleaned data.
              Keys are area names and values are DataFrames.
    """

    df_clean = (
        df.rename(columns=lambda x: x.strip().lower().replace(" ", "_"))
        .dropna(how="all", axis=1)
        .dropna(how="all", axis=1)
        .drop(
            columns=[
                "code",
                "center_name",
                "level_/_unit",
                "last_name",
                "first_name",
                "service_type",
                "start_time",
            ]
        )
        .assign(
            time=lambda df_: pd.to_datetime(df_["date"], errors="coerce").dt.time,
            month_=lambda df_: pd.to_datetime(df_["date"], errors="coerce").dt.strftime(
                "%Y-%m"
            ),
            date=lambda df_: pd.to_datetime(df_["date"], errors="coerce").dt.strftime(
                "%d %b %Y"
            ),
            center=lambda df_: df_["teacher"].apply(
                lambda x: (
                    re.search(r"\((.*?)\)", x).group(1)
                    if re.search(r"\((.*?)\)", x)
                    else ""
                )
            ),
            teacher_clean=lambda df_: df_["teacher"]
            .str.title()
            .apply(lambda x: re.sub(r"\s*\(.*?\)", "", x)),
            area=lambda df_: df_["center"].map(CenterMap().get_center_area_map()),
        )
        .drop_duplicates()
        .loc[
            :,
            [
                "teacher",
                "teacher_clean",
                "center",
                "area",
                "class_type",
                "date",
                "time",
                "month_",
            ],
        ]
        .rename(columns=lambda c: c.replace("_", " ").title().strip())
    )

    # Dictionary to store results
    result = {}

    # Create summary DF
    df_summary = (df_clean
        .groupby(["Area", "Teacher Clean", "Month"])
        .agg(count=("Teacher Clean", "count"))
        .reset_index()
        .rename(columns={"Teacher Clean": "Teacher", "Month": "Month", "count": "Count"})
        .sort_values(["Area", "Teacher", "Month"], ascending=[True, True, False])
        .pivot(index=["Area", "Teacher"], columns="Month", values="Count")
        .fillna(0)
        .astype(int)
    )
    df_summary = df_summary[df_summary.columns[::-1]]  # Reverse the column order
    result["Summary"] = df_summary 

    # Create DF per area
    for area in ["JKT 1", "JKT 2", "JKT 3", "BDG", "SBY", "CIK"]:
        df_area_result = df_clean.loc[df_clean["Area"] == area].reset_index(drop=True).drop(columns="Month")
        result[area] = df_area_result
    result["Unmapped"] = df_clean.loc[df_clean["Area"].isnull()]
    # Create raw data
    result["Raw Data"] = df_clean

    return result
