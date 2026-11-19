import os
import sys
import io
import json
import base64
import contextlib
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import nbformat as nbf

base_dir = r"c:\Users\prave\Downloads\RideOps_CaseStudy"
notebooks_dir = os.path.join(base_dir, "backend", "notebooks")
nb_path = os.path.join(notebooks_dir, "rideops_deep_operational_analysis.ipynb")

os.environ['MPLCONFIGDIR'] = os.path.join(base_dir, '.matplotlib_cache')
os.makedirs(os.path.join(base_dir, '.matplotlib_cache'), exist_ok=True)

with open(nb_path, 'r', encoding='utf-8') as f:
    nb = nbf.read(f, as_version=4)

# Global execution namespace
exec_scope = {
    'display': lambda x: print(x.to_string() if isinstance(x, (pd.DataFrame, pd.Series)) else str(x))
}

print(f"Executing {len(nb.cells)} cells directly in Python process...")

exec_counter = 1
for idx, cell in enumerate(nb.cells):
    if cell.cell_type == 'code':
        source = cell.source
        cell.outputs = []
        cell.execution_count = exec_counter
        exec_counter += 1
        
        # Buffer stdout
        stdout_buf = io.StringIO()
        try:
            # Clear previous plots
            plt.close('all')
            
            with contextlib.redirect_stdout(stdout_buf):
                exec(source, exec_scope)
            
            out_text = stdout_buf.getvalue()
            if out_text:
                cell.outputs.append(nbf.v4.new_output(
                    output_type='stream',
                    name='stdout',
                    text=out_text
                ))
            
            # Check if any matplotlib figures were generated and not yet closed/saved
            # or if figures were saved to backend/notebooks
            # If plt has figures open, save them as inline image outputs
            for fig_num in plt.get_fignums():
                fig = plt.figure(fig_num)
                img_buf = io.BytesIO()
                fig.savefig(img_buf, format='png', bbox_inches='tight')
                img_buf.seek(0)
                img_b64 = base64.b64encode(img_buf.read()).decode('utf-8')
                cell.outputs.append(nbf.v4.new_output(
                    output_type='display_data',
                    data={
                        'image/png': img_b64,
                        'text/plain': '<Figure size ...>'
                    }
                ))
            plt.close('all')
            print(f"  ✓ Cell {idx} executed successfully (outputs: {len(cell.outputs)})")
        except Exception as e:
            print(f"  ✗ Error in Cell {idx}: {e}")
            cell.outputs.append(nbf.v4.new_output(
                output_type='error',
                ename=type(e).__name__,
                evalue=str(e),
                traceback=[str(e)]
            ))

# Save executed notebook
with open(nb_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

# Also update legacy notebook rideops_support_analysis.ipynb
legacy_path = os.path.join(notebooks_dir, "rideops_support_analysis.ipynb")
with open(legacy_path, 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print(f"Successfully populated all cell outputs and saved to:\n  - {nb_path}\n  - {legacy_path}")
