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



closure : List Arrow → List ℕ → List ℕ
closure ∘ found                = found
closure ((⇒ n) ∷ rest) found   = n ∷ (closure rest (n ∷ found))
closure ((n ⇒ q) ∷ rest) found with (n ∈ found) or (n ∈ (closure rest found))
...                               | true  = closure (q ∷ rest) found
...                               | false = closure rest found



_,_⊢_ : List Arrow → List ℕ → ℕ → Bool
cs , ps ⊢ q = q ∈ (closure cs ps)



----------------------------------------



data Separation : Set where
  model : List ℕ → List ℕ → Separation


_,_⊨_ : Separation → List Arrow → ℕ → Bool
((model holds _) , cs ⊨ n) = (cs , holds ⊢ n)

_,_¬⊨_ : Separation → List Arrow → ℕ → Bool
((model _ fails) , cs ¬⊨ n) = any (_∋_ (closure cs (n ∷ ∘))) fails




--_,_,_¬⊨_ : List Separation → List Arrow → List ℕ → ℕ → Bool



