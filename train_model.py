import os
import pandas as pd
from app import create_app, db
from app.models import Expense
from app.ml_logic import train_model, BASE_DIR

# Initialize Flask context
app = create_app()
app.app_context().push()

# Load existing training data
train_path = os.path.join(BASE_DIR, "..", "training_data.csv")
df_old = pd.read_csv(train_path) if os.path.exists(train_path) else pd.DataFrame(columns=["note","category"])

# Pull user-approved expense data from DB
data = [{"note": e.note, "category": e.category} for e in Expense.query.all() if e.note and e.category]
df_new = pd.DataFrame(data)

# Combine & clean
df = pd.concat([df_old, df_new]).drop_duplicates(subset=["note","category"])
df.to_csv(train_path, index=False)

# Retrain model
train_model()
print("✅ Model retrained and updated successfully.")
