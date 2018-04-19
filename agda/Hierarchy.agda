open import Agda.Builtin.Bool
open import Agda.Builtin.List
open import Agda.Builtin.Nat renaming (Nat to ℕ)

open import common

module Hierarchy
  (T    : Set)
  (_==_ : T → T → Bool)
  (_⊢_  : List T → T → Set)
  (_⊢̷_  : List T → List T → Set)
  (idx  : ℕ → T)
  where

_∈nc_ : T → List T → Set
x ∈nc xs = istrue (mkmembership _==_ x xs)

_⊂nc_ : List T → List T → Set
xs ⊂nc ys = istrue (all (λ x → mkmembership _==_ x ys) xs)

data _⇒_ (ts : List T)(x : T) : Set where
  arrow : ts ⊢ x → ts ⇒ x
  evident : x ∈nc ts → ts ⇒ x
  deduce : ∀{ss} → (∀{s} → s ∈ ss → ts ⇒ s) → ss ⇒ x → ts ⇒ x

