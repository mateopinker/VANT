# Mission Requirements

This file defines what the VANT must achieve before detailed aerodynamic, structural, CAD, or CFD work is considered valid.

Values marked `TBD` must be replaced with measured, calculated, or agreed values before freezing the preliminary design.

## 1. Mission Definition

| Requirement | Current value | Status | Notes |
| --- | --- | --- | --- |
| Aircraft type | Fixed-wing VANT / UAV | Assumed | Confirm whether VTOL or hybrid capability is excluded. |
| Main mission | Learning / prototype aircraft | Provisional | Replace with the real mission: mapping, surveillance, endurance, payload delivery, testing platform, etc. |
| Secondary mission | Aerodynamic design and CFD learning platform | Provisional | Useful for documenting aero, fuselage, and wing design decisions. |
| Operating environment | Outdoor, low-altitude flight | Assumed | Define wind limits and field conditions. |
| Crew / control | Remotely piloted or autopilot-assisted | TBD | Define whether fully manual, stabilized, autonomous, or mixed. |

## 2. Takeoff and Landing

| Requirement | Current value | Status | Notes |
| --- | --- | --- | --- |
| Takeoff method | TBD | Open | Choose: hand launch, wheels, catapult, bungee, or other. |
| Landing method | TBD | Open | Choose: belly landing, wheels, parachute, net, or other. |
| Required takeoff distance | TBD | Open | Only relevant if using wheels/runway. |
| Required landing distance | TBD | Open | Only relevant if using wheels/runway. |
| Minimum safe launch speed | TBD | Open | Should be above stall speed with margin. |

## 3. Performance Targets

| Requirement | Symbol | Current value | Status | Notes |
| --- | --- | --- | --- | --- |
| Estimated takeoff mass | `m_TO` | TBD kg | Open | First critical value. Include mass margin. |
| Design weight | `W = m_TO g` | TBD N | Open | Calculated from takeoff mass. |
| Cruise speed | `V_cruise` | TBD m/s | Open | Needed for Reynolds number and drag estimates. |
| Stall speed target | `V_stall` | TBD m/s | Open | Drives required wing area. |
| Maximum speed | `V_max` | TBD m/s | Open | Needed for structural and control checks. |
| Endurance | `t_flight` | TBD min | Open | Drives battery sizing. |
| Range | `R` | TBD km | Open | Depends on cruise speed and endurance. |
| Operating altitude | `h` | TBD m | Open | Affects air density if not near sea level. |
| Maximum wind for flight test | `V_wind,max` | TBD m/s | Open | Important for first flights. |

## 4. Preliminary Sizing Requirements

| Quantity | Symbol | Required? | Notes |
| --- | --- | --- | --- |
| Wing area | `S` | Yes | From stall speed and lift coefficient. |
| Wingspan | `b` | Yes | Limited by manufacturing, transport, and stiffness. |
| Mean aerodynamic chord | `MAC` / `c̄` | Yes | Needed for Reynolds number and static margin. |
| Aspect ratio | `AR = b²/S` | Yes | Affects induced drag and wing structural difficulty. |
| Wing loading | `W/S` | Yes | One of the most important aircraft-level parameters. |
| Thrust-to-weight ratio | `T/W` | Yes | Needed for climb and launch safety. |
| Reynolds number | `Re = ρVc/μ` | Yes | Needed before selecting airfoil. |
| Static margin | `SM = (x_NP - x_CG)/c̄` | Yes | Needed for longitudinal stability. |

## 5. Payload Requirements

| Requirement | Current value | Status | Notes |
| --- | --- | --- | --- |
| Payload type | TBD | Open | Camera, sensor, dummy payload, telemetry, etc. |
| Payload mass | TBD kg | Open | Must be included in mass budget. |
| Payload dimensions | TBD mm | Open | Drives fuselage internal volume. |
| Payload access | TBD | Open | Define whether removable, fixed, or service hatch required. |
| Payload CG location constraint | TBD | Open | Important for stability and battery placement. |

