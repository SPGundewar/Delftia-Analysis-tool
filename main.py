import requests
import pandas as pd
from tqdm import tqdm

# -------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------
TAXON_ID = "80866"  # Delftia genus
OUT_CSV = "delftia_genomes_metadata_full.csv"
PAGE_SIZE = 500

# -------------------------------------------------------------
# FETCH FROM NCBI DATASETS
# -------------------------------------------------------------
url = f"https://api.ncbi.nlm.nih.gov/datasets/v2/genome/taxon/{TAXON_ID}/dataset_report"
params = {
    "filters.assembly_status": "latest",
    "filters.exclude_atypical": "true",
    "page_size": PAGE_SIZE
}

records, page_token = [], None
print("🔄 Fetching genome metadata for Delftia (taxon=80866)...")

while True:
    if page_token:
        params["page_token"] = page_token

    r = requests.get(url, params=params)
    if r.status_code != 200:
        print("Error:", r.status_code, r.text)
        break

    data = r.json()
    for g in data.get("reports", []):
        asm = g.get("assembly_info", {})
        stats = g.get("assembly_stats", {})
        qc = g.get("checkm_info", {})
        ann = g.get("annotation_info", {})
        ani = g.get("average_nucleotide_identity", {})
        wgs = g.get("wgs_info", {})

        rec = {
            # --- Basic identifiers ---
            "Assembly": asm.get("assembly_name"),
            "GenBank": asm.get("genbank_accession") or g.get("accession"),
            "RefSeq": asm.get("refseq_accession"),
            "Scientific_name": g.get("organism", {}).get("organism_name"),
            "Tax_ID": g.get("organism", {}).get("tax_id"),

            # --- Annotation & taxonomy ---
            "Taxonomy_check_status": ani.get("taxonomy_check_status"),
            "Annotation": ann.get("annotation_name"),
            "Annotation_Date": ann.get("annotation_date"),

            # --- Genome structure ---
            "Size_(Mb)": round(float(stats.get("total_sequence_length", 0)) / 1e6, 2),
            "Chromosomes": stats.get("number_of_chromosomes"),
            "Contigs": stats.get("number_of_contigs"),
            "Level": asm.get("assembly_level"),
            "Release_Date": asm.get("release_date"),
            "WGS_accession": wgs.get("wgs_project_accession"),
            "Contig_N50_(kb)": round(float(stats.get("contig_n50", 0)) / 1e3, 2),
            "Scaffold_N50_(kb)": round(float(stats.get("scaffold_n50", 0)) / 1e3, 2),
            "Scaffolds": stats.get("number_of_scaffolds"),
            "GC_percent": stats.get("gc_percent"),
            "BUSCO": stats.get("busco_score"),

            # --- Project / submitter ---
            "Sequencing_technology": asm.get("sequencing_tech"),
            "Submitter": asm.get("submitter"),
            "BioProject": asm.get("bioproject_accession"),
            "BioSample": asm.get("biosample", {}).get("accession"),

            # --- Gene counts ---
            "Genes": ann.get("gene_count"),
            "Protein_coding": ann.get("protein_count"),
            "Pseudogenes": ann.get("pseudogene_count"),

            # --- Extras & QC ---
            "Type_material": asm.get("is_type_material"),
            "CheckM_marker_set": qc.get("checkm_marker_set"),
            "CheckM_completeness(%)": qc.get("completeness"),
            "CheckM_contamination(%)": qc.get("contamination"),
            "Modifier": asm.get("modifier")
        }

        # --- Quality flag (optional) ---
        rec["High_quality"] = (
            asm.get("assembly_level") == "Complete Genome"
            and (qc.get("completeness", 0) or 0) >= 95
            and (qc.get("contamination", 0) or 0) <= 5
            and str(asm.get("genome_notes", "")).lower().find("metagenome") == -1
        )

        records.append(rec)

    page_token = data.get("next_page_token")
    if not page_token:
        break

# -------------------------------------------------------------
# SAVE TO CSV
# -------------------------------------------------------------
df = pd.DataFrame(records)
# df.to_csv(OUT_CSV, index=False)
print(f"✅ Saved {len(df)} genomes to {OUT_CSV}")



import json
import pandas as pd

records = []
with open("assembly_data_report.jsonl") as f:
    for line in f:
        j = json.loads(line)
        asm = j.get("assemblyInfo", {})
        stats = j.get("assemblyStats", {})
        ann = j.get("annotationInfo", {})
        gene_counts = ann.get("stats", {}).get("geneCounts", {})


        records.append({
            "Assembly": asm.get("assemblyName"),
            "Accession": j.get("accession"),
            "Scientific_name": j.get("organism", {}).get("organismName"),
            "Size(Mb)": round(int(stats.get("totalSequenceLength", 0)) / 1e6, 2),
            "GC(%)": stats.get("gcPercent"),
            "Genes": gene_counts.get("total"),
            "Proteins": gene_counts.get("proteinCoding"),
            "Pseudogenes": gene_counts.get("pseudogene"),
            "Annotation_date": ann.get("releaseDate"),
            "Submitter": asm.get("submitter"),
            "BioProject": asm.get("bioprojectAccession")
        })

df = pd.DataFrame(records)
print(df.head())




import pandas as pd

# Path to your Delftia .gff file
GFF_FILE = "genomic.gff"

genes = []

with open(GFF_FILE, "r") as f:
    for line in f:
        # Skip comments
        if line.startswith("#"):
            continue

        parts = line.strip().split("\t")
        if len(parts) != 9:
            continue

        seqid, source, feature_type, start, end, score, strand, phase, attributes = parts

        # Only keep gene and CDS entries
        if feature_type not in ["gene", "CDS"]:
            continue

        # Parse attributes field
        attr_dict = {}
        for a in attributes.split(";"):
            if "=" in a:
                k, v = a.split("=", 1)
                attr_dict[k] = v

        genes.append({
            "sequence_id": seqid,
            "feature_type": feature_type,
            "gene_id": attr_dict.get("ID", ""),
            "gene_name": attr_dict.get("Name", ""),
            "product": attr_dict.get("product", ""),
            "protein_id": attr_dict.get("protein_id", ""),
            "start": int(start),
            "end": int(end),
            "strand": strand
        })

# Convert to DataFrame
gff_df_genes = pd.DataFrame(genes)

# Filter only the "gene" rows for unique features
gff_df_genes = gff_df_genes[gff_df_genes["feature_type"] == "gene"]

# Add a genome identifier manually
gff_df_genes["genome_id"] = "GCF_000018665.1"

print(gff_df_genes.head(10))
print(f"✅ Parsed {len(gff_df_genes)} genes from {GFF_FILE}")


