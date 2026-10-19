import numpy as np
from typing import Dict

class AdaptiveConstraintEngine:
    """
    Operationalizes the Veto logic defined in the Dual-Phase Resonance Protocol (DPRP).
    Enforces Holographic Boundary constraints and the composite Meaning Metric (M).
    """
    def __init__(self, target_df: float = 2.0, tolerance: float = 0.2):
        self.target_df = target_df
        self.tolerance = tolerance
        self.meaning_metric_history = []

    def evaluate_final_block(self, eigenvalues: np.ndarray, mu_hat: float, m_ir: float, omega: float) -> Dict:
        """
        Evaluates the final 24-hour block of the Frustration Matrix diagonalization.
        """
        # 1. Level Spacing Audit (GUE constraint)
        # Ensure eigenvalues remain repulsed; no degeneracy allowed.
        sorted_evals = np.sort(eigenvalues)
        gaps = np.diff(sorted_evals)
        min_gap = np.min(gaps)
        
        # 2. Holographic Boundary Check
        df_current = 2.0 + mu_hat
        df_stable = abs(df_current - self.target_df) <= self.tolerance
        
        # 3. Meaning Metric (M) Calculation
        # M is a composite of Structural Order (omega), Functional Mass (m_ir), and Gap Integrity
        coherence_factor = np.clip(min_gap * 100, 0, 1) # Normalizing gap repulsion
        meaning_metric = (omega * 0.4) + (m_ir * 0.4) + (coherence_factor * 0.2)
        self.meaning_metric_history.append(meaning_metric)
        
        # 4. Final Veto Logic
        veto_triggered = False
        if not df_stable or min_gap < 1e-4 or meaning_metric < 0.85:
            veto_triggered = True
            
        return {
            "phase": "FINAL_BLOCK_STABILIZATION",
            "meaning_metric": float(meaning_metric),
            "df_current": float(df_current),
            "min_eigenvalue_gap": float(min_gap),
            "veto_triggered": bool(veto_triggered),
            "status": "HALT" if veto_triggered else "LOCKED_AND_STABLE"
        }
