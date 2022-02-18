# Term Project Proposal

## Description

Our pen plotter project will use a cylindrical axis system, and it involves a radial arm that rotates around a hub and a lead screw that moves the pen 
radially. One motor will rotate the hub, which will rotate the radial arm, and another motor will rotate the lead screw. We will attach the lead screw nut
to the pen using a 3D printed part. The nut in the lead screw will ideally be translating linearly and not rotating; to prevent the pen from rotating, 
we will incorporate a slider mechanism above the lead screw and attach the corresponding moving piece to the pen carrier as well. We plan to 3D print a 
mount to keep both motors at the origin (which we will define as the top-middle position of the paper). For the radial arm, we will have a drive shaft 
connected to the rotating hub. The other end of the drive shaft will be connected to a wheel that will assist in the rotation of the radial arm. There will 
be a 3D printed support wheel attached to the end of the slider and lead screw combination to prevent system failure from the weight of the components
similar to cantilever beam deflection.

To move the pen vertically, we will be using a solenoid. The solenoid will control the pen displacement and determine whether or not the pen is in 
contact with the paper. The entire assembly will be mounted on an acrylic platform. This way, the paper can be placed on top of a flat and smooth surface 
to ensure accurate and smooth strokes. The motors and the solenoid will be controlled using the Nucleo L476 development board and Shoe provided by 
the ME405 Tub.

## Bill of Materials

| Qty. | Part                     | Source                | Est. Cost |
|:----:|:-------------------------|:----------------------|:---------:|
|  2   | Pittperson Gearmotors    | ME405 Tub             |     -     |
|  1   | Nucleo with Shoe         | ME405 Tub             |     -     |
|  1   | Black  Sharpie&trade;    | Home                  |     -     |
|  2   | Motor Mount Parts        | Innovation Sandbox    |     -     |
|  1   | Pen Carrier              | Innovation Sandbox    |     -     |
|  1   | Support Wheel            | Innovation Sandbox    |     -     |
|  1   | V-Slot Framing Extrusion | Innovation Sandbox    |     -     |
|  1   | Solenoid                 | Digikey               |   $4.95   |
|  1   | Track Roller Bearings    | Amazon                |   $10.99  |
|  1   | Driving Wheel            | Amazon                |     $     |
|  1   | Drive Shaft?             | Amazon               |     $     |

## Scaled Sketch of Proposed System

