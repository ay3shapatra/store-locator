import pandas as pd
import re

# Load the Excel file
df = pd.read_excel("kisnastoresindia.xlsx")

def extract_components(address):
    if pd.isna(address):
        return pd.Series([None]*6)
    
    house = re.search(r'\b([A-Z]?\d+/\d+|[A-Z]?\d+-\d+|[A-Z]?\d+)\b', address)
    street = re.search(r'([A-Za-z\s]+(?:Marg|Road|Street|Lane))', address)
    landmark = re.search(r'(Near [^,]+|Opposite [^,]+)', address)
    postal = re.search(r'\b\d{6}\b', address)
    floor = re.search(r'(Ground Floor|First Floor|Second Floor)', address, re.IGNORECASE)
    locality = re.search(r',\s*([^,]+?),\s*[A-Za-z]+[-\s\d]*$', address)

    return pd.Series([
        house.group(1) if house else None,
        street.group(1) if street else None,
        landmark.group(1) if landmark else None,
        locality.group(1) if locality else None,
        postal.group(0) if postal else None,
        floor.group(1) if floor else None
    ])

# Apply function and add new columns
df[['House Number', 'Street', 'Landmark', 'Locality', 'Postal Code', 'Floor Info']] = df['Store Address'].apply(extract_components)

# Save to a new Excel file
df.to_excel("kisnastoresindia_with_components.xlsx", index=False)

print("✅ File saved as 'kisnastoresindia_with_components.xlsx'")
