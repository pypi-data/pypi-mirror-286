from porcupine.porcupine import *
import pytest

def test_calculate_statistics():
    res_pca_pathway = pd.DataFrame({
        'pathway': ['pathway1'],
        'pathway_size': [5],
        'pc1': [3.5]
    })

    res_pca_rndm_set = pd.DataFrame({
        'pathway_size': [5, 5, 5, 5, 5],
        'pc1': [1.0, 2.0, 3.0, 4.0, 5.0]
    })
    
    result = calculate_statistics(res_pca_pathway.iloc[0], res_pca_rndm_set)

    assert result['pathway'][0] == 'pathway1'
    assert result['pathway_size'][0] == 5
    assert result['pc1'][0] == 3.5
    assert result['pval'][0] == pytest.approx(0.2592593, abs=0.00001) # R result
    assert result['es'][0] == pytest.approx(0.3162278, abs=0.00001) # R result 


def test_porcupine():
    res_pca_pathways = pd.DataFrame({
        'pathway': ['pathway1', 'pathway2'],
        'pathway_size': [5, 5],
        'pc1': [2.5, 3.0]
    })

    res_pca_rndm = pd.DataFrame({
        'pathway_size': [5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
        'pc1': [1.2, 2.1, 3.1, 2.8, 1.9, 2.2, 3.0, 2.5, 1.7, 2.3]
    })
    
    result = porcupine(res_pca_pathways, res_pca_rndm)
    
    assert result['pathway'].iloc[0] == 'pathway1'
    assert result['pathway'].iloc[1] == 'pathway2'
    assert result['pathway_size'].iloc[0] == 5
    assert result['pathway_size'].iloc[1] == 5
    assert result['pc1'].iloc[0] == 2.5
    assert result['pc1'].iloc[1] == 3.0
    assert result['pval'].iloc[0] == pytest.approx(0.13651215, abs=0.00001) # R result 
    assert result['pval'].iloc[1] == pytest.approx(0.00204256 , abs=0.00001) # R result
    assert result['es'].iloc[0] == pytest.approx(0.369182, abs=0.00001) # R result
    assert result['es'].iloc[1] == pytest.approx(1.208232, abs=0.00001) # R result

