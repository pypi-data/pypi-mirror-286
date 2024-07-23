# JSON and callbacks for the TDC Resource module

from .entity import Entity

class Resource(Entity):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._description = {
            "name": "the name of the TDC resource",
            "description": "the description of the TDC resource",
            "api_code": "Link to the API code in the TDC repo",
            "website_docs": "Link to the website documentation on the resource",
            "tutorial_notebook": "Link to the Google Colab tutorial notebook on the resource",
            "txt": "instruction tuning set on the TDC resource",}  # all resource-specific variables and their description
        self._functions = {} # all functions specific to the resource entity
        self._main = lambda _: None  # entity_class_main
        self._instructions = "Each resource has its own usage instructions. See each individual JSON foe each of PrimeKG and CELLxGENE."  # general instructions on how to use the entity; does not use parent TxT class. only the entity class
        self["instruction tuning set"] = "Please see each individual resource (i.e., PrimeKG and CELLxGENE) for their corresponding instructions."  # a dataset for instruction tuning containing questions and code responses. should use TxT class
        
base = Resource()  # every entity has a base instantiation so agent can just obtain description and functions 

# instantiate the necessary resources
PrimeKG = Resource(
    name="PrimeKG",
    description="Precision Medicine Oriented Knowledge Graph. From the publication Building a knowledge graph to enable precision medicine by Chandak et al. in Scientific Data 2023. \
        Original Github Repo https://github.com/mims-harvard/PrimeKG . Full paper text https://www.biorxiv.org/content/10.1101/2022.05.01.489928v2.full . \
Developing personalized diagnostic strategies and targeted treatments requires a deep understanding of disease biology and the ability to dissect the relationship between molecular and genetic factors and their phenotypic consequences. However, such knowledge is fragmented across publications, non-standardized research repositories, and evolving ontologies describing various scales of biological organization between genotypes and clinical phenotypes. \
We introduce PrimeKG, a precision medicine-oriented knowledge graph that provides a holistic view of diseases. PrimeKG integrates 20 high-quality resources to describe 17,080 diseases with 4,050,249 relationships representing ten major biological scales, including disease-associated protein perturbations, biological processes and pathways, anatomical and phenotypic scale, and the entire range of approved and experimental drugs with their therapeutic action, considerably expanding previous efforts in disease-rooted knowledge graphs. \
PrimeKG supports drug-disease prediction by including an abundance of ’indications’, ’contradictions’ and ’off-label use’ edges, which are usually missing in other knowledge graphs. We accompany PrimeKG's graph structure with text descriptions of clinical guidelines for drugs and diseases to enable multi-modal analyses.\
    The full description https://zitniklab.hms.harvard.edu/projects/PrimeKG/ . This Entity provides access to TDC's implementation of PrimeKG",
    api_code="https://github.com/mims-harvard/TDC/blob/main/tdc/resource/primekg.py",
    website_docs="https://tdcommons.ai/resources/overview/",
    tutorial_notebook="https://colab.research.google.com/drive/1kYH8nt3nW7tXYBPNcfYuDbWxGTqOEnWg?usp=sharing",
    txt="Q: Obtain drug repositioning opportunities for drug DB00945 \n \
        A: \n import networkx as nx \n \
from tdc.resource import PrimeKG \n \
\n \
# Load the PrimeKG data\n \
kg = PrimeKG() \n \
data = kg.get_data()\n \
data = data[data['relation'].str.contains('drug')]\n \
\n \
# Create a graph from the knowledge graph data\n \
G = nx.from_pandas_edgelist(data, 'x_id', 'y_name', edge_attr='relation')\n \
\n \
# Example function to find repositioning opportunities for a given drug\n \
def find_repositioning_opportunities(drug):\n \
    neighbors = list(G.neighbors(drug))\n \
    diseases = [node for node in neighbors if G[drug][node]['relation'] == 'drug_protein']\n \
    return diseases\n \
\n \
# Find repositioning opportunities for a specific drug\n \
drug_name = 'DB00945'\n \
repositioning_opportunities = find_repositioning_opportunities(drug_name)\n \
print(repositioning_opportunities) \n\n \
Q: Get the disease nodes connected to drugs in the knowlkedge graph \n \
A: \n from tdc.resource import PrimeKG \n \
data = PrimeKG(path = './data') \n \
drug_feature = data.get_features(feature_type = 'drug')\n \
data.to_nx()\n \
data.get_node_list('disease')"
)

