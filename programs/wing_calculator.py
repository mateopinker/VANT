"""Basic wing sizing calculator for the VANT project.

This is a first-pass estimator for project notes. It uses simple textbook
relationships and assumes steady level flight at sea-level density by default.
"""

from __future__ import annotations

import argparse
import math
import sys
from dataclasses import dataclass


SEA_LEVEL_DENSITY_KG_M3 = 1.225
GRAVITY_M_S2 = 9.80665


@dataclass(frozen=True)
class WingInputs:
    mass_kg: float
    span_m: float
    cruise_speed_ms: float
    cl_max: float
    air_density_kg_m3: float = SEA_LEVEL_DENSITY_KG_M3
    area_m2: float | None = None
    chord_m: float | None = None
    root_chord_m: float | None = None
    tip_chord_m: float | None = None


@dataclass(frozen=True)
class WingResults:
    area_m2: float
    mean_chord_m: float
    aspect_ratio: float
    weight_n: float
    wing_loading_kg_m2: float
    wing_loading_n_m2: float
    required_cl_at_cruise: float
    stall_speed_ms: float
    stall_speed_kmh: float


def positive_float(value: str) -> float:
    number = float(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return number


def prompt_positive(label: str, default: float | None = None) -> float:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        raw = input(f"{label}{suffix}: ").strip()
        if not raw and default is not None:
            return default
        try:
            value = float(raw)
        except ValueError:
            print("Enter a number greater than zero.")
            continue
        if value > 0:
            return value
        print("Enter a number greater than zero.")


def prompt_optional_positive(label: str) -> float | None:
    raw = input(f"{label} [blank if unknown]: ").strip()
    if not raw:
        return None
    try:
        value = float(raw)
    except ValueError:
        print("Value ignored because it was not a number.")
        return None
    if value <= 0:
        print("Value ignored because it was not greater than zero.")
        return None
    return value


def area_and_mean_chord(inputs: WingInputs) -> tuple[float, float]:
    if inputs.area_m2 is not None:
        return inputs.area_m2, inputs.area_m2 / inputs.span_m

    if inputs.chord_m is not None:
        area = inputs.span_m * inputs.chord_m
        return area, inputs.chord_m

    if inputs.root_chord_m is not None and inputs.tip_chord_m is not None:
        mean_chord = (inputs.root_chord_m + inputs.tip_chord_m) / 2
        area = inputs.span_m * mean_chord
        return area, mean_chord

    raise ValueError(
        "provide wing area, rectangular chord, or both root and tip chord"
    )


def calculate(inputs: WingInputs) -> WingResults:
    area_m2, mean_chord_m = area_and_mean_chord(inputs)
    weight_n = inputs.mass_kg * GRAVITY_M_S2
    aspect_ratio = inputs.span_m**2 / area_m2
    wing_loading_kg_m2 = inputs.mass_kg / area_m2
    wing_loading_n_m2 = weight_n / area_m2
    dynamic_pressure = 0.5 * inputs.air_density_kg_m3 * inputs.cruise_speed_ms**2
    required_cl_at_cruise = weight_n / (dynamic_pressure * area_m2)
    stall_speed_ms = math.sqrt(
        (2 * weight_n) / (inputs.air_density_kg_m3 * area_m2 * inputs.cl_max)
    )

    return WingResults(
        area_m2=area_m2,
        mean_chord_m=mean_chord_m,
        aspect_ratio=aspect_ratio,
        weight_n=weight_n,
        wing_loading_kg_m2=wing_loading_kg_m2,
        wing_loading_n_m2=wing_loading_n_m2,
        required_cl_at_cruise=required_cl_at_cruise,
        stall_speed_ms=stall_speed_ms,
        stall_speed_kmh=stall_speed_ms * 3.6,
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Calculate first-pass wing sizing values for VANT."
    )
    parser.add_argument("--mass-kg", type=positive_float, help="aircraft mass in kg")
    parser.add_argument("--span-m", type=positive_float, help="wingspan in meters")
    parser.add_argument("--area-m2", type=positive_float, help="known wing area")
    parser.add_argument("--chord-m", type=positive_float, help="rectangular chord")
    parser.add_argument("--root-chord-m", type=positive_float, help="root chord")
    parser.add_argument("--tip-chord-m", type=positive_float, help="tip chord")
    parser.add_argument(
        "--cruise-speed-ms",
        type=positive_float,
        help="target cruise speed in meters per second",
    )
    parser.add_argument(
        "--cl-max",
        type=positive_float,
        default=1.2,
        help="maximum lift coefficient used for stall estimate",
    )
    parser.add_argument(
        "--rho",
        type=positive_float,
        default=SEA_LEVEL_DENSITY_KG_M3,
        help="air density in kg/m^3",
    )
    return parser


def interactive_inputs() -> WingInputs:
    print("VANT wing calculator")
    print("Leave area/chord fields blank except the geometry you know.")
    mass_kg = prompt_positive("Aircraft mass, kg")
    span_m = prompt_positive("Wingspan, m")
    area_m2 = prompt_optional_positive("Known wing area, m^2")
    chord_m = None
    root_chord_m = None
    tip_chord_m = None

    if area_m2 is None:
        chord_m = prompt_optional_positive("Rectangular chord, m")

    if area_m2 is None and chord_m is None:
        root_chord_m = prompt_positive("Root chord, m")
        tip_chord_m = prompt_positive("Tip chord, m")

    cruise_speed_ms = prompt_positive("Cruise speed, m/s")
    cl_max = prompt_positive("Estimated CL max", 1.2)
    air_density_kg_m3 = prompt_positive(
        "Air density, kg/m^3", SEA_LEVEL_DENSITY_KG_M3
    )

    return WingInputs(
        mass_kg=mass_kg,
        span_m=span_m,
        cruise_speed_ms=cruise_speed_ms,
        cl_max=cl_max,
        air_density_kg_m3=air_density_kg_m3,
        area_m2=area_m2,
        chord_m=chord_m,
        root_chord_m=root_chord_m,
        tip_chord_m=tip_chord_m,
    )


def inputs_from_args(args: argparse.Namespace) -> WingInputs:
    required = {
        "--mass-kg": args.mass_kg,
        "--span-m": args.span_m,
        "--cruise-speed-ms": args.cruise_speed_ms,
    }
    missing = [name for name, value in required.items() if value is None]
    if missing:
        raise ValueError(f"missing required argument(s): {', '.join(missing)}")

    geometry_count = sum(
        [
            args.area_m2 is not None,
            args.chord_m is not None,
            args.root_chord_m is not None or args.tip_chord_m is not None,
        ]
    )
    if geometry_count != 1:
        raise ValueError(
            "provide exactly one geometry method: --area-m2, --chord-m, "
            "or --root-chord-m with --tip-chord-m"
        )
    if (args.root_chord_m is None) != (args.tip_chord_m is None):
        raise ValueError("--root-chord-m and --tip-chord-m must be used together")

    return WingInputs(
        mass_kg=args.mass_kg,
        span_m=args.span_m,
        cruise_speed_ms=args.cruise_speed_ms,
        cl_max=args.cl_max,
        air_density_kg_m3=args.rho,
        area_m2=args.area_m2,
        chord_m=args.chord_m,
        root_chord_m=args.root_chord_m,
        tip_chord_m=args.tip_chord_m,
    )


def print_results(results: WingResults) -> None:
    print("\nWing estimate")
    print("-------------")
    print(f"Wing area:              {results.area_m2:.4f} m^2")
    print(f"Mean chord:             {results.mean_chord_m:.4f} m")
    print(f"Aspect ratio:           {results.aspect_ratio:.2f}")
    print(f"Aircraft weight:        {results.weight_n:.2f} N")
    print(f"Wing loading:           {results.wing_loading_kg_m2:.2f} kg/m^2")
    print(f"Wing loading:           {results.wing_loading_n_m2:.2f} N/m^2")
    print(f"Required CL at cruise:  {results.required_cl_at_cruise:.2f}")
    print(f"Estimated stall speed:  {results.stall_speed_ms:.2f} m/s")
    print(f"Estimated stall speed:  {results.stall_speed_kmh:.2f} km/h")


def main(argv: list[str]) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        inputs = interactive_inputs() if not argv else inputs_from_args(args)
        print_results(calculate(inputs))
    except ValueError as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
