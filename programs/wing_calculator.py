"""Basic wing sizing calculator for the VANT project.

This is a first-pass estimator for project notes. It uses simple textbook
relationships and assumes steady level flight at sea-level density by default.
The calculator is configured around takeoff performance, but can be easily
modified to size for cruise or landing.
"""

import math

#####################################################
#####################################################
################# THRUST CALCULATOR #################
#####################################################
#####################################################

##VARIABLES##
mass = 2.50  # mass of the aircraft in kg
thrust = 20  # thrust available in Newtons at takeoff
velocity_launch = 10  # takeoff velocity in m/s
drop_height = 0.5  # drop height in meters for takeoff
angle_of_attack = 15  # thrust angle in degrees at takeoff
air_density = 1.225  # air density at sea level in kg/m^3
gravity = 9.81  # gravity in m/s^2


##CALCULATIONS##
drop_time = math.sqrt(2 * drop_height / gravity)
extra_speed = (thrust / mass) * drop_time  # extra speed gained from thrust during drop
final_velocity = velocity_launch + extra_speed  # final takeoff velocity in m/s

lift_required = mass * gravity  # lift required to balance weight in Newtons

# Thrust lift component
thrust_lift = thrust * math.sin(math.radians(angle_of_attack))

# Wing lift component
wing_lift = lift_required - thrust_lift


##OUTPUTS##
print(f"Lift required: {lift_required:.2f} N")
print(f"Thrust lift component: {thrust_lift:.2f} N")
print(f"Wing lift component: {wing_lift:.2f} N")
print(f"Final takeoff velocity: {final_velocity:.2f} m/s")


#####################################################
#####################################################
#################### WING SIZING ####################
#####################################################
#####################################################

##VARIABLES##
wing_span = 1.6  # total tip-to-tip wingspan in meters
fuselage_width = 0.09  # center fuselage width in meters, this part does not make lift
sections_per_half_wing = 10   # number of sections from fuselage side to wing tip
lift_margin = 1.00  # multiply wing lift by this for safety margin
kinematic_viscosity = 1.46e-5  # air kinematic viscosity in m^2/s

bottom_bracket = 0.005  # minimum chord checked in m
top_bracket = 0.50  # maximum chord checked in m
exit_step = 0.001  # acceptable lift error as fraction of target lift
max_iterations = 1000

s7055_polars = [
    (50000, 8.5, 1.1260, 0.03122),
    (100000, 9, 1.1926, 0.02335),
    (200000, 10.5, 1.2375, 0.02594),
    (500000, 12, 1.3135, 0.02908),
    (1000000, 12.75, 1.3914, 0.02776),
]
# Re, AoA, Cl, Cd (AoA taken 2 degrees off of max Cl to avoid stall and Ncrit = 5)


##FUNCTIONS##
def interp_s7055_polar(Re):
    """
    Linear interpolation of the S7055 polar.
    Reynolds number selects AoA, Cl and Cd.
    No extrapolation beyond the data range.
    """
    Re0, a0, cl0, cd0 = s7055_polars[0]
    ReN, aN, clN, cdN = s7055_polars[-1]

    if Re <= Re0:
        return a0, cl0, cd0
    if Re >= ReN:
        return aN, clN, cdN

    n = 0
    while n != len(s7055_polars) - 1:
        Re_low, a_low, cl_low, cd_low = s7055_polars[n]
        Re_high, a_high, cl_high, cd_high = s7055_polars[n + 1]

        if Re <= Re_high:
            t = (Re - Re_low) / (Re_high - Re_low)
            AoA = a_low + t * (a_high - a_low)
            Cl = cl_low + t * (cl_high - cl_low)
            Cd = cd_low + t * (cd_high - cd_low)
            return AoA, Cl, Cd

        n = n + 1

    return aN, clN, cdN


def elliptical_lift_per_span(y, total_lift, span):
    """
    Ideal finite-wing lift distribution:
    L'(y) = 4L/(pi*b) * sqrt(1 - (2y/b)^2)
    """
    inside_root = 1 - (2 * y / span) ** 2

    if inside_root < 0:
        inside_root = 0

    lift_per_span = (4 * total_lift / (math.pi * span)) * math.sqrt(inside_root)

    return lift_per_span


def elliptical_section_lift(y_inner, y_outer, total_lift, span):
    """
    Exact lift in one spanwise section from the same elliptical distribution.
    """
    u_inner = 2 * y_inner / span
    u_outer = 2 * y_outer / span

    def ellipse_integral(u):
        return u * math.sqrt(max(0, 1 - u**2)) + math.asin(u)

    section_lift = (total_lift / math.pi) * (
        ellipse_integral(u_outer) - ellipse_integral(u_inner)
    )

    return section_lift


def lift_per_span_for_chord(chord):
    """
    Lift per unit span produced by this local chord.
    Chord changes Reynolds number, so Cl changes too.
    """
    Re = final_velocity * chord / kinematic_viscosity
    AoA, Cl, Cd = interp_s7055_polar(Re)
    dynamic_pressure = 0.5 * air_density * final_velocity**2
    lift_per_span = dynamic_pressure * chord * Cl
    drag_per_span = dynamic_pressure * chord * Cd

    return lift_per_span, drag_per_span, AoA, Cl, Cd, Re


def chord_for_lift_per_span(target_lift_per_span):
    """
    Bisection search for the chord that gives the wanted local lift per span.
    This is the same basic idea as the prop code, but for a fixed wing section.
    """
    lower_chord = bottom_bracket
    upper_chord = top_bracket

    lift_high = lift_per_span_for_chord(upper_chord)[0]

    if lift_high < target_lift_per_span:
        raise ValueError("top_bracket is too small for the elliptical lift distribution")

    chord = (lower_chord + upper_chord) / 2
    iteration = 0

    while iteration < max_iterations:
        chord = (lower_chord + upper_chord) / 2
        lift_mid = lift_per_span_for_chord(chord)[0]
        error = abs(target_lift_per_span - lift_mid)

        if error < exit_step * target_lift_per_span:
            break

        if lift_mid < target_lift_per_span:
            lower_chord = chord
        else:
            upper_chord = chord

        iteration = iteration + 1

    return chord


