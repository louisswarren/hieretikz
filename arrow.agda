open import Agda.Builtin.Bool


_or_ : Bool → Bool → Bool
true or _      = true
_ or true      = true
false or false = false

_and_ : Bool → Bool → Bool
false and _   = false
_ and false   = false
true and true = true


----------------------------------------



data ℕ : Set where
  zero : ℕ
  suc  : ℕ → ℕ
{-# BUILTIN NATURAL ℕ #-}


_≡_ : ℕ → ℕ → Bool
zero ≡ zero   = true
suc n ≡ suc m = n ≡ m
_ ≡ _         = false



----------------------------------------


infixr 5 _∷_

data List (A : Set) : Set where
  ∘   : List A
  _∷_ : A → List A → List A
{-# BUILTIN LIST List #-}
{-# BUILTIN NIL  ∘    #-}
{-# BUILTIN CONS _∷_  #-}


any : {A : Set} → (A → Bool) → List A → Bool
any _ ∘        = false
any f (x ∷ xs) = (f x) or (any f xs)


_∈_ : ℕ → List ℕ → Bool
x ∈ ∘        = false
x ∈ (y ∷ ys) with x ≡ y
...             | true  = true
...             | false = x ∈ ys


_∋_ : List ℕ → ℕ → Bool
xs ∋ y = y ∈ xs

----------------------------------------



data Arrow : Set where
  ⇒_  : ℕ → Arrow
  _⇒_ : ℕ → Arrow → Arrow

_≡≡_ : Arrow → Arrow → Bool
(⇒ q) ≡≡ (⇒ s)     = q ≡ s
(p ⇒ q) ≡≡ (r ⇒ s) = (p ≡ r) and (q ≡≡ s)
_ ≡≡ _             = false

_∈∈_ : Arrow → List Arrow → Bool
x ∈∈ ∘        = false
x ∈∈ (y ∷ ys) with x ≡≡ y
...              | true  = true
...              | false = x ∈∈ ys


closure : List Arrow → List ℕ → List ℕ
closure ∘ found                = found
closure ((⇒ n) ∷ rest) found   = n ∷ (closure rest (n ∷ found))
closure ((n ⇒ q) ∷ rest) found with (n ∈ found) or (n ∈ (closure rest found))
...                               | true  = closure (q ∷ rest) found
...                               | false = closure rest found



_,_⊢_ : List Arrow → List ℕ → ℕ → Bool
cs , ps ⊢ q = q ∈ (closure cs ps)

_⊢_ : List Arrow → Arrow → Bool
cs ⊢ (⇒ q)   = q ∈ (closure cs ∘)
cs ⊢ (p ⇒ q) = ((⇒ p) ∷ cs) ⊢ q


----------------------------------------



data Separation : Set where
  model : List ℕ → List ℕ → Separation


modelsupports : Separation → List Arrow → ℕ → Bool
modelsupports (model holds _) cs n = cs , holds ⊢ n


modeldenies : Separation → List Arrow → ℕ → Bool
modeldenies (model _ fails) cs n = any (_∋_ (closure cs (n ∷ ∘))) fails


_⟪!_⟫_ : List Arrow → Separation → Arrow → Bool
cs ⟪! m ⟫ (⇒ q) = modeldenies m cs q
cs ⟪! m ⟫ (p ⇒ q) = (modelsupports m cs p) and (cs ⟪! m ⟫ q)


_⟪_⟫_ : List Arrow → List Separation → Arrow → Bool
cs ⟪ ∘ ⟫ arr = false
cs ⟪ m ∷ ms ⟫ arr = (cs ⟪! m ⟫ arr) or (cs ⟪ ms ⟫ arr)



----------------------------------------



data Relation : Set where
  Proved    : Relation
  Derivable : Relation
  Separated : Relation
  Unknown   : Relation


consider : List Arrow → List Separation → Arrow → Relation
consider cs ms arr with (arr ∈∈ cs)
...                   | true  = Proved
...                   | false with (cs ⊢ arr)
...                              | true  = Derivable
...                              | false with (cs ⟪ ms ⟫ arr)
...                                         | true  = Separated
...                                         | false = Unknown


proofs : List Arrow
proofs =
   (3 ⇒ (⇒ 4)) ∷
--   (5 ⇒ (⇒ 4)) ∷
   (6 ⇒ (⇒ 4)) ∷
   (3 ⇒ (⇒ 3)) ∷
   (3 ⇒ (⇒ 3)) ∷
   (9 ⇒ (⇒ 3)) ∷
   (9 ⇒ (⇒ 3)) ∷
   (5 ⇒ (⇒ 7)) ∷
   (9 ⇒ (⇒ 7)) ∷
   (6 ⇒ (⇒ 8)) ∷
   (10 ⇒ (⇒ 8)) ∷
   (10 ⇒ (⇒ 7)) ∷
   (5 ⇒ (⇒ 10)) ∷
   (10 ⇒ (⇒ 4)) ∷
   (5 ⇒ (⇒ 11)) ∷
   (6 ⇒ (⇒ 11)) ∷
   (11 ⇒ (⇒ 4)) ∷
   (10 ⇒ (⇒ 7)) ∷
   (8 ⇒ (⇒ 4)) ∷
   (9 ⇒ (⇒ 7)) ∷
   (9 ⇒ (⇒ 8)) ∷
   (3 ⇒ (⇒ 8)) ∷
   (5 ⇒ (3 ⇒ (⇒ 9))) ∷
   (6 ⇒ (7 ⇒ (⇒ 10))) ∷
   (6 ⇒ (3 ⇒ (⇒ 3))) ∷
   (7 ⇒ (⇒ 7)) ∷
   (7 ⇒ (⇒ 7)) ∷
   (7 ⇒ (8 ⇒ (⇒ 10))) ∷
   (3 ⇒ (10 ⇒ (⇒ 9))) ∷
   (5 ⇒ (⇒ 1)) ∷
   (3 ⇒ (1 ⇒ (⇒ 9))) ∷
   (1 ⇒ (⇒ 2)) ∷
   (10 ⇒ (⇒ 2)) ∷ ∘

cms : List Separation
cms =
  (model (12 ∷ 6 ∷ 11 ∷ 4 ∷ 1 ∷ ∘) (5 ∷ 3 ∷ 7 ∷ 7 ∷ ∘)) ∷
  (model (6 ∷ 3 ∷ 11 ∷ 4 ∷ 7 ∷ 8 ∷ 3 ∷ 9 ∷ 10 ∷ 1 ∷ ∘) (5 ∷ ∘)) ∷
  (model (12 ∷ 5 ∷ 11 ∷ 4 ∷ 1 ∷ ∘) (6 ∷ 3 ∷ ∘)) ∷
  (model (5 ∷ 3 ∷ 11 ∷ 4 ∷ 7 ∷ 8 ∷ 3 ∷ 9 ∷ 10 ∷ 1 ∷ ∘) (6 ∷ ∘)) ∷
  (model (12 ∷ 4 ∷ 11 ∷ ∘) (5 ∷ 6 ∷ 3 ∷ 8 ∷ 9 ∷ 1 ∷ ∘)) ∷
  (model (12 ∷ 5 ∷ 6 ∷ 4 ∷ 11 ∷ 1 ∷ ∘) (3 ∷ ∘)) ∷
  (model (12 ∷ 4 ∷ 11 ∷ 7 ∷ ∘) (9 ∷ 5 ∷ 6 ∷ 10 ∷ 8 ∷ 1 ∷ ∘)) ∷
  (model (10 ∷ 9 ∷ ∘) (1 ∷ ∘)) ∷
  (model (3 ∷ 4 ∷ 11 ∷ ∘) (9 ∷ 5 ∷ 6 ∷ 10 ∷ 7 ∷ 1 ∷ ∘)) ∷
  (model (12 ∷ 7 ∷ 1 ∷ ∘) (4 ∷ 11 ∷ 8 ∷ ∘)) ∷
  (model (9 ∷ 3 ∷ 10 ∷ 8 ∷ 1 ∷ ∘) (11 ∷ ∘)) ∷
  (model (12 ∷ 4 ∷ 10 ∷ 1 ∷ ∘) (11 ∷ 3 ∷ ∘)) ∷
  (model (3 ∷ 6 ∷ 5 ∷ ∘) (∘)) ∷
  (model (1 ∷ 2 ∷ 3 ∷ 4 ∷ 5 ∷ 6 ∷ 7 ∷ 8 ∷ 9 ∷ 10 ∷ 11 ∷ ∘) (12 ∷ ∘)) ∷ ∘

testp : Arrow
testp = (5 ⇒ (⇒ 10))

testd : Arrow
testd = (5 ⇒ (⇒ 4))

tests : Arrow
tests = (5 ⇒ (⇒ 3))

testu : Arrow
testu = (6 ⇒ (⇒ 1))


main = (closure proofs (5 ∷ ∘))
