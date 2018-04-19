open import Agda.Builtin.List
open import Agda.Builtin.Nat renaming (Nat to ℕ)
open import Agda.Builtin.Unit

module Reduce (T : ℕ → Set) where

data Vec (A : Set) : ℕ → Set where
  []  : Vec A zero
  _∷_ : ∀{n} → A → Vec A n → Vec A (suc n)
infixr 5 _∷_

record Σ (A : Set)(B : A → Set) : Set where
  constructor _,_
  field
    fst : A
    snd : B fst
open Σ

_×_ : Set → Set → Set
A × B = Σ A λ _ → B

data _⊎_ (A B : Set) : Set where
  inl : A → A ⊎ B
  inr : B → A ⊎ B

Maybe : Set → Set
Maybe A = A ⊎ ⊤

ΣT = Σ ℕ T

∣_∣ : ΣT → ℕ
∣ fst , snd ∣ = fst

reduce : ∀{n} → Vec ΣT n → (∀{k} → Vec ΣT n → T (suc k) → Maybe (T k)) → Vec ΣT n
reduce [] f = []
reduce (x ∷ xs) f = {!   !}
