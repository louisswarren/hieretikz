open import Agda.Builtin.Bool
open import Agda.Builtin.List
open import Agda.Builtin.Nat renaming (Nat to ℕ)
open import Agda.Builtin.Equality

not : Bool → Bool
not false = true
not true  = false


_++_ : {A : Set} → List A → List A → List A
[]       ++ ys = ys
(x ∷ xs) ++ ys = x ∷ (xs ++ ys)
infixr 4 _++_

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

all : {A : Set} → (A → Bool) → List A → Bool
all f [] = true
all f (x ∷ xs) with f x
...            | false = false
...            | true  = all f xs

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

iter : {A : Set} → (ℕ → A) → ℕ → List A
iter f zero = f zero ∷ []
iter f (suc n) = f (suc n) ∷ iter f n


record Σ (S : Set)(T : S → Set) : Set where
  constructor _,_
  field
    fst : S
    snd : T fst

_×_ : Set → Set → Set
S × T = Σ S (λ _ → T)


data False : Set where
record True : Set where

isTrue : Bool → Set
isTrue false = False
isTrue true  = True

isFalse : Bool → Set
isFalse b = isTrue (not b)

trueIsTrue : ∀{x} → x ≡ true → isTrue x
trueIsTrue refl = _

falseIsFalse : ∀{x} → x ≡ false → isFalse x
falseIsFalse refl = _


--test : ∀ xs → ∀ ys → istrue (all (λ z → mkmembership _==_ z ys) xs) → xs ⊂ ys
--test [] ys pf = empty
--test (x ∷ xs) ys pf = recur {!   !} (test xs ys {!   !})

_∘_ : ∀{k n m}{A : Set k}{B : A → Set n}{C : (x : A) → B x → Set m}
      → (f : {x : A} → (y : B x) → C x y)
      → (g : (x : A) → B x)
      → ((x : A) → C x (g x))
(f ∘ g) x = f (g x)


data Inspect {A : Set}(x : A) : Set where
  _with≡_ : (y : A) → x ≡ y → Inspect x

inspect : {A : Set} → (x : A) → Inspect x
inspect x = x with≡ refl

data All {A : Set}(P : A → Set) : List A → Set where
  []  : All P []
  _∷_ : ∀{x xs} → P x → All P xs → All P (x ∷ xs)

AllTrue : {A : Set} → (A → Bool) → (List A → Set)
AllTrue P = All (isTrue ∘ P)

AllFalse : {A : Set} → (A → Bool) → (List A → Set)
AllFalse P = All (isFalse ∘ P)

data Find {A : Set}(P : A → Bool) : List A → Set where
  missing : ∀{xs}     → AllFalse P xs → Find P xs
  found   : ∀ xs y ys → isTrue (P y)         → Find P (xs ++ y ∷ ys)

find : {A : Set} → (P : A → Bool) → (xs : List A) → Find P xs
find P [] = missing []
find P (x ∷ xs) with inspect (P x)
...             | true  with≡ eq = found [] x xs (trueIsTrue eq)
...             | false with≡ eq with find P xs
...                              | missing pf = missing (falseIsFalse eq ∷ pf)
...                              | found pre y ys pf = found (x ∷ pre) y ys pf


data _⊎_ (A B : Set) : Set where
  inl : A → A ⊎ B
  inr : B → A ⊎ B
