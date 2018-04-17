open import Agda.Builtin.Bool
open import Agda.Builtin.List
open import Agda.Builtin.Nat renaming (Nat to ℕ)


_++_ : {A : Set} → List A → List A → List A
[]       ++ ys = ys
(x ∷ xs) ++ ys = x ∷ (xs ++ ys)

filter : {A : Set} → (A → Bool) → List A → List A
filter f [] = []
filter f (x ∷ xs) with f x
...               | false = filter f xs
...               | true  = x ∷ filter f xs

mkmembership : {A : Set} → (A → A → Bool) → (A → List A → Bool)
mkmembership _==_ a [] = false
mkmembership _==_ a (x ∷ xs) with a == x
...                          | false = mkmembership _==_ a xs
...                          | true  = true

all : {A : Set} → (A → Bool) → List A → Bool
all f [] = true
all f (x ∷ xs) with f x
...            | false = false
...            | true  = all f xs

any : {A : Set} → (A → Bool) → List A → Bool
any f [] = false
any f (x ∷ xs) with f x
...            | false = any f xs
...            | true  = true

mkintersects : {A : Set} → (A → A → Bool) → List A → List A → Bool
mkintersects {A} eq xs ys = any is-in-ys xs
                            where
                              is-in-ys : A → Bool
                              is-in-ys x = mkmembership eq x ys

iter : {A : Set} → (ℕ → A) → ℕ → List A
iter f zero = f zero ∷ []
iter f (suc n) = f (suc n) ∷ iter f n


data _∈_ {A : Set}(a : A) : List A → Set where
  refl  : ∀{xs}   → a ∈ (a ∷ xs)
  recur : ∀{x xs} → a ∈ xs → a ∈ (x ∷ xs)

data _⊂_ {A : Set} : List A → List A → Set where
  empty : ∀{ys} → [] ⊂ ys
  recur : ∀{xs ys x} → x ∈ ys → xs ⊂ ys → (x ∷ xs) ⊂ ys

record Σ (S : Set)(T : S → Set) : Set where
  constructor _,_
  field
    fst : S
    snd : T fst

_×_ : Set → Set → Set
S × T = Σ S (λ _ → T)


data False : Set where
record True : Set where

istrue : Bool → Set
istrue true = True
istrue false = False



--test : ∀ xs → ∀ ys → istrue (all (λ z → mkmembership _==_ z ys) xs) → xs ⊂ ys
--test [] ys pf = empty
--test (x ∷ xs) ys pf = recur {!   !} (test xs ys {!   !})
