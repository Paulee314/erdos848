# Claude (API) on Argon's remaining items — 2026-11-01

Items A–D3: claude-opus-5. Items D4–D5: claude-sonnet-5 (opus-5 returned refusal twice on the follow-up prompt). Nothing here has been applied to the .tex.

# ITEM A — Logical independence / framing

**VERDICT: Agree.**

**Reason.** It has been verified by inspection that the proof of Theorem~\ref{thm:main} invokes only the per-type density bounds and the mod-900 maximization; neither Li's theorem nor Sawhney's is used as a premise. Presenting them as "inputs" is therefore inaccurate and, worse, imports an ineffectivity claim that is false of this paper's own argument (the Section 4 tail bound is elementary: $q^2\le ab+1\le N^2+1$). The honest framing is: Sawhney is the predecessor statement being sharpened (and is implied by the main theorem for any $\eta<1/50$), Li supplies only the exact extremal value $f(N)$ used in the "picture is complete" discussion.

**(i) Replacement for Remark 1.5:**

```latex
\begin{remark}[Ineffectivity]\label{rem:ineff}
No explicit $N_0(\varepsilon)$ is claimed anywhere in this note. The density bounds of
Section~\ref{sec:dens} are stated in an $\varepsilon$--$T$--$N_0$ form in which the truncation
parameter $T=T(\varepsilon)$ and then $N_0$ are chosen but not tracked. This is a matter of
convenience rather than of principle: the tail estimate of Lemma~\ref{lem:tail} is elementary
(it uses only $q^{2}\le ab+1\le N^{2}+1$ for the prime squares $q^{2}$ in question), and the
remaining ingredients are the finite congruence computations of
Sections~\ref{sec:gluing} and~\ref{sec:opt}. An explicit $N_0(\varepsilon)$ could therefore be
extracted by tracking $T(\varepsilon)$, the tail sum over primes $q>T$, and the $O_T(1)$ CRT
error; we do not carry this out. We stress that the proof of Theorem~\ref{thm:main} is logically
independent of \cite{Sawhney}: no estimate of Sawhney's is used, and no ineffectivity is inherited
from it. Li's theorem \cite{Li} is likewise not used in the proof of Theorem~\ref{thm:main}; it is
quoted only for the exact extremal value $f(N)=\lfloor (N+18)/25\rfloor$ inside a single extremal
class, in the surrounding discussion.
\end{remark}
```

**(ii) Replacement for the Section 9 "Summary of logical status" paragraph:**

```latex
\paragraph{Summary of logical status.}
Theorem~\ref{thm:main} depends on: (i) the analytic density bounds of Section~\ref{sec:dens},
proved here from first principles; and (ii) the finite checks (A), each of which is an exhaustive
enumeration over an explicitly bounded search space. It does \emph{not} depend on the formalized
result of Li \cite{Li,LiRepo}, and it does \emph{not} depend on the stability statement of Sawhney
\cite{Sawhney}. Theorem~\ref{thm:li} is quoted only for the exact extremal value
$f(N)=\lfloor (N+18)/25\rfloor$ attained inside a single extremal class, which is what allows the
picture to be described as complete; the audit (C) is reported for readers who wish to rely on that
value, not because Theorem~\ref{thm:main} rests on it. Theorem~\ref{thm:sawhney} is the predecessor
statement that the present work sharpens: Theorem~\ref{thm:main} implies
Theorem~\ref{thm:sawhney} for every fixed $\eta<1/50$ (take $\varepsilon<1/50-\eta$ in
Theorem~\ref{thm:main}), so the admissible $\eta$ is improved from $\approx 0.0023$ to anything
below $1/50=0.02$. Finally, Theorem~\ref{thm:main} does not depend on the numerical range (B),
which is reported as independent corroborating evidence.
```

**(iii) Abstract — two edits.** Replace `in a Lean-formalized proof which we take as an input;` by `in a Lean-formalized proof;` and insert one sentence immediately before `No explicit $N_0$ is claimed.`:

```latex
The argument is self-contained: it uses neither Li's theorem nor Sawhney's, and it implies
Sawhney's stability statement for every fixed $\eta<1/50$; Li's theorem is quoted only for the
exact extremal value $f(N)$ attained inside a single class.
```

**Risk.** The claim of independence must be literally true in the final file: before pasting, grep Sections 3–8 for any appeal to `\cite{Sawhney}` or `\cite{Li}` inside a proof (the "large-prime error terms handled as in Sawhney" phrase in the old remark suggests Section 4 may once have deferred to him — the deferral must now be fully replaced by the corrected Lemma 4.1). Also check the labels `lem:tail`, `sec:gluing`, `sec:dens`, `sec:opt` match the file. A referee may ask why Theorems 1.2/1.3 are stated at all; keeping them is still right (context + the exact value), but the subsection title "Inputs: Li's theorem and Sawhney's stability theorem" should probably become "Context: Li's theorem and Sawhney's stability theorem".

