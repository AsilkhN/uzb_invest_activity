import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier


def classification():
    # Load data
    train_data = pd.read_excel('invest_reg.xlsx', sheet_name='train_r', usecols=[1, 2, 3, 4, 5, 6])
   
    # Extract target variable and features
    X_train = train_data.drop('Уровень инвестиционной активности', axis=1)
    y_train = train_data['Уровень инвестиционной активности']

    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Load data from the test file
    test_data = pd.read_excel('invest_reg.xlsx', sheet_name='predict', usecols=[1, 2, 3, 4, 5])
    regname = pd.read_excel('invest_reg.xlsx', sheet_name='predict')
   
    # Classify regions
    predictions = model.predict(test_data)

    predictions = dict(zip(regname['Регионы'], predictions))

    return predictions

    # # Add a column with predictions to the region data
    # test_data['Уровень инвестиционной активности'] = predictions

    # # Save the results to a new file
    # test_data.to_excel('reg_class.xlsx', index=False)

    # # Output the result
