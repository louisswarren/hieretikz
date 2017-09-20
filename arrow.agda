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


modusponens : ℕ → Arrow → Arrow
modusponens n (⇒ q)   = (⇒ q)
modusponens n (p ⇒ q) with (n ≡ p)
...                      | true  = modusponens n q
...                      | false = p ⇒ (modusponens n q)


reduce : ℕ → List Arrow → List Arrow
reduce n ∘ = ∘
reduce n (arr ∷ rst) = (modusponens n arr) ∷ (reduce n rst)


search : List Arrow → List ℕ
search ∘ = ∘
search ((⇒ n) ∷ rst)   = n ∷ (search (reduce n rst))
search ((n ⇒ q) ∷ rst) with (n ∈ (search rst))
...                       | true  = search (q ∷ rst)
...                       | false = search rst


_⊢_ : List Arrow → Arrow → Bool
cs ⊢ (⇒ q) = q ∈ (search cs)
cs ⊢ (p ⇒ q) = ((⇒ p) ∷ cs) ⊢ q
