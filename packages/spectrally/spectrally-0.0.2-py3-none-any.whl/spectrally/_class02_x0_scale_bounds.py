# -*- coding: utf-8 -*-
"""
Created on Sat Jul  6 17:31:49 2024

@author: dvezinet
"""


import numpy as np


from . import _class01_model_dict


#############################################
#############################################
#    DEFAULTS
#############################################


_DEF_SCALES_FACTORS = {
    'width': 2,   # lambD / 2
    'shift': 2,   # lambD / 2
}


_DEF_X0_FACTORS = {
    'width': 10,  # lambD / 10
    'shift': 10,  # lambD / 10
}


_DEF_X0 = {
    'lognorm': {
        'sigma': 1.,
    },
}


#############################################
#############################################
#    harmonize dict for scale, bounds, x0
#############################################


def _get_dict(
    lx_free_keys=None,
    dmodel=None,
    din=None,
    din_name=None,
):

    # --------------
    # trivial
    # --------------

    if din is None:
        return {}

    # --------------
    # non-trivial
    # --------------

    c0 = (
        isinstance(din, dict)
        and all([isinstance(k0, str) for k0 in din.keys()])
    )
    if not c0:
        msg = (
            f"Arg '{din_name}' must be a dict of the form:\n"
            "\t- key_of_free_variable: value (float)\n"
            "Provided:\n{din}"
        )
        raise Exception(msg)

    # --------------
    # check keys
    # --------------

    derr = {
        k0: v0 for k0, v0 in din.items()
        if k0 not in lx_free_keys or not np.isscalar(v0)
    }
    if len(derr) > 0:
        lstr = [f"\t- '{k0}': {v0}" for k0, v0 in derr.items()]
        msg = (
            "The following key / values are non-conform from '{din_name}':/n"
            + "\n".join(lstr)
            + "\nAll keys must be natching free variable names!\n"
            "Available keys:\n{lk_free_keys}"
        )
        raise Exception(msg)

    # --------------
    # convert to ind / val format
    # --------------

    dout = {}
    for k0, v0 in din.items():

        # get func name and type + variable name
        ftype = dmodel['_'.join(k0.split('_')[:-1])]['type']
        if not ftype in _class01_model_dict._DMODEL.keys():
            msg = (
                "Unknown function type for variable:\n"
                f"\t- var: {k0}\n"
                f"\t- ftype: {ftype}\n"
            )
            raise Exception(msg)


        var = k0.split('_')[-1]

        if ftype not in dout.keys():
            dout[ftype] = {}

        if var not in dout[ftype].keys():
            dout[ftype][var] = {'ind': [], 'val': []}

        dout[ftype][var]['ind'].append(lx_free_keys.index(k0))
        dout[ftype][var]['val'].append(v0)

    # --------------
    # sort
    # --------------

    lktypes = list(dout.keys())
    for k0 in lktypes:
        lkvar = list(dout[k0].keys())
        for k1 in lkvar:
            inds = np.argsort(dout[k0][k1]['ind'])
            dout[k0][k1]['ind'] = np.array(dout[k0][k1]['ind'])[inds]
            dout[k0][k1]['val'] = np.array(dout[k0][k1]['val'])[inds]

    return dout


#############################################
#############################################
#       get scales, bounds
#############################################


