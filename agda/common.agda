open import Agda.Builtin.Bool
open import Agda.Builtin.List


_++_ : {A : Set} → List A → List A → List A
[]       ++ ys = ys
(x ∷ xs) ++ ys = x ∷ (xs ++ ys)

filter : {A : Set} → (A → Bool) → List A → List A
filter f [] = []
filter f (x ∷ xs) with f x
...               | false = filter f xs
...               | true  = x ∷ filter f xs

mkmembership : {A : Set} → (A → A → Bool) → (A → List A → Bool)
mkmembership _==_ a [] = false
mkmembership _==_ a (x ∷ xs) with a == x
...                          | false = mkmembership _==_ a xs
...                          | true  = true

any : {A : Set} → (A → Bool) → List A → Bool
any f [] = false
any f (x ∷ xs) with f x
...            | false = any f xs
...            | true  = true

mkintersects : {A : Set} → (A → A → Bool) → List A → List A → Bool
mkintersects {A} eq xs ys = any is-in-ys xs
                            where
                              is-in-ys : A → Bool
                              is-in-ys x = mkmembership eq x ys
