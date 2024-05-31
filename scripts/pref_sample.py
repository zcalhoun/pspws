"""
This script conducts the analysis for the preferential sampling adjustment and
saves the results to a new file.
"""

import argparse
import numpy as np
import geopandas as gpd
from libpysal.weights import Rook
import pymc as pm


def main(args):

    # Load the data
    data = gpd.read_file(args.data)

    # Create the adjacency matrix
    adj = Rook.from_dataframe(data).to_sparse().todense()

    # Get the temperature data and create a masked array
    temp = data['tempAvg'].values
    temp = np.ma.array(temp, mask=np.isnan(temp))

    counts = data['num_statio'].values
    population = data['population'].values / 1000

    init_val = (temp - temp.mean()) / temp.std()
    init_val = init_val.filled(0)

    coords = {
        "tract": data.index.values
    }

    # Run ICAR model
    print("fitting model 1")
    with pm.Model(coords=coords) as m1:
        sigma = pm.InverseGamma('sigma', 0.001, 0.001)
        eps = pm.InverseGamma('eps', mu=0.1, sigma=0.1, dims="tract")
        mu = pm.Normal('mu', mu = temp.mean() , sigma = 2)
        phi = pm.ICAR('phi', W=adj, initval=init_val)

        # Likelihood
        T = pm.Normal('temp', mu + np.sqrt(sigma)*phi, sigma = np.sqrt(eps), observed=temp)

        # Sample
        trace_1 = pm.sample(1000, chains=1, random_seed=42)

    with m1:
        ppc = pm.sample_posterior_predictive(trace_1, var_names=['temp'])
    
    data['m1_temp'] = ppc.posterior_predictive['temp'].mean(axis=(0,1)).values
    data['m1_temp_std'] = ppc.posterior_predictive['temp'].std(axis=(0,1)).values

    # Run ICAR+PS model
    print('fitting model 2')
    with pm.Model(coords=coords) as m2:
        # Priors
        sigma = pm.InverseGamma('sigma', 0.001, 0.001, initval=1)
        eps = pm.InverseGamma('eps', mu=0.1, sigma=0.1, dims=("tract",))
        mu = pm.Normal('mu', mu = temp.mean(), sigma = 2)
        phi = pm.ICAR('phi', W=adj, initval=init_val)
        theta_0 = pm.Normal('theta_0', mu = -1, sigma = 1)
        theta_1 = pm.Normal('theta_1', mu=-1, sigma= 1)

        # Likelihood
        T_est = mu + np.sqrt(sigma) * phi
        T = pm.Normal('temp', T_est, sigma = np.sqrt(eps), observed=temp, dims="tract")
        intensity = pm.math.exp(theta_0 + theta_1*phi)
        rates = intensity * population
        lam = pm.Poisson('lam', mu = rates, observed=counts)

        # Sample
        trace_2 = pm.sample(1000, tune=1000, chains=1, random_seed=42)#, target_accept=0.9)


    with m2:
        ppc = pm.sample_posterior_predictive(trace_2, var_names=['temp'])
    
    data['m2_temp'] = ppc.posterior_predictive['temp'].mean(axis=(0,1)).values
    data['m2_temp_std'] = ppc.posterior_predictive['temp'].std(axis=(0,1)).values

    # Save the file to the output directory
    print("saving file")
    data.to_file(args.output)


if __name__ == "__main__":
    # Create the argparser
    parser = argparse.ArgumentParser(description="Preferential Sampling Adjustment Script")

    # Arguments
    parser.add_argument("--data", type=str, help="Path to the data file")

    # output file
    parser.add_argument("--output", type=str, help="Path to the output file")

    # Parse the arguments
    args = parser.parse_args()

    # Run the main function
    main(args)
