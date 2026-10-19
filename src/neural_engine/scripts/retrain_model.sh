#!/bin/bash

# Exit immediately if any command fails
set -e

echo "=================================================="
echo "AZGC LABORATORIES: EXASCALE MLOPS PIPELINE"
echo "=================================================="

# Fetch cluster environment variables, defaulting to local values if not set
NODE_ID=${HOSTNAME:-"local-dev-node"}
TARGET_DF=${TARGET_FRACTAL_DIMENSION:-2.0}
TOLERANCE=${VETO_TOLERANCE:-0.2}

echo "[SYSTEM] Node Identifier: $NODE_ID"
echo "[SYSTEM] Target Fractal Dimension (df): $TARGET_DF"
echo "[SYSTEM] Boundary Tolerance: $TOLERANCE"
echo "[SYSTEM] Commencing QCI-DPRP Engine sequence..."
echo "--------------------------------------------------"

# Execute the core engine 
# (This runs the run_engine.py file we created earlier)
python /app/run_engine.py

echo "--------------------------------------------------"
echo "[SYSTEM] Execution completed successfully on node $NODE_ID."
echo "=================================================="
