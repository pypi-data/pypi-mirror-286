"""
map with dataset labels and descriptions
"""
from .entity import Entity
from ...resource.dataloader import DataLoader # for pinnacle scdti
from ...multi_pred.dti import DTI # BindingDB, kiba, davis
from ...multi_pred.ppi import PPI # huri
from ...multi_pred.gda import GDA # DisGeNET
from ...multi_pred.drugres import DrugRes # GSDC

import json

class Dataset(Entity):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._description = {
            "name": "the name of the dataset",
            "description": "a description of the dataset",
            "task": "The TDC task associated with the dataset",
            "ml_task": "The ML Task (i.e., Binary Classification, Regression, etc.) the dataset is created for",
            "statistics": "the statistics associated with the dataset",
            "split": "the available data splits for the dataset",
            "schema": "a mapping of column names to a dictionary containing the type of the column and a description for the column"
        }
        self._functions = {
            "get": "get the dataset as a pandas dataframe",
            "get_task": "get the TDC task associated with the dataset",
            "get_schema": "get a JSON for the dataset schema"
        }
        self._main = lambda ds: ds_map[ds]()
        self._instructions = "How to use Dataset entity. This class allows retrieval of TDC datasets. \
            f(dataset name) -> ML-ready, usually pandas dataframe, representation of the target dataset. \
                Read the parent entity class description to understand how to call entity class main methods in general. \
                    Let D := as an instance of the Dataset entity class. Then, example usage would be: \
                        D.entity_class_main('Li, Michelle, et al.') -> DataFrame ;\
                            D.entity_class_main('HuRI') -> DataFrame"

        self["instruction tuning set"] = "Examples for instruction tuning presented here as pairs of queries and Python code responses. \n \
            Q: Provide a pandas DataFrame for the dataset Li, Michelle, et al. \n\n \
            A: \n from tdc.agents.action_spaces import prism \n \n \
                P = prism.PrismTxT() ; P.get_dataset('Li, Michelle, et al.') \n\n # next example \n\n \
            Q: Obtain data splits for the dataset Li, Michelle, et al. \n\n \
            A: \n from tdc.resource.dataloader import DataLoader ; data = DataLoader(name='opentargets_dti') ; data.get_split() \n\n \
                # note we had to refer to tdc website documentation at https://tdcommons.ai/multi_pred_tasks/scdti/ \n\n \
            Q: Get datasets for the Drug Target Interaction prediction task (TDC.DTI) \n\n \
            A: \n from tdc.agents.action_spaces import prism \n\n \
                P = prism.PrismTxT() \n \
                    df1 = P.get_dataset('BindingDB_Kd') ; df2 = P.get_dataset('BindingDB_IC50') ; df3 = P.get_dataset('BindingDB_Ki') \n \n \
                        # return df1, df2, and df3 in appropriate format.. say a list \n \
                            [df1, df2, df3]"
        
        
    def get(self):
        return self["lambda_f"]()
    
    def get_task(self):
        return self["task"]
    
    def get_schema(self):
        return json.dumps(self["schema"], indent=4)
    
base = Dataset() # every entity has a base instantiation so agent can just obtain description and functions

