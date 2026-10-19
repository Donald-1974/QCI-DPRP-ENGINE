# run_engine.py

import time
from src.quantum_core.syk_diagonalization import SYKDiagonalizer
from src.governance.adaptive_constraint import AdaptiveConstraintEngine

def main():
    print("==================================================")
    print("INITIALIZING QCI-DPRP ENGINE")
    print("==================================================\n")
    
    # Initialize the core modules
    print("[SYSTEM] Booting SYK Diagonalizer (N=1024)...")
    diagonalizer = SYKDiagonalizer(matrix_size=1024, coupling_variance=1.0)
    
    print("[SYSTEM] Booting Adaptive Constraint Engine (Target df=2.0)...")
    ace = AdaptiveConstraintEngine(target_df=2.0, tolerance=0.2)
    
    time.sleep(1)
    print("\n[PHASE] Executing Dual-Phase Resonance Protocol...\n")
    
    # Simulate a run of 3 sequential blocks to show continuous monitoring
    for block in range(1, 4):
        print(f"--- Block {block} Diagonalization ---")
        
        # 1. Quantum Core extracts observables
        metrics = diagonalizer.diagonalize_and_extract()
        print(f"Extracted mu_hat: {metrics['mu_hat']:.4f}")
        print(f"Extracted m_ir:   {metrics['m_ir']:.4f}")
        print(f"Extracted omega:  {metrics['omega']:.4f}")
        
        # 2. Governance evaluates the block
        status = ace.evaluate_final_block(
            eigenvalues=metrics['eigenvalues'],
            mu_hat=metrics['mu_hat'],
            m_ir=metrics['m_ir'],
            omega=metrics['omega']
        )
        
        # 3. Output Results
        print(f"Veto Status:      {status['status']}")
        print(f"Meaning Metric:   {status['meaning_metric']:.4f}")
        print(f"Fractal Dim (df): {status['df_current']:.4f}")
        print(f"Min Gap:          {status['min_eigenvalue_gap']:.6f}\n")
        
        if status['veto_triggered']:
            print(f"[ALERT] Veto triggered on block {block}. Halting projection to prevent topological drift.")
            break
        
        time.sleep(1)
        
    if not status['veto_triggered']:
        print("==================================================")
        print("FINAL STATE: LOCKED_AND_STABLE")
        print("==================================================")

if __name__ == "__main__":
    main()
