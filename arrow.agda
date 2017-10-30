open import Data.Bool.Base using (Bool)
------------------------------------------------------------------------
-- The Agda standard library
--
-- IO
------------------------------------------------------------------------

open import Coinduction
open import Data.Unit
open import Data.String
open import Data.Colist
open import Function
import IO.Primitive as Prim
open import Level

------------------------------------------------------------------------
-- The IO monad

-- One cannot write "infinitely large" computations with the
-- postulated IO monad in IO.Primitive without turning off the
-- termination checker (or going via the FFI, or perhaps abusing
-- something else). The following coinductive deep embedding is
-- introduced to avoid this problem. Possible non-termination is
-- isolated to the run function below.

infixl 1 _>>=_ _>>_

data IO {a} (A : Set a) : Set (suc a) where
  lift   : (m : Prim.IO A) → IO A
  return : (x : A) → IO A
  _>>=_  : {B : Set a} (m : ∞ (IO B)) (f : (x : B) → ∞ (IO A)) → IO A
  _>>_   : {B : Set a} (m₁ : ∞ (IO B)) (m₂ : ∞ (IO A)) → IO A

{-# NON_TERMINATING #-}

run : ∀ {a} {A : Set a} → IO A → Prim.IO A
run (lift m)   = m
run (return x) = Prim.return x
run (m  >>= f) = Prim._>>=_ (run (♭ m )) λ x → run (♭ (f x))
run (m₁ >> m₂) = Prim._>>=_ (run (♭ m₁)) λ _ → run (♭ m₂)

putStr∞ : Costring → IO ⊤
putStr∞ s =
  ♯ lift (Prim.putStr s) >>
  ♯ return _

putStr : String → IO ⊤
putStr s = putStr∞ (toCostring s)

putStrLn∞ : Costring → IO ⊤
putStrLn∞ s =
  ♯ lift (Prim.putStrLn s) >>
  ♯ return _

putStrLn : String → IO ⊤
putStrLn s = putStrLn∞ (toCostring s)

_∨_ : Bool → Bool → Bool
Bool.true ∨ _  = Bool.true
Bool.false ∨ b = b


_∧_ : Bool → Bool → Bool
Bool.false ∧ _ = Bool.false
Bool.true ∧ b  = b


if_then_else_ : {A : Set} → Bool → A → A → A
if Bool.true  then a else _ = a
if Bool.false then _ else b = b


----------------------------------------

_>>>_ : String → String → String
_>>>_ = primStringAppend

infixl 1 _>>>_



----------------------------------------

data Principle : Set where
  # : String → Principle


_=p=_ : Principle → Principle → Bool
(# a) =p= (# b) = a == b

----------------------------------------

data List (A : Set) : Set where
  []  : List A
  _∷_ : A → List A → List A
infixr 5 _∷_


[[_]] : {A : Set} → A → List A
[[ x ]] = x ∷ []


any : {A : Set} → (A → Bool) → List A → Bool
any _ []       = Bool.false
any f (x ∷ xs) = (f x) ∨ (any f xs)


_∈∈_ : Principle → List Principle → Bool
x ∈∈ []       = Bool.false
x ∈∈ (y ∷ ys) with x =p= y
...             | Bool.true  = Bool.true
...             | Bool.false = x ∈∈ ys


_∋∋_ : List Principle → Principle → Bool
xs ∋∋ y = y ∈∈ xs



----------------------------------------


data Arrow : Set where
  ⇒_  : Principle → Arrow
  _⇒_ : Principle → Arrow → Arrow


_≡≡_ : Arrow → Arrow → Bool
(⇒ q) ≡≡ (⇒ s)     = q =p= s
(p ⇒ q) ≡≡ (r ⇒ s) = (p =p= r) ∧ (q ≡≡ s)
_ ≡≡ _             = Bool.false


_∈∈∈∈_ : Arrow → List Arrow → Bool
x ∈∈∈∈ []       = Bool.false
x ∈∈∈∈ (y ∷ ys) with x ≡≡ y
...              | Bool.true  = Bool.true
...              | Bool.false = x ∈∈∈∈ ys


closure : List Arrow → List Principle → List Principle
closure [] found               = found
closure ((⇒ n) ∷ rest) found   = n ∷ (closure rest (n ∷ found))
closure ((n ⇒ q) ∷ rest) found with (n ∈∈ found) ∨ (n ∈∈ (closure rest found))
...                               | Bool.true  = closure (q ∷ rest) found
...                               | Bool.false = closure rest found


_,_⊢_ : List Arrow → List Principle → Principle → Bool
cs , ps ⊢ q = q ∈∈ (closure cs ps)


_⊢_ : List Arrow → Arrow → Bool
cs ⊢ (⇒ q)   = q ∈∈ (closure cs [])
cs ⊢ (p ⇒ q) = ((⇒ p) ∷ cs) ⊢ q



----------------------------------------



data Separation : Set where
  model : List Principle → List Principle → Separation


modelsupports : Separation → List Arrow → Principle → Bool
modelsupports (model holds _) cs n = cs , holds ⊢ n


modeldenies : Separation → List Arrow → Principle → Bool
modeldenies (model _ fails) cs n = any (_∋∋_ (closure cs ([[ n ]]))) fails


_⟪!_⟫_ : List Arrow → Separation → Arrow → Bool
cs ⟪! m ⟫ (⇒ q) = modeldenies m cs q
cs ⟪! m ⟫ (p ⇒ q) = (modelsupports m cs p) ∧ (cs ⟪! m ⟫ q)


_⟪_⟫_ : List Arrow → List Separation → Arrow → Bool
cs ⟪ [] ⟫ arr     = Bool.false
cs ⟪ m ∷ ms ⟫ arr = (cs ⟪! m ⟫ arr) ∨ (cs ⟪ ms ⟫ arr)



----------------------------------------



data Relation : Set where
  Proved    : Relation
  Derivable : Relation
  Separated : Relation
  Unknown   : Relation


consider : List Arrow → List Separation → Arrow → Relation
consider cs ms arr with (arr ∈∈∈∈ cs)
...                   | Bool.true  = Proved
...                   | Bool.false with (cs ⊢ arr)
...                              | Bool.true  = Derivable
...                              | Bool.false with (cs ⟪ ms ⟫ arr)
...                                         | Bool.true  = Separated
...                                         | Bool.false = Unknown


proofs : List Arrow
proofs =
   ((# "3") ⇒ (⇒ (# "4"))) ∷
--   ((# "5") ⇒ (⇒ (# "4"))) ∷
   ((# "6") ⇒ (⇒ (# "4"))) ∷
   ((# "3") ⇒ (⇒ (# "3"))) ∷
   ((# "3") ⇒ (⇒ (# "3"))) ∷
   ((# "9") ⇒ (⇒ (# "3"))) ∷
   ((# "9") ⇒ (⇒ (# "3"))) ∷
   ((# "5") ⇒ (⇒ (# "7"))) ∷
   ((# "9") ⇒ (⇒ (# "7"))) ∷
   ((# "6") ⇒ (⇒ (# "8"))) ∷
   ((# "10") ⇒ (⇒ (# "8"))) ∷
   ((# "10") ⇒ (⇒ (# "7"))) ∷
   ((# "5") ⇒ (⇒ (# "10"))) ∷
   ((# "10") ⇒ (⇒ (# "4"))) ∷
   ((# "5") ⇒ (⇒ (# "11"))) ∷
   ((# "6") ⇒ (⇒ (# "11"))) ∷
   ((# "11") ⇒ (⇒ (# "4"))) ∷
   ((# "10") ⇒ (⇒ (# "7"))) ∷
   ((# "8") ⇒ (⇒ (# "4"))) ∷
   ((# "9") ⇒ (⇒ (# "7"))) ∷
   ((# "9") ⇒ (⇒ (# "8"))) ∷
   ((# "3") ⇒ (⇒ (# "8"))) ∷
   ((# "5") ⇒ ((# "3") ⇒ (⇒ (# "9")))) ∷
   ((# "6") ⇒ ((# "7") ⇒ (⇒ (# "10")))) ∷
   ((# "6") ⇒ ((# "3") ⇒ (⇒ (# "3")))) ∷
   ((# "7") ⇒ (⇒ (# "7"))) ∷
   ((# "7") ⇒ (⇒ (# "7"))) ∷
   ((# "7") ⇒ ((# "8") ⇒ (⇒ (# "10")))) ∷
   ((# "3") ⇒ ((# "10") ⇒ (⇒ (# "9")))) ∷
   ((# "5") ⇒ (⇒ (# "1"))) ∷
   ((# "3") ⇒ ((# "1") ⇒ (⇒ (# "9")))) ∷
   ((# "1") ⇒ (⇒ (# "2"))) ∷
   ((# "10") ⇒ (⇒ (# "2"))) ∷ []

cms : List Separation
cms =
  (model ((# "12") ∷ (# "6") ∷ (# "11") ∷ (# "4") ∷ (# "1") ∷ []) ((# "5") ∷ (# "3") ∷ (# "7") ∷ (# "7") ∷ [])) ∷
  (model ((# "6") ∷ (# "3") ∷ (# "11") ∷ (# "4") ∷ (# "7") ∷ (# "8") ∷ (# "3") ∷ (# "9") ∷ (# "10") ∷ (# "1") ∷ []) ((# "5") ∷ [])) ∷
  (model ((# "12") ∷ (# "5") ∷ (# "11") ∷ (# "4") ∷ (# "1") ∷ []) ((# "6") ∷ (# "3") ∷ [])) ∷
  (model ((# "5") ∷ (# "3") ∷ (# "11") ∷ (# "4") ∷ (# "7") ∷ (# "8") ∷ (# "3") ∷ (# "9") ∷ (# "10") ∷ (# "1") ∷ []) ((# "6") ∷ [])) ∷
  (model ((# "12") ∷ (# "4") ∷ (# "11") ∷ []) ((# "5") ∷ (# "6") ∷ (# "3") ∷ (# "8") ∷ (# "9") ∷ (# "1") ∷ [])) ∷
  (model ((# "12") ∷ (# "5") ∷ (# "6") ∷ (# "4") ∷ (# "11") ∷ (# "1") ∷ []) ((# "3") ∷ [])) ∷
  (model ((# "12") ∷ (# "4") ∷ (# "11") ∷ (# "7") ∷ []) ((# "9") ∷ (# "5") ∷ (# "6") ∷ (# "10") ∷ (# "8") ∷ (# "1") ∷ [])) ∷
  (model ((# "10") ∷ (# "9") ∷ []) ((# "1") ∷ [])) ∷
  (model ((# "3") ∷ (# "4") ∷ (# "11") ∷ []) ((# "9") ∷ (# "5") ∷ (# "6") ∷ (# "10") ∷ (# "7") ∷ (# "1") ∷ [])) ∷
  (model ((# "12") ∷ (# "7") ∷ (# "1") ∷ []) ((# "4") ∷ (# "11") ∷ (# "8") ∷ [])) ∷
  (model ((# "9") ∷ (# "3") ∷ (# "10") ∷ (# "8") ∷ (# "1") ∷ []) ((# "11") ∷ [])) ∷
  (model ((# "12") ∷ (# "4") ∷ (# "10") ∷ (# "1") ∷ []) ((# "11") ∷ (# "3") ∷ [])) ∷
  (model ((# "3") ∷ (# "6") ∷ (# "5") ∷ []) ([])) ∷
  (model ((# "1") ∷ (# "2") ∷ (# "3") ∷ (# "4") ∷ (# "5") ∷ (# "6") ∷ (# "7") ∷ (# "8") ∷ (# "9") ∷ (# "10") ∷ (# "11") ∷ []) ((# "12") ∷ [])) ∷ []

testp : Relation
testp = consider proofs cms ((# "5") ⇒ (⇒ (# "10")))

testd : Relation
testd = consider proofs cms ((# "5") ⇒ (⇒ (# "4")))

tests : Relation
tests = consider proofs cms ((# "5") ⇒ (⇒ (# "3")))

testu : Relation
testu = consider proofs cms ((# "6") ⇒ (⇒ (# "1")))

testcl : List Principle
testcl = closure proofs ((# "5") ∷ [])



stringifylp : List Principle → String
stringifylp [] = "[]"
stringifylp ((# s) ∷ xs) = s >>> " ∷ " >>> (stringifylp xs)


main = run (putStrLn (stringifylp testcl))
