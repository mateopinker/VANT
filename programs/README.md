# Programs

Small project utilities live here.

These scripts are for early calculations and project logging support. They are not a substitute for structural analysis, aerodynamic validation, or safe test planning.

## Wing Calculator

Run the first wing calculator interactively:

```powershell
python programs/wing_calculator.py
```

Or pass values directly:

```powershell
python programs/wing_calculator.py --mass-kg 2.5 --span-m 1.2 --chord-m 0.22 --cruise-speed-ms 15 --cl-max 1.2
```

The calculator accepts:

- `--area-m2` for known wing area.
- `--chord-m` for a rectangular wing.
- `--root-chord-m` and `--tip-chord-m` for a simple tapered wing.

