import pandas as pd
import numpy as np
import statsmodels.api as sm
from statsmodels.tools.numdiff import approx_fprime
from statsmodels.tools.numdiff import approx_fprime_cs
from scipy.stats import norm
from decimal import Decimal

class delta_method:
    
    def __init__(self,beta=None,g=None,vcov=None,sm_results=None,complex_step=True,epsilon=None,level=0.95,g_args=(),g_kwargs={},centered=False):

        '''Initializes an instance of the delta_method.
        
        Args:
            beta:           (float or numpy.ndarray) point estimate(s). Default: None.
            g:              (function) function of estimated parameter(s) beta. Default: None.
            vcov:           (float or numpy.ndarray) variance-covariance scalar or matrix for elements in beta. Default: None.
            sm_results:     (stats models results) statsmodels results object containing estimation results. If provided
                                beta, g, vcov should not be provided.
            complex_step:   (bool) whether to use the complex-step method to compute Jacobian of g. Default = True.
            epsilon:        (float) step size for computing Jacobian of g
            level:          (float) confidence level for . Default: 0.9
            g_args:         (tuple) arguments to pass to g. Default: ()
            g_kwargs:       (dict) keyword arguments to pass to g. Default: {}
            centered:       (bool) whether to compute Jacobean centered at beta. Default: False

        Returns:
            None

        Attributes:
            jacobian:   (numpy.ndarray) approximated Jacobian of g evaluated at beta
            results:    (Pandas DataFrame) computed results
        '''
        
        # If statsmodels results provided, set values for beta, param_names, vcov, g_kwargs
        if sm_results is not None:
        
            beta = sm_results.params
            param_names = sm_results.params.index
            vcov = sm_results.cov_params().to_numpy()
            g_kwargs={'param_names':sm_results.params.index}
            
        # Make sure that beta is a one dimensional numpy array
        beta = np.r_[beta]

        # Approximate the Jacobian of g at beta
        coeff = np.r_[g(*((beta,)+g_args), **g_kwargs)]

        N_beta = len(beta)
        N_g = len(coeff)

        jacobian = np.zeros((N_g,N_beta))

        for n_g in range(N_g):

            g_fun = lambda x: np.r_[g(*((x,)+g_args), **g_kwargs)][n_g]

            if complex_step:
                jacobian[n_g] = approx_fprime_cs(x=beta,f=g_fun,epsilon=epsilon,args=(),kwargs={})
            else:
                jacobian[n_g] = approx_fprime(x=beta,f=g_fun,epsilon=epsilon,args=(),kwargs={},centered=centered)
                
        self.jacobian = jacobian

        # Compute the remaining results
        std_err = np.sqrt(np.diagonal(jacobian.dot(vcov).dot(jacobian.T)))
        
        z = coeff/std_err
        p = norm.cdf(-np.abs(z))*2

        ci_upper = coeff - norm.ppf((1+level)/2)*std_err
        ci_lower = coeff + norm.ppf((1+level)/2)*std_err

        level_string = str(Decimal(level*100).normalize())

        results = pd.DataFrame(index=['g_'+str(i+1) for i in range(N_g)])
        results['Coefficient'] = coeff
        results['Std. err.'] = std_err
        results['z'] = z
        results['P>|z|'] = p
        results[level_string+'% ci [upper]'] = ci_upper
        results[level_string+'% ci [lower]'] = ci_lower

        self.results = results