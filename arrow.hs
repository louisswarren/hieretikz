import Data.Bool
import Data.List


data Arrow = Assertion String | Implication String Arrow


closure :: [Arrow] -> [String] -> [String]
closure []                         found = found
closure ((Assertion n) : rest)     found = n : (closure rest (n : found))
closure ((Implication n q) : rest) found =
    if ((elem n found) || (elem n (closure rest found))) then
        (closure (q : rest) found)
    else (closure rest found)

isDerivable :: [Arrow] -> [String] -> String -> Bool
isDerivable axioms premises conclusion = elem conclusion (closure axioms premises)

entails :: [Arrow] -> Arrow -> Bool
entails axioms (Assertion n)     = elem n (closure axioms [])
entails axioms (Implication n q) = entails ((Assertion n) : axioms) q


proofs :: [Arrow]
proofs = [
   (Implication "3" (Assertion "4")),
--   (5 ⇒ (⇒ 4)) ∷
   (Implication "6" (Assertion "4")),
   (Implication "3" (Assertion "3")),
   (Implication "3" (Assertion "3")),
   (Implication "9" (Assertion "3")),
   (Implication "9" (Assertion "3")),
   (Implication "5" (Assertion "7")),
   (Implication "9" (Assertion "7")),
   (Implication "6" (Assertion "8")),
   (Implication "10" (Assertion "8")),
   (Implication "10" (Assertion "7")),
   (Implication "5" (Assertion "10")),
   (Implication "10" (Assertion "4")),
   (Implication "5" (Assertion "11")),
   (Implication "6" (Assertion "11")),
   (Implication "11" (Assertion "4")),
   (Implication "10" (Assertion "7")),
   (Implication "8" (Assertion "4")),
   (Implication "9" (Assertion "7")),
   (Implication "9" (Assertion "8")),
   (Implication "3" (Assertion "8")),
   (Implication "5" (Implication "3" (Assertion "9"))),
   (Implication "6" (Implication "7" (Assertion "10"))),
   (Implication "6" (Implication "3" (Assertion "3"))),
   (Implication "7" (Assertion "7")),
   (Implication "7" (Assertion "7")),
   (Implication "7" (Implication "8" (Assertion "10"))),
   (Implication "3" (Implication "10" (Assertion "9"))),
   (Implication "5" (Assertion "1")),
   (Implication "3" (Implication "1" (Assertion "9"))),
   (Implication "1" (Assertion "2")),
   (Implication "10" (Assertion "2"))]

cl = closure proofs ["5"]

main = putStrLn (show cl)
