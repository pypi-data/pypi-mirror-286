# Compile with:
# c++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup -I/Library/Frameworks/Python.framework/Headers
# -I"/Users/diego.pedregal/Google Drive/C++/armadillo-10.8.2/include" -llapack -lblas $(python3 -m
# pybind11 --includes) pythonBSM.cpp -o BSMc$(python3-config --extension-suffix)
import copy

import numpy as np
import pandas as pd

RunningFromPackage = True
if RunningFromPackage:
    from UComp import ARIMAc
    from UComp import tsfile
else:
    import ARIMAc
    import tsfile


class ARIMAmodel:
    """
    ARIMAmodel
    Estimates and forecasts a general ARIMA model

    Inputs:
    - y: a time series to forecast (it may be either a numerical vector or a time series object).
         This is the only input required. If a vector, the additional input \code{s} should be
         supplied compulsorily (see below).
    - u: a matrix of input time series. If the output wanted to be forecast, matrix u should contain
         future values for inputs.
    - model: the model to estimate. A vector c(p,d,q,P,D,Q) containing the model orders
             of an ARIMA(p,d,q)x(P,D,Q)_s model. A constant may be estimated with the
             cnst input. Use a NULL to automatically identify the ARIMA model.
    - cnst: flag to include a constant in the model (TRUE/FALSE/NULL). Use NULL to estimate
    - s: seasonal period of time series (1 for annual, 4 for quarterly, ...)
    - h: forecast horizon. If the model includes inputs h is not used, the lenght of u is used instead.
    - criterion: information criterion for identification stage ("aic", "bic", "aicc")
    - verbose: intermediate estimation output (TRUE / FALSE)
    - lambda_: Box-Cox lambda parameter (NULL: estimate)
    - maxOrders: a vector c(p,d,q,P,D,Q) containing the maximum orders of model orders
                 to search for in the automatic identification
    - bootstrap: use bootstrap simulation for predictive distributions
    - nSimul: number of simulation runs for bootstrap simulation of predictive distributions
    - fast: fast identification (avoids post-identification checks)

    Returns:
    An object (structure) of class ARIMA. It is a list with fields including
    all the inputs and the fields listed below as outputs.

    See Also:
        ARIMA, ARIMAvalidate, UC, ETS, TETS

    Author: Diego J. Pedregal
    """
    def __init__(self, y: pd.DataFrame, u: np.array = np.array([]), model: np.array = np.array([]),
                 cnst: float = None, s: int = None, criterion: str = "bic", h: int = 24,
                 verbose: bool = False, lambdaBoxCox: float = 1.0,
                 maxOrders: np.array = np.array([3, 2, 3, 2, 1, 2]), bootstrap: bool = False,
                 nSimul: int = 5000, fast: bool = False, command: str = 'estimate'):
        if isinstance(y, np.ndarray) and np.isnan(s):
            raise ValueError("Either 'y' should be a Panda time series or 's' should be supplied!!")
        if isinstance(y, pd.Series) or isinstance(y, pd.DataFrame):
            aux = y.resample('YE').count()
            s = aux[aux.index[1]]
        self.y = y
        self.u = u
        self.model = model
        if isinstance(cnst, bool) and cnst:
            self.cnst = 1.0
        elif isinstance(cnst, bool) and not cnst:
            self.cnst = 0.0
        elif cnst is None:
            self.cnst = 9999.9
        else:
            self.cnst = cnst
        if s is None:
            s = 1  # Asignar un valor por defecto si no se proporciona.
        if s > 24:
            raise ValueError("Data with period greater than 24 are not allowed!!")
        self.s = s
        if h is None:
            h = 2 * s
        self.h = h
        self.identDiff = True
        self.identMethod = "gm"
        self.criterion = criterion
        self.verbose = verbose
        self.bootstrap = bootstrap
        self.nSimul = nSimul
        self.maxOrders = maxOrders
        self.error = np.empty((0, 0))
        self.yFor = np.empty((0, 0))
        self.yForV = np.empty((0, 0))
        self.ySimul = np.empty((0, 0))
        self.table = ""
        self.p = np.empty((0, 0))
        self.BIC = np.empty((0, 0))
        self.AIC = np.empty((0, 0))
        self.AICc = np.empty((0, 0))
        self.IC = np.empty((0, 0))
        self.lambdaBoxCox = lambdaBoxCox
        self.fast = fast
        if u.size == 0:
            u = np.array([-99999])
            rowu = 0
            colu = 0
        else:
            if isinstance(u, pd.Series) or isinstance(u, pd.DataFrame):
                u = u.values
            if len(u.shape) == 1:
                rowu = 1
                colu = u.shape[0]
            else:
                rowu, colu = u.shape
            if rowu > colu:
                u = np.transpose(u)
                rowu, colu = u.shape
        Ucopy = self.u
        self.estim_(command)
        m = copy.deepcopy(self)
        IC = self.IC
        if model.shape[0] == 0 and not fast or not np.isfinite(IC):
            if s == 1 and np.sum(np.abs(np.array(m.model[:3]) - np.array([0, 1, 1]))) != 0:
                # Datos anuales
                self.model = [0, 1, 1, 0, 0, 0]
                self.u = Ucopy
                self.estim_(command)
                if np.isfinite(self.IC) and self.IC < IC:
                    IC = self.IC
                    m = copy.deepcopy(self)
                if m.model[1] > 0:
                    self.model = copy.deepcopy(m.model)
                    self.model[1] = self.model[1] - 1
                    self.model[2] = min(self.model[2] + 1, maxOrders[2])
                    if not all(np.array(self.model) == np.array([0, 1, 1, 0, 0, 0])):
                        self.u = Ucopy
                        self.estim_(command)
                        if np.isfinite(self.IC) and self.IC < IC:
                            IC = self.IC
                            m = copy.deepcopy(self)
            elif s > 1:
                # Datos no anuales
                if np.sum(np.abs(np.array(self.model) - np.array([0, 1, 1, 0, 1, 1]))) != 0:
                    self.model = [0, 1, 1, 0, 1, 1]
                    self.u = Ucopy
                    self.estim_(command)
                    if np.isfinite(self.IC) and self.IC < IC:
                        IC = self.IC
                        m = copy.deepcopy(self)
                if m.model[1] > 0 and m.model[4] > 0:
                    self.model = copy.deepcopy(m.model)
                    self.model[1] = self.model[1] - 1
                    self.model[0] = min(self.model[0] + 1, maxOrders[0])
                    if np.sum(np.abs(np.array(self.model) - np.array([0, 1, 1, 0, 1, 1]))) != 0:
                        self.u = Ucopy
                        self.estim_(command)
                        if np.isfinite(self.IC) and self.IC < IC:
                            IC = self.IC
                            m = copy.deepcopy(self)
        # copy final model in self
        self.model = m.model
        self.cnst = m.cnst
        self.error = m.error
        self.yFor = m.yFor
        self.yForV = m.yForV
        self.ySimul = m.ySimul
        self.table = m.table
        self.p = m.p
        self.BIC = m.BIC
        self.AIC = m.AIC
        self.AICc = m.AICc
        self.IC = m.IC
        self.lambdaBoxCox = m.lambdaBoxCox

    def estim_(self, command: str = 'estimate'):
        m = self
        u = self.u
        if u.size == 0:
            u = np.array([-99999])
            rowu = 0
            colu = 0
        else:
            if len(u.shape) == 1:
                rowu = 1
                colu = u.shape[0]
            else:
                rowu, colu = u.shape
            if rowu > colu:
                u = np.transpose(u)
                rowu, colu = u.shape
        output = ARIMAc.ARIMAfunC(command, self.y, u.flatten(), rowu, colu, self.model, self.cnst, self.s,
                    self.criterion, self.h, self.verbose, self.lambdaBoxCox, self.maxOrders,
                    self.bootstrap, self.nSimul, self.fast, self.identDiff, self.identMethod)
        if output.model == 'error':
            raise ValueError("Error in ARIMA estimation!!")
        else:
            m.p = output.p
            m.lambdaBoxCox = output.lambdaBoxCox
            m.model = output.orders
            m.cnst = output.cnst
            m.u = output.u
            m.BIC = output.BIC
            m.AIC = output.AIC
            m.AICc = output.AICc
            m.IC = output.IC
            m.table = ' '.join([str(i) for i in output.table])
        if isinstance(m.u, np.ndarray) and m.u.ndim > 1:
            lu = m.u.shape[0]
            if lu == 1:
                lu = m.u.shape[1]
        else:
            lu = len(m.u)
        if lu > 0:
            m.h = lu - len(m.y)
        if isinstance(m.y, pd.Series) and m.h > 0:
            fake = pd.Series([*m.y, np.nan], index=pd.date_range(start=m.y.index[0], periods=len(m.y) + 1,
                                                                    freq=m.y.index.freq))
            m.yFor = pd.Series(output.yFor, index=pd.date_range(start=fake.index[-1], periods=len(output.yFor),
                                                                      freq=m.y.index.freq))
            m.yForV = pd.Series(output.yForV,
                                   index=pd.date_range(start=fake.index[-1], periods=len(output.yForV),
                                                       freq=m.y.index.freq))
            if m.bootstrap:
                m.ySimul = np.array(output.ySimul)
                m.ySimul = np.transpose(m.ySimul.reshape((m.nSimul, len(m.ySimul) // m.nSimul)))
            if command == 'validate':
                m.error = pd.Series(output.error,
                                    index=pd.date_range(start=fake.index[-1], periods=len(output.error),
                                                        freq=m.y.index.freq))
        elif m.h > 0:
            m.yFor = output.yFor
            m.yForV = output.yForV
            m.ySimul = output.ySimul
            m.error = output.error
        if command == 'validate' and self.verbose == True:
            print(m.table)
        return m


    # def plot(self):
    #     if any(self.comp.shape) == 0:
    #         self.components()
    #     if isinstance(self.comp, pd.Series) or isinstance(self.comp, pd.DataFrame):
    #         toplot = self.comp
    #     else:
    #         toplot = pd.DataFrame(self.comp, range(self.comp.shape[0]))
    #     toplot.plot(subplots=True, layout=(len(toplot.columns), 1), figsize=(10, 6), sharex=True)


def ARIMA(y: pd.DataFrame, u: np.array = np.array([]), model: np.array = np.array([]),
          cnst = None, s = None, criterion: str = "bic", h: int = 24,
          verbose: bool = False, lambdaBoxCox: np.array = np.array(1.0),
          maxOrders: np.array = np.array([3, 2, 3, 2, 1, 2]), bootstrap: bool = False,
          nSimul: int = 5000, fast: bool = False):
    """
    ARIMA
    Estimates and forecasts a general ARIMA model

    Inputs:
    - y: a time series to forecast (it may be either a numerical vector or a time series object).
         This is the only input required. If a vector, the additional input \code{s} should be
         supplied compulsorily (see below).
    - u: a matrix of input time series. If the output wanted to be forecast, matrix u should contain
         future values for inputs.
    - model: the model to estimate. A vector c(p,d,q,P,D,Q) containing the model orders
             of an ARIMA(p,d,q)x(P,D,Q)_s model. A constant may be estimated with the
             cnst input. Use a NULL to automatically identify the ARIMA model.
    - cnst: flag to include a constant in the model (TRUE/FALSE/NULL). Use NULL to estimate
    - s: seasonal period of time series (1 for annual, 4 for quarterly, ...)
    - h: forecast horizon. If the model includes inputs h is not used, the lenght of u is used instead.
    - criterion: information criterion for identification stage ("aic", "bic", "aicc")
    - verbose: intermediate estimation output (TRUE / FALSE)
    - lambda_: Box-Cox lambda parameter (NULL: estimate)
    - maxOrders: a vector c(p,d,q,P,D,Q) containing the maximum orders of model orders
                 to search for in the automatic identification
    - bootstrap: use bootstrap simulation for predictive distributions
    - nSimul: number of simulation runs for bootstrap simulation of predictive distributions
    - fast: fast identification (avoids post-identification checks)

    Returns:
    An object (structure) of class ARIMA. It is a list with fields including
    all the inputs and the fields listed below as outputs.

    See Also:
        ARIMA, ARIMAvalidate, UC, ETS, TETS

    Author: Diego J. Pedregal
    """
    m = ARIMAmodel(y, u, model, cnst, s, criterion, h, verbose, lambdaBoxCox,
                   maxOrders, bootstrap, nSimul, fast, 'validate')
    return m

