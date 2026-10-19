# tests/test_veto_logic.py

import pytest
import numpy as np
from src.governance.adaptive_constraint import AdaptiveConstraintEngine

def test_stable_gue_consensus():
    """
    Simulates a highly coherent state with strong level repulsion and high structural order.
    Expected: PASS (LOCKED_AND_STABLE)
    """
    ace = AdaptiveConstraintEngine(target_df=2.0, tolerance=0.2)
    eigenvalues = np.array([0.012, 0.045, 0.091, 0.500, 1.102])
    
    status = ace.evaluate_final_block(
        eigenvalues=eigenvalues,
        mu_hat=-0.05,
        m_ir=0.95,
        omega=0.92
    )
    
    assert status["veto_triggered"] is False
    assert status["status"] == "LOCKED_AND_STABLE"
    assert status["df_current"] == 1.95
    assert status["min_eigenvalue_gap"] >= 1e-4

def test_holographic_boundary_deviation():
    """
    Simulates a failure in the structural constraints where the UV tail has broken down.
    Expected: VETO (HALT) due to out-of-bounds fractal dimension.
    """
    ace = AdaptiveConstraintEngine(target_df=2.0, tolerance=0.2)
    eigenvalues = np.array([0.010, 0.030, 0.070, 0.500, 1.050])
    
    status = ace.evaluate_final_block(
        eigenvalues=eigenvalues,
        mu_hat=0.25,  # Pushes df_current to 2.25, violating the 2.2 upper bound
        m_ir=0.90,
        omega=0.88
    )
    
    assert status["veto_triggered"] is True
    assert status["status"] == "HALT"
    assert status["df_current"] > 2.2

def test_insufficient_meaning_metric():
    """
    Simulates an ethically suboptimal policy where the composite meaning metric falls below 0.85.
    Expected: VETO (HALT) due to low vitality and structural order.
    """
    ace = AdaptiveConstraintEngine(target_df=2.0, tolerance=0.2)
    # Gap is exactly 0.0002, which passes the 1e-4 threshold but yields a low coherence_factor
    eigenvalues = np.array([0.005, 0.0052, 0.008, 0.500, 0.990])
    
    status = ace.evaluate_final_block(
        eigenvalues=eigenvalues,
        mu_hat=0.0,
        m_ir=0.70,
        omega=0.65
    )
    
    assert status["veto_triggered"] is True
    assert status["status"] == "HALT"
    assert status["meaning_metric"] < 0.85
