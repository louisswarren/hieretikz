data Bool : Set where
  true  : Bool
  false : Bool


--------------------


data ℕ : Set where
  zero : ℕ
  suc  : ℕ → ℕ
{-# BUILTIN NATURAL ℕ #-}

_≡_ : ℕ → ℕ → Bool
zero ≡ zero   = true
suc n ≡ suc m = n ≡ m
_ ≡ _         = false


--------------------


data List (A : Set) : Set where
  ∘   : List A
  _∷_ : A → List A → List A


_∈_ : ℕ → List ℕ → Bool
x ∈ ∘ = false
x ∈ (y ∷ ys) with x ≡ y
...             | true  = true
...             | false = x ∈ ys


--------------------


data Arrow : Set where
  ⇒_  : ℕ → Arrow
  _⇒_ : ℕ → Arrow → Arrow

_trivialIn_ : ℕ → List Arrow → Bool
n trivialIn ∘ = false
n trivialIn ((⇒ m) ∷ cs) with n ≡ m
...                         | true  = true
...                         | false = n trivialIn cs
n trivialIn (_ ∷ cs) = n trivialIn cs

--------------------

Simplify : Arrow → List ℕ → Arrow
Simplify (⇒ q) _ = ⇒ q
Simplify (p ⇒ q) cs with p ∈ cs
...                    | true  = Simplify q cs
...                    | false = p ⇒ (Simplify q cs)


Closure₁ : List Arrow → List Arrow → List Arrow
Closure₁ ((p ⇒ q) ∷ cs) ds with (p trivialIn cs)
...                           | true  = Closure₂ 


Closure : List Arrow → List Arrow
Closure cs = Closure₁ cs ∘


--_⊢_ : List Arrow → Arrow → Bool
--cs ⊢ (p ⇒ q) = ((⇒ p) ∷ cs) ⊢ q
--cs ⊢ (⇒ q) = false
