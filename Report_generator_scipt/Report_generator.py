"""
AA Pathway Protection Predictor
Analyzes bacterial genomes for protective potential against C. difficile
"""

import pandas as pd
import os
from collections import defaultdict

# ========================
# CONFIGURATION
# ========================
ESSENTIAL_AAS = {
    'Cysteine': {'KOs': ['K00640', 'K01738'], 'ECs': ['2.3.1.30', '2.5.1.47']},
    'Isoleucine': {'KOs': ['K01652', 'K00266'], 'ECs': ['4.3.1.19', '2.2.1.6']},
    'Leucine': {'KOs': ['K01652', 'K00266'], 'ECs': ['4.3.1.19', '2.2.1.6']},
    'Proline': {'KOs': ['K00286'], 'ECs': ['1.5.1.2']},
    'Tryptophan': {'KOs': ['K01698'], 'ECs': ['4.1.3.27']},
    'Valine': {'KOs': ['K01652', 'K00266'], 'ECs': ['4.3.1.19', '2.2.1.6']},
    'Arginine': {'KOs': ['K00611'], 'ECs': ['2.3.1.1', '3.5.1.16']},
    'Asparagine': {'KOs': ['K01953'], 'ECs': ['6.3.5.4']},
    'Glutamate': {'KOs': ['K00284', 'K01779'], 'ECs': ['1.4.1.2', '5.1.1.13']},
    'Glutamine': {'KOs': ['K01915'], 'ECs': ['6.3.1.2']},
    'Histidine': {'KOs': ['K00013', 'K00014'], 'ECs': ['1.1.1.23', '2.4.2.17']},
    'Lysine': {'KOs': ['K00266', 'K00817'], 'ECs': ['2.6.1.17', '4.1.1.20']},
    'Methionine': {'KOs': ['K00797', 'K00800'], 'ECs': ['2.3.1.46', '4.4.1.8']},
    'Threonine': {'KOs': ['K00003', 'K00872'], 'ECs': ['1.1.1.3', '4.2.3.1']}
}

PROTECTIVE_THRESHOLD = 0.8  # 80% pathway overlap required
CD_REFERENCE = "C_difficile_annotations.emapper.annotations"
TARGET_DIR = "microbe_genomes"

# ========================
# CORE FUNCTIONS
# ========================
def load_annotations(file_path):
    """Load and standardize eggNOG-mapper annotations"""
    try:
        # Smart header detection
        with open(file_path) as f:
            first_line = f.readline().strip()
            has_header = any(first_line.startswith(x) for x in ('#query', 'query'))
        
        df = pd.read_csv(
            file_path,
            sep='\t',
            comment='#' if not has_header else None,
            header=0 if has_header else None,
            dtype=str,
            low_memory=False
        )
        
        # Standardize columns
        cols = [
            'query', 'seed_ortholog', 'evalue', 'score', 'eggNOG_OGs', 'max_annot_lvl',
            'COG_category', 'Description', 'Preferred_name', 'GOs', 'EC', 'KEGG_ko',
            'KEGG_Pathway', 'KEGG_Module', 'KEGG_Reaction', 'KEGG_rclass', 'BRITE',
            'KEGG_TC', 'CAZy', 'BiGG_Reaction', 'PFAMs'
        ]
        df.columns = cols[:len(df.columns)]
        
        # Clean critical fields
        for col in ['KEGG_ko', 'EC']:
            if col in df.columns:
                df[col] = df[col].str.replace('ko:', '').fillna('')
        
        return df
    
    except Exception as e:
        print(f"❌ Failed to load {file_path}: {str(e)}")
        return None

