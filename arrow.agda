data Bool : Set where
  true  : Bool
  false : Bool


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



data List (A : Set) : Set where
  ∘   : List A
  _∷_ : A → List A → List A


any : {A : Set} → (A → Bool) → List A → Bool
any _ ∘        = false
any f (x ∷ xs) = (f x) or (any f xs)


apply : {A B : Set} → (A → B) → List A → List B
apply _ ∘        = ∘
apply f (x ∷ xs) = (f x) ∷ (apply f xs)


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