# Li, Michelle, et al. dataset entity
pinnacle_opentargets = Dataset(
    name = "Li, Michelle, et al.",
    task = "scDTI: The goal is to train a model for predicting the probability that a protein is a candidate therapeutic target in a specific \
        cell type. The model learns an estimator for a function of a protein target and a cell-type-specific biological context as input, and \
            the model is tasked to predict the probability the candidate protein is a therapeutic target in that cell type.",
    description = "To curate target information for a therapeutic area, we examine the drugs indicated for the therapeutic area of interest and\
        its descendants. The two therapeutic areas examined are rheumatoid arthritis (RA) and inflammatory bowel disease. Positive examples (i.e.,\
            where the label y = 1) are proteins targeted by drugs that have at least completed phase 2 of clinical trials for treating a specific \
                therapeutic area. As such, a protein is a promising candidate if a compound that targets the protein is safe for humans and effective \
                    for treating the disease. We retain positive training examples activated in at least one cell type-specific protein interaction network.\
                        We define negative examples (i.e., where the label y = 0) as druggable proteins that do not have any known association with the \
                            therapeutic area of interest according to Open Targets. A protein is deemed druggable if targeted by at least one existing drug.\
                                We extract drugs and their nominal targets from Drugbank. We retain negative training examples activated in at least one cell\
                                    type-specific protein interaction network.",
    ml_task = "Classification. Given the protein and cell-context, predict whether the protein is a therapeutic target.",
    statistics = "The final number of positive (negative) samples for RA and IBD were 152 (1,465) and 114 (1,377), respectively. In PINNACLE, \
        this dataset was augmented to include 156 cell types.",
    split = "Cold Protein Split. We split the dataset such that about 80%% of the proteins are in the training set, about 10%% of the proteins are in\
        the validation set, and about 10%% of the proteins are in the test set. The data splits are consistent for each cell type context to avoid data\
            leakage.",
    schema = {
        "diseaseId": {
            "type": "string",
            "description": "Disease ID. The two therapeutic areas examined are rheumatoid arthritis (RA) and inflammatory bowel disease. For \
                rheumatoid arthritis, we collected therapeutic data (i.e., targets of drugs indicated for the therapeutic area) from OpenTargets \
                    for rheumatoid arthritis (EFO 0000685), ankylosing spondylitis (EFO 0003898), and psoriatic arthritis (EFO 0003778). \
                        For inflammatory bowel disease, we collected therapeutic data for ulcerative colitis (EFO 0000729), collagenous colitis \
                            (EFO 1001293), colitis (EFO 0003872), proctitis (EFO 0005628), Crohn’s colitis (EFO 0005622), lymphocytic colitis (EFO 1001294),\
                                Crohn’s disease (EFO 0000384), microscopic colitis (EFO 1001295), inflammatory bowel disease (EFO 0003767), \
                                    appendicitis (EFO 0007149), ulcerative proctosigmoiditis (EFO 1001223), and small bowel Crohn’s disease (EFO 0005629)."
        },
        "targetId_genename": {
            "type": "string",
            "description": "Protein Target"
        },
        "Y": {
            "type": "int",
            "description": "Binary Indicator. Y=1 if the protein is a viable drug target for this disease and Y=0 otherwise."
        }
    },
    lambda_f = lambda: DataLoader("opentargets_dti").get_data()
)

binding_db_kd = Dataset(
    name = "BindingDB_Kd",
    task = "DTI: Drug-target interaction prediction task aims to predict the interaction activity score in silico given only the accessible compound \
        structural information and protein amino acid sequence.",
    description = "BindingDB is a public, web-accessible database of measured binding affinities, focusing chiefly on the interactions of protein \
        considered to be drug-targets with small, drug-like molecules. This is the Kd dataset.",
    ml_task = "Regression. Given the target amino acid sequence/compound SMILES string, predict their binding affinity.",
    statistics = "(# of DTI pairs, # of drugs, # of proteins) 52,284/10,665/1,413 for Kd, 991,486/549,205/5,078 for IC50, 375,032/174,662/3,070 for Ki.",
    split = "Random Split, Cold Drug Split, or Cold Protein Split",
    schema = {
        "Drug": {
            "type": "string",
            "description": "Drug SMILES string"
        },
        "Target": {
            "type": "string",
            "description": "Protein Target Amino Acid Sequence"
        },
        "Y": {
            "type": "decimal",
            "description": "Binding Affinity"
        }
    },
    lambda_f = lambda: DTI(name = 'BindingDB_Kd').harmonize_affinities(mode = 'mean').get_data()
)

binding_db_ic50 = Dataset(
    name = "BindingDB_IC50",
    task = "DTI: Drug-target interaction prediction task aims to predict the interaction activity score in silico given only the accessible compound \
        structural information and protein amino acid sequence.",
    description = "BindingDB is a public, web-accessible database of measured binding affinities, focusing chiefly on the interactions of protein \
        considered to be drug-targets with small, drug-like molecules. This is the IC50 dataset.",
    ml_task = "Regression. Given the target amino acid sequence/compound SMILES string, predict their binding affinity.",
    statistics = "(# of DTI pairs, # of drugs, # of proteins) 52,284/10,665/1,413 for Kd, 991,486/549,205/5,078 for IC50, 375,032/174,662/3,070 for Ki.",
    split = "Random Split, Cold Drug Split, or Cold Protein Split",
    schema = {
        "Drug": {
            "type": "string",
            "description": "Drug SMILES string"
        },
        "Target": {
            "type": "string",
            "description": "Protein Target Amino Acid Sequence"
        },
        "Y": {
            "type": "decimal",
            "description": "Binding Affinity"
        }
    },
    lambda_f = lambda: DTI(name = 'BindingDB_IC50').harmonize_affinities(mode = 'mean').get_data()
)