def pathway_status(df, ko_list, ec_list):
    """Calculate pathway completeness score (0-1)"""
    if df is None or (not ko_list and not ec_list):
        return 0.0
    
    # KO-based scoring
    ko_score = 0.0
    if ko_list:
        present_kos = {ko.upper() for ko in df['KEGG_ko'].str.split(',').explode() if ko}
        ko_score = sum(ko.upper() in present_kos for ko in ko_list) / len(ko_list)
    
    # EC-based scoring
    ec_score = 0.0
    if ec_list:
        present_ecs = {ec for ec in df['EC'].str.split(',').explode() if ec}
        ec_score = sum(ec in present_ecs for ec in ec_list) / len(ec_list)
    
    return max(ko_score, ec_score) if (ko_list or ec_list) else 0.0

def analyze_genome(target_df, reference_df):
    """Core analysis comparing target to reference"""
    results = {}
    diagnostics = defaultdict(dict)
    
    for aa, data in ESSENTIAL_AAS.items():
        # Verify reference pathway exists
        ref_score = pathway_status(reference_df, data['KOs'], data['ECs'])
        if ref_score < 0.8:
            print(f"⚠️  Reference lacks {aa} pathway (completeness: {ref_score:.0%})")
        
        # Check target genome
        target_score = pathway_status(target_df, data['KOs'], data['ECs'])
        results[aa] = target_score >= 0.8
        
        # Store diagnostics
        present_kos = {ko.upper() for ko in target_df['KEGG_ko'].str.split(',').explode() if ko}
        present_ecs = {ec for ec in target_df['EC'].str.split(',').explode() if ec}
        
        diagnostics[aa] = {
            'status': '✅' if results[aa] else '❌',
            'missing_kos': list(set(ko.upper() for ko in data['KOs']) - present_kos),
            'missing_ecs': list(set(data['ECs']) - present_ecs),
            'completeness': f"{target_score:.0%}"
        }
    
    overlap = sum(results.values()) / len(results)
    is_protective = overlap >= PROTECTIVE_THRESHOLD
    return overlap, is_protective, diagnostics

def generate_report(species, overlap, protective, diagnostics):
    """Create comprehensive markdown report"""
    report = [
        "# AMINO ACID PATHWAY ANALYSIS REPORT",
        "="*50,
        f"**Species:** {species}",
        f"**Pathway Overlap:** {overlap:.1%}",
        f"**Protective Potential:** {'✅ YES' if protective else '❌ NO'}",
        "",
        "## Pathway Status",
        "| Amino Acid  | Status | Completeness | Missing KOs | Missing ECs |",
        "|-------------|--------|--------------|-------------|-------------|"
    ]
    
    for aa, data in diagnostics.items():
        row = [
            f"| {aa:<11}",
            f"| {data['status']:<6}",
            f"| {data['completeness']:<12}",
            f"| {', '.join(data['missing_kos']) or '-':<11}",
            f"| {', '.join(data['missing_ecs']) or '-':<11} |"
        ]
        report.append(''.join(row))
    
    report_path = f"{species}_protection_report.md"
    with open(report_path, 'w') as f:
        f.write('\n'.join(report))
    
    return report_path

# ========================
# MAIN WORKFLOW
# ========================
def main():
    print("\n" + "="*50)
    print("AA PATHWAY PROTECTION PREDICTOR".center(50))
    print("="*50)
    
    # Load reference genome
    print(f"\n🔬 Loading reference: {CD_REFERENCE}")
    cd_df = load_annotations(CD_REFERENCE)
    if cd_df is None:
        return
    
    # Process target genomes
    for filename in sorted(os.listdir(TARGET_DIR)):
        if filename.endswith(".emapper.annotations"):
            species = filename.split('.')[0]
            print(f"\n🧪 Analyzing {species}")
            
            target_df = load_annotations(os.path.join(TARGET_DIR, filename))
            if target_df is None:
                continue
            
            # Core analysis
            overlap, protective, diagnostics = analyze_genome(target_df, cd_df)
            
            # Generate report
            report_file = generate_report(species, overlap, protective, diagnostics)
            print(f"📊 Results saved to {report_file}")
    
    print("\n" + "="*50)
    print("ANALYSIS COMPLETE".center(50))
    print("="*50)

if __name__ == "__main__":
    main()