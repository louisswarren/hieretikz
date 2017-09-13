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


_++_ : List ℕ → List ℕ → List ℕ
[] ++ ys        = ys
(x :: xs) ++ ys with (x ∈ ys)
...               | true  = xs ++ ys
...               | false = x :: (xs ++ ys)

map : {A : Set} → (A → A) → List A → List A
map f []        = []
map f (x :: xs) = (f x) :: (map f xs)


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


-- SingleClosure : Arrow → List ℕ → List ℕ
-- SingleClosure (ts ⇒ h) ps with ts ⊂ ps
-- ...                     | true  = h :: ps
-- ...                     | false = ps
--
-- Closure' : List Arrow → List ℕ → List ℕ
-- Closure' [] roots = roots
-- Closure' (c :: cs) roots = (SingleClosure c roots) ++ (Closure' cs roots)
--
-- Closure : List Arrow → List ℕ → List ℕ
-- Closure arrows roots with (Closure' arrows roots) ⊂ roots
-- ...                     | true = roots
-- ...                     | false = Closure arrows (Closure' arrows roots)
--
--
-- _,_⊢_ : List Arrow → List ℕ → ℕ → Bool
-- _ , [] ⊢ _ = false
-- thms , p :: premises ⊢ conc = true
--

ArrowIntro : ℕ → Arrow → Arrow
ArrowIntro n (ts ⇒ h) = (n :: ts) ⇒ h

ArrowElim : ℕ → Arrow → Arrow
ArrowElim _ ([] ⇒ h) = [] ⇒ h
ArrowElim n ((t :: ts) ⇒ h) with (t == n)
...                            | true  = ArrowElim  n (ts ⇒ h)
...                            | false = ArrowIntro t (ArrowElim n (ts ⇒ h))

Reduce : List Arrow → List ℕ → List Arrow
Reduce cs [] = cs
Reduce cs (n :: ns) with (map (ArrowElim n) cs) ⊂⊂ cs
...                    | true  = cs
...                    | false = Reduce (map (ArrowElim n) cs) (n :: ns)
