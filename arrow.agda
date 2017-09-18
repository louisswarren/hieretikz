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


Simplify : Arrow → List ℕ → Arrow
Simplify (⇒ q) _ = ⇒ q
Simplify (p ⇒ q) cs with p ∈ cs
...                    | true  = Simplify q cs
...                    | false = p ⇒ (Simplify q cs)