binding_db_ki = Dataset(
    name = "BindingDB_Ki",
    task = "DTI: Drug-target interaction prediction task aims to predict the interaction activity score in silico given only the accessible compound \
        structural information and protein amino acid sequence.",
    description = "BindingDB is a public, web-accessible database of measured binding affinities, focusing chiefly on the interactions of protein \
        considered to be drug-targets with small, drug-like molecules. This is the Ki dataset.",
    ml_task = "Regression. Given the target amino acid sequence/compound SMILES string, predict their binding affinity.",
    statistics = "(# of DTI pairs, # of drugs, # of proteins) 52,284/10,665/1,413 for Kd, 991,486/549,205/5,078 for IC50, 375,032/174,662/3,070 for Ki.",
    split = "Random Split, Cold Drug Split, or Cold Protein Split",
    schema = {
        "Drug": {
            "type": "string",
            "description": "Drug SMILES string"
        },
        "Target": {
            "type": "string",
            "description": "Protein Target Amino Acid Sequence"
        },
        "Y": {
            "type": "decimal",
            "description": "Binding Affinity"
        }
    },
    lambda_f = lambda: DTI(name = 'BindingDB_Ki').harmonize_affinities(mode = 'mean').get_data()
)

davis = Dataset(
    name = "Davis",
    task = "DTI: Drug-target interaction prediction task aims to predict the interaction activity score in silico given only the accessible compound \
        structural information and protein amino acid sequence.",
    description = "The interaction of 72 kinase inhibitors with 442 kinases covering >80%% of the human catalytic protein kinome.",
    ml_task = "Regression. Given the target amino acid sequence/compound SMILES string, predict their binding affinity",
    statistics = "25,772 DTI pairs, 68 drugs, 379 proteins",
    split = "Random Split, Cold Drug Split, or Cold Protein Split",
    schema = {
        "Drug": {
            "type": "string",
            "description": "Drug SMILES string"
        },
        "Target": {
            "type": "string",
            "description": "Protein Target Amino Acid Sequence"
        },
        "Y": {
            "type": "decimal",
            "description": "Binding Affinity"
        }
    },
    lambda_f = lambda: DTI(name = 'DAVIS').get_data()
)

kiba = Dataset(
    name = "KIBA",
    task = "DTI: Drug-target interaction prediction task aims to predict the interaction activity score in silico given only the accessible compound \
        structural information and protein amino acid sequence.",
    description = "Toward making use of the complementary information captured by the various bioactivity types, including IC50, K(i), and K(d), Tang\
        et al. introduces a model-based integration approach, termed KIBA to generate an integrated drug-target bioactivity matrix.",
    ml_task = "Regression. Given the target amino acid sequence/compound SMILES string, predict their binding affinity",
    statistics = "117,657 DTI pairs, 2,068 drugs, 229 proteins.",
    split = "Random Split, Cold Drug Split, or Cold Protein Split",
    schema = {
        "Drug": {
            "type": "string",
            "description": "Drug SMILES string"
            },
        "Target": {
            "type": "string",
            "description": "Protein Target Amino Acid Sequence"
            },
        "Y": {
            "type": "decimal",
            "description": "Binding Affinity"
            }
        },
    lambda_f = lambda: DTI(name = 'KIBA').get_data()
)

huri = Dataset(
    name = "HuRI",
    task = "PPI: Protein-protein interactions (PPI) are very important to discover new putative therapeutic targets to cure\
        disease. Expensive and time-consuming wet-lab results are usually required to obtain PPI activity. PPI prediction \
            aims to predict the PPI activity given a pair of proteins' amino acid sequences. ",
    description = " All pairwise combinations of human protein-coding genes are systematically being interrogated to \
        identify which are involved in binary protein-protein interactions. In the most recent effort 17,500 proteins \
            have been tested and a first human reference interactome (HuRI) map has been generated. From the Center for \
                Cancer Systems Biology at Dana-Farber Cancer Institute.",
    ml_task = "Binary Classification. Given the target amino acid sequence pairs, predict if they interact or not.",
    statistics = "51,813 positive PPI pairs, 8,248 proteins",
    split = "Random Split, Cold Drug Split, or Cold Protein Split",
    schema = {
        "Protein1": {
            "type": "string",
            "description": "Protein1 amino acid sequence"
            },
        "Protein2": {
            "type": "string",
            "description": "Protein2 Amino Acid Sequence"
            },
        "Y": {
            "type": "Binary",
            "description": "Indicator for binding interaction"
            }
        },
    lambda_f = lambda: PPI(name = 'HuRI').get_data()
)

