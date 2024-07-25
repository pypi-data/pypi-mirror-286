import sys

sys.path.append('./')

from porcupine.init import *


edges_data = {
    'reg': ['geneA', 'geneB', 'geneC', 'geneD', 'geneE'],
    'tar': ['gene1', 'gene2', 'gene3', 'gene4', 'gene5']
}
edges = pd.DataFrame(edges_data)

pathways = [
    ('pathway1', ['gene1', 'gene2', 'gene3', 'gene4','gene5']),
    ('pathway2', ['gene2', 'gene3', 'gene4','gene9']),
    ('pathway3', ['gene4', 'gene5']),
    ('pathway4', ['gene10', 'gene11'])
]

def test_filter_pathways():
    pathways_filt = filter_pathways(pathways, edges)
    assert len(pathways_filt) == 3  

    

def test_filter_pathways_size():
    pathways_filt = filter_pathways(pathways, edges)
    pathways_filt_size = filter_pathways_size(pathways_filt,minSize=3,maxSize=4)
    assert len(pathways_filt_size) == 1