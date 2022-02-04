import sys

sys.path.append("../..")
from barry.config import setup
from barry.fitter import Fitter
from barry.models.bao_power_Beutler2017 import PowerBeutler2017
from barry.datasets.dataset_power_spectrum import PowerSpectrum_SDSS_DR12
from barry.samplers import EnsembleSampler

# Run a quick test using emcee to fit a mock mean.

if __name__ == "__main__":
    pfn, dir_name, file = setup(__file__)

    data = PowerSpectrum_SDSS_DR12(isotropic=True, recon="iso")
    model = PowerBeutler2017(isotropic=data.isotropic, recon=data.recon, marg="full")

    sampler = EnsembleSampler(num_walkers=16, num_steps=5000, num_burn=300, temp_dir=dir_name)

    fitter = Fitter(dir_name)
    fitter.add_model_and_dataset(model, data)
    fitter.set_sampler(sampler)
    fitter.set_num_walkers(1)
    fitter.fit(file)

    if fitter.should_plot():
        from chainconsumer import ChainConsumer

        posterior, weight, chain, evidence, model, data, extra = fitter.load()[0]

        c = ChainConsumer()
        c.add_chain(chain, weights=weight, parameters=model.get_labels())
        c.plotter.plot(filename=pfn + "_contour.pdf")
