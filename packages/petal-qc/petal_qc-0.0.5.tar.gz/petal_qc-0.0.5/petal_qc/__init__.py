"""petal_qc python module."""
__version__ = "0.0.5"


def coreMetrology():
    """Launches the Core metrology analysis ahd PDB script."""
    from .metrology.coreMetrology import main
    main()

def doMetrology():
    """Launches the Core metrology analysis in the command line."""
    from .metrology.do_metrology import main
    main()

def coreThermal():
    """Launches the Core thermal analysis ahd PDB script."""
    from .thermal.coreThermal import main
    main()

def bustapeReport():
    """Launches the Core metrology analysis ahd PDB script."""
    from .BTreport.CheckBTtests import main
    # from .BTreport.bustapeReport import main
    main()

def dashBoard():
    """Launches the Core thermal analysis ahd PDB script."""
    from .dashBoard import main
    main()
