open import Agda.Builtin.Bool
open import Agda.Builtin.List

open import common

module Hierarchy (Γ : Set)(_==_ : Γ → Γ → Bool) where

_∈_ = membership _==_

record Arrow : Set where
  constructor _⇒_
  field
    tails : List Γ
    head  : Γ

domain : List Arrow → List Γ
domain [] = []
domain ((tails ⇒ head) ∷ rs) = head ∷ (tails ++ domain rs)

record Tier : Set where
  constructor _⊃̷_
  field
    low  : List Γ
    high : List Γ

closure : List Γ → List Arrow → List Γ
closure γs rs = ?

completion : Tier → List Arrow → Tier
completion (low ⊃̷ high) rs = clow ⊃̷ filter γs in-upwards-closure
                             where
                               γs = domain rs
                               clow = closure low rs
                               in-upwards-closure : Γ → Bool
                               in-upwards-closure γ = {!   !}
