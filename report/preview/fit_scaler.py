def fit_scaler(fit_values, values):
    fit_values, values = finite(fit_values), finite(values)
    mean, scale = fit_values.mean(axis=0), fit_values.std(axis=0)
    if np.any(scale <= 0):
        raise InvalidInput("Constant fit feature")
    return (values - mean) / scale, {"mean": mean.tolist(), "scale": scale.tolist()}
