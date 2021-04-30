from sklearn.model_selection import train_test_split
from scipy.stats import uniform, randint
from sklearn.model_selection import RandomizedSearchCV
import numpy as np
import pandas as pd
import re
import xgboost as xgb

def display_scores(scores):
    print("Scores: {0}\nMean: {1:.3f}\nStd: {2:.3f}".format(scores, np.mean(scores), np.std(scores)))
    
def report_best_scores(results, n_top=3):
    for i in range(1, n_top + 1):
#         i = 201 - i
        candidates = np.flatnonzero(results['rank_test_score'] == i)
        for candidate in candidates:
            print("Model with rank: {0}".format(i))
            print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
                  results['mean_test_score'][candidate],
                  results['std_test_score'][candidate]))
            print("Parameters: {0}".format(results['params'][candidate]))
            print("")

def get_params(results, rank = 1):
    candidates = np.flatnonzero(results['rank_test_score'] == rank)
    return results['params'][candidates[0]]

def getModelAndBestParams(X, y):
    params = {
        "colsample_bytree": uniform(0.5, 0.5),
        "colsample_bylevel": uniform(0.5, 0.5),
        "colsample_bynode": uniform(0.5, 0.5),
        "gamma": uniform(0, 1),
        "learning_rate": uniform(0, 1), # default 0.1 
        "max_depth": randint(2, 10), # default 3
        "n_estimators": randint(100, 200), # default 100
        "subsample": uniform(0.5, 0.5)
    }
    xgb_model = xgb.XGBRegressor(n_jobs = -1, random_state = 42)
    search = RandomizedSearchCV(xgb_model, param_distributions=params, random_state=42, n_iter=50, refit= True, 
                                scoring = "neg_mean_absolute_error", n_jobs=-1, return_train_score=True)
    search.fit(X, y)
    return search, get_params(search.cv_results_)

def getProcessedData(goi_id, testSize = 0.2, randomState = 42):
    pat = pd.read_csv('~/COMMPASS/COMMPASS/IA13/Expression Estimates - Gene Based/MMRF_CoMMpass_IA13a_E74GTF_HtSeq_Gene_Counts.csv')
    pat = pat.set_index(pat.GENE_ID)
    pat = pat.drop(columns = 'GENE_ID')
    pat = pat.loc[:, pat.columns.str.endswith('1_BM') | pat.columns.str.endswith('1_PB')]

    # cell = pd.read_csv('HMCL66_HTSeq_GENE_Counts_v2.csv')
    # cell = cell.set_index(cell.Sample)
    # cell = cell.drop(['Sample', 'GENE_NAME'], axis = 1)

    # ccle = pd.read_csv('CCLE_RNAseq_genes_counts_20180929.csv')
    # ccle['Name'] = ccle.Name.map(lambda x : re.sub('\.\d+$', '', x))
    # ccle = ccle.set_index(ccle.Name)
    # ccle = ccle.drop(['Name', 'Description'], axis = 1)
    # ccle_hlt = ccle.loc[:,ccle.columns.map(lambda x : x.endswith('HAEMATOPOIETIC_AND_LYMPHOID_TISSUE'))]

    goi_names = pd.read_csv('cd138genes.csv', header = None)
    goi_names = goi_names.rename({0 :'GENE_NAMES'}, axis = 1)

    goi_pat = pat.loc[goi_id]
    goi_pat = goi_pat.set_index(goi_names.iloc[:, 0])
    goi_pat = goi_pat.T
    goi_pat_log = np.log2(goi_pat)
    goi_pat_log = goi_pat_log.replace(-np.inf, 0)

    y_log = goi_pat_log.CD38
    X_log = goi_pat_log.drop('CD38', axis = 1)

    X_log_train, X_log_test, y_log_train, y_log_test = train_test_split(X_log, y_log, test_size=testSize, random_state=randomState)
    
    return X_log_train, X_log_test, y_log_train, y_log_test

