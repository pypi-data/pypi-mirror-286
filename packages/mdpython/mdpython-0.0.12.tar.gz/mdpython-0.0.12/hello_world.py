import mdpython.fileutils.excel as mdexcel
import json
from mdpython.datautils import jsonutil

# Get URLs
xl = mdexcel.Excel(r"c:\users\dell\onedrive\desktop\dummy_data.xlsx")
urls = xl.extract_urls(["A", "B"])
print(json.dumps(urls['data'], indent=2))

# Save as CSV
jsonutil.list_to_csv(urls['data'], r"c:\users\dell\onedrive\desktop\out.csv",
                     colkey=urls['keys'])