## 6. Propulsion and Power Requirements

Known information comes from the current BOM and electrical wiring notes.

| Component | Current value | Status | Notes |
| --- | --- | --- | --- |
| Battery architecture | 6S LiPo system | Provisional | Wiring document assumes 6S LiPo, 22.2 V nominal and 25.2 V full charge. |
| Motor | T-Motor P60C V2, 150 kv, 6S-compatible, max 2400 W according to BOM | Received / provisional | Verify exact datasheet, propeller, current, and thrust data. |
| ESC | TBD, 6S-rated | Open | Must be selected/confirmed before power tests. |
| Propeller | TBD | Open | Critical for thrust, efficiency, current draw, and ground clearance. |
| DC-DC / BEC | 2-6S BEC, 5 A, selectable output | Ordered | Confirm output voltage and current before powering flight controller. |
| Connectors | XT90 connector sets | Ordered | Check current rating and solder quality. |

## 7. Flight Control and Electronics Requirements

| Requirement | Current value | Status | Notes |
| --- | --- | --- | --- |
| Flight controller | TBD | Open | Define Pixhawk, Matek, SpeedyBee, Arduino, custom, etc. |
| Receiver / telemetry | TBD | Open | Needed for control and range. |
| Servos | MG90S micro servos, 5 units ordered | Provisional | Verify torque, backlash, voltage, and control surface loads. |
| Servo voltage | TBD | Open | Depends on BEC output and servo limits. |
| GPS | TBD | Open | Needed for autonomous navigation. |
| Airspeed sensor | TBD | Open | Strongly recommended for fixed-wing autopilot tuning. |

## 8. Manufacturing Requirements

| Requirement | Current value | Status | Notes |
| --- | --- | --- | --- |
| Fuselage manufacturing | TBD | Open | Likely CAD-designed; confirm 3D printing/material strategy. |
| Wing manufacturing | Fiberglass cloth and carbon tubes available/ordered | Provisional | Define whether foam core, ribs + skin, or molded/composite method. |
| Composite material | Ultrafine fiberglass cloth, 1 m x 1.27 m x 0.03 mm, 4 units ordered | Ordered | Confirm areal weight and resin compatibility. |
| Spar/reinforcement | Carbon fiber tubes, size TBD | Ordered | Need exact diameter, wall thickness, length, and bending stiffness. |
| 3D printer volume | TBD | Open | Drives fuselage segmentation and joint design. |
| Adhesive / resin | TBD | Open | Must be compatible with fiberglass, carbon, foam, and printed material. |

## 9. Safety Requirements

| Requirement | Current value | Status | Notes |
| --- | --- | --- | --- |
| Propeller removed during electrical tests | Required | Active | Already stated in electrical first power-up checklist. |
| Battery polarity check | Required | Active | Required before any power-up. |
| Flight controller never connected to raw 6S | Required | Active | Use regulated 5 V only unless documentation says otherwise. |
| Range check before first flight | TBD | Open | Must be added to flight test checklist. |
| CG check before every flight | Required | Open | Define acceptable CG range. |
| Control direction check before every flight | Required | Open | Must be added to preflight checklist. |

## 10. Definition of a Valid Preliminary Design

The preliminary design is not valid until the following are available:

- [ ] Mission type selected.
- [ ] Takeoff and landing methods selected.
- [ ] Initial mass budget completed.
- [ ] Target stall speed selected.
- [ ] Wing area calculated.
- [ ] Wingspan, chord, and aspect ratio selected.
- [ ] Reynolds number range estimated.
- [ ] Airfoil candidates compared at the correct Reynolds number.
- [ ] Propeller, ESC, and battery combination checked.
- [ ] Fuselage internal layout defined.
- [ ] CG range estimated.
- [ ] Static margin estimated.
- [ ] First flight test checklist created.