disgenet = Dataset(
    name = "DisGeNET",
    task = "GDA: Gene-disease associations (GDA) quantify the relation among a pair of gene and disease. The GDA is usually\
        constructed as a network where we can probe the gene-disease mechanisms by taking into account multiple genes and\
            diseases factors. This task is to predict the association of any gene and disease from both a biochemical modeling\
                and network edge classification perspectives.",
    description = "DisGeNET is a discovery platform containing one of the largest publicly available collections of genes \
        and variants associated to human diseases. DisGeNET integrates data from expert curated repositories, GWAS catalogues,\
            animal models and the scientific literature. DisGeNET data are homogeneously annotated with controlled vocabularies\
                and community-driven ontologies. TDC uses the curated subset from UNIPROT, CGI, ClinGen, Genomics England, CTD\
                    (human subset), PsyGeNET, and Orphanet. TDC maps disease ID to disease definition through MedGen and maps \
                        GeneID to uniprot amino acid sequence.",
    ml_task = " Regression. Given the disease description and the amino acid sequence of the gene, predict their association.",
    statistics = "52,476 gene-disease pairs, 7,399 genes, 7,095 diseases",
    split = "Random Split",
    schema = {
        "Gene": {
            "type": "string",
            "description": "Gene amino acid sequence"
            },
        "Disease_ID": {
            "type": "string",
            "description": "Unique ID for a disease"
            },
        "Disease": {
            "type": "string",
            "description": "Name of disease and a description"
            },
        "Y": {
            "type": "Binary",
            "description": "score for association strenth"
            }
        },
    lambda_f = lambda: GDA(name = 'DisGeNET').get_data()
)

GDSC1 = Dataset(
    name = "GDSC1",
    task = "DrugRes: To design drug for individual or a group with certain characteristics is the central goal of precision medicine. \
        For example, the same anti-cancer drug could have various responses to different cancer cell lines. This task aims to predict the\
            drug response rate given a pair of drug and the cell line genomics profile. ",
    description = "Genomics in Drug Sensitivity in Cancer (GDSC) is a resource for therapeutic biomarker discovery in cancer cells. It contains\
        wet lab IC50 for 100s of drugs in 1000 cancer cell lines. In this dataset, we use RMD normalized gene expression for cancer lines and\
            SMILES for drugs. Y is the log normalized IC50. This is the version 1 of GDSC.",
    ml_task = "Regression. Given the gene expression of cell lines and the SMILES of drug, predict the drug sensitivity level.",
    statistics = "177,310 pairs, 958 cancer cells and 208 drugs",
    split = "Random Split",
    schema = {
        "Drug_ID": {
            "type": "string",
            "description": "Drug ID"
            },
        "Drug": {
            "type": "string",
            "description": "Drug SMILES string"
            },
        "Cell Line_ID": {
            "type": "string",
            "description": "Cell line ID"
            },
         "Cell Line": {
            "type": "vector<double>",
            "description": "Gene expression profile for the cell line"
            },
        "Y": {
            "type": "Double",
            "description": "Drug sensitivity level"
            }
        },
    lambda_f = lambda: DrugRes(name = 'GDSC1').get_data()
)

GDSC2 = Dataset(
    name = "GDSC2",
    task = "DrugRes: To design drug for individual or a group with certain characteristics is the central goal of precision medicine. \
        For example, the same anti-cancer drug could have various responses to different cancer cell lines. This task aims to predict the\
            drug response rate given a pair of drug and the cell line genomics profile. ",
    description = "Genomics in Drug Sensitivity in Cancer (GDSC) is a resource for therapeutic biomarker discovery in cancer cells. It contains\
        wet lab IC50 for 100s of drugs in 1000 cancer cell lines. In this dataset, we use RMD normalized gene expression for cancer lines and \
            SMILES for drugs. Y is the log normalized IC50. This is the version 2 of GDSC, which uses improved experimental procedures.",
    ml_task = "Regression. Given the gene expression of cell lines and the SMILES of drug, predict the drug sensitivity level.",
    statistics = "92,703 pairs, 805 cancer cells and 137 drugs",
    split = "Random Split",
    schema = {
        "Drug_ID": {
            "type": "string",
            "description": "Drug ID"
            },
        "Drug": {
            "type": "string",
            "description": "Drug SMILES string"
            },
        "Cell Line_ID": {
            "type": "string",
            "description": "Cell line ID"
            },
         "Cell Line": {
            "type": "vector<double>",
            "description": "Gene expression profile for the cell line"
            },
        "Y": {
            "type": "Double",
            "description": "Drug sensitivity level"
            }
        },
    lambda_f = lambda: DrugRes(name = 'GDSC2').get_data()
)

datasets = [
    GDSC1,
    GDSC2,
    disgenet,
    huri,
    kiba,
    davis,
    binding_db_ki,
    binding_db_kd,
    binding_db_ic50,
    pinnacle_opentargets
]

ds_map = {ds["name"]: ds.get for ds in datasets}