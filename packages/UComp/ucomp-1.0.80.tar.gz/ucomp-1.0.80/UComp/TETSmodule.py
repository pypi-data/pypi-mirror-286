# Compile with:
# c++ -O3 -Wall -shared -std=c++11 -undefined dynamic_lookup -I/Library/Frameworks/Python.framework/Headers
# -I"/Users/diego.pedregal/Google Drive/C++/armadillo-10.8.2/include" -llapack -lblas $(python3 -m
# pybind11 --includes) pythonBSM.cpp -o BSMc$(python3-config --extension-suffix)
import numpy as np
import pandas as pd


RunningFromPackage = True
if RunningFromPackage:
    from UComp import ETSc
    from UComp import TETSc
    from UComp import tsfile
else:
    import ETSc
    import TETSc
    import tsfile


class TETSmodel:
    """
    TETSmodel
    Estimates and forecasts a general Tobit TETS model

    Inputs:
    - y: a time series to forecast (can be a numerical vector or a time series object).
         This is the only required input. If it is a vector, the 's' input should be supplied compulsorily (see below).
    - s: seasonal period of the time series (1 for annual, 4 for quarterly, ...)
    - u: a matrix of input time series. If the output is to be forecasted, matrix 'u' should contain future
         values for inputs.
    - model: the model to estimate. It is a single string indicating the type of model for each component with one or two letters:
             - Error: ? / A
             - Trend: ? / N / A / Ad
             - Seasonal: ? / N / A
    - h: forecast horizon. If the model includes inputs, 'h' is not used, the length of 'u' is used instead.
    - criterion: information criterion for identification ("aic", "bic", or "aicc").
    - lambda_: Box-Cox lambda parameter (None: estimate)
    - forIntervals: estimate forecasting intervals (True / False)
    - bootstrap: use bootstrap simulation for predictive distributions
    - nSimul: number of simulation runs for bootstrap simulation of predictive distributions
    - verbose: intermediate estimation output (True / False)
    - alphaL: constraints limits for alpha parameter
    - betaL: constraints limits for beta parameter
    - gammaL: constraints limits for gamma parameter
    - phiL: constraints limits for phi parameter
    - Ymin: scalar or vector of time varying censoring values from below (default -Inf)
    - Ymax: scalar or vector of time varying censoring values from above (default Inf)

    Returns:
    An object (structure) of class TETS. It is a list with fields including
    all the inputs and the fields listed below as outputs. All the functions
    in this package fill in part of the fields of any TETS object as
    specified in what follows (function ETS fills in all of them at once):

    After running TETSmodel or TETSestim:
       p:      Estimated parameters
       yFor:   Forecasted values of output
       yForV:  Variance of forecasted values of output
       ySimul: Bootstrap simulations for forecasting distribution evaluation

    After running TETSvalidate:
       table: Estimation and validation table
       comp:  Estimated components in matrix form

    After running TETScomponents:
       comp: Estimated components in matrix form

    See Also:
        ETSmodel, PTS, PTSmodel, UC, ARIMA

    Author: Diego J. Pedregal
    """
    def __init__(self, y: pd.DataFrame, s: int = np.nan, u: np.array = np.array([]), model: str = "???",
        h: int = 24, criterion: str = "aicc", forIntervals: bool = False,
        bootstrap: bool = False, nSimul: int = 5000, verbose: bool = False,
        alphaL: np.array = np.array([0, 1]), betaL: np.array = np.array([0, 1]),
        gammaL: np.array = np.array([0, 1]), phiL: np.array = np.array([0.8, 0.98]),
        Ymin: np.array = -np.inf, Ymax: np.array = np.inf):

        p0 = np.array([-99999])
        if isinstance(y, np.ndarray) and np.isnan(s):
            raise ValueError("Either 'y' should be a Panda time series or 's' should be supplied!!")
        if isinstance(y, pd.Series) or isinstance(y, pd.DataFrame):
            aux = y.resample('YE').count()
            s = aux[aux.index[1]]
        Ymax = np.array(Ymax)
        Ymin=  np.array(Ymin)
        if len(Ymax.shape) == 0:
            Ymax = np.full(y.shape[0], Ymax)
        if Ymax.shape[0] < y.shape[0]:
            Ymax = np.concatenate((Ymax, np.full(y.shape[0] - Ymax.shape[0], Ymax[-1])))
        if len(Ymin.shape) == 0:
            Ymin = np.full(y.shape[0], Ymin)
        if Ymin.shape[0] < y.shape[0]:
            Ymin = np.concatenate((Ymin, np.full(y.shape[0] - Ymin.shape[0], Ymin[-1])))
        self.y = y
        self.u = u
        self.model = model
        self.s = s
        self.h = h
        self.criterion = criterion
        self.forIntervals = forIntervals
        self.bootstrap = bootstrap
        self.nSimul = nSimul
        self.verbose = verbose
        self.alphaL = alphaL
        self.betaL = betaL
        self.gammaL = gammaL
        self.phiL = phiL
        self.yFor = np.empty((0, 0))
        self.yForV = np.empty((0, 0))
        self.comp = np.empty((0, 0))
        self.ySimul = np.empty((0, 0))
        self.table = ""
        self.p = np.empty((0, 0))
        self.p0 = p0
        self.Ymax = Ymax
        self.Ymin = Ymin
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
        # Check for censoring constraints
        aux1 = Ymax - y
        aux2 = y - Ymin
        aux1 = aux1[~np.isnan(aux1)]
        aux2 = aux2[~np.isnan(aux2)]
        modelETS = False
        if np.min(aux1[np.isfinite(aux1)]) > 0 and np.min(aux2[np.isfinite(aux2)]) > 0:
            modelETS = True
        if modelETS:
            # Call ETSestim function (assuming it's implemented elsewhere)
            m1 = ETSc.ETSfunC("estimate", y, u.flatten(), rowu, colu, model, s, h, verbose, criterion,
                              False, alphaL, betaL, gammaL, phiL, "standard", forIntervals,
                              bootstrap, nSimul, np.array([0, 0]), False, p0, 1.0)
        else:
            m1 = TETSc.TETSfunC("estimate", y, u.flatten(), rowu, colu, model, s, h, criterion, False,
                                False, forIntervals, bootstrap, nSimul, verbose, 1.0,
                                alphaL, betaL, gammaL, phiL, p0, Ymin, Ymax)
        if m1.model != "error":  # ERROR!!!
            if isinstance(y, np.ndarray):
                yFor = np.array(m1.yFor)
            else:
                tNext = pd.date_range(y.index[-1], periods=2, freq=y.index.freq)[1]
                yFor = tsfile.ts(np.array(m1.yFor), tNext, y.index.freq)
            if yFor.size != 0:
                self.yFor = yFor
                if isinstance(y, np.ndarray):
                    self.yForV = np.array(m1.yForV)
                else:
                    self.yForV = tsfile.ts(np.array(m1.yForV), tNext, y.index.freq)
            self.model = m1.model
            self.p = np.array(m1.p)


    def components(self):
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
        aux1 = self.Ymax - self.y
        aux2 = self.y - self.Ymin
        aux1 = aux1[~np.isnan(aux1)]
        aux2 = aux2[~np.isnan(aux2)]
        modelETS = False
        if np.min(aux1[np.isfinite(aux1)]) > 0 and np.min(aux2[np.isfinite(aux2)]) > 0:
            modelETS = True
        if modelETS:
            # Call ETSestim function (assuming it's implemented elsewhere)
            m1 = ETSc.ETSfunC("components", self.y, u.flatten(), rowu, colu, self.model, self.s, self.h,
                              self.verbose, self.criterion, False, self.alphaL, self.betaL, self.gammaL, self.phiL,
                              "standard", self.forIntervals, self.bootstrap, self.nSimul, np.array([0, 0]), False,
                              self.p0, 1.0)
        else:
            m1 = TETSc.TETSfunC("components", self.y, u.flatten(), rowu, colu, self.model, self.s, self.h,
                                self.criterion, False, False, self.forIntervals, self.bootstrap, self.nSimul,
                                self.verbose, 1.0, self.alphaL, self.betaL, self.gammaL, self.phiL, self.p0,
                                self.Ymin, self.Ymax)
        self.comp = np.array(m1.comp)
        nrows = int(self.comp.shape[0] / self.y.shape[0])
        self.comp = np.transpose(np.reshape(self.comp, (nrows, np.floor_divide(self.comp.size, nrows))))
        self.v = self.comp[:, 0]
        if m1.compNames[-1] == "/":
            names = m1.compNames[:-1]
        else:
            names = m1.compNames
        names = names.split("/")
        if not isinstance(self.y, np.ndarray):
            self.comp = tsfile.ts(self.comp, self.y.index[0], self.y.index.freq)
        else:
            self.comp = pd.DataFrame(self.comp, index=range(self.comp.shape[0]))
        self.comp.columns = names


    def validate(self, show=True):
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
        aux1 = self.Ymax - self.y
        aux2 = self.y - self.Ymin
        aux1 = aux1[~np.isnan(aux1)]
        aux2 = aux2[~np.isnan(aux2)]
        modelETS = False
        if np.min(aux1[np.isfinite(aux1)]) > 0 and np.min(aux2[np.isfinite(aux2)]) > 0:
            modelETS = True
        if modelETS:
            # Call ETSestim function (assuming it's implemented elsewhere)
            m1 = ETSc.ETSfunC("validate", self.y, u.flatten(), rowu, colu, self.model, self.s, self.h,
                              self.verbose, self.criterion, False, self.alphaL, self.betaL, self.gammaL, self.phiL,
                              "standard", self.forIntervals, self.bootstrap, self.nSimul, np.array([0, 0]), False,
                              self.p0, 1.0)
        else:
            m1 = TETSc.TETSfunC("validate", self.y, u.flatten(), rowu, colu, self.model, self.s, self.h,
                                self.criterion, False, False, self.forIntervals, self.bootstrap, self.nSimul,
                                self.verbose, 1.0, self.alphaL, self.betaL, self.gammaL, self.phiL, self.p0,
                                self.Ymin, self.Ymax)
        comp = np.array(m1.comp)
        nrows = int(comp.shape[0] / self.y.shape[0])
        comp = np.transpose(np.reshape(comp, (nrows, np.floor_divide(comp.size, nrows))))
        self.v = comp[:, 0]
        self.table = ' '.join([str(i) for i in m1.table])
        if show:
            print(self.table)


    def plot(self):
        if any(self.comp.shape) == 0:
            self.components()
        if isinstance(self.comp, pd.Series) or isinstance(self.comp, pd.DataFrame):
            toplot = self.comp
        else:
            toplot = pd.DataFrame(self.comp, range(self.comp.shape[0]))
        toplot.plot(subplots=True, layout=(len(toplot.columns), 1), figsize=(10, 6), sharex=True)


