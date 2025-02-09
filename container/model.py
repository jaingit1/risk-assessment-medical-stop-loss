import os
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import RandomOverSampler
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

# Paths and directories
source_dir = 'generated_data'
os.makedirs(source_dir, exist_ok=True)
policy_summary_data_path = os.path.join(source_dir, 'policy_summary_data.csv')

# Load DataFrames from CSV files
df_main_loaded = pd.read_csv(policy_summary_data_path)
df_model = df_main_loaded.copy()
df_model.fillna(0, inplace=True)

# Features and target definition
features = ['Medical Paid', 'RX Paid','Ongoing Treatment']
target = 'RN Recommendations (Target)'
all_features = features

# Label encoding for the target variable
label_encoder = LabelEncoder()
df_model['Target'] = label_encoder.fit_transform(df_model[target])

# Preprocessing pipelines
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])
# categorical_transformer = Pipeline(steps=[
#     ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
#     ('onehot', OneHotEncoder(sparse_output=False, drop='first'))
# ])

# Column transformer
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, features)
        # ('cat', categorical_transformer, categorical_features)
    ])

# Full pipeline with preprocessing and model
model_pipeline = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('classifier', RandomForestClassifier(random_state=42))
])

# Split the data into train and test sets
X = df_model[all_features]
y = df_model['Target']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Oversample the training data
ros = RandomOverSampler(random_state=42)
X_train_resampled, y_train_resampled = ros.fit_resample(X_train, y_train)

# Fit the pipeline
model_pipeline.fit(X_train_resampled, y_train_resampled)

# Save the pipeline
joblib.dump(model_pipeline, 'risk_assessment_model_pipeline.pkl')
print("Model pipeline saved to 'risk_assessment_model_pipeline.pkl'")
