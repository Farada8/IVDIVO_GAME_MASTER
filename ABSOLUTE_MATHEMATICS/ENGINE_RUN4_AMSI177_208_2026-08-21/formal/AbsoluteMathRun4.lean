namespace AbsoluteMathRun4

universe u v w

/-- Context extension refines exact equivalence. -/
theorem context_refinement
    {X K₁ K₂ O : Type}
    (embed : K₁ → K₂)
    (obs : K₂ → X → O)
    (x y : X)
    (hxy : ∀ k₂ : K₂, obs k₂ x = obs k₂ y) :
    ∀ k₁ : K₁, obs (embed k₁) x = obs (embed k₁) y := by
  intro k₁
  exact hxy (embed k₁)

/-- Point-separating contexts force exact representation injectivity. -/
theorem point_separating_injective
    {X Z K O : Type}
    (obs : K → X → O)
    (sep : ∀ x y : X, x ≠ y → ∃ k : K, obs k x ≠ obs k y)
    (B : X → Z)
    (preserve : ∀ x y : X, B x = B y → ∀ k : K, obs k x = obs k y) :
    Function.Injective B := by
  intro x y hB
  by_contra hxy
  obtain ⟨k, hk⟩ := sep x y hxy
  exact hk (preserve x y hB k)

/-- Stricter defect threshold implies feasibility at every weaker threshold. -/
theorem feasible_set_monotonicity
    {A : Type}
    (defect : A → Nat)
    (ε₁ ε₂ : Nat)
    (hε : ε₁ ≤ ε₂) :
    {a : A | defect a ≤ ε₁} ⊆ {a : A | defect a ≤ ε₂} := by
  intro a ha
  exact le_trans ha hε

/-- A recursive-update collision forbids deterministic update U. -/
theorem recursive_collision_no_go
    {H Z A : Type}
    (state : H → Z)
    (append : H → A → H)
    (h₁ h₂ : H) (a : A)
    (hsame : state h₁ = state h₂)
    (hdiff : state (append h₁ a) ≠ state (append h₂ a)) :
    ¬ ∃ U : Z → A → Z, ∀ h : H, ∀ a' : A,
        state (append h a') = U (state h) a' := by
  intro hU
  obtain ⟨U, hrec⟩ := hU
  apply hdiff
  calc
    state (append h₁ a) = U (state h₁) a := hrec h₁ a
    _ = U (state h₂) a := by rw [hsame]
    _ = state (append h₂ a) := (hrec h₂ a).symm

end AbsoluteMathRun4