def getGOI():
    goi_id = [
         'ENSG00000141905', #NFIC
         'ENSG00000185811', #IKZF1
         'ENSG00000100811', #YY1
         'ENSG00000143437', #ARNT
         'ENSG00000120837', #NFYB
         'ENSG00000115966', #ATF2
         'ENSG00000185591', #SP1
         'ENSG00000170345', #FOS
         'ENSG00000118260', #CREB1
         'ENSG00000028277', #POU2f2
         'ENSG00000112592', #TBP
         'ENSG00000103495', #MAZ
         'ENSG00000101076', #HNF4A
         'ENSG00000175745', #NR2F1
         'ENSG00000126561', #STAT5A
         'ENSG00000120690', #ELF1
         'ENSG00000179348', #GATA2
         'ENSG00000068305', #MEF2A
         'ENSG00000173039', #RELA
         'ENSG00000066336', #SPI1
         'ENSG00000131196', #NFATC1
         'ENSG00000130522', #JUND
         'ENSG00000118513', #MYB
         'ENSG00000196092', #PAX5
         'ENSG00000164330', #EBF1
         'ENSG00000172216', #CEBPB
         'ENSG00000171223', #JUNB
         'ENSG00000141568', #FOXK2
         'ENSG00000119950', #MXI1
         'ENSG00000147133', #TAF1
         'ENSG00000143373', #ZNF687
         'ENSG00000107485', #GATA3
         'ENSG00000120798', #NR2C1
         'ENSG00000175029', #CTBP2
         'ENSG00000010244', #ZNF207
         'ENSG00000168610', #STAT3
         'ENSG00000170365', #SMAD1
         'ENSG00000169375', #SIN3A
         'ENSG00000167081', #PBX3
         'ENSG00000182979', #MTA1
         'ENSG00000106462', #EZH2
         'ENSG00000148516', #ZEB1
         'ENSG00000089902', #RCOR1
         'ENSG00000143889', #HNRNPLL
         'ENSG00000112658', #SRF
         'ENSG00000069399', #BCL3
         'ENSG00000164754', #RAD21
         'ENSG00000102554', #KLF5
         'ENSG00000125952', #MAX
         'ENSG00000136997', #MYC
         'ENSG00000156273', #BACH1
         'ENSG00000171940', #ZNF217
         'ENSG00000139083', #ETV6
         'ENSG00000074266', #EED
         'ENSG00000119866', #BCL11A
         'ENSG00000104320', #NBN
         'ENSG00000100393', #EP300
         'ENSG00000140262', #TCF12
         'ENSG00000149480', #MTA2
         'ENSG00000104856', #RELB
         'ENSG00000156127', #BATF
         'ENSG00000134107', #BHLHE40
         'ENSG00000073861', #TBX21
         'ENSG00000020633', #RUNX3
         'ENSG00000100219', #XBP1
         'ENSG00000168310', #IRF2
         'ENSG00000115415', #STAT1
         'ENSG00000049768', #FOXP3
         'ENSG00000196628', #TCF4
         'ENSG00000151090', #THRB
         'ENSG00000129514', #FOXA1
         'ENSG00000181195', #PENK
         'ENSG00000091831', #ESR1
         'ENSG00000197780', #TAF13
         'ENSG00000082175', #PGR
         'ENSG00000135100', #HNF1A
         'ENSG00000143190', #POU2F1
         'ENSG00000101096', #NFATC2
         'ENSG00000186350', #RXRA
         'ENSG00000169083', #AR
         'ENSG00000128710', #HOXD10
         'ENSG00000077092', #RARB
         'ENSG00000111424', #VDR
         'ENSG00000005436', #GCFC2
         'ENSG00000123268', #ATF1
         'ENSG00000168214', #RBPJ
         'ENSG00000113580', #NR3C1
         'ENSG00000141510', #TP53
         'ENSG00000184895', #SRY
         'ENSG00000245848', #CEBPA
         'ENSG00000128709', #HOXD9
         'ENSG00000162772', #ATF3
         'ENSG00000175832', #ETV4
         'ENSG00000101412', #E2F1
         'ENSG00000140374', #ETFA
         'ENSG00000105379', #ETFB
         'ENSG00000179388', #EGR3
         'ENSG00000184937', #WT1
         'ENSG00000106546', #AHR
         'ENSG00000131759', #RARA
         'ENSG00000109320', #NFKB1
         'ENSG00000105698', #USF2
         'ENSG00000125347', #IRF1
         'ENSG00000138795', #LEF1
         'ENSG00000126767', #ELK1
         'ENSG00000138378', #STAT4
         'ENSG00000102145', #GATA1
         'ENSG00000157557', #ETS2
         'ENSG00000134954', #ETS1
         'ENSG00000004468' #CD38
    ]
    
    return goi_id