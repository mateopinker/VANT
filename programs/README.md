# Programs

Small project utilities live here.

These scripts are for early calculations and project logging support. They are not a substitute for structural analysis, aerodynamic validation, or safe test planning.

## Wing Calculator

Run the wing calculator:

```powershell
python programs/wing_calculator.py
```

Change the values in the `##VARIABLES##` sections to size a different aircraft,
wing span, fuselage width, launch speed, or S7055 polar data.

The wing calculator uses an elliptical lift distribution across the span and
prints a simple half-wing table.
