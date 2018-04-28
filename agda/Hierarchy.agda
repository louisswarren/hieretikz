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

isFound? : (x : T)(xs : List T) → Set
isFound? x xs = Find (_==_ x) xs

data _∈_ (x : T) : List T → Set where
  head : ∀{y ys} → isTrue (x == y) → x ∈ (y ∷ ys)
  tail : ∀{y ys} → x ∈ ys          → x ∈ (y ∷ ys)

data _∉_ (x : T) : List T → Set where
  empty : x ∉ []
  noteq : ∀{y ys} → isFalse (x == y) → x ∉ ys → x ∉ (y ∷ ys)

missing∉ : ∀{xs x} → AllFalse (_==_ x) xs → x ∉ xs
missing∉ {[]} allpf = empty
missing∉ {x ∷ xs} (x₂ ∷ allpf) = noteq x₂ (missing∉ allpf)

found∈ : ∀{x} → ∀ xs y ys → isTrue (x == y) → x ∈ (xs ++ y ∷ ys)
found∈ [] y ys pf = head pf
found∈ (x ∷ xs) y ys pf = tail (found∈ xs y ys pf)

decide : ∀{x xs} → isFound? x xs → (x ∈ xs) ⊎ (x ∉ xs)
decide (missing pf)        = inr (missing∉ pf)
decide (found xs' y ys pf) = inl (found∈ xs' y ys pf)

data _⇒_ (ts : List T)(x : T) : Set where
  arrow : ts ⊢ x → ts ⇒ x
  evident : x ∈ ts → ts ⇒ x
--  deduce : ∀{ss} → (∀{s} → s ∈ ss → ts ⇒ s) → ss ⇒ x → ts ⇒ x ????????


data ⊢list : Set where
  [] : ⊢list
  _∷_ : ∀{xs x} → xs ⊢ x → ⊢list → ⊢list

data Closure (rs : ⊢list) : (List T) → Set where
  base : ∀{xs x} → x ∈ xs → Closure rs x
