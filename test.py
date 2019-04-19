import gpuPhenomHM
import numpy as np
import numpy.testing as npt
from astropy.cosmology import Planck15 as cosmo
from scipy import constants as ct
import time
import pdb

def test():
    df = 1e-4
    freq, phiRef, f_ref, m1, m2, chi1z, chi2z, distance, deltaF, inclination = np.logspace(-5, -1, 1024), 0.0, 1e-5, 1e6, 5e6, 0.8, 0.8, cosmo.luminosity_distance(3.0).value*1e6*ct.parsec, -1.0, np.pi/3.

    l_vals = np.array([2, 2, 3, 4, 4, 3], dtype=np.uint32) #
    m_vals = np.array([2, 1, 3, 4, 3, 2], dtype=np.uint32) #, 

    df = 1e-8
    interp_freq = np.arange(1e-5, 1e-1 + df, df)

    to_gpu=0
    to_interp = 0
    cpu_phenomHM = gpuPhenomHM.GPUPhenomHM(len(freq),
     l_vals,
     m_vals,
     to_gpu, to_interp)

    #cpu_phenomHM.add_interp(interp_freq, len(interp_freq))
    for i in range(1):
        st = time.perf_counter()
        cpu_phenomHM.cpu_gen_PhenomHM(freq, m1,  # solar masses
                     m2,  # solar masses
                     chi1z,
                     chi2z,
                     distance,
                     inclination,
                     phiRef,
                     deltaF,
                     f_ref)

    cpu_amp, cpu_phase = cpu_phenomHM.Get_Waveform()

    #amp = np.abs(cpu_amp).flatten()
    #phase = np.unwrap(np.arctan2(cpu_amp.real, cpu_amp.imag)).flatten()
    #cpu_phenomHM.interp_wave(amp, phase)
    print('cpu', time.perf_counter() - st)
    #print(np.sum(np.real(cpu_amp.conj()*cpu_amp)))

    #for i in range(4):
    #    st = time.perf_counter()
    #    spline = np.interp(interp_freq, freq, amp[:len(freq)])
    #    print('scipy', time.perf_counter() - st)


    to_gpu=1
    to_interp = 1
    gpu_phenomHM = gpuPhenomHM.GPUPhenomHM(len(freq),
     l_vals,
     m_vals,
     to_gpu, to_interp)

    #for _ in range(5):
    for i in range(1):
        st = time.perf_counter()
        gpu_phenomHM.gpu_gen_PhenomHM(freq, m1,  # solar masses
                     m2,  # solar masses
                     chi1z,
                     chi2z,
                     distance,
                     inclination,
                     phiRef,
                     deltaF,
                     f_ref)
        #check = gpu_phenomHM.Likelihood()
        print('gpu', time.perf_counter() - st)#, 'like', check)
    #import pdb; pdb.set_trace()
    #gpu_amp, gpu_phase = gpu_phenomHM.gpu_Get_Waveform()
    #assert(np.allclose(cpu_amp, gpu_amp))
    #assert(np.allclose(cpu_phase, gpu_phase))
    #print('CPU MATCHES GPU!!!!')

    gpu_phenomHM.add_interp(int(1e7))
    for i in range(10):
        st = time.perf_counter()
        gpu_phenomHM.gpu_gen_PhenomHM(freq, m1,  # solar masses
                     m2,  # solar masses
                     chi1z,
                     chi2z,
                     distance,
                     inclination,
                     phiRef,
                     deltaF,
                     f_ref)
        gpu_phenomHM.interp_wave(1e-5, 1e-8, int(1e6))
        print('gpu', time.perf_counter() - st)
    gpu_amp, gpu_phase = gpu_phenomHM.gpu_Get_Waveform()
    #pdb.set_trace()

if __name__ == "__main__":
    test()
