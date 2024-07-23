import os
from tempfile import TemporaryDirectory
from logging import debug, info, warning

import pandas as pd
from numbers import Number
import re
from math import isnan
import numpy as np
from tqdm import tqdm

from openpyxl import load_workbook
from openpyxl_image_loader import SheetImageLoader

from mastdb.core.utils import print_json, value_cleanup, number_cleanup, array_formatter, yesno_cleanup, string_cleanup
from mastdb.core.io import APIConnector
from mastdb.services.references import ReferencesService
from mastdb.services.experiments import ExperimentsService
from mastdb.services.run_results import RunResultsService
from mastdb.services.numerical_models import NumericalModelsService

#
# Read Excel sheet functions
#

def read_experiments(filename: str) -> pd.DataFrame:
    """Read experiments from Summary sheet"""
    info("  Reading sheet (Summary)")
    Database_summary = pd.read_excel(open(filename, "rb"), sheet_name="Summary")

    # Initialize an empty list to store the data
    data_summary = []

    # Iterate through the rows
    for index, row in Database_summary.iterrows():
        # Check if the row is empty (all NaN values)
        if row.isnull().all():
            break  # Exit the loop if an empty row is encountered
        data_summary.append(row)
        
    # Convert the collected data to a new DataFrame
    experiments = pd.DataFrame(data_summary)

    # Rename the columns
    experiments.rename(columns = {
        "Building #": "building_id",
        "Scheme": "scheme",
        "Reference": "reference",
        "Publication year": "publication_year",
        "Short description": "description",
        "Experiment ID": "experiment_id",
        "Scale of test": "test_scale",
        "Number of simultaneous excitations": "simultaneous_excitations_nb",
        "Directions of applied excitations": "applied_excitation_directions",
        "Number of test runs": "run_results_nb",
        "Number of storeys": "storeys_nb",
        "Total building height": "total_building_height",
        "Diaphragm material": "diaphragm_material",
        "Roof material and geometry": "roof_material_geometry",
        "Type of masonry unit": "masonry_unit_type",
        "Masonry unit material": "masonry_unit_material",
        "Mortar type": "mortar_type",
        "Compressive strength of masonry": "masonry_compressive_strength",
        "Masonry walls thickness": "masonry_wall_thickness",
        "Number of wall leaves": "wall_leaves_nb",
        "Internal walls": "internal_walls",
        "Mechanical connectors present": "mechanical_connectors",
        "Activation of connectors": "connectors_activation",
        "Retrofitted": "retrofitted",
        "Application of retrofitting": "retrofitting_application",
        "Type of retrofitting": "retrofitting_type",
        "First estimated fundamental period": "first_estimated_fundamental_period",
        "Last estimated fundamental period": "last_estimated_fundamental_period",
        "Maximum horizontal PGA": "max_horizontal_pga",
        "Maximum estimated DG": "max_estimated_dg",
        "Material characterization available": "material_characterizations",
        "Associated type of test": "associated_test_types",
        "Reference for material characterization": "material_characterization_refs",
        "Experimental results reported": "experimental_results_reported",
        "Measured data openly available as digital files": "open_measured_data",
        "Link to request data": "link_to_request_data",
        "Digitalized data available": "digitalized_data",
        "Types of cracks observed": "crack_types_observed",
        "Motivation of the experimental campaign": "experimental_campaign_motivation",
        "Link to experimental paper": "link_to_experimental_paper",
        "Corresponding author": "corresponding_author_name",
    }, inplace=True)
    
    # Drop some columns
    del experiments["scheme"] # do not handle scheme image yet
    del experiments["run_results_nb"] # dynamically calculated

    # Split author string
    experiments[["corresponding_author_name", "corresponding_author_email"]] = experiments["corresponding_author_name"].str.rsplit("\n", n=1, expand=True)
    
    # Prepare array values
    for col in ["applied_excitation_directions", "masonry_wall_thickness", "retrofitting_type", "material_characterizations", "material_characterization_refs", "associated_test_types", "experimental_results_reported", "crack_types_observed"]:
        experiments[col] = experiments[col].apply(array_formatter)

    # Clean number values
    for col in ["publication_year", "storeys_nb", "total_building_height", "masonry_compressive_strength", "wall_leaves_nb", "first_estimated_fundamental_period", "last_estimated_fundamental_period", "max_horizontal_pga", "max_estimated_dg"]:
        experiments[col] = experiments[col].apply(number_cleanup)
    # for some reason pandas changes None for NaN, so we need to change it back
    experiments = experiments.replace({np.nan:None})
    
    # Split open measures data field
    experiments["link_to_open_measured_data"] = experiments["open_measured_data"].map(lambda x: x if x.startswith("http") else None)
    
    # Clean boolean values
    for col in ["open_measured_data", "digitalized_data", "internal_walls", "retrofitted"]:
        experiments[col] = experiments[col].apply(yesno_cleanup)

    # Clean string values
    for col in ["experimental_campaign_motivation"]:
        experiments[col] = experiments[col].apply(string_cleanup)

    building_heights = []
    link_to_material_papers = []
    for i in experiments["building_id"]:
        experiment_data = pd.read_excel(open(filename, "rb"), sheet_name=f"B{i}", usecols="A:C", header=15)
        # find experiment_data value when information is "Building height (without roof structure)"
        building_height = experiment_data[experiment_data["Information"] == "Building height (without roof structure)"]["Value"].values[0]
        building_heights.append(building_height)
        # find experiment_data value when information is "Link to material characterization document"
        # note: assuming links without Information are also material characterization documents
        experiment_links = experiment_data[(experiment_data["Value"].notna()) & (experiment_data["Value"].str.startswith("http")) & ((experiment_data["Information"].isna()) | (experiment_data["Information"].str.contains("Link to material characterization document")))]
        #print(experiment_links["Value"].tolist())
        link_to_material_papers.append(experiment_links["Value"].tolist())
    experiments["building_height"] = building_heights
    experiments["link_to_material_papers"] = link_to_material_papers

    return experiments

