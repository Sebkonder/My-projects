"""
LPA (Larva-Adult) population model: flip bifurcation and its criticality.

This module studies a discrete-time stage-structured population model and
determines, for given parameters, whether its period-doubling (flip)
bifurcation is supercritical or subcritical.

Pipeline:
  - F                  : the model map (state -> next state)
  - find_fixed_point   : the non-trivial equilibrium (L*, A*)
  - jacobian           : linearisation at the fixed point (stability)
  - find_flip_b        : the reproduction rate b at which an eigenvalue hits -1
                         (the flip / period-doubling bifurcation)
  - kuznetsov_c        : the first Lyapunov coefficient c via normal-form
                         (B_form / C_form) reduction. c > 0 => supercritical
                         (a stable 2-cycle is born); c < 0 => subcritical.
                         The numerical value is cross-checked against a
                         closed-form analytical expression (c_anal).
  - bifurcation_diagram: long-term behaviour of L and A as b varies.

Requires: numpy, scipy, matplotlib
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq

def F(state, b, cal, mul, mua):
  L, A = state
  return np.array([b*A, L*(1-mul)*np.exp(-cal*A) + A*(1-mua)])

def find_fixed_point(b, cal, mul, mua):
    if b is None or mua == 0:
        return None
    b1 = b * (1 - mul)/mua
    if b1 <= 1.0:
        return None
    A_star = 1/cal * np.log(b1)
    L_star = b * A_star
    return np.array([L_star, A_star])

def jacobian(L, A, cal, mul, mua):
    gamma = cal * A
    rho = L / A
    return np.array([[0, rho],
                     [mua / rho, 1 - mua - gamma * mua]])

def analytical_derivs(L, A, cal, mul, mua):
    rho = L / A
    gamma = cal * A
    D2 = np.zeros((2, 2, 2))
    D2[1,0,1] = D2[1,1,0] = -gamma*mua/L
    D2[1,1,1] = gamma**2 * mua / A
    D3 = np.zeros((2, 2, 2, 2))
    D3[1,0,1,1] = D3[1,1,0,1] = D3[1,1,1,0] = (gamma**2 * mua)/(L*A)
    D3[1,1,1,1] = -gamma**3 * mua/A**2
    return D2, D3

def analytical_eigenvals(rho, mua):
  return (np.array([-mua/rho, 1.0]), np.array([-rho, 1.0]))

def B_form(D2, x, y):
    B = np.zeros(2)
    for i in [0,1]:
      for j in [0,1]:
        for k in [0,1]:
          B[i] += D2[i,j,k] * x[j] * y[k]
    return B

def C_form(D3, x, y, z):
    C = np.zeros(2)
    for i in [0,1]:
      for j in [0,1]:
        for k in [0,1]:
          for l in [0,1]:
            C[i] += D3[i,j,k,l] * x[j] * y[k] * z[l]
    return C

def kuznetsov_c(b, cal, mul, mua, verbose=False):
    if b is None:
        return None
    fp = find_fixed_point(b, cal, mul, mua)
    if fp is None: return None
    L, A = fp
    gamma, rho = cal * A, L / A
    J = jacobian(L, A, cal, mul, mua)
    eigs = sorted(np.linalg.eigvals(J), key=lambda x: x.real)
    p, q = analytical_eigenvals(rho, mua)
    p = p / np.dot(p, q)
    D2, D3 = analytical_derivs(L, A, cal, mul, mua)
    Bqq = B_form(D2, q, q)
    Cqqq = C_form(D3, q, q, q)
    h = np.linalg.solve(J - np.eye(2), Bqq)
    Bqh = B_form(D2, q, h)
    c = np.dot(p, Cqqq) / 6.0 - np.dot(p, Bqh) / 2.0
    c_anal = (gamma**2*(2*gamma + 3))/(3*A**2*(gamma + 4))
    if verbose:
        print(f"  (L*, A*) = ({L:.4f}, {A:.4f}) | c = {c:.8f} "
              f"({'SUPERCRITICAL' if c > 0 else 'SUBCRITICAL'}) | c_anal = {c_anal:.8f}")
    return {'c': c, 'L_star': L, 'A_star': A, 'eigenvalues': eigs}

def find_flip_b(cal, mul, mua):
    bt = mua / (1 - mul)
    def objective(bv):
        fp = find_fixed_point(bv, cal, mul, mua)
        if fp is None: return 1.0
        return np.min(np.linalg.eigvals(jacobian(*fp, cal, mul, mua)).real) + 1.0
    bs = np.linspace(bt*1.01, bt+2000, 1000)
    vals = [objective(bv) for bv in bs]
    for i in range(len(vals)-1):
        if vals[i]*vals[i+1] < 0: return brentq(objective, bs[i], bs[i+1])
    return None

def bifurcation_diagram(cal, mul, mua, b_flip=None):
    bt = mua / (1 - mul)
    bf = b_flip or find_flip_b(cal, mul, mua)
    bmax = (bf or bt * 10) * 2

    bs = np.linspace(0, bmax, 1000)
    bp, Lp, Ap = [], [], []

    for bv in bs:
        fp = find_fixed_point(bv, cal, mul, mua)
        st = np.abs(fp * (1 + 0.02 * np.random.randn(2))) if fp is not None else np.array([.5, .5])
        ok = True
        for _ in range(700):
            st = F(st, bv, cal, mul, mua)
            if np.any(np.isnan(st)) or np.any(st > 1e8) or np.any(st < 0):
                ok = False
                break
        if not ok:
          continue
        for _ in range(300):
            st = F(st, bv, cal, mul, mua)
            if np.any(np.isnan(st)) or np.any(st > 1e8) or np.any(st < 0):
              break
            bp.append(bv); Lp.append(st[0]); Ap.append(st[1])

    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    ax[0].scatter(bp, Lp, s=.08, c='royalblue', alpha=.25)
    ax[0].set_ylabel('$L_t$')
    ax[0].set_title(f'$c_{{la}}={cal},\\ \\mu_l={mul},\\ \\mu_a={mua}$')
    ax[1].scatter(bp, Ap, s=.08, c='darkorange', alpha=.25)
    ax[1].set_ylabel('$A_t$'); ax[1].set_xlabel('$b$')
    for a in ax:
        if bf:
          a.axvline(bf, c='red', ls='--', alpha=.7, label=f'Flip $b={bf:.2f}$')
        a.axvline(bt, c='green', ls='--', alpha=.7, label=f'Transcritical $b={bt:.2f}$')
    ax[0].legend()
    plt.tight_layout()
    plt.show()
    plt.close()

sets = [(0.4, 0.9, 0.7), (0.26, 0.2, 0.5), (0.1, 0.1, 0.2)]

if __name__ == "__main__":
    for i, (cal, mul, mua) in enumerate(sets):
        bf = find_flip_b(cal, mul, mua)
        print(f"Set {i+1}: cal={cal}, mul={mul}, mua={mua} | b_flip={bf}")
        if bf:
            kuznetsov_c(bf, cal, mul, mua, verbose=True)
        else:
            print("  No flip bifurcation found in range.")
        bifurcation_diagram(cal, mul, mua, bf)