def _get_scales_bounds(
    nxfree=None,
    lamb=None,
    data=None,
    iok_all=None,
    dind=None,
    dscales=None,
    dbounds_low=None,
    dbounds_up=None,
):

    # ------------------
    # initialize
    # ------------------

    scales = np.zeros((nxfree,), dtype=float)
    bounds0 = np.zeros((nxfree,), dtype=float)
    bounds1 = np.zeros((nxfree,), dtype=float)

    # ------------------
    # prepare
    # ------------------

    lambD = lamb[-1] - lamb[0]
    lambd = lamb[1] - lamb[0]
    lambm = np.mean(lamb)

    data_max = np.nanmax(data[iok_all])
    data_min = np.nanmin(data[iok_all])
    data_mean = np.nanmean(data[iok_all])
    data_median = np.nanmedian(data[iok_all])
    data_pulse_sign = np.sign(data_mean - data_median)

    ldins = [(dscales, scales), (dbounds_low, bounds0), (dbounds_up, bounds1)]

    # ------------------
    # all linear
    # ------------------

    kfunc = 'linear'
    if dind.get(kfunc) is not None:

        a1max = (data_max - data_min) / lambD

        # -------
        # a1

        kvar = 'a1'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = a1max
            bounds0[ival] = -10.
            bounds1[ival] = 10.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # -------
        # a0

        kvar = 'a0'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = max(
                np.abs(data_min - a1max*lamb[0]),
                np.abs(data_max + a1max*lamb[0]),
            )
            bounds0[ival] = -10.
            bounds1[ival] = 10.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

    # --------------------
    # all exponentials
    # --------------------

    kfunc = 'exp_lamb'
    if dind.get(kfunc) is not None:

        rate = np.nanmax([
            np.abs(
                np.log(data_max * lamb[0] / (data_min * lamb[-1]))
                / (1/lamb[-1] - 1./lamb[0])
            ),
            np.abs(
                np.log(data_min * lamb[0] / (data_max * lamb[-1]))
                / (1/lamb[-1] - 1./lamb[0])
            ),
        ])

        # rate
        kvar = 'rate'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = rate
            bounds0[ival] = 0.
            bounds1[ival] = 10.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # amp
        kvar = 'amp'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = data_mean * np.exp(rate/lambm) * lambm
            bounds0[ival] = 0.
            bounds1[ival] = 10.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

    # -----------------
    # all gaussians
    # -----------------

    kfunc = 'gauss'
    if dind.get(kfunc) is not None:

        # amp
        kvar = 'amp'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = data_max - data_min
            bounds0[ival] = 0.
            bounds1[ival] = 10.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # vccos
        kvar = 'vccos'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = (lambD/lambm) / _DEF_SCALES_FACTORS['shift']
            bounds0[ival] = -1.
            bounds1[ival] = 1.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # sigma
        kvar = 'sigma'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = lambD / _DEF_SCALES_FACTORS['width']
            bounds0[ival] = 1e-3
            bounds1[ival] = 2

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

    # -----------------
    # all lorentz
    # -----------------

    kfunc = 'lorentz'
    if dind.get(kfunc) is not None:

        # amp
        kvar = 'amp'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = data_max - data_min
            bounds0[ival] = 0.
            bounds1[ival] = 10.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # vccos
        kvar = 'vccos'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = (lambD/lambm) / _DEF_SCALES_FACTORS['shift']
            bounds0[ival] = -1.
            bounds1[ival] = 1.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # gam
        kvar = 'gam'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = lambD / _DEF_SCALES_FACTORS['width']
            bounds0[ival] = 1e-3
            bounds1[ival] = 2

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

    # -----------------
    # all pvoigt
    # -----------------

    kfunc = 'pvoigt'
    if dind.get(kfunc) is not None:

        # amp
        kvar = 'amp'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = data_max - data_min
            bounds0[ival] = 0.
            bounds1[ival] = 10.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # vccos
        kvar = 'vccos'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = (lambD/lambm) / _DEF_SCALES_FACTORS['shift']
            bounds0[ival] = -1.
            bounds1[ival] = 1.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # sigma
        kvar = 'sigma'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = lambD / _DEF_SCALES_FACTORS['width']
            bounds0[ival] = 1e-3
            bounds1[ival] = 2

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # gam
        kvar = 'gam'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = lambD / _DEF_SCALES_FACTORS['width']
            bounds0[ival] = 1e-3
            bounds1[ival] = 2

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

    # -----------------
    # all voigt
    # -----------------

    kfunc = 'voigt'
    if dind.get(kfunc) is not None:

        # amp
        kvar = 'amp'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = data_max - data_min
            bounds0[ival] = 0.
            bounds1[ival] = 10.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # vccos
        kvar = 'vccos'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = (lambD/lambm) / _DEF_SCALES_FACTORS['shift']
            bounds0[ival] = -1.
            bounds1[ival] = 1.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # sigma
        kvar = 'sigma'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = lambD / _DEF_SCALES_FACTORS['width']
            bounds0[ival] = 1e-3
            bounds1[ival] = 2

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # gam
        kvar = 'gam'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = lambD / _DEF_SCALES_FACTORS['width']
            bounds0[ival] = 1e-3
            bounds1[ival] = 2

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

    # ------------------
    # all pulse1
    # ------------------

    kfunc = 'pulse1'
    if dind.get(kfunc) is not None:

        _get_scales_bounds_pulse(
            dind=dind,
            kfunc=kfunc,
            ldins=ldins,
            # data
            data_min=data_min,
            data_max=data_max,
            data_pulse_sign=data_pulse_sign,
            # lamb
            lamb=lamb,
            lambd=lambd,
            lambm=lambm,
            lambD=lambD,
            # arrays to fill
            scales=scales,
            bounds0=bounds0,
            bounds1=bounds1,
        )

    # ------------------
    # all pulse2
    # ------------------

    kfunc = 'pulse2'
    if dind.get(kfunc) is not None:

        _get_scales_bounds_pulse(
            dind=dind,
            kfunc=kfunc,
            ldins=ldins,
            # data
            data_min=data_min,
            data_max=data_max,
            data_pulse_sign=data_pulse_sign,
            # lamb
            lamb=lamb,
            lambd=lambd,
            lambm=lambm,
            lambD=lambD,
            # arrays to fill
            scales=scales,
            bounds0=bounds0,
            bounds1=bounds1,
        )

    # ------------------
    # all lognorm
    # ------------------

    kfunc = 'lognorm'
    if dind.get(kfunc) is not None:

        # useful for guessing

        # max at t - t0 = exp(mu - sigma**2)
        # max = amp * exp(sigma**2/2 - mu)
        # variance = (exp(sigma**2) - 1) * exp(2mu + sigma**2)
        # => mu = 0.5 * (log(std**2 / (exp(sigma**2) - 1)) - sigma**2)
        # skewness = (exp(sigma**2) + 2) * sqrt(exp(sigma**2) - 1)

        sigma = _DEF_X0[kfunc]['sigma']

        std = lambD / 5
        std_min = lambD / 100
        std_max = lambD

        mu = 0.5 * (np.log(std**2/(np.exp(sigma**2) - 1)) - sigma**2)
        mu_abs = np.abs(mu)
        mu_min = 0.5 * (np.log(std_min**2/(np.exp(sigma**2) - 1)) - sigma**2)
        mu_max = 0.5 * (np.log(std_max**2/(np.exp(sigma**2) - 1)) - sigma**2)

        # sigma
        kvar = 'sigma'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = sigma
            bounds0[ival] = 0.1
            bounds1[ival] = 5

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # mu
        kvar = 'mu'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = mu_abs
            bounds0[ival] = mu_min / mu_abs
            bounds1[ival] = mu_max / mu_abs

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # amp
        # max = amp * exp(sigma**2/2 - mu)
        kvar = 'amp'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = (data_max - data_min) * np.exp(mu - 0.5*sigma**2)
            if data_pulse_sign > 0:
                bounds0[ival] = 0.
                bounds1[ival] = 10.
            else:
                bounds0[ival] = -10.
                bounds1[ival] = 0.

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

        # tau
        # max at lamb - (lamb00 + lambD * tau) = exp(mu - sigma**2)
        kvar = 'tau'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = 1
            bounds0[ival] = 0
            bounds1[ival] = 1

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=None if ii == 0 else scales
                )

    return scales, bounds0, bounds1