def read_references(filename: str) -> pd.DataFrame:
    """Read references from Test references sheet"""
    info("  Reading sheet (Test references)")
    references = pd.read_excel(open(filename, "rb"), sheet_name="Test references", usecols="A:C", header=1)
    references.drop("Excel sheet name", axis=1, inplace=True)
    references.rename(columns={"Building #": "experiment_id", "Reference": "full_reference"}, inplace=True)
    return references

def read_run_results(filename: str, experiment_ids) -> pd.DataFrame:
    """Read run results from the per-experiment sheets"""
    def run_id_check(x):
        if isinstance(x, Number):
            return not isnan(x)
        return x != None and x.strip() != "-"# and x.strip() != "Initial" and x.strip() != "Final"

    run_results = []
    for i in tqdm(experiment_ids, desc="Reading run results from experiment sheets", leave=False):
        debug(f"  Reading sheet (B{i})")
        results = pd.read_excel(open(filename, "rb"), sheet_name=f"B{i}", usecols="F:U", header=2)
        results = results.loc[results["Run ID"].apply(run_id_check)]
        results.rename(columns = {
            "Run ID": "run_id",
            "Nominal PGA X-dir.": "nominal_pga_x",
            "Nominal PGA Y-dir.": "nominal_pga_y",
            "Nominal PGA Z-dir.": "nominal_pga_z",
            "Actual PGA X-dir.": "actual_pga_x",
            "Actual PGA Y-dir.": "actual_pga_y",
            "Actual PGA Z-dir.": "actual_pga_z",
            "DG reported": "dg_reported",
            "DG derived": "dg_derived",
            "Max. Top Drift X-dir.": "max_top_drift_x",
            "Max. Top Drift Y-dir.": "max_top_drift_y",
            "Res. Top Drift X-dir.": "residual_top_drift_x",
            "Res. Top Drift Y-dir.": "residual_top_drift_y",
            "Base shear coef.": "base_shear_coef",
            "Reported T1 X-dir.": "reported_t1_x",
            "Reported T1 Y-dir.": "reported_t1_y",
        }, inplace=True)
        results["run_id"] = results["run_id"].map(lambda x: x if isinstance(x, Number) else x.strip())
        # Convert id column to string
        results["run_id"] = results["run_id"].astype(str)
        results["experiment_id"] = np.repeat(i, len(results))
        for col in ["reported_t1_x", "reported_t1_y"]:
            results[col] = results[col].apply(number_cleanup)
        # change NaN for None
        results = results.replace({np.nan:None})
        run_results.append(results)
    
    return pd.concat(run_results, ignore_index=True)