CELLxGENE = Resource(
    name="CELLxGENE",
    description="CZ CellXGene [ 53] is an open-source platform for single-cell RNA sequencing data analysis. We leverage the CZ CellXGene to develop a TDC-2 \
Resource Model for constructing large-scale single-cell datasets that maps gene expression profiles \
of individual cells across tissues, healthy and disease states. TDC-2 leverages the SOMA (Stack of\
Matrices, Annotated) API, adopts TileDB-SOMA [66] for modeling sets of 2D annotated matrices\
with measurements of features across observations and enables memory-efficient querying of single cell modalities (i.e., scRNA-seq, snRNA-seq), across healthy and diseased samples, with tabular\
annotations of cells, samples, and patients the samples come from.\
We develop a remote procedure call (RPC) API taking the string name of the\
desired reference dataset as specified in the CellXGene [53 ]. The remote procedure call for fetching\
data is defined as a Python generator expression, allowing the user to iterate over the constructed\
single-cell atlas without loading it into memory [67]. Specifying the RPC as a Python generator\
expression allows us to use memory-efficient querying as provided by TileDB [66 ]. The single-cell\
datasets can be integrated with therapeutics ML workflows in TDC-2 using tools such as PyTorch’s\
IterableDataset module [68]. The original CellXGene Census documentation can be found here https://chanzuckerberg.github.io/cellxgene-census/index.html .\
    it uses TileDB and the data schema can be found here https://chanzuckerberg.github.io/cellxgene-census/cellxgene_census_docsite_schema.html .\
        TDC-2 leverages the SOMA (Stack of Matrices, Annotated) API, adopts TileDB-SOMA for modeling sets of 2D annotated matrices with measurements of features across observations, and enables memory-efficient querying of multiple distinct single-cell modalities (i.e., scRNA-seq, snRNA-seq), across healthy and diseased samples, with tabular annotations of cells, samples, and patients the samples come from.\
We provide two APIs. First, a standard resource-based querying API for simple cross-compatibility with the CellXGene Census Discover Python API.\
Second, we've developed a TDC Dataloader over the Census corpus for ease of building large cell atlases based on a reference dataset.\
Below first example usage of the implemented Census Resource. For more information regarding the data schema and TileDB-SOMA, you may reference the CellXGene Census Discovery Data Schema Documentation.\
    The TDC CellXGene DataLoader API allows you to build large-scale cell atlases based on a reference dataset. It retrieves all cells containing non-zero counts for the genes present in the reference dataset. This is a python generator expression and provides indices for cell and gene, allowing the user to retrieve any desired metadata using those indices. The expression count for each cell and gene pair is also included. To mantain consistency with the standard TDC-2 dataloader API, the output is a pandas dataframe.\
        Single-cell model embeddings can also be retrieved with this API. Here are some benchmark results https://chanzuckerberg.github.io/cellxgene-census/articles/2024/20240710_embedding_metrics_dec_2023_lts.html . \
            The benchmarks were run on the following embeddings: scVI latent spaces from a model trained on all Census data ; Fine-tuned Geneformer ; scGPT. ; Universal Cell Embeddings (UCE). The full text of the paper is here https://www.biorxiv.org/content/10.1101/2023.10.30.563174v1.full .\
                census datasets are https://cellxgene.cziscience.com/datasets .",
    api_code="https://github.com/mims-harvard/TDC/blob/main/tdc/resource/cellxgene_census.py",
    website_docs="best to look at turotial notebook and original docs in the description.",
    tutorial_notebook="https://colab.research.google.com/drive/1xTgBwKUfP2b8j6Fqh28M2GUp2ScfENMX?usp=sharing",
    txt="Q: obtain a python generator for all T cell male entries in the atlas referencing Tabula Sapiens - Blood dataset. Then, print the head of the first dataframe slice\n\
        A: \n from tdc.multi_pred.single_cell import CellXGene\n\
from pandas import DataFrame\n\
dataloader = CellXGene(name='Tabula Sapiens - Blood')\n\
gen = dataloader.get_data(\n\
    value_filter=\"cell_type == 'T cell' and sex == 'male'\")\n\
df = next(gen)\n\
df.head()\n\n\
    # use the following before running any of the below code snippets\n\
        from tdc.resource import cellxgene_census\n\
            # initialize Census Resource and query filters\n\
resource = cellxgene_census.CensusResource()\n\
gene_value_filter = \"feature_id in ['ENSG00000161798', 'ENSG00000188229']\"\n\
gene_column_names = [\"feature_name\", \"feature_length\"]\n\
cell_value_filter = \"tissue == 'brain' and sex == 'male'\"\n\
cell_column_names = [\"assay\", \"cell_type\", \"tissue\"]\n\
    Q: query a slice of the feature presence matrix and obtain the output in pyarrow\n\
    A:\n \
        sparse_tensor = resource.get_feature_dataset_presence_matrix(\n\
    upper=5,\n\
    lower=0,\n\
    measurement_name=\"RNA\",\n\
    fmt=\"pyarrow\",\n\
    todense=False)\n\n\
    Q: use the Census Resource to obtain cell metadata from the obs matrix\n\
    A:\n obsdf = resource.get_cell_metadata(\n\
    value_filter=cell_value_filter,\n\
    column_names=cell_column_names,\n\
    fmt=\"pandas\")\n\n\
    Q: using the Census Resource to obtain gene metadata form the var matrix\n\
    A:\n varpyarrow = resource.get_gene_metadata(\n\
    value_filter=gene_value_filter,\n\
    column_names=gene_column_names,\n\
    fmt=\"pyarrow\",\n\
    measurement_name=\"RNA\")\n\n\
    Q: using the Census Resource for retrieving raw RNA data for a specific tissue and sex from the counts (X) matrix. As per memory-efficient querying, this will by defaults provide a python generator expression. For details on converting to other data formats, you can reference the resource source code.\n\
    A:\n X = resource.query_measurement_matrix(measurement_name=\"RNA\",\n\
                                fmt=\"pyarrow\",\n\
                                value_adjustment=\"raw\",\n\
                                value_filter=\"tissue == 'brain' and sex == 'male'\")\n\n\
    Q: obtain embeddings from fine-tuned geneformer and scgpt\n\
    A:\n resource.get_anndata(add_embeddings=True, emb_names=['geneformer', 'scgpt'], obs_value_filter = \"tissue_general == 'central nervous system'\", organism = \"homo_sapiens\")"
)
resources: list[str] = [
    "PrimeKG",
    "CELLxGENE"
]  # list of resource strings
resource_entities = [
    PrimeKG,
    CELLxGENE
]
# any variables needed for the main function