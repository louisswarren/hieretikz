open import Agda.Builtin.Bool
open import Agda.Builtin.List


_++_ : {A : Set} → List A → List A → List A
[]       ++ ys = ys
(x ∷ xs) ++ ys = x ∷ (xs ++ ys)

filter : {A : Set} → List A → (A → Bool) → List A
filter [] f = []
filter (x ∷ xs) f with f x
...               | false = filter xs f
...               | true  = x ∷ filter xs f

membership : {A : Set} → (_==_ : A → A → Bool) → (A → List A → Bool)
membership _==_ a [] = false
membership _==_ a (x ∷ xs) with a == x
...                        | false = membership _==_ a xs
...                        | true  = true