def read_experiment_images(filename: str, experiment_ids) -> TemporaryDirectory:
    """Read experiment images from the Summary sheet"""
    temp_dir = TemporaryDirectory()
    info(f"  Reading images from experiment sheets into {temp_dir.name}")
    wb = load_workbook(filename)
    sheet = wb["Summary"]
    image_loader = SheetImageLoader(sheet)
        
    row = 1
    for i in tqdm(experiment_ids, desc="Reading images from experiment sheets", leave=False):
        row += 1
        cell = f"B{row}"
        if image_loader.image_in(cell):
            image = image_loader.get(cell)
            #image.save(os.path.join("examples/images", f"B{i}.png"))
            image.save(os.path.join(temp_dir.name, f"{i}.png"))

    return temp_dir


def read_xlsx(filename: str, with_images: bool) -> pd.DataFrame:
    """Read experiments, references and run results from an Excel file"""
    # Experiments
    experiments = read_experiments(filename)
    # Full references
    Database_references = read_references(filename)

    # Extract some reference fields from the experiments data frame
    references = experiments[["reference", "publication_year", "link_to_experimental_paper", "corresponding_author_name", "corresponding_author_email", "link_to_request_data"]].drop_duplicates().copy()
    references["request_data_available"] = references["link_to_request_data"].map(lambda x: x if not x.startswith("http") else "Available on request")
    references["link_to_request_data"] = references["link_to_request_data"].map(lambda x: x if x.startswith("http") else None)
    references.index = np.arange(1, len(references)+1)
    # Clean reference fields from experiments
    experiments["reference_id"] = experiments["reference"].map(lambda x: references[references["reference"] == x].index[0])
    experiments = experiments.drop(["link_to_experimental_paper", "corresponding_author_name", "corresponding_author_email", "link_to_request_data"], axis=1)
    experiments.index = np.arange(1, len(experiments)+1)

    # Merge the references data frame with the full references data frame
    full_reference = pd.merge(experiments[["reference_id"]], Database_references, left_index=True, right_on="experiment_id").drop("experiment_id", axis=1).drop_duplicates()
    references = pd.merge(references, full_reference, left_index=True, right_on="reference_id").drop("reference_id", axis=1)

    # Run results
    run_results = read_run_results(filename, experiments["building_id"])

    # Images
    images_dir = None
    if with_images:
        images_dir = read_experiment_images(filename, experiments["building_id"])
    
    return experiments, references, run_results, images_dir

def read_numerical_models(conn: APIConnector, filename: str) -> pd.DataFrame:
    """Read numerical models from the Numerical models sheet"""
    info("Retrieving known building IDs")
    experiments = sorted(ExperimentsService(conn).list(), key=lambda x: x['building_id'])
    
    sheet_names = pd.ExcelFile(filename).sheet_names
    
    buildings_experiments = {}
    buildings_general_info = {}
    buildings_material_properties = {}
    for experiment in experiments:
        building_id = experiment["building_id"]
        sheet_name = f"B{building_id}"
        if sheet_name in sheet_names:
            debug(f"  Reading sheet: {sheet_name}")
            buildings_experiments[building_id] = experiment
            general_info = pd.read_excel(open(filename, "rb"), sheet_name=sheet_name, usecols="A:C", header=13, nrows=13)
            general_info.columns = ["Field", "Value", "Comment"]
            general_info["Value"] = general_info["Value"].apply(string_cleanup)
            general_info["Comment"] = general_info["Comment"].apply(string_cleanup)
            buildings_general_info[building_id] = general_info
            material_properties = pd.read_excel(open(filename, "rb"), sheet_name=sheet_name, usecols="A:D", header=28, nrows=9)
            material_properties.columns = ["Field", "Value", "Unit", "Comment"]
            material_properties["Value"] = material_properties["Value"].apply(value_cleanup)
            material_properties["Comment"] = material_properties["Comment"].apply(string_cleanup)
            buildings_material_properties[building_id] = material_properties
    
    return buildings_experiments, buildings_general_info, buildings_material_properties