#############################################
#############################################
#       get x0
#############################################


def _get_x0(
    nxfree=None,
    lamb=None,
    data=None,
    iok=None,
    dind=None,
    dx0=None,
    scales=None,
    binning=None,
):

    # ------------------
    # initialize
    # ------------------

    x0 = np.zeros((nxfree,), dtype=float)

    # ------------------
    # prepare
    # ------------------

    lamb0 = lamb[0]
    lambD = lamb[-1] - lamb[0]
    lambd = lamb[1] - lamb[0]
    lambm = np.mean(lamb)
    if binning is False:
        lamb_amax = lamb[iok][np.argmax(data[iok])]
        lamb_amin = lamb[iok][np.argmin(data[iok])]
    else:
        raise NotImplementedError()

    data_max = np.nanmax(data[iok])
    data_min = np.nanmin(data[iok])
    data_mean = np.nanmean(data[iok])
    data_median = np.median(data[iok])
    data_pulse_sign = np.sign(data_mean - data_median)

    lamb_ext = lamb_amax if data_pulse_sign > 0 else lamb_amin

    ldins = [(dx0, x0)]

    # ------------------
    # all linear
    # ------------------

    kfunc = 'linear'
    if dind.get(kfunc) is not None:

        a1max = ((data_max - data_min) / lambD) / 10

        # -------
        # a1

        kvar = 'a1'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = a1max / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # -------
        # a0

        kvar = 'a0'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = np.abs(data_min - a1max*lamb[0]) / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

    # --------------------
    # all exponentials
    # ------------------

    kfunc = 'exp_lamb'
    if dind.get(kfunc) is not None:

        rate = np.nanmax([
            np.abs(
                np.log(data_max * lamb[0] / (data_min * lamb[-1]))
                / (1/lamb[-1] - 1./lamb[0])
            ),
            np.abs(
                np.log(data_min * lamb[0] / (data_max * lamb[-1]))
                / (1/lamb[-1] - 1./lamb[0])
            ),
        ]) / 10.

        # rate
        kvar = 'rate'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = rate / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # amp
        kvar = 'amp'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            scales[ival] = data_mean * np.exp(rate/lambm) * lambm / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

    # -----------------
    # all gaussians
    # -----------------

    kfunc = 'gauss'
    if dind.get(kfunc) is not None:

        # amp
        kvar = 'amp'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = (data_max - data_min) / 2 / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # vccos
        kvar = 'vccos'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = lambD / _DEF_X0_FACTORS['shift'] / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # sigma
        kvar = 'sigma'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = lambD / _DEF_X0_FACTORS['width'] / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

    # -----------------
    # all lorentz
    # -----------------

    kfunc = 'lorentz'
    if dind.get(kfunc) is not None:

        # amp
        kvar = 'amp'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = (data_max - data_min) / 2 / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # vccos
        kvar = 'vccos'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = lambD / _DEF_X0_FACTORS['shift'] / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # gam
        kvar = 'gam'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = lambD / _DEF_X0_FACTORS['width'] / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

    # -----------------
    # all pvoigt
    # -----------------

    kfunc = 'pvoigt'
    if dind.get(kfunc) is not None:

        # amp
        kvar = 'amp'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = (data_max - data_min) / 2. / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # vccos
        kvar = 'vccos'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = lambD / _DEF_X0_FACTORS['shift'] / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # sigma
        kvar = 'sigma'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = lambD / _DEF_X0_FACTORS['width'] / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # gam
        kvar = 'gam'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = lambD / _DEF_X0_FACTORS['width'] / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

    # -----------------
    # all voigt
    # -----------------

    kfunc = 'voigt'
    if dind.get(kfunc) is not None:

        # amp
        kvar = 'amp'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = (data_max - data_min) / 2 / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # vccos
        kvar = 'vccos'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = lambD / _DEF_X0_FACTORS['shift'] / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # sigma
        kvar = 'sigma'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = lambD / _DEF_X0_FACTORS['width'] / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # gam
        kvar = 'gam'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = lambD / _DEF_X0_FACTORS['width'] / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

    # ------------------
    # all pulse1
    # ------------------

    kfunc = 'pulse1'
    if dind.get(kfunc) is not None:

        _get_x0_pulse(
            dind=dind,
            kfunc=kfunc,
            ldins=ldins,
            # data
            data_min=data_min,
            data_max=data_max,
            data_pulse_sign=data_pulse_sign,
            # lamb
            lamb0=lamb0,
            lambd=lambd,
            lambm=lambm,
            lambD=lambD,
            lamb_ext=lamb_ext,
            # arrays to fill
            x0=x0,
            scales=scales,
        )

    # ------------------
    # all pulse2
    # ------------------

    kfunc = 'pulse2'
    if dind.get(kfunc) is not None:

        _get_x0_pulse(
            dind=dind,
            kfunc=kfunc,
            ldins=ldins,
            # data
            data_min=data_min,
            data_max=data_max,
            data_pulse_sign=data_pulse_sign,
            # lamb
            lamb0=lamb0,
            lambd=lambd,
            lambm=lambm,
            lambD=lambD,
            lamb_ext=lamb_ext,
            # arrays to fill
            x0=x0,
            scales=scales,
        )

    # ------------------
    # all lognorm
    # ------------------

    kfunc = 'lognorm'
    if dind.get(kfunc) is not None:

        # useful for guessing
        sigma = _DEF_X0[kfunc]['sigma']
        mu = 0.5 * (np.log((lambD / 10)**2/(np.exp(sigma**2) - 1)) - sigma**2)
        mu_sign = np.sign(mu)
        exp = np.exp(mu - sigma**2)

        # sigma
        kvar = 'sigma'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = 1

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # mu
        kvar = 'mu'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = mu_sign

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # t0
        # max at lamb - (lamb00 + lambD * tau) = exp(mu - sigma**2)
        kvar = 'tau'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = (lamb_ext - exp - lamb0) / lambD / scales[ival]

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

        # amp
        # max = amp * exp(sigma**2/2 - mu)
        kvar = 'amp'
        vind = dind['jac'][kfunc].get(kvar)
        if vind is not None:
            ival, ivar = vind['val'], vind['var']
            x0[ival] = data_pulse_sign

            for ii, (din, val) in enumerate(ldins):
                _update_din_from_user(
                    din, kfunc, kvar, val,
                    scales=scales,
                )

    return x0


