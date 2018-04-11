open import Agda.Builtin.Bool
open import Agda.Builtin.List
open import Agda.Builtin.Nat renaming (Nat to ℕ)

open import common

module Hierarchy
  (Γ    : Set)
  (_==_ : Γ → Γ → Bool)
  (_⊢_  : List Γ → Γ → Set)
  (_⊢̷_  : List Γ → List Γ → Set)
  (idx  : ℕ → Γ)
  where

Arrow : Set
Arrow = Σ (List Γ × Γ) λ x → Σ.fst x ⊢ Σ.snd x

intersects = mkintersects _==_

data _⊃_ : List Γ → Γ → Set where
  arrow     : ∀{γs γ} → γs ⊢ γ → γs ⊃ γ
  trivial   : ∀{γs γ} → γ ∈ γs → γs ⊃ γ
  deduction : ∀{γs γ αs} → (∀ α → α ∈ αs → γs ⊃ α) → αs ⊃ γ → γs ⊃ γ

data _⊃̷_ : List Γ → List Γ → Set where
  tier       : ∀{αs βs} → αs ⊢̷ βs → αs ⊃̷ βs
  close      : ∀{αs βs γ} → αs ⊃̷ βs → αs ⊃ γ → (γ ∷ αs) ⊃̷ βs
  consistent : ∀{αs βs γ β} → αs ⊃̷ βs → β ∈ βs → (γ ∷ αs) ⊃ β → αs ⊃̷ (γ ∷ βs)

closure : (γs : List Γ) → List Arrow → List (Σ Γ (_⊃_ γs))
closure γs [] = []
closure γs (((tails , head) , pf) ∷ rs) = {!   !}

--domain : List Arrow → List Γ
--domain [] = []
--domain ((tails ⊃ head) ∷ rs) = head ∷ (tails ++ domain rs)
--
--closure : List Γ → List Arrow → List Γ
--closure γs rs = ?
--
--completion : Tier → List Arrow → Tier
--completion (low ⊃̷ high) rs = clow ⊃̷ filter inconsistent (domain rs)
--  where
--    clow = closure low rs
--    inconsistent : Γ → Bool
--    inconsistent γ = intersects (closure (γ ∷ clow) rs) high
--
----unknown : List Γ → ℕ → List Arrow → List Tier → List Arrow
----unknown γs n rs ts = {!   !}
--
--
--