def to_float(x):
    if x is None:
        return None
    val = x.replace(",", ".")
    if isinstance(x, str):
        val = re.sub(r'[^\d.]', '', x)
    try:
        return float(val)
    except:
        return val

def do_upload_models(conn: APIConnector, filename: str, dry_run: bool) -> None:
    """Upload a numerical models file to the MAST service

    Args:
        conn: API Connector instance to use
        filename: Path to the file to upload
    """
    # Check if the file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    info(f"Upload of {filename} to {conn.api_url}")
    exp_service = ExperimentsService(conn)
    num_models_service = NumericalModelsService(conn)
    
    buildings_experiments, buildings_general_info, buildings_material_properties = read_numerical_models(conn, filename)
    building_ids = sorted(buildings_experiments.keys())
    
    for building_id in tqdm(building_ids, total=len(building_ids), desc="Uploading numerical models", leave=False):
        experiment = buildings_experiments[building_id]
        general_info = buildings_general_info[building_id]
        material_properties = buildings_material_properties[building_id]
        numerical_model = {
            "experiment_id": experiment["id"],
        }
        general_info_fields = [
            { "name": "software_used", "label": "Software used", },
            { "name": "modeling_approach", "label": "Modeling approach", },
            { "name": "units", "label": "Units of the model", },
            { "name": "frame_elements", "label": "Element type for frame elements", },
            { "name": "diaphragm_elements", "label": "Element type for diaphragms", },
            { "name": "damping_model", "label": "Damping model", },
            { "name": "global_geometry_def", "label": "Global geometry definition", },
            { "name": "element_geometry_def", "label": "Element geometry definition", },
            { "name": "mass_def", "label": "Mass definition", },
            { "name": "gravity_loads_def", "label": "Gravity loads definition", },
            { "name": "wall_connections", "label": "Wall-to-wall connections", },
            { "name": "floor_connections", "label": "Floor-to-wall connections", },
            { "name": "base_support", "label": "Base support", }
        ]
        
        for field in general_info_fields:
            numerical_model[field["name"]] = general_info[general_info["Field"] == field["label"]]["Value"].values[0]
            numerical_model[f"{field['name']}_comment"] = general_info[general_info["Field"] == field["label"]]["Comment"].values[0]
        
        material_properties_fields = [
            { "name": "elastic_modulus", "label": "Elastic modulus of elasticity", },
            { "name": "shear_modulus", "label": "Shear modulus", },
            { "name": "compression_strength", "label": "Compression strength", },
            { "name": "tension_strength", "label": "Tension strength", },
            { "name": "cohesion", "label": "Cohesion", },
            { "name": "friction_coeff", "label": "Friction coefficient", },
            { "name": "residual_friction_coeff", "label": "Residual friction coefficient", },
            { "name": "damping_ratio", "label": "Damping ratio", },
            { "name": "softening_coeff", "label": "Softening coefficient", },
        ]

        for field in material_properties_fields:
            numerical_model[field["name"]] = to_float(material_properties[material_properties["Field"].str.contains(field["label"])]["Value"].values[0])
            numerical_model[f"{field['name']}_comment"] = material_properties[material_properties["Field"].str.contains(field["label"])]["Comment"].values[0]
            if field["name"] == "elastic_modulus":
                numerical_model[field["name"]] = int(numerical_model[field["name"]]) if numerical_model[field["name"]] is not None else None
        
        if dry_run:
            info(f"  [{building_id}] Numerical model")
            print_json(numerical_model)
        else:
            # delete previous numerical model
            exp_service.delete_numerical_model(numerical_model["experiment_id"])
            # create new numerical model
            num_models_service.create(numerical_model)
    