# ITEM B — Human-readable structure of the 64 closed sets

**VERDICT: Agree.**

**Reason.** A 64-element enumeration that a reader cannot reproduce by hand is the weakest point of a computer-assisted maximization; the seven families make the closure lemma checkable in principle, and the arithmetic identity $1+1+12+12+30+6+2=64$ is an immediate consistency check on the computation. The structure is a consequence of compatibility being a *disjunction* of the mod-$4$ and mod-$9$ conditions, which is worth recording explicitly.

**Replacement text (insert immediately after the proof of Lemma 6.1):**

```latex
\begin{remark}[Explicit list of the Galois-closed sets]\label{rem:closedlist}
The $64$ closed sets can be written down by hand, so that the enumeration in
Lemma~\ref{lem:closure} is checkable in principle without a computer. Identify the $36$ signatures
with pairs $(u,v)\in(\Z/4)\times(\Z/9)$ as in Section~\ref{sec:opt}. Compatibility of two
signatures is the \emph{disjunction} of the mod-$4$ and the mod-$9$ condition, so for a single
signature $i=(a,b)$,
\[
 R(i)=\bigl(R_4(a)\times \Z/9\bigr)\ \cup\ \bigl(\Z/4\times R_9(b)\bigr),
\]
where $R_4(a)=\{u:\,4\mid ua+1\}$ and $R_9(b)=\{v:\,9\mid vb+1\}$; these are singletons when $a$ is
odd, resp. $3\nmid b$, and empty otherwise. Intersecting such sets, one finds that the Galois-closed
signature sets are exactly:
\begin{enumerate}
\item the empty set \hfill($1$ set);
\item the full set of all $36$ signatures \hfill($1$);
\item the singletons $\{(u,v)\}$ with $u\in\{1,3\}$ and $v$ a unit mod $9$ \hfill($12$);
\item their duals $R(\{(u,v)\})$, each of size $12$ \hfill($12$);
\item the two-element sets $\{(1,v_1),(3,v_2)\}$ with $v_1\neq v_2$ units mod $9$ \hfill($30$);
\item the sets $(\Z/4)\times\{v\}$, of size $4$, with $v$ a unit mod $9$ \hfill($6$);
\item the sets $\{u\}\times(\Z/9)$, of size $9$, with $u\in\{1,3\}$ \hfill($2$).
\end{enumerate}
Families (1), (2), (5), (6), (7) are preserved by $R$, while $R$ exchanges families (3) and (4).
The total is $1+1+12+12+30+6+2=64$, in agreement with the enumeration.
\end{remark}
```

**Risk.** The remark asserts a structural fact about $R$ (the disjunctive form, hence the shape of $R(i)$) and an identification of signatures with $(\Z/4)\times(\Z/9)$; both must match the definitions actually used in Section 6 — in particular whether signatures range over all of $\Z/4\times\Z/9$ or only over units, and whether "self-dual" is meant setwise or familywise (the text above says "preserved by $R$", i.e. familywise, which is the safe claim: e.g. $R\bigl((\Z/4)\times\{v\}\bigr)=(\Z/4)\times R_9(v)$). If the paper's $R$ has any extra constraint beyond the disjunction, the list must be re-derived before publishing it.

# ITEM C — Title vs scope

**VERDICT: Agree (the current title understates the theorem).**

**Reason.** The theorem's hypothesis is "not contained in a single extremal class", which also covers sets meeting one class plus outside types and sets avoiding both classes entirely; "meeting both extremal classes" names only the extremal configurations. Argon's phrase "outside a single extremal class" is slightly ambiguous (it can be read as "disjoint from"), so I prefer the literal negation.

**Recommended title:**

```latex
\title{A sharp stability threshold for Erd\H{o}s Problem 848:\\
admissible sets not contained in a single extremal class\\
have density at most $1/50$}
```

