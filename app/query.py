import os
from google.oauth2 import service_account
from google.cloud import bigquery
from google.cloud import language
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

# Load the credentials from the environment variable
print(os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

bigquery_client = bigquery.Client()

# Initialize Language client
language_client = language.LanguageServiceClient()


# Function to convert natural language to SQL using Gemini
def convert_nl_to_sql(natural_language_prompt):
    document = language.Document(content=natural_language_prompt, type_=language.Document.Type.PLAIN_TEXT)
    response = language_client.analyze_syntax(document=document)
    print(f"type(response): {type(response)}")
    print(f"response: {response}")

    # This is a placeholder for the actual Gemini API call
    # You would need to replace this with the actual API call to Gemini
    # sql_query = "SELECT * FROM your_table WHERE condition"  # Replace with actual logic

    return response

# Example natural language prompt
natural_language_prompt = ("Generate a SQL query that returns the 10 most frequent words in Shakespeare's works."
                           "Select from bigquery-public-data.samples.shakespeare")

# Convert to SQL
sql_query = convert_nl_to_sql(natural_language_prompt)

# Execute the SQL query
query_job = bigquery_client.query(sql_query)

# Fetch results
results = query_job.result()

# Print results
for row in results:
    print(row)