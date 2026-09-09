
# Mathematical Algorithms in SageMath

A collection of four SageMath notebooks containing algorithms and exercises I did during my university studies. The notebooks explore computational algebra, number theory, Fourier transforms, and numerical methods for polynomial roots through implementations, worked examples, and comparisons with SageMath's built-in functions.

The original exercise statements, comments, and most function names are in Polish.

## Notebook overview

| Notebook | Main topics |
| --- | --- |
| [Algebra.ipynb](Algebra.ipynb) | Number theory, polynomial evaluation, modular arithmetic, and determinants |
| [Analiza.ipynb](Analiza.ipynb) | Square-free polynomials, polynomial radicals, and square-free factorization |
| [Fourier.ipynb](Fourier.ipynb) | Discrete and fast Fourier transforms, polynomial multiplication, and timing comparisons |
| [Szacowania.ipynb](Szacowania.ipynb) | Polynomial root bounds, real-root isolation, and numerical approximation |

---

## Algebra.ipynb — Algebra and number theory

Implementations of fundamental algorithms for integers, polynomials, finite fields, and integer matrices.

| Function | Description |
| --- | --- |
| `czy_zaprzyjaznione(n, m)` | Checks whether two numbers satisfy the amicable-number divisor-sum conditions. |
| `Horner(f, a)` | Evaluates a polynomial using Horner's method. |
| `nwd_r(a, b)` | Computes a greatest common divisor using the recursive Euclidean algorithm. |
| `TCR(M, A)` | Solves systems of congruences with pairwise coprime moduli using the Chinese Remainder Theorem. Includes Lagrange-style and iterative Newton-style implementations. |
| `TCR2(m1, m2, a1, a2)` | Combines two congruences as a helper for the iterative CRT implementation. |
| `potega(a, n)` | Computes a nonnegative integer power by repeated squaring. |
| `fi(n)` | Computes Euler's totient function from prime factorization. |
| `potega_mod(a, n, m)` | Explores modular exponentiation using totient-based exponent reduction and repeated squaring. |
| `det_mod(M)` | Computes an integer matrix determinant through finite-field calculations and CRT reconstruction, using a Hadamard-based bound. |

## Analiza.ipynb — Square-free polynomial decomposition

Algorithms for detecting repeated polynomial factors and working with their multiplicities.

| Function | Description |
| --- | --- |
| `czy_bezkwadratowy(f)` | Tests whether a polynomial is square-free by checking the GCD of the polynomial and its derivative. |
| `radykal(f)` | Computes the polynomial radical, removing repeated factors through division by `gcd(f, f.derivative())`. |
| `rozklad_bezkwadratowy(f)` | Implements the Guersenzvaig–Szechtman square-free factorization algorithm and returns factors with their multiplicities. |
| `czy_kwadrat(f)` | Tests whether a polynomial is a square by checking factor multiplicities and its leading coefficient. |

## Fourir.ipynb — Fourier transforms and polynomial multiplication

A progression from a direct discrete Fourier transform calculation to FFT-based polynomial multiplication.

| Function / example | Description |
| --- | --- |
| `pierw_pierw(n, K=CC)` | Constructs a primitive nth root of unity using a trigonometric expression. |
| Direct DFT example | Computes a discrete Fourier transform from its defining sum. |
| `fft(L, omega=0)` | Implements the recursive radix-2 Cooley–Tukey FFT for sequences whose length is a power of two. |
| `nast_pot_2(n)` | Finds the smallest power of two greater than or equal to a positive input. |
| `mnozenie_fft(f, g)` | Multiplies integer-coefficient polynomials using zero-padding, FFTs, pointwise multiplication, and an inverse transform, followed by rounding. |
| `mnozenie_pisemne(f, g)` | Implements schoolbook polynomial multiplication by directly summing coefficient products. |

The final cells compare execution times for schoolbook multiplication, the custom FFT implementation, and SageMath's built-in multiplication on randomly generated degree-5,000 polynomials.

## Szacowania.ipynb — Polynomial root bounds and approximation

Methods for bounding, isolating, and approximating real polynomial roots.

### Root bounds and polynomial transformations

- `Cauchy_1(f)` and `Cauchy_2(f)`: two coefficient-based bounds on the absolute values of polynomial roots.
- `depress(f)`: normalizes and shifts a polynomial to eliminate its next-to-leading coefficient.
- `Hong(f)`: implements Hong's upper-bound formula for real roots.
- `local_max(f)`: implements the local-max root-bound algorithm attributed to Vikglas in the exercises.
- `Laguerre_Samuelson(f)`: computes the interval endpoints from the Laguerre–Samuelson formula, followed by a plotting example.

### Real-root isolation

- `zmiany_znaku(L)`: counts sign changes in a sequence, ignoring zeros.
- `Alesina_Galuzzi(f, ab)`: isolates positive roots using interval transformations, coefficient sign changes, and recursive subdivision.
- A second version of `Alesina_Galuzzi` refines the intervals to exclude roots of the first and second derivatives.
- Examples also isolate negative roots by applying the algorithm to `f(-x)` and reflecting the resulting intervals.

### Numerical root approximation

- `bisekcja(f, ab, epsilon)`: approximates a root by interval bisection.
- `__QIR_4` and `__QIR_N`: helper procedures for Quadratic Interval Refinement.
- `QIR(f, ab, epsilon)`: refines a sign-changing interval using secant-based predictions and adaptive subdivision.
- `pierwiastki_rzeczywiste(f, epsilon)`: combines square-free factorization, root isolation, and QIR to approximate real roots and associate them with their multiplicities.

---

## Running the notebooks

Open the `.ipynb` files in Jupyter with a **SageMath kernel**. They use Sage-specific syntax and mathematical objects.

Execute the relevant setup and function-definition cells before running the examples. `TCR` and `Alesina_Galuzzi` each have two definitions. Executing the later definition replaces the earlier version in the active kernel.

These notebooks preserve coursework implementations and example checks. They are intended for studying the algorithms; input assumptions and edge cases should be checked before reusing them as general-purpose routines.