**Alternative** (shorter, Argon's wording, acceptable if the running head needs to be tight):

```latex
\title{A sharp stability threshold for Erd\H{o}s Problem 848:\\
admissible sets outside a single extremal class\\
have density at most $1/50$}
```

**Risk.** If the preprint has already circulated under the old title (SSRN/arXiv/email), changing it costs citation continuity; in that case add a footnote "an earlier version circulated under the title \dots". Also ensure the sharpness clause in the abstract still makes clear that the extremizers *do* meet both classes, so the stronger title is not read as claiming a different extremal set.

# ITEM D1 — The $127$ clause

**VERDICT: Agree.** The clause as written asserts that $127$ is among the products witnessing $25\mid ab+1$, which is false and is contradicted two lines later; this is a plain editing slip.

**Replacement text (for the sentence beginning "because $7\cdot 7+1=50$ \dots"):**

```latex
because $7\cdot 7+1=50$ and $18\cdot 18+1=325$ are both divisible by $25$, so that $25\mid ab+1$
whenever $a\equiv b\equiv 7\ (25)$ or $a\equiv b\equiv 18\ (25)$. (By contrast $7\cdot 18+1=127$ is
\emph{not} divisible by $25$: the two classes are not glued to each other by $25$. This will
matter.) We call these the two \emph{extremal classes}.
```

**Risk.** None beyond ensuring the following sentence "We call these the two \emph{extremal classes}." is not duplicated (it is included in the replacement above; delete the old copy).

# ITEM D2 — Hand proof of Proposition 2.2

**VERDICT: Agree (add as a remark, keep the computational proof as the proof).**

**Reason.** The hand argument is three lines and makes a key structural fact ($25$ cannot glue across the classes, so $4$ must) visible to the reader; keeping the mod-$100$ computation as the official proof preserves the paper's audit trail. It should be labelled as the cross-class local step, not as a replacement for whatever global content Proposition 2.2 has.

**Replacement text (insert after the proof of Proposition 2.2; substitute the correct label):**

```latex
\begin{remark}[The cross-class check by hand]\label{rem:hand100}
The mod-$100$ computation above is short enough to be done by hand. Let $u\equiv 7\ (25)$ and
$v\equiv 18\ (25)$. Then $uv+1\equiv 7\cdot 18+1=127\equiv 2\ (25)$, so $25\nmid uv+1$, and the only
prime square dividing $100$ that can divide $uv+1$ for all such $u,v$ is $4$. Hence we need
$uv\equiv 3\ (4)$, i.e. $\{u\bmod 4,\ v\bmod 4\}=\{1,3\}$. Modulo $100$ the relevant residues are
$u\in\{7,32,57,82\}$, with $u\equiv 3,0,1,2\ (4)$ respectively, and $v\in\{18,43,68,93\}$, with
$v\equiv 2,3,0,1\ (4)$ respectively. The only pairs with $uv\equiv 3\ (4)$ are therefore
$(u,v)=(7,93)$ and $(u,v)=(57,43)$, which are exactly the pairs underlying $A_1$ and $A_2$.
\end{remark}
```

**Risk.** The remark covers only the *cross-class* half of the statement and only the local (divisibility) direction; if Proposition 2.2 also asserts that no other prime square can serve, or classifies unions of classes to other moduli, the remark must not be read as a full alternative proof — the opening sentence "The mod-$100$ computation above" should be adjusted to name precisely which step it reproduces.

# ITEM D3 — Runner-up display

**VERDICT: Agree (partial): recompute the display from the unrounded constant and add a one-line note; do not merely annotate the wrong digits.**

**Reason.** $828\cdot 0.0142450=11.79486$ but $828\cdot 0.0142449748\ldots=11.794839\ldots$; quoting a product of a rounded input to six significant figures is misleading even though nothing downstream changes. The cleanest fix is to display the correct values and say once that all decimals are rounded.

**Replacement text (adjust the display to the corrected figures and append the note):**

```latex
\[
 828\,J' = 11.794839\ldots,\qquad \text{numerator } 15.403040\ldots
\]
All decimal values quoted in this section are rounded for display; the underlying computation uses
$J'=0.0142449748\ldots$ rather than the rounded $J'=0.0142450$. The discrepancy is confined to the
fifth decimal place and does not affect any of the inequalities used below.
```

**Risk.** I cannot see the surrounding display, so the LaTeX above must be fitted to the actual equation (the quantities being named may differ, and the second number may be a numerator of a specific fraction in the objective). The author must confirm the final sentence — that the rounding does not affect any inequality — by checking the actual margin between the runner-up and the optimum; if that margin is small, state it numerically instead.

# ITEM D4 — "439 pairs" wording

**VERDICT: Agree.** The two counts measure different things (441 ordered pairs with $R(A)\subseteq B$; 439 after deleting the two single-class configurations), and as written the lemma attributes 439 to "the compatibility constraints" alone, which is a verifiable misstatement.

**Replacement text (final sentence of Lemma 6.1):**

```latex
There are exactly $64$ Galois-closed signature sets, and exactly $441$ ordered pairs $(X,X')$ of

---

**ITEM D4.** Verdict: The sentence must separate the raw compatibility count (441) from the count after excluding the two trivial pairs (439), rather than attaching "439" directly to "pairs of them satisfying the compatibility constraints."

```latex
There are exactly $64$ Galois-closed signature sets, and exactly $441$ ordered pairs
of them satisfy the compatibility constraint $R(A)\subseteq B$; excluding the two
trivial pairs $(\emptyset, X_{\mathrm{full}})$ and $(X_{\mathrm{full}}, \emptyset)$,
which correspond to configurations contained in a single extremal class, leaves
$439$ pairs.
```

**ITEM D5.** Verdict: "a two declarations" should simply be "two declarations" (the indefinite article is spurious before a plural noun).

```latex
The repository as published did not compile against the toolchain we used; two declarations were missing the implicit binders they use, which the project's autoImplicit = false setting turns into a build stall;
```