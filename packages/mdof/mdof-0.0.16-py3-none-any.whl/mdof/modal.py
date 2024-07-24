"""
This module implements functions that extract modal information
from a state space realization or transfer function.
"""
import numpy as np
import scipy.linalg as sl
from numpy import pi
from mdof.validation import OutputEMAC, MPC


def _condeig(a): # TODO: make this match matlab source code for condeig
    """
    vals, vecs, conds = condeig(A) Computes condition numbers for the
    eigenvalues of a matrix. The condition numbers are the reciprocals
    of the cosines of the angles between the left and right eigenvectors.
    Inspired by Arno Onken's Octave code for condeig.

    https://github.com/macd/rogues/blob/master/rogues/utils/condeig.py
    """
    m, n = a.shape
    # eigenvalues, left and right eigenvectors
    lamr, vl, vr = sl.eig(a, left=True, right=True)
    vl = vl.T.conj()
    # Normalize vectors
    for i in range(n):
        vl[i, :] = vl[i, :] / np.sqrt(abs(vl[i, :] ** 2).sum())
    # Condition numbers are reciprocal of the cosines (dot products) of the
    # left eignevectors with the right eigenvectors.
    c = abs(1 / np.diag(np.dot(vl, vr))) 
    return vr, lamr, c

    
def system_modes(realization, dt, **options):
    """
    Modal identification from a state space system realization.

    :param realization:     realization in the form of state space coefficients ``(A,B,C,D)``
    :type realization:      tuple
    :param dt:              timestep.
    :type dt:               float
    :param decimation:      decimation factor. default: 1
    :type decimation:       int, optional
    :param Observability:   Observability matrix; can be reused from :func:`mdof.realize.srim`.
                            default: None
    :type Observability:    array, optional

    :return:                system modes, including natural frequencies, damping ratios, mode shapes,
                            condition numbers, and modal validation metrics EMAC and MPC.
    :rtype:                 dictionary
    """
    decimation = options.get("decimation",
                             1)
    Observability = options.get("Observability",
                                None)
    
    dt = dt*decimation

    A,_,C,_ = realization
    # eigendecomp A
    Psi,Gam,cnd = _condeig(A)  # eigenvectors (Psi) & eigenvalues (Gam) of the matrix A

    # get damping and frequencies from eigendecomp of A
    Lam = (np.log(Gam))/dt
    Omega = np.abs(Lam) # radians per second.
    freq = Omega/(2*pi) # cycles per second (Hz)
    damp = -np.real(Lam)/Omega

    # get modeshapes from C and eigendecomp of A
    modeshape = C@Psi

    # energy condensed output EMAC (extended modal amplitude coherence)
    energy_condensed_emaco = OutputEMAC(A,C,Observability=Observability,Psi=Psi,Gam=Gam,**options)

    # MPC (modal phase collinearity)
    mpc = MPC(A,C,Psi=Psi)

    # for perfect data, the modes of the state space model come in pairs.
    # each pair's corresponding eigenvalues and eigenvectors are complex conjugates.
    # this means that we need to weed out unique roots: 
    # get indices of (1) roots that only show up once, and (2) the first of each pair.
    _, notroots = np.unique(freq.round(decimals=5), return_index=True)
    
    # print(notroots)
    modes = {str(i):
                {'freq': freq[i],  # identified frequency
                'damp': damp[i],   # identified damping ratio
                'modeshape': modeshape[:,i],  # identified modeshape
                'cnd': cnd[i],     # condition number of the eigenvalue
                'energy_condensed_emaco': energy_condensed_emaco[i],  # energy condensed output emac
                'mpc': mpc[i],     # MPC
                }
            for i in range(len(freq)) if i not in notroots # and energy_condensed_emaco[i] > 0.5 and mpc[i] > 0.5
            }

    return modes

    
def spectrum_modes(periods, amplitudes, **options):
    """
    Modal identification from a transfer function.

    :param periods:     transfer function periods
    :type periods:      array
    :param amplitudes:  transfer function amplitudes
    :type amplitudes:   array

    :return:            (fundamental_periods, fundamental_amplitudes)
    :rtype:             tuple
    """
    from scipy.signal import find_peaks
    # height = options.get("height", 0.4)
    # width = options.get("width", 0.2)
    # rel_height = options.get("rel_height", 0.1)
    prominence = options.get("prominence", max(amplitudes)*0.3)
    
    # peaks, _ = find_peaks(amplitudes, height=height, width=width, rel_height=rel_height, prominence=prominence)
    peaks, _ = find_peaks(amplitudes, prominence=prominence)
    fundamental_periods = periods[peaks]
    fundamental_amplitudes = amplitudes[peaks]
    
    return (fundamental_periods, fundamental_amplitudes)
    