# 🧬 **Delftia Learning & Genomics Platform**
### _Open Pedagogy • Genome Analytics • Machine Learning for Microbial Discovery_

---

## 🌍 **Overview**
This repository hosts the development of an **open-source educational and research platform** focused on _Delftia acidovorans_ and _Delftia tsuruhatensis_ — unique microbes known for **gold biomineralization** and **harmane biosynthesis**.

The project blends:
- 🧫 **Microbiology Education** – GitHub-based electronic lab notebooks (ELNs) for student learning  
- 🧠 **Bioinformatics & Machine Learning** – automated pipelines to parse, analyze, and predict gene clusters  
- 📘 **Open Science** – Alt-Textbook & JMBE-aligned framework for open pedagogy and reproducible research  

---

## 🎯 **Core Goals**
| Theme | Description |
|--------|-------------|
| 🧪 **Education Integration** | Develop Quarto + GitHub-based lab notebooks where students explore real genomic data. |
| 🧬 **Data Infrastructure** | Build a structured genome–sequence–gene database for _Delftia_ species. |
| 🤖 **Machine Learning Analysis** | Apply ML to predict functional genes and clusters (gold/harmane biosynthetic pathways). |
| 📊 **Visualization & Dashboards** | Create interactive dashboards (Quarto / Streamlit) for genome insights. |
| 🧩 **Open Publication** | Share workflows via a JMBE “Tips & Tools” article and open-access Pressbook. |

---

