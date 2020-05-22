import pandas as pd
import os
from sqlalchemy import create_engine
engine = create_engine('sqlite://', echo=False)

csv_path = os.path.join(os.path.dirname(__file__), "..", "module1-introduction-to-sql", "buddymove_holidayiq.csv")
df = pd.read_csv(csv_path)
print(df)
