import pandas as pd
from porcupine.pca_scores import * 
import pytest 
import os 

data_path = os.path.join(os.path.dirname(__file__), 'random_dataset_run_pca.csv')
data_df = pd.read_csv(data_path)

def test_get_features_scores():
    reg = ['reg1','reg2','reg3','reg4','reg5']
    reg = pd.Series(reg)

    tar = ['tar1','tar2','tar3','tar4','tar5']
    tar = pd.Series(tar)
    result = get_features_scores(data_df,'pathway_test', reg, tar)
    R_result = pd.DataFrame({
        'pc1': [-0.32376649, -0.24143134,-0.45551180, 0.26443944, -0.46082036, 0.06025483, -0.38935195,-0.17027459, 0.40090910, -0.04652329],
        'pc2': [0.32023960, -0.47852493, -0.20569483, -0.47162908, 0.10547065, -0.38004211, 0.14675621, -0.43796926, 0.18524924, 0.02209828]
    })

    assert np.abs(result['pc1'].iloc[0]) == pytest.approx(np.abs(R_result['pc1'].iloc[0]), abs = 0.0001)
    assert np.abs(result['pc2'].iloc[0]) == pytest.approx(np.abs(R_result['pc2'].iloc[0]), abs = 0.0001)
    assert np.abs(result['pc1'].iloc[1]) == pytest.approx(np.abs(R_result['pc1'].iloc[1]), abs = 0.0001)
    assert np.abs(result['pc2'].iloc[1]) == pytest.approx(np.abs(R_result['pc2'].iloc[1]), abs = 0.0001)