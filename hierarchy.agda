module hierarchy where

data Bool : Set where
  true  : Bool
  false : Bool

_and_ : Bool → Bool → Bool
true and true = true
true and false = false
false and true = false
false and false = false

_or_ : Bool → Bool → Bool
true or true = true
true or false = true
false or true = true
false or false = false


data ℕ : Set where
  zero : ℕ
  suc  : ℕ → ℕ

_==_ : ℕ → ℕ → Bool
zero == zero   = true
suc n == suc m = n == m
_ == _         = false




data List (A : Set) : Set where
  []   : List A
  _::_ : A → List A → List A

_∈_ : ℕ → List ℕ → Bool
x ∈ []      = false
x ∈ (y :: ys) with x == y
...              | true  = true
...              | false = x ∈ ys

_⊂_ : List ℕ → List ℕ → Bool
[] ⊂ ys      = true
(x :: xs) ⊂ ys with x ∈ ys
...               | true  = xs ⊂ ys
...               | false = false


_++_ : {A : Set} → List A → List A → List A
[] ++ ys        = ys
(x :: xs) ++ ys = x :: (xs ++ ys)

map : {A : Set} → (A → A) → List A → List A
map f []        = []
map f (x :: xs) = (f x) :: (map f xs)


any : {A : Set} → (A → Bool) → List A → Bool
any _ []        = false
any f (x :: xs) = (f x) or (any f xs)

all : {A : Set} → (A → Bool) → List A → Bool
all _ []        = true
all f (x :: xs) = (f x) and (all f xs)


data Arrow : Set where
  _⇒_ : List ℕ → ℕ → Arrow

_⇔_ : Arrow → Arrow → Bool
(at ⇒ ah) ⇔ (bt ⇒ bh) = ((at ⊂ bt) and (bt ⊂ at)) and (ah == bh)

_∈∈_ : Arrow → List Arrow → Bool
x ∈∈ []      = false
x ∈∈ (y :: ys) with x ⇔ y
...               | true  = true
...               | false = x ∈∈ ys

_⊂⊂_ : List Arrow → List Arrow → Bool
[] ⊂⊂ ys      = true
(x :: xs) ⊂⊂ ys with x ∈∈ ys
...                | true  = xs ⊂⊂ ys
...                | false = false


ArrowSearch : List Arrow → List Arrow → ℕ → Bool
ArrowSearch [] ds g = false
ArrowSearch (([] ⇒ h) :: cs) ds g with (h == g)
...         | true  = true
...         | false = ArrowSearch cs (([] ⇒ h) :: ds) g
ArrowSearch ((ts ⇒ h) :: cs) ds g with (h == g)
...         | true  = (all (ArrowSearch (cs ++ ds) []) ts)
                  or (ArrowSearch cs ((ts ⇒ h) :: ds) g)
...         | false = ArrowSearch cs ((ts ⇒ h) :: ds) g


_⊢_ : List Arrow → Arrow → Bool
cs ⊢ ((t :: ts) ⇒ h) = (([] ⇒ t) :: cs) ⊢ (ts ⇒ h)
cs ⊢ ([] ⇒ h)        = ArrowSearch cs [] h
