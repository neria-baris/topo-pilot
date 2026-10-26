import numpy as np
from theory_exact import N, TWO_PI, build, filt, hellinger_matrix, sample, certificate, amp
rng = np.random.default_rng(7)
res = {}
for fam, mode in (("cylinder","O"), ("square","O")):
    T, E, a_of_w = build(fam, mode, 1.25)
    W = sample(T, E, 1000, 32, rng)
    b = filt(T, E, W); D = hellinger_matrix(b)
    th, _ = amp(b, np.arange(N*N)//N, N)
    real = certificate(D, th)
    shuf = [certificate(D, rng.permutation(th)) for _ in range(30)]
    # searched null: best kappa over 30 random circle maps f = angle around a random belief direction pair
    best = []
    for _ in range(30):
        A = rng.normal(size=(N*N, 2)); z = np.sqrt(b) @ A
        r = certificate(D, np.arctan2(z[:,1], z[:,0])); best.append(r[0]/r[1] if np.isfinite(r[1]) else 0)
    res[fam] = dict(real_kappa=real[0]/real[1] if np.isfinite(real[1]) else 0,
                    shuffle_kappa_max=max((s[0]/s[1] if np.isfinite(s[1]) else 0) for s in shuf),
                    random_map_kappa_max=max(best), random_map_kappa_med=float(np.median(best)))
print(res)
