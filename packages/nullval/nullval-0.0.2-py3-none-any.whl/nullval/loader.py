import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET


############### loading the required files #############################################
################# formatting it to the required format ################################


def load_to_df(file_path):
    """
    Load data from CSV, XML, Excel, or JSON file into a Pandas DataFrame.

    Parameters:
    - file_path (str): Path to the file to be loaded.

    Returns:
    - df (DataFrame): Pandas DataFrame containing the loaded data.
    """
    try:
        # Determine file type based on extension
        file_type = file_path.split(".")[-1].lower()

        if file_type == "csv":
            df = pd.read_csv(file_path)
        elif file_type == "xml":
            tree = ET.parse(file_path)
            root = tree.getroot()

            data = []
            for item in root.findall("row"):
                row = {}
                for child in item:
                    row[child.tag] = child.text
                data.append(row)

            df = pd.DataFrame(data)
        elif file_type in ["xls", "xlsx"]:
            df = pd.read_excel(
                file_path, sheet_name="Sheet1"
            )  # Specify sheet name if necessary
        elif file_type == "json":
            df = pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        # Print information about columns
        print(f"Loaded {file_type.upper()} file successfully.")
        print("Columns:")
        print(df.columns)

        return df

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

    except Exception as e:
        print(f"Error loading file '{file_path}':")
        print(e)
        return None


#################### passing the data frame ##################################
################### spotting the location of the outliers #####################


def nulls_and_outs(df, q1=0.05, q3=0.95):
    """
    Finds the locations of null values and outliers in a DataFrame, and drops columns with categorical variables.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    q1 (float): The lower quartile value. Default is 0.25.
    q3 (float): The upper quartile value. Default is 0.75.

    Returns:
    dict: A dictionary with two keys 'nulls' and 'outliers', each containing the locations of null values and outliers respectively.
    pd.DataFrame: The DataFrame after dropping categorical columns.
    """
    # Drop categorical columns
    df = df.select_dtypes(exclude=["object", "category"])

    null_locations = {}
    outlier_indices = {}

    # Identify null values
    nulls = df.isnull()
    for col in df.columns:
        null_indices = nulls.index[nulls[col]].tolist()
        if null_indices:
            null_locations[col] = null_indices

    # Iterate over numeric columns
    for col in df.select_dtypes(include="number").columns:
        # Calculate quartiles and IQR
        Q1 = df[col].quantile(q1)
        Q3 = df[col].quantile(q3)
        IQR = Q3 - Q1

        # Define outlier boundaries
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        # Find indices of outliers
        outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index.tolist()

        # Store outliers in dictionary
        outlier_indices[col] = outliers

    return {
        "upper": upper_bound,
        "lower": lower_bound,
        "nulls": null_locations,
        "outliers": outlier_indices,
    }, df


# now that we have our indexes of the null values and the outliers
# based on the identified patterns in the data we create effective solutions to solve them
"""
step 1 - find the most ideal method for the appropriate solution
1- lagrange polynomial for the data points present in the middle really bad for extrapolation good for interpolation
when less points are considered for imputation
2 - splines is good for extrapolation 
4 - polynomail interpolation can be used for a variety of use cases with higher degree good for more complex relationships and viceversa




"""


"""

# Example usage:
data = {
    'A': [1, 2, 3, None, 5, 100],
    'B': [10, 12, None, 14, 16, 18],
    'C': ['cat', 'dog', 'cat', 'dog', 'cat', 'dog']
}
df = pd.DataFrame(data)

# Override quartile values
q1_override = 0.25
q3_override = 0.75

result, df_cleaned = nulls_and_outs(df, q1=q1_override, q3=q3_override)
print(result["lower"])
print(result["upper"])
print("Null values:", result['nulls'])
print("Outliers:", result['outliers'])
print("DataFrame after dropping categorical columns:")
print(df_cleaned)

"""
