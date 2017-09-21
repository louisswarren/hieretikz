data Bool : Set where
  true  : Bool
  false : Bool


_or_ : Bool → Bool → Bool
true or true   = true
true or false  = true
false or true  = true
false or false = false



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


_∈_ : ℕ → List ℕ → Bool
x ∈ ∘        = false
x ∈ (y ∷ ys) with x ≡ y
...             | true  = true
...             | false = x ∈ ys



----------------------------------------



data Arrow : Set where
  ⇒_  : ℕ → Arrow
  _⇒_ : ℕ → Arrow → Arrow



closure : List Arrow → List ℕ → List ℕ
closure ∘ found                = found
closure ((⇒ n) ∷ rest) found   = n ∷ (closure rest (n ∷ found))
closure ((n ⇒ q) ∷ rest) found with (n ∈ found) or (n ∈ (closure rest found))
...                               | true  = closure (q ∷ rest) found
...                               | false = closure rest found


_⊢_ : List Arrow → Arrow → Bool
cs ⊢ (⇒ q)   = q ∈ (closure cs ∘)
cs ⊢ (p ⇒ q) = ((⇒ p) ∷ cs) ⊢ q
