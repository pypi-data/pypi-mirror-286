import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from pathlib import Path
import json
import torch
from gpytorch.means import ConstantMean, ZeroMean
from gpytorch.likelihoods import GaussianLikelihood, FixedNoiseGaussianLikelihood
# Import MeLOn
import maingopy.melonpy as melonpy
# If you are not getting MeLOn through MAiNGO, use:
# import melonpy 

def generate_melon_scaler_object(scaler):
        scaler_data = melonpy.ScalerData()
        
        if scaler is None:
            scaler_data = melonpy.SCALER_TYPE.IDENTITY
            scaler_data.parameters = {}
        elif isinstance(scaler, MinMaxScaler):
            scaler_data.type = melonpy.SCALER_TYPE.MINMAX
            
            scaled_bounds = scaler.get_params()['feature_range']
            scaler_data.parameters = {
                melonpy.SCALER_PARAMETER.UPPER_BOUNDS : scaler.data_max_.tolist(),
                melonpy.SCALER_PARAMETER.LOWER_BOUNDS : scaler.data_min_.tolist(),
                melonpy.SCALER_PARAMETER.SCALED_LOWER_BOUNDS : [scaled_bounds[0]]*len(scaler.data_max_.tolist()), 
                melonpy.SCALER_PARAMETER.SCALED_UPPER_BOUNDS : [scaled_bounds[1]]*len(scaler.data_max_.tolist())
            }
        elif isinstance(scaler, StandardScaler):
            scaler_data.type = melonpy.SCALER_TYPE.STANDARD          
            scaler_data.parameters = {
                melonpy.SCALER_PARAMETER.STD_DEV : np.sqrt(scaler.var_).tolist(),
                melonpy.SCALER_PARAMETER.MEAN : scaler.mean_.tolist()
            }
        else:
            raise Exception("Unsupported scaler type. Scaler has to be either a scikit-learn MinMaxScaler or StandardScaler instance or None (=identity(no scaling))")
        
        return scaler_data 

def generate_melon_gp_object(GP_model, GP_likelihood, X, y, matern, scaler):
    gp_data = melonpy.GPData()
    
    gp_data.X = X.numpy()
    gp_data.Y = y.numpy()

    gp_data.nX, gp_data.DX = X.shape

    if len(y.shape) == 1:
        gp_data.DY = 1
    else:
        gp_data.DY = y.shape[1]

    noise = GP_likelihood.noise.detach().numpy()
    cov_mat = GP_model.covar_module(X)

    if isinstance(GP_likelihood, GaussianLikelihood):
        K_numpy = cov_mat.numpy() + noise * np.eye(N=gp_data.nX)
    elif isinstance(GP_likelihood, FixedNoiseGaussianLikelihood):
        K_numpy = cov_mat.numpy() + np.diag(noise)
    else:
        raise Exception(f'Likelihood {type(GP_likelihood)} currently not supported.') 

    gp_data.K = K_numpy
    gp_data.invK = np.linalg.inv(K_numpy)

    gp_data.matern = matern
    kernel_data = melonpy.KernelData()
    kernel_data.sf2 = GP_model.covar_module.outputscale.detach().numpy().astype(float).item()               #outputscale sigma*K
    kernel_data.ell = GP_model.covar_module.base_kernel.lengthscale.detach().numpy().squeeze().tolist()     #lenghtscales kernel
    gp_data.kernelData = kernel_data

    if not 'input' in scaler:
        scaler['input'] = None
    gp_data.inputScalerData = generate_melon_scaler_object(scaler['input'])


    if not 'output' in scaler or not isinstance(scaler['output'], StandardScaler):
        raise Exception('The output scaler has to be as scikit-learn StandardScaler instance')   

    gp_data.predictionScalerData = generate_melon_scaler_object(scaler['output'])

    gp_data.stdOfOutput = np.sqrt(scaler['output'].var_)[0]
    if isinstance(GP_model.mean_module, ConstantMean):
        gp_data.meanFunction = GP_model.mean_module.constant.detach().numpy().tolist()
    elif isinstance(GP_model.mean_module, ZeroMean):
        gp_data.meanFunction = 0
    else: 
        raise Exception(f'GP uses {type(GP_model.mean_module)} as a mean function. Currently only ConstantMean or ZeroMean are supported as mean modules.') 

    return gp_data


def save_model_to_json(filepath, filename, GP_model, GP_likelihood, X, y, matern, scalers=dict()):
    prediction_parameters = dict()
    prediction_parameters["nX"] = X.shape[0]
    prediction_parameters["DX"] = X.shape[1]

    if len(y.shape) == 1:
        prediction_parameters["DY"] = 1
    else:
        prediction_parameters["DY"] = y.shape[1]

    prediction_parameters["matern"] = matern
    
    if isinstance(GP_model.mean_module, ConstantMean):
        prediction_parameters["meanfunction"] = GP_model.mean_module.constant.detach().numpy().tolist()
    elif isinstance(GP_model.mean_module, ZeroMean):
        prediction_parameters["meanfunction"] = 0
    else: 
        raise Exception(f'GP uses {type(GP_model.mean_module)} as a mean function. Currently only ConstantMean or ZeroMean are supported as mean modules.') 

    prediction_parameters["X"] = X.numpy().tolist()
    prediction_parameters["Y"] = y.numpy().tolist()

    noise = GP_likelihood.noise.detach().numpy()

    cov_mat = GP_model.covar_module(X).numpy()

    if isinstance(GP_likelihood, GaussianLikelihood):
        K_numpy = cov_mat.numpy() + noise * np.eye(N=prediction_parameters["nX"])
    elif isinstance(GP_likelihood, FixedNoiseGaussianLikelihood):
        K_numpy = cov_mat.numpy() + np.diag(noise)
    else:
        raise Exception(f'Likelihood {type(GP_likelihood)} currently not supported.') 

    prediction_parameters["K"] = K_numpy.tolist()
    prediction_parameters["invK"] = np.linalg.inv(K_numpy).tolist()

    if not 'input' in scalers or not isinstance(scalers['input'], MinMaxScaler):
        raise Exception("There has to be an inputscaler which is a scikit-learn MinMaxScaler instance")

    prediction_parameters["problemLowerBound"] = scalers['input'].data_min_.tolist()
    prediction_parameters["problemUpperBound"] = scalers['input'].data_max_.tolist()
    
    if not 'output' in scalers or not isinstance(scalers['output'], StandardScaler):
        raise Exception("There has to be an output scaler which is a scikit-learn StandardScaler instance")
    
    prediction_parameters["stdOfOutput"] = np.sqrt(scalers['output'].var_).item()
    prediction_parameters["meanOfOutput"] = scalers['output'].mean_.item()

    prediction_parameters["sf2"] = GP_model.covar_module.outputscale.detach().numpy().astype(float).item()           #outputscale sigma*K
    prediction_parameters["ell"] = GP_model.covar_module.base_kernel.lengthscale.detach().numpy().flatten().tolist()     #lenghtscales kernel

    Path(filepath).mkdir(parents=True, exist_ok=True)
    
    with Path(filepath).joinpath(filename).open('w') as outfile:
        json.dump(prediction_parameters, outfile)
