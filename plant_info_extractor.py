#3.1.4
# Import necessary libraries
import openai
import csv
import os
import re
import requests

# Set OpenAI API key and organization
openai.api_key = "OPENAI_API_KEY"
openai.organization = "YOUR_ORG_ID"

# Function to retrieve plant details using GPT-4
def get_plant_details(plant_name):
    # This model can be changed for easier or harder tasks
    model_engine = "text-davinci-002"
    prompt = (f"Provide detailed plant attributes for {plant_name} in a clear and structured format without any extra labels. "
              f"Include the following attributes, separated by semicolons: "
              f"Height, Spread, Soil, Sunlight, Bloom Time, Flower Color, Fragrance, and Hardiness Zones.")

    # Send API request, handle timeouts, and parse the response
    try:
        response = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.7, timeout=10)
    except requests.exceptions.ReadTimeout:
        print(f"Timeout reached for {plant_name}. Skipping.")
        return None

    response = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=1024, n=1, stop=None, temperature=0.7)

    details = response.choices[0].text.strip()

    # Extract and store plant attributes in a dictionary
    attributes = {
        "Height": convert_units(extract_attribute(r"height:?\s*((?:\d+-)?\d+\s*(?:ft|feet|inches|inch|in|\')?)", details)),
        "Spread": convert_units(extract_attribute(r"spread:?\s*((?:\d+-)?\d+\s*(?:ft|feet|inches|inch|in|\')?)", details)),
        "Soil": extract_attribute(r"soil:?\s*([\w\s-]+)", details),
        "Sunlight": extract_attribute(r"sunlight:?\s*([\w\s-]+)", details),
        "Bloom Time": extract_attribute(r"bloom time:?\s*([\w\s-]+)", details),
        "Flower Color": extract_attribute(r"flower color:?\s*([\w\s-]+)", details),
        "Fragrance": extract_attribute(r"fragrance:?\s*([\w\s-]+)", details),
        "Hardiness Zones": extract_attribute(r"hardiness zones:?\s*([\d\s-]+)", details),
    }

    return attributes

# Function to convert units in height and spread attributes
def convert_units(value):
    value = value.strip().lower()
    value = re.sub(r"\s*feet|\s*ft'", " ft", value)
    value = re.sub(r"\s*inches|\s*inch|\s*in'", " in", value)
    return value

# Function to extract an attribute from the text using regex
def extract_attribute(pattern, text):
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    else:
        return ""

# Function to clean plant names by removing size indicators
def clean_plant_name(plant_name):
    plant_name = re.sub(r'\s+\d+(\.\d+)?\s?(CAL|G|IN)', '', plant_name)
    return plant_name

# Main function to read plant names, retrieve their information, and write to a CSV file
def main():
    plants_file = open('plants.txt', 'r')
    plants = [clean_plant_name(line.strip()) for line in plants_file.readlines()]

    # Create and write to the CSV file
    with open('plant_info.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Plant Name", "Height", "Spread", "Soil", "Sunlight", "Bloom Time", "Flower Color", "Fragrance", "Hardiness Zones"])

        # Loop through plant names, get their details, and write to the CSV file
        for plant in plants:
            try:
                info = get_plant_details(plant)
                print(f"\n{plant} Plant Attributes:")
                for key, value in info.items():
                    print(f"{key}: {value}")
                writer.writerow([plant, info["Height"], info["Spread"], info["Soil"], info["Sunlight"], info["Bloom Time"], info["Flower Color"], info["Fragrance"], info["Hardiness Zones"]])
                print(f"Got information for {plant}")
            except Exception as e:
                print(f"Error getting information for {plant}: {str(e)}")

# Run the main function if the script is executed
if __name__ == "__main__":
    main()
