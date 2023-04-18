#3.2.4
import openai
import csv
import os
import re
import requests
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORG_ID")

def clean_plant_name(plant_name):
    plant_name = re.sub(r'\s+\d+(\.\d+)?\s?(CAL|G|IN)', '', plant_name)
    return plant_name

def convert_units(value):
    value = value.strip().lower()
    value = re.sub(r"\s*feet|\s*ft'", " ft", value)
    value = re.sub(r"\s*inches|\s*inch|\s*in'", " in", value)
    return value

def main():
    plants_file = open('plants.txt', 'r')
    plants = [(line.strip(), clean_plant_name(line.strip())) for line in plants_file.readlines()]

    with open('plant_info.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Plant Name", "Hardiness Zone", "Light Requirement", "Water Requirement", "Growth Rate", "Growth Habit", "Max Height", "Max Width", "Flower Color", "Flowering Season", "Tolerances", "Botanical Name"])

        for original_plant, cleaned_plant in plants:
            try:
                model_engine = "gpt-3.5-turbo"
                prompt = (f"please return, without any other text, concise plant attributes/information with only the following attributes in a csv form. Hardiness Zone, Light Requirement, Water Requirement, Growth Rate, Growth Habit, Max Height, Max Width, Flower Color, Flowering Season, Tolerances and Botanical name for the following plant: {cleaned_plant}.Please include all attributes in the output, separated by commas. If an attribute has no value, use a comma with no value next to it. For attributes with multiple values, separate them using a dash (-) instead of a comma.")

                response = openai.ChatCompletion.create(
                    model=model_engine,
                    messages=[{"role": "system", "content": "You are a helpful assistant that provides information about plants."},
                      {"role": "user", "content": prompt}],
                    max_tokens=1024,
                    n=1,
                    temperature=0.6
                )
                print(response)
                details = response.choices[0].message['content'].strip().split(',')

                max_height = convert_units(details[5].strip())
                max_width = convert_units(details[6].strip())

                details = [details[i].strip() for i in range(5)] + [max_height, max_width] + [details[i].strip() for i in range(7, 11)]

                writer.writerow([original_plant] + details)
                print(f"Got information for {original_plant}")
            except Exception as e:
                print(f"Error getting information for {original_plant}: {str(e)}")

if __name__ == "__main__":
    main()
