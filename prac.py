#Note: The openai-python library support for Azure OpenAI is in preview.
import os
import openai
from dotenv import load_dotenv
load_dotenv()
openai.api_type = "azure"
openai.api_base = "https://ahex-ai.openai.azure.com/"
openai.api_version = "2023-09-15-preview"
openai.api_key = os.getenv("996d1769a4b14d96bd2ba7ec07f650f9")

response = openai.chat.completions.create(
  engine="MaybeatHome",
  prompt="### Postgres SQL tables, with their properties:\n#\n# Employee(id, name, department_id)\n# Department(id, name, address)\n# Salary_Payments(id, employee_id, amount, date)\n#\n### A query to list the names of the departments which employed more than 10 employees in the last 3 months\n\nSELECT Department.name\nFROM Department\nWHERE Department.id IN (\n    SELECT Employee.department_id\n    FROM Employee\n    WHERE Employee.id IN (\n        SELECT Salary_Payments.employee_id\n        FROM Salary_Payments\n        WHERE Salary_Payments.date >= NOW() - INTERVAL '3 months'\n        GROUP BY Salary_Payments.employee_id\n        HAVING COUNT(*) > 10\n    )\n)",
  temperature=0,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  stop=["#",";"])

print(response)