def TETS(y: pd.DataFrame, s: int = np.nan, u: np.array = np.array([]), model: str = "???",
        h: int = 24, criterion: str = "aicc", forIntervals: bool = False,
        bootstrap: bool = False, nSimul: int = 5000, verbose: bool = False,
        alphaL: np.array = np.array([0, 1]), betaL: np.array = np.array([0, 1]),
        gammaL: np.array = np.array([0, 1]), phiL: np.array = np.array([0.8, 0.98]),
        Ymin: np.array = -np.inf, Ymax: np.array = np.inf):
    """
    TETS
    Estimates and forecasts a general Tobit TETS model

    Inputs:
    - y: a time series to forecast (can be a numerical vector or a time series object).
         This is the only required input. If it is a vector, the 's' input should be supplied compulsorily (see below).
    - s: seasonal period of the time series (1 for annual, 4 for quarterly, ...)
    - u: a matrix of input time series. If the output is to be forecasted, matrix 'u' should contain future
         values for inputs.
    - model: the model to estimate. It is a single string indicating the type of model for each component with one or two letters:
             - Error: ? / A
             - Trend: ? / N / A / Ad
             - Seasonal: ? / N / A
    - h: forecast horizon. If the model includes inputs, 'h' is not used, the length of 'u' is used instead.
    - criterion: information criterion for identification ("aic", "bic", or "aicc").
    - lambda_: Box-Cox lambda parameter (None: estimate)
    - forIntervals: estimate forecasting intervals (True / False)
    - bootstrap: use bootstrap simulation for predictive distributions
    - nSimul: number of simulation runs for bootstrap simulation of predictive distributions
    - verbose: intermediate estimation output (True / False)
    - alphaL: constraints limits for alpha parameter
    - betaL: constraints limits for beta parameter
    - gammaL: constraints limits for gamma parameter
    - phiL: constraints limits for phi parameter
    - Ymin: scalar or vector of time varying censoring values from below (default -Inf)
    - Ymax: scalar or vector of time varying censoring values from above (default Inf)

    Returns:
    An object (structure) of class TETS. It is a list with fields including
    all the inputs and the fields listed below as outputs. All the functions
    in this package fill in part of the fields of any TETS object as
    specified in what follows (function ETS fills in all of them at once):

    After running TETSmodel or TETSestim:
       p:      Estimated parameters
       yFor:   Forecasted values of output
       yForV:  Variance of forecasted values of output
       ySimul: Bootstrap simulations for forecasting distribution evaluation

    After running TETSvalidate:
       table: Estimation and validation table
       comp:  Estimated components in matrix form

    After running TETScomponents:
       comp: Estimated components in matrix form

    See Also:
        ETSmodel, PTS, PTSmodel, UC, ARIMA

    Author: Diego J. Pedregal

    See Also:
        ETSmodel, PTS, PTSmodel, UC, ARIMA

    Author: Diego J. Pedregal
    """
    m = TETSmodel(y, s, u, model, h, criterion, forIntervals,
                 bootstrap, nSimul, verbose, alphaL, betaL, gammaL, phiL, Ymin, Ymax)
    m.components()
    m.validate(m.verbose)
    return m

