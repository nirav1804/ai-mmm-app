import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import numpy as np

def run_meridian_model(df, media_cols, target_col):
    df = df.copy()
    df = df.dropna()
    
    X = df[media_cols]
    y = df[target_col]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = LinearRegression()
    model.fit(X_scaled, y)

    coef = model.coef_

    results = pd.DataFrame({
        'media_channel': media_cols,
        'coefficient': coef,
        'normalized_contribution': coef / np.sum(np.abs(coef)),
        'estimated_roi': coef / X.mean().values
    })

    return results
