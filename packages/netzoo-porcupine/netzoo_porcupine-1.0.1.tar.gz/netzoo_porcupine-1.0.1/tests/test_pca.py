import os
import pandas as pd
from porcupine.run_pca import * 
from porcupine.pca_pathway import process_pathway
import pytest 

data_path = os.path.join(os.path.dirname(__file__), 'random_dataset_run_pca.csv')
data_df = pd.read_csv(data_path)

def test_run_pca():

    result = run_pca(data_df)
    
    assert result['pc1'].iloc[0] == pytest.approx(40.076, abs=0.001) #R result 
    assert result['n_edges'].iloc[0] == 10 #R result


def test_process_pathway():
    net_data = data_df
    pathway_data = pd.Series({'pathway':'PATHWAY1', 'genes' : ['gene1','gene2','gene3','gene4','gene5']})
    edges_data = {
    'reg': ['geneA', 'geneB', 'geneC', 'geneD', 'geneE'], 
    'tar': ['gene1', 'gene2', 'gene3', 'gene4', 'gene6']}
    edges_df = pd.DataFrame(edges_data)
    
    res = process_pathway(pathway_data,net_data, edges_df)

    assert res[1] == pytest.approx(48.73503, abs=0.001) #R result
    assert res[2] == 4 #R result
    assert res[3] == 5 #R result