# #######################
# generic pdate from dict
# #######################


def _update_din_from_user(din, kfunc, kvar, val, scales=None):

    if din.get(kfunc, {}).get(kvar) is not None:
        ind = din[kfunc][kvar]['ind']
        if scales is None:
            val[ind] = din[kfunc][kvar]['val']
        else:
            val[ind] = din[kfunc][kvar]['val'] / scales[ind]

    return


# ###########################
# generic pulse scales bounds
# ###########################


def _get_scales_bounds_pulse(
    dind=None,
    kfunc=None,
    ldins=None,
    # data
    data_min=None,
    data_max=None,
    data_pulse_sign=None,
    # lamb
    lamb=None,
    lambd=None,
    lambm=None,
    lambD=None,
    # arrays to fill
    scales=None,
    bounds0=None,
    bounds1=None,
):

    # amp
    kvar = 'amp'
    vind = dind['jac'][kfunc].get(kvar)
    if vind is not None:
        ival, ivar = vind['val'], vind['var']
        scales[ival] = (data_max - data_min)
        if data_pulse_sign > 0.:
            bounds0[ival] = 0
            bounds1[ival] = 10.
        else:
            bounds0[ival] = -10.
            bounds1[ival] = 0.

        for ii, (din, val) in enumerate(ldins):
            _update_din_from_user(
                din, kfunc, kvar, val,
                scales=None if ii == 0 else scales
            )

    # tau
    kvar = 'tau'
    vind = dind['jac'][kfunc].get(kvar)
    if vind is not None:
        ival, ivar = vind['val'], vind['var']
        scales[ival] = 1
        bounds0[ival] = 0
        bounds1[ival] = 1

        for ii, (din, val) in enumerate(ldins):
            _update_din_from_user(
                din, kfunc, kvar, val,
                scales=None if ii == 0 else scales
            )

    # tup
    kvar = 't_up'
    vind = dind['jac'][kfunc].get(kvar)
    if vind is not None:
        ival, ivar = vind['val'], vind['var']
        scales[ival] = 0.05 * lambD
        bounds0[ival] = 1.e-3
        bounds1[ival] = 20

        for ii, (din, val) in enumerate(ldins):
            _update_din_from_user(
                din, kfunc, kvar, val,
                scales=None if ii == 0 else scales
            )

    # tdown
    kvar = 't_down'
    vind = dind['jac'][kfunc].get(kvar)
    if vind is not None:
        ival, ivar = vind['val'], vind['var']
        scales[ival] = 0.2 * lambD
        bounds0[ival] = 1.e-3
        bounds1[ival] = 20

        for ii, (din, val) in enumerate(ldins):
            _update_din_from_user(
                din, kfunc, kvar, val,
                scales=None if ii == 0 else scales
            )

    return


