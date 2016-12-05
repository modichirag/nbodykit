from mpi4py_test import MPIWorld
from nbodykit.lab import *

@MPIWorld(NTask=[1, 4])
def test_fftpower(comm):
    cosmo = cosmology.default_cosmology.get()

    # debug logging
    setup_logging(logging.DEBUG)

    # zeldovich particles
    source = Source.ZeldovichParticles(comm, cosmo, nbar=3e-4, redshift=0.55, BoxSize=1380., Nmesh=8, rsd='z', seed=42)

    # compute P(k,mu) and multipoles
    alg = algorithms.FFTPower(comm, source, mode='2d', Nmesh=8, poles=[0,2,4])
    edges, pkmu, poles = alg.run()

    # and save
    output = "./test_zeldovich.pickle"
    result = alg.save(output, edges=edges, pkmu=pkmu, poles=poles)


@MPIWorld(NTask=[2, 4], required=[2, 4])
def test_taskmanager(comm):
    # debug logging
    setup_logging(logging.DEBUG)

    # cosmology
    cosmo = cosmology.default_cosmology.get()

    cpus_per_task = 2

    with TaskManager(cpus_per_task, debug=True, comm=comm) as tm:

        for seed in tm.iterate([0, 1, 2]):

            # zeldovich particles
            source = Source.ZeldovichParticles(tm.comm, cosmo, nbar=3e-4, redshift=0.55, BoxSize=1380., Nmesh=8, rsd='z', seed=seed)

            # compute P(k,mu) and multipoles
            alg = algorithms.FFTPower(tm.comm, source, mode='2d', Nmesh=8, poles=[0,2,4])
            edges, pkmu, poles = alg.run()

            # and save
            output = "./test_batch_zeldovich_seed%d.pickle" %seed
            result = alg.save(output, edges=edges, pkmu=pkmu, poles=poles)