##CALCULATIONS##
target_wing_lift = wing_lift * lift_margin
dynamic_pressure = 0.5 * air_density * final_velocity**2

if fuselage_width < 0:
    raise ValueError("fuselage_width cannot be negative")

if fuselage_width >= wing_span:
    raise ValueError("fuselage_width must be smaller than wing_span")

lifting_span = wing_span - fuselage_width
semi_span = lifting_span / 2
section_width = semi_span / sections_per_half_wing
fuselage_half_width = fuselage_width / 2

span_stations = []
half_wing_lift = 0
half_wing_area = 0
half_wing_profile_drag = 0
half_wing_chord_squared = 0

n = 0
while n != sections_per_half_wing:
    y_inner = n * section_width
    y_outer = (n + 1) * section_width
    y_mid = (y_inner + y_outer) / 2
    y_from_centerline = fuselage_half_width + y_mid

    lift_per_span = elliptical_lift_per_span(y_mid, target_wing_lift, lifting_span)
    section_lift = elliptical_section_lift(
        y_inner,
        y_outer,
        target_wing_lift,
        lifting_span,
    )

    chord = chord_for_lift_per_span(lift_per_span)
    (
        solved_lift_per_span,
        drag_per_span,
        wing_AoA,
        wing_Cl,
        wing_Cd,
        Reynolds,
    ) = lift_per_span_for_chord(chord)

    section_drag = drag_per_span * section_width

    span_stations.append(
        (
            y_from_centerline,
            y_mid,
            lift_per_span,
            section_lift,
            chord,
            wing_AoA,
            wing_Cl,
            wing_Cd,
            Reynolds,
            section_drag,
        )
    )

    half_wing_lift = half_wing_lift + section_lift
    half_wing_area = half_wing_area + chord * section_width
    half_wing_profile_drag = half_wing_profile_drag + section_drag
    half_wing_chord_squared = half_wing_chord_squared + chord**2 * section_width

    n = n + 1

final_lift = 2 * half_wing_lift
wing_area = 2 * half_wing_area
profile_drag = 2 * half_wing_profile_drag
mean_aero_chord = (2 * half_wing_chord_squared) / wing_area
average_chord = wing_area / lifting_span
aspect_ratio = lifting_span**2 / wing_area
fuselage_side_chord = span_stations[0][4]
tip_chord = span_stations[-1][4]
fuselage_side_Reynolds = span_stations[0][8]
tip_Reynolds = span_stations[-1][8]
fuselage_non_lifting_area = fuselage_width * fuselage_side_chord
total_planform_area_with_fuselage = wing_area + fuselage_non_lifting_area

required_Cl = target_wing_lift / (dynamic_pressure * wing_area)
induced_Cd = required_Cl**2 / (math.pi * aspect_ratio)  # elliptical distribution, e = 1
induced_drag = dynamic_pressure * wing_area * induced_Cd
drag = profile_drag + induced_drag
wing_loading = lift_required / wing_area
mass_loading = mass / wing_area


##OUTPUTS##
print("")
print(f"Target wing lift: {target_wing_lift:.2f} N")
print(f"Elliptical lift check: {final_lift:.2f} N")
print("")
print("Fuselage correction")
print(f"Total wing span: {wing_span:.3f} m")
print(f"Fuselage width: {fuselage_width:.3f} m")
print(f"Lifting wing span: {lifting_span:.3f} m")
print(f"Non-lifting fuselage area approx: {fuselage_non_lifting_area:.3f} m^2")
print(f"Total planform including fuselage strip: {total_planform_area_with_fuselage:.3f} m^2")
print("")
print(f"Fuselage-side chord approx: {fuselage_side_chord:.3f} m")
print(f"Tip chord approx: {tip_chord:.3f} m")
print(f"Average chord: {average_chord:.3f} m")
print(f"Mean aerodynamic chord: {mean_aero_chord:.3f} m")
print(f"Wing area: {wing_area:.3f} m^2")
print(f"Aspect ratio: {aspect_ratio:.2f}")
print(f"Fuselage-side Reynolds approx: {fuselage_side_Reynolds:.0f}")
print(f"Tip Reynolds approx: {tip_Reynolds:.0f}")
print(f"Profile drag estimate: {profile_drag:.2f} N")
print(f"Induced Cd estimate: {induced_Cd:.5f}")
print(f"Induced drag estimate: {induced_drag:.2f} N")
print(f"Drag estimate: {drag:.2f} N")
print(f"Wing loading: {wing_loading:.1f} N/m^2")
print(f"Mass loading: {mass_loading:.2f} kg/m^2")

print("")
print("Half-wing elliptical lift distribution")
print("y(m)     L'(N/m)   dL(N)    chord(m)  AoA(deg)  Cl      Cd       Re")

n = 0
while n != len(span_stations):
    y_from_centerline, y_mid, lift_per_span, section_lift, chord, wing_AoA, wing_Cl, wing_Cd, Reynolds, section_drag = span_stations[n]

    print(
        f"{y_from_centerline:.3f}    "
        f"{lift_per_span:.2f}     "
        f"{section_lift:.2f}     "
        f"{chord:.3f}     "
        f"{wing_AoA:.2f}     "
        f"{wing_Cl:.4f}  "
        f"{wing_Cd:.5f}  "
        f"{Reynolds:.0f}"
    )

    n = n + 1