def do_upload(conn: APIConnector, filename: str, with_images: bool, dry_run: bool) -> None:
    """Upload a database file to the MAST service

    Args:
        conn: API Connector instance to use
        filename: Path to the file to upload
    """
    # Check if the file exists
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    info(f"Upload of {filename} to {conn.api_url}")

    # Read the Excel file
    experiments, references, results, images_dir = read_xlsx(filename, with_images)
    
    if dry_run:
        info("Dry run: no data will be uploaded")
        info("  Writing experiments.csv")
        experiments.to_csv("experiments.csv", sep=",", index=False)
        info("  Writing references.csv")
        references.to_csv("references.csv", sep=",", index=False)
        return
    
    # Use services
    ref_service = ReferencesService(conn)
    exp_service = ExperimentsService(conn)
    res_service = RunResultsService(conn)
    # map reference short name to IDs from the database
    ref_ids = {}
    # map experiment IDs from the Excel file to IDs from the database
    exp_ids = {}
    
    # Write the references to the database
    for index, row in tqdm(references.iterrows(), total=references.shape[0], desc="Uploading references", leave=False):
        debug(f">>> checking reference {index}")
        try:
            debug(f">>> adding or updating reference {index}")
            res = ref_service.createOrUpdate(row.to_dict())
            ref_ids[row["reference"]] = res["id"]
            debug(f"<<< reference {index} written with ID {res['id']}")
        except Exception as e:
            warning(f"<<< reference {index} not written: {e}")
    
    # Apply the reference IDs from the database to the experiments
    experiments["reference_id"] = experiments["reference"].map(lambda x: int(ref_ids[x]) if x in ref_ids else None)
    experiments = experiments.drop("reference", axis=1)

    # Write the experiments to the database
    for index, row in tqdm(experiments.iterrows(), total=experiments.shape[0], desc="Uploading experiments", leave=False):
        if not row["reference_id"] or isnan(row["reference_id"]):
            debug(f">>> NOT writing experiment {index}: {row['reference_id']}")
            continue
        debug(f">>> writing experiment {index}")
        try:
            res = exp_service.createOrUpdate(row.to_dict())
            exp_ids[row["building_id"]] = res["id"]
            debug(f"<<< experiment {index} written with ID {res['id']}")
        except Exception as e:
            warning(f"<<< experiment {index} not written: {e}")

    # Upload experiment images
    if images_dir is not None:
        info(f"Uploading scheme images from {images_dir.name}")
        for img_filename in tqdm(os.listdir(images_dir.name), desc="Uploading images", leave=False):
            try:
                # image file is named by the experiment ID in the Excel file
                exp_id = int(img_filename.split(".")[0])
                res = exp_service.upload_scheme_file(exp_ids[exp_id], os.path.join(images_dir.name, img_filename))
                debug(f"<<< image {img_filename} uploaded with response {res}")
            except Exception as e:
                warning(f"<<< image {img_filename} not uploaded: {e}")
        images_dir.cleanup()
    
    # Apply the experiment IDs to the results
    results["experiment_id"] = results["experiment_id"].map(lambda x: int(exp_ids[x]) if x in exp_ids else None)

    # Write the run results to the database
    info(f"Uploading run results")
    exp_run_results_deleted = []
    for index, row in tqdm(results.iterrows(), total=results.shape[0], desc="Uploading run results", leave=False):
        if not row["experiment_id"] or isnan(row["experiment_id"]):
            debug(f">>> NOT writing run result {index}: {row['experiment_id']}")
            continue
        debug(f">>> writing run result {index} from experiment {row['experiment_id']}")
        try:
            if row["experiment_id"] not in exp_run_results_deleted:
                exp_service.delete_run_results(row["experiment_id"])
                exp_run_results_deleted.append(row["experiment_id"])
            payload = row.to_dict()
            res = res_service.create(payload)
            debug(f"<<< run result {index} written")
        except Exception as e:
            warning(f"<<< run result {index} not written: {e}")
    