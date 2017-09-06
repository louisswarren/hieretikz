module hierarchy where

data Bool : Set where
  true  : Bool
  false : Bool

_and_ : Bool → Bool → Bool
true and true = true
true and false = false
false and true = false
false and false = false


data ℕ : Set where
  zero : ℕ
  suc  : ℕ → ℕ

_==_ : ℕ → ℕ → Bool
zero == zero   = true
suc n == suc m = true
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


_++_ : List ℕ → List ℕ → List ℕ
[] ++ ys        = ys
(x :: xs) ++ ys with (x ∈ ys)
...               | true  = xs ++ ys
...               | false = x :: (xs ++ ys)



data Arrow : Set where
  _⇒_ : List ℕ → ℕ → Arrow

SingleClosure : Arrow → List ℕ → List ℕ
SingleClosure (ts ⇒ h) ps with ts ⊂ ps
...                     | true  = h :: ps
...                     | false = ps

Closure' : List Arrow → List ℕ → List ℕ
Closure' [] roots = roots
Closure' (c :: cs) roots = (SingleClosure c roots) ++ (Closure' cs roots)

Closure : List Arrow → List ℕ → List ℕ
Closure arrows roots with (Closure' arrows roots) ⊂ roots
...                     | true = roots
...                     | false = Closure arrows (Closure' arrows roots)


_,_⊢_ : List Arrow → List ℕ → ℕ → Bool
_ , [] ⊢ _ = false
thms , p :: premises ⊢ conc = true

