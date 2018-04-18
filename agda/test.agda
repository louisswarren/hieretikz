open import Agda.Builtin.List
open import Agda.Builtin.Nat renaming (Nat to ℕ)

data _⊢_ : List ℕ → ℕ → Set where
  proof : ∀ xs → ∀ x → xs ⊢ x

data _⊢̷_ : List ℕ → List ℕ → Set where
  sep : ∀ xs → ∀ ys → xs ⊢̷ ys

id : {A : Set} → A → A
id x = x

import Hierarchy
open Hierarchy ℕ _==_ _⊢_ _⊢̷_ id



triv : ∀ n → n ∈nc (n ∷ [])
triv n = ?