## 🧱 **Repository Structure**
```bash
delftia-genomics-platform/
├── data/
│   ├── raw/                     # Raw NCBI genome downloads (JSONL, GFF, FNA)
│   ├── processed/               # Parsed metadata and cleaned tables
│   └── db/                      # SQLite / Postgres schemas for genome, sequence, gene
│
├── notebooks/
│   ├── exploration/             # Jupyter notebooks for exploratory data analysis
│   ├── ML_models/               # ML model training & evaluation notebooks
│   └── ELN_template.qmd         # Quarto-based electronic lab notebook template
│
├── scripts/
│   ├── fetch_genomes.py         # Automated download from NCBI Datasets API
│   ├── parse_assembly_json.py   # Extracts metadata (size, GC%, CheckM, etc.)
│   ├── parse_gff_genes.py       # Extracts gene info (start, end, product, etc.)
│   └── build_database.py        # Populates SQLite/Postgres DB with all parsed info
│
├── dashboard/
│   └── delftia_dashboard.qmd    # Interactive visualization dashboard (under dev)
│
├── models/
│   ├── feature_extraction.py    # Extracts sequence features for ML
│   ├── train_cluster_model.py   # ML for gene cluster prediction
│   └── embeddings/              # Pretrained embeddings or sequence vectors
│
├── docs/
│   ├── alt_textbook_proposal.md # Draft for Alt-Textbook grant
│   └── jmbe_tips_tools_draft.md # Draft for publication
│
├── requirements.txt
├── LICENSE
└── README.md
````

---

## 🧬 **Data Pipeline Overview**

1. **Fetch genomes:**
   Use the NCBI Datasets v2 API to download all *Delftia* assemblies (~140 genomes).

   ```bash
   python scripts/fetch_genomes.py
   ```

2. **Parse metadata:**
   Extract key fields (size, GC%, genes, completeness, contamination).

   ```bash
   python scripts/parse_assembly_json.py
   ```

3. **Parse gene annotations:**
   Extract each gene’s ID, product, coordinates, and protein sequence from `.gff` files.

   ```bash
   python scripts/parse_gff_genes.py
   ```

4. **Build local database:**
   Merge all parsed information into a relational database (`genome`, `sequence`, `gene`).

   ```bash
   python scripts/build_database.py
   ```

---

## 🧠 **Machine Learning & Bioinformatics Approaches**

### 🧩 1. **Feature Extraction**

From each gene or protein sequence:

* k-mer frequency profiles
* GC skew, codon usage, amino acid composition
* Pfam / InterPro functional domains
* Embeddings from protein language models (e.g., ESM-2, ProtBERT)

### 🔍 2. **Gold Cluster & Harmane Gene Detection**

* Keyword-based mapping from `.gff` annotation (`product ~ delftibactin*, harmane*`)
* Similarity search using BLAST / DIAMOND
* Functional classification using Random Forest or CNN on feature vectors

### 🤖 3. **Predictive Modeling**

| Model                          | Purpose                      | Description                                                          |
| ------------------------------ | ---------------------------- | -------------------------------------------------------------------- |
| **Random Forest / XGBoost**    | Gene function classification | Uses engineered sequence features                                    |
| **Autoencoder + Clustering**   | Novel cluster detection      | Learns hidden representations of unknown genes                       |
| **Graph Neural Network (GNN)** | Pathway inference            | Builds network of gene–gene co-occurrence                            |
| **Transformer (ESM / ProtT5)** | Embedding-based prediction   | Captures semantic similarity between known and unknown cluster genes |

Outputs:

* Predicted *gold cluster gene set* per genome
* Confidence scores + visualization on genome map

---

## 📊 **Dashboard (In Progress)**

Built using **Quarto + Plotly / Streamlit**, enabling users to:

* Search and filter *Delftia* genomes by metadata (size, completeness, GC%).
* Visualize genomic maps with identified gold/harmane clusters.
* Download curated genome tables or gene lists.
* Explore ML-based predictions interactively.

---

## 🧰 **Tech Stack**

| Category         | Tools                                   |
| ---------------- | --------------------------------------- |
| Data Parsing     | Python, Pandas, Requests, Biopython     |
| Database         | SQLite / PostgreSQL                     |
| Machine Learning | Scikit-learn, PyTorch, ESM / ProtBERT   |
| Visualization    | Quarto, Plotly, Streamlit               |
| Collaboration    | GitHub, Git LFS, Quarto Notebooks       |
| Deployment       | GitHub Pages / Streamlit Cloud (future) |

---

## 📘 **Educational Integration**

This project supports **open pedagogy** and **experiential learning**:

* Students use GitHub ELNs to document their data analyses.
* Each student can clone the ELN template and complete guided activities (e.g., “Identify a gold cluster in your assigned Delftia genome”).
* The dataset and workflow will form part of a **Spring 2026 microbiology lab module**, funded by the **Alt-Textbook Project**.

---

## 🧾 **Next Milestones**

| Timeline    | Task                              | Output                              |
| ----------- | --------------------------------- | ----------------------------------- |
| 🗓️ Month 1 | Data collection + DB schema       | CSV/SQLite of all *Delftia* genomes |
| 🗓️ Month 2 | Feature extraction & baseline ML  | Preliminary gene classification     |
| 🗓️ Month 3 | Dashboard prototype               | Interactive Quarto interface        |
| 🗓️ Month 4 | Draft JMBE “Tips & Tools” article | Short paper + IRB documentation     |

---

## 👩‍🏫 **Project Team**

| Name                     | Role                                                       |
| ------------------------ | ---------------------------------------------------------- |
| **Dr. Carlos C. Goller** | Project Lead / Faculty Mentor                              |
| **Soham Gundewar**       | Data Engineering • Machine Learning • Tool Development     |
| **Shruti Kulkarni**      | Educational Integration • Documentation • Dashboard Design |

---

## 📄 **License**

Openly available under the [MIT License](LICENSE).
All educational materials are shared under the NC State **Alt-Textbook Open Education** framework.

---

## 💡 **Citation**

> Gundewar S., Kulkarni S., and Goller C. (2025).
> *Delftia Learning & Genomics Platform: Integrating Open Pedagogy, Bioinformatics, and Machine Learning for Microbiology Education.*
> North Carolina State University.

---

## ⭐ **Acknowledgments**

* NC State University Libraries — *Alt-Textbook Project*
* *Journal of Microbiology & Biology Education (JMBE)* – Tips & Tools guidelines
* NCBI Datasets, MIBiG, and RefSeq for genome data
* The Biological Sciences Department at NC State University

---

> “Turning genomes into classrooms — where every gene tells a story.”

```

---


