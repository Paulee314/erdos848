-- Our own final check of Li's #848 formalization (written 30 Oct 2026; run only after the full lake build ends with full_exit=0).
-- Compile from repo/lean4 with the project's built libraries on LEAN_PATH (see run_final_v1.sh). Nothing of Li's is run.
import Erdos848.PaperGeneratedCertificateProvider

-- 1. Which axioms the final theorem depends on. Accept only: propext, Classical.choice, Quot.sound.
#print axioms Erdos848.PaperGeneratedCertificateProvider.all_N

-- 2. The theorem's type, and the definitions it is stated with, printed for a human read.
#check @Erdos848.PaperGeneratedCertificateProvider.all_N
#print Erdos848.OriginalProblem848Statement
#print Erdos848.NonSquarefreeProductProp

-- 3. Our own transcription of Erdős #848 as stated on erdosproblems.com ("ab+1 is never squarefree (for all a,b ∈ A)",
--    a = b included; extremal set n ≡ 7 (mod 25)), written with Mathlib's `Squarefree` only. If this compiles, Li's theorem
--    proves exactly this statement for every N.
theorem erdos848_our_statement :
    ∀ N : ℕ, ∀ A : Finset ℕ, A ⊆ Finset.Icc 1 N →
      (∀ a ∈ A, ∀ b ∈ A, ¬ Squarefree (a * b + 1)) →
      A.card ≤ ((Finset.Icc 1 N).filter fun n => n % 25 = 7).card :=
  Erdos848.PaperGeneratedCertificateProvider.all_N

#print axioms erdos848_our_statement
