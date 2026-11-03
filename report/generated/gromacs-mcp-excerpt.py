        wd, err = _workdir_or_error(workdir)
        if err:
            return err
        assert wd is not None
        if ntomp is not None and ntomp <= 0:
            return _error("ntomp must be positive when provided")
        if nsteps is not None and nsteps < 0:
            return _error("nsteps must be non-negative when provided")
        safe_tpr = _safe_file_arg(wd, tpr, "tpr", must_exist=True)
        safe_deffnm = _safe_deffnm(deffnm)
        args = [GMX_BIN, "mdrun", "-v", "-s", safe_tpr, "-deffnm", safe_deffnm]
        if ntomp is not None:
            args += ["-ntomp", str(ntomp)]
        if nsteps is not None:
            args += ["-nsteps", str(nsteps)]
        args += _validate_arg_tokens(extra_args, "extra_args")
