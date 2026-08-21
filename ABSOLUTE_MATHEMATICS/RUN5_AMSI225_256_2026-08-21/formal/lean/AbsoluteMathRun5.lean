namespace AbsoluteMathRun5

universe u v w

/-- P1: equivalence under a larger context family implies equivalence under an embedded smaller family. -/
theorem context_refinement
    {X K₁ K₂ O : Type}
    (embed : K₁ → K₂)
    (obs : K₂ → X → O)
    (x y : X)
    (hxy : ∀ k₂ : K₂, obs k₂ x = obs k₂ y) :
    ∀ k₁ : K₁, obs (embed k₁) x = obs (embed k₁) y := by
  intro k₁
  exact hxy (embed k₁)

/-- P2: point-separating contexts force an exact behavior-preserving representation to be injective. -/
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

/-- P3: a candidate feasible at a stricter natural-number defect threshold remains feasible at a weaker threshold. -/
theorem feasible_set_monotonicity
    {A : Type}
    (defect : A → Nat)
    (ε₁ ε₂ : Nat)
    (hε : ε₁ ≤ ε₂) :
    {a : A | defect a ≤ ε₁} ⊆ {a : A | defect a ≤ ε₂} := by
  intro a ha
  exact Nat.le_trans ha hε

/-- P10: a collision in the compressed state with different same-input successors forbids deterministic recursive update. -/
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

/--
Phase-boundary core lemma.
If no candidate defect lies strictly above ε₁ and at-or-below ε₂,
then the feasible membership predicate is identical at the two thresholds.
This is the key finite breakpoint fact behind the Run2/Run4 d*(ε) step-function argument.
-/
theorem no_breakpoint_same_feasibility
    {A : Type}
    (defect : A → Nat)
    (ε₁ ε₂ : Nat)
    (hε : ε₁ ≤ ε₂)
    (hgap : ∀ a : A, ¬ (ε₁ < defect a ∧ defect a ≤ ε₂)) :
    ∀ a : A, (defect a ≤ ε₁ ↔ defect a ≤ ε₂) := by
  intro a
  constructor
  · intro h
    exact Nat.le_trans h hε
  · intro h₂
    by_contra hnot
    have hlt : ε₁ < defect a := Nat.lt_of_not_ge hnot
    exact hgap a ⟨hlt, h₂⟩

/--
Signature-extension revocation core lemma.
If a relation identifies x and y but a newly included operation h sends them to non-related outputs,
the relation cannot be compatible with h.
-/
theorem signature_extension_revocation
    {X : Type}
    (rel : X → X → Prop)
    (h : X → X)
    (x y : X)
    (hxy : rel x y)
    (hbreak : ¬ rel (h x) (h y)) :
    ¬ (∀ a b : X, rel a b → rel (h a) (h b)) := by
  intro compatible
  exact hbreak (compatible x y hxy)

end AbsoluteMathRun5