# #######################
# generic pulse x0
# #######################


def _get_x0_pulse(
    dind=None,
    kfunc=None,
    ldins=None,
    # data
    data_min=None,
    data_max=None,
    data_pulse_sign=None,
    # lamb
    lambd=None,
    lambm=None,
    lambD=None,
    lamb0=None,
    lamb_ext=None,
    # arrays to fill
    x0=None,
    scales=None,
):

    # amp
    kvar = 'amp'
    vind = dind['jac'][kfunc].get(kvar)
    if vind is not None:
        ival, ivar = vind['val'], vind['var']
        x0[ival] = (data_max - data_min) * data_pulse_sign / scales[ival]

        for ii, (din, val) in enumerate(ldins):
            _update_din_from_user(
                din, kfunc, kvar, val,
                scales=scales,
            )

    # tau
    kvar = 'tau'
    vind = dind['jac'][kfunc].get(kvar)
    if vind is not None:
        ival, ivar = vind['val'], vind['var']
        x0[ival] = (lamb_ext - lamb0) / lambD

        for ii, (din, val) in enumerate(ldins):
            _update_din_from_user(
                din, kfunc, kvar, val,
                scales=scales,
            )

    # tup
    kvar = 't_up'
    vind = dind['jac'][kfunc].get(kvar)
    if vind is not None:
        ival, ivar = vind['val'], vind['var']
        x0[ival] = 1

        for ii, (din, val) in enumerate(ldins):
            _update_din_from_user(
                din, kfunc, kvar, val,
                scales=scales,
            )

    # tdown
    kvar = 't_down'
    vind = dind['jac'][kfunc].get(kvar)
    if vind is not None:
        ival, ivar = vind['val'], vind['var']
        x0[ival] = 1

        for ii, (din, val) in enumerate(ldins):
            _update_din_from_user(
                din, kfunc, kvar, val,
                scales=scales,
            )

    return