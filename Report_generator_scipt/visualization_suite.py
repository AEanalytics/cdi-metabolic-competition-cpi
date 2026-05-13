"""
AA Pathway Visualization Suite
- Heatmaps
- Radar Charts
- Missing Pathway Analysis
Author: Ebenezer T. A., Anastatsia N.K
Master's Thesis Project
Year: 2026
"""

import glob
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from collections import defaultdict

# ========================
# CONFIGURATION
# ========================
ESSENTIAL_AAS = {
    'Cysteine': {
        'KOs': ['K00640', 'K01738', 'K12339'],  # Serine acetyltransferase + cysteine synthase
        'ECs': ['2.3.1.30', '2.5.1.47', '4.4.1.8']
    },
    'Isoleucine': {
        'KOs': ['K01652', 'K01653', 'K00266', 'K00267'],  # Threonine dehydratase + acetolactate synthase
        'ECs': ['4.3.1.19', '2.2.1.6', '1.1.1.86']
    },
    'Leucine': {
        'KOs': ['K01652', 'K01653', 'K00266', 'K00267'],  # Shared with isoleucine
        'ECs': ['4.3.1.19', '2.2.1.6', '1.1.1.86']
    },
    'Proline': {
        'KOs': ['K00286', 'K00288', 'K00287'],  # Gamma-glutamyl kinase + P5C reductase
        'ECs': ['2.7.2.11', '1.5.1.2', '1.2.1.88']
    },
    'Tryptophan': {
        'KOs': ['K01695', 'K01696', 'K01697', 'K01698'],  # Trp operon enzymes
        'ECs': ['4.1.1.48', '4.1.3.27', '4.2.1.20']
    },
    'Valine': {
        'KOs': ['K01652', 'K01653', 'K00266', 'K00267'],  # Branched-chain AA pathway
        'ECs': ['4.3.1.19', '2.2.1.6', '1.1.1.86']
    },
    'Arginine': {
        'KOs': ['K00611', 'K01478', 'K01513'],  # N-acetylglutamate synthase/kinase
        'ECs': ['2.3.1.1', '2.7.2.8', '3.5.1.16']
    },
    'Asparagine': {
        'KOs': ['K01953', 'K01954'],  # Asparagine synthetases
        'ECs': ['6.3.1.1', '6.3.5.4']
    },
    'Glutamate': {
        'KOs': ['K00284', 'K00285'],  # Glutamate dehydrogenases
        'ECs': ['1.4.1.2', '1.4.1.4']
    },
    'Glutamine': {
        'KOs': ['K01915', 'K01953'],  # Glutamine synthetase
        'ECs': ['6.3.1.2', '6.3.5.4']
    },
    'Histidine': {
        'KOs': ['K00013', 'K00014', 'K00015'],  # His operon
        'ECs': ['1.1.1.23', '2.4.2.17', '3.6.1.31']
    },
    'Lysine': {
        'KOs': ['K00265', 'K00266', 'K00817'],  # DAP pathway
        'ECs': ['1.2.1.31', '2.6.1.17', '4.1.1.20']
    },
    'Methionine': {
        'KOs': ['K00797', 'K00799', 'K00800'],  # Homoserine O-transsuccinylase
        'ECs': ['2.3.1.46', '2.5.1.48', '4.4.1.8']
    },
    'Threonine': {
        'KOs': ['K00003', 'K00024', 'K00872'],  # Homoserine dehydrogenase/kinase
        'ECs': ['1.1.1.3', '2.7.1.39', '4.2.3.1']
    }
}

PROTECTIVE_THRESHOLD = 0.8
REPORT_PATTERN = "*_protection_report.md"

# ========================
# CORE FUNCTIONS
# ========================
def parse_reports():
    """Robust report parser with multi-format support"""
    data = []
    
    for report in glob.glob(REPORT_PATTERN):
        try:
            with open(report) as f:
                content = f.read()
            
            species = report.split('_protection_report.md')[0]
            records = {'Species': species}
            
            # Extract table data
            table = [line.split('|')[1:-1] for line in content.split('\n') 
                    if line.startswith('|') and 'Amino Acid' not in line]
            
            for row in table:
                if len(row) >= 3:  # Valid AA row
                    aa = row[0].strip()
                    if aa in ESSENTIAL_AAS:
                        completeness = row[2].strip().replace('%','')
                        records[aa] = float(completeness)/100 if '%' in row[2] else 0.0
            
            data.append(records)
            
        except Exception as e:
            print(f"⚠️ Skipping {report}: {str(e)}")
    
    return pd.DataFrame(data).set_index('Species')

# ========================
# VISUALIZATION MODULES
# ========================
def generate_heatmap(df, filename="pathway_heatmap.pdf"):
    """Publication-ready heatmap with dynamic sizing"""
    plt.figure(figsize=(max(10, len(df.columns)*0.8), max(6, len(df)*0.6)))
    
    ax = sns.heatmap(
        df,
        annot=True,
        fmt=".0%",
        cmap="RdYlGn",
        center=PROTECTIVE_THRESHOLD,
        linewidths=0.5,
        cbar_kws={'label': 'Pathway Completeness'},
        vmin=0,
        vmax=1
    )
    
    # Highlight protective thresholds
    for text in ax.texts:
        score = float(text.get_text().strip('%'))
        text.set_color('white' if score >= PROTECTIVE_THRESHOLD else 'black')
        if score >= PROTECTIVE_THRESHOLD:
            text.set_fontweight('bold')
    
    plt.title("Amino Acid Pathway Conservation", pad=20, fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"✅ Saved heatmap to {filename}")

def generate_radar(df, filename="radar_chart.html"):
    """Interactive radar plot for top candidates"""
    protective_species = df[df.mean(axis=1) >= PROTECTIVE_THRESHOLD]
    
    if not protective_species.empty:
        fig = px.line_polar(
            protective_species.reset_index().melt(id_vars='Species'),
            r='value',
            theta='variable',
            color='Species',
            line_close=True,
            template="plotly_white",
            title=f"Top Protective Candidates (≥{PROTECTIVE_THRESHOLD:.0%} Avg)"
        )
        fig.write_html(filename)
        print(f"✅ Saved interactive radar to {filename}")
    else:
        print("ℹ️ No species met protective threshold for radar chart")

# ========================
# MAIN WORKFLOW
# ========================
def main():
    print("\n" + "="*50)
    print("AA PATHWAY VISUALIZATION SUITE".center(50))
    print("="*50)
    
    # Data extraction
    print("\n🔍 Parsing reports...")
    df = parse_reports()
    
    if df.empty:
        print("\n❌ No valid data found. Verify:")
        print(f"- Reports exist matching: {REPORT_PATTERN}")
        print("- Files contain complete tables with percentages")
        return
    
    # Visualizations
    print("\n📊 Generating visualizations...")
    generate_heatmap(df)
    generate_radar(df)
    
    # Summary
    print("\n🎉 Visualization Complete!")
    print(f"- Heatmap: pathway_heatmap.pdf")
    print(f"- Interactive Radar: radar_chart.html")
    print("\n🔍 Next Steps:")
    print("1. Identify species with mostly green cells in heatmap")
    print("2. Explore top candidates in interactive radar chart")
    print("3. Cross-validate with experimental data")

if __name__ == "__main__":
    main()
