# Plant Information Extractor 
This is a Python script that extracts plant information using OpenAI gpt-3.5-turbo and writes the information to a CSV file. The main function reads plant names from a file named plants.txt, retrieves their information using the gpt-3.5-turbo model, and writes the information to a CSV file named plant_info.csv. The script is easily adaptable for various purposes and can be extended to work with other objects or APIs.

## Requirements

- Python 3.7+
- OpenAI Python package
- Python-dotenv package
- An OpenAI API key

# requirements.txt
```
openai==0.27.0
python-dotenv==0.19.2
requests==2.26.0
```

## Setup
### Install the required libraries using pip:

```
pip install -r requirements.txt
```

Obtain an API key from OpenAI and set the openai.api_key variable in the script to your API key.

Set the openai.organization variable in the script to your organization ID.

Set up an environment file `.env` with the following content:
```
OPENAI_API_KEY=your_openai_api_key
OPENAI_ORG_ID=your_openai_organization_id
```
### Usage
Create a file named plants.txt and add plant names, one per line.

Run the script:

```
python plant_info_extractor.py
```

The extracted plant information will be saved in a CSV file named plant_info.csv.

### Other Uses

This script can be adapted for various purposes, such as:

Extracting information about animals, minerals, or other objects by modifying the prompt in the get_plant_details function.
Retrieving information from other APIs or sources by replacing the text-davinci-002 API call in the get_plant_details function.
Saving the extracted information in different file formats or databases by modifying the file handling code in the main function.
Adapting the code for web scraping by integrating it with a web scraping library such as Beautiful Soup or Scrapy.
