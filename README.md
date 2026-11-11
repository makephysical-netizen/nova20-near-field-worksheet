# NOVA20 near-field evaluation worksheet

**Pilot v0.2. No hardware validation is claimed.** Published by Alex / Benewake through `makephysical-netizen` as an evaluation aid.

This small, dependency-free browser worksheet helps a robot developer reject obviously unsuitable near-field sensor placements. Enter the proposed NOVA20 mounting height, downward tilt, target height and distance. The page reports which evenly spaced nominal rays could cross the target's vertical front-face height band within the entered slant-range window.

**Use it online:** [open the geometry worksheet](https://makephysical-netizen.github.io/nova20-near-field-worksheet/) and [read the bench-test guide](https://makephysical-netizen.github.io/nova20-near-field-worksheet/guide.html).

You can also download this repository and open `index.html` locally. The calculation runs in the browser without an account, telemetry or a network request. The companion `guide.html` describes a repeatable low-object bench test and the raw data to record.

## What the result means

A green ray only passes a simple geometric screen. It does not prove that the sensor will return a valid distance, detect the object's material, or stop a robot. The model assumes a flat floor, a vertical target face, evenly spaced nominal rays and a fan oriented in the target's vertical plane. It omits beam width, reflectivity, ambient light, noise, mounting obstruction, software filtering and vehicle stopping distance.

The defaults use the [official NOVA20 Datasheet V2.1](https://ai.benewake.com/en/resources/technical-documents/nova20-datasheet/) as a **planning reference**: 20 channels, up to 40° field of view, a blind zone of at most 0.1 m and a 1 m range at the datasheet's 10% reflectivity / 100 klux condition. Check the latest specification and the actual channel angles for the hardware revision being tested. The datasheet does not state an enclosure protection rating.

## A useful first test

1. Mark the real missing region in robot coordinates and compare it with the current sensor's data.
2. Fix the mount, target distance, material and ambient light; log raw channel ID, distance, signal strength and invalid returns.
3. Repeat at several distances and lateral positions with the complete robot body installed.
4. Compare measured returns with the nominal geometry before changing obstacle filtering or control logic.

The [NOVA20 product page](https://ai.benewake.com/en/products/nova20/) and [Benewake contact page](https://ai.benewake.com/en/contact/) are the current official paths for product information and technical or sample inquiries. Availability and lead time require confirmation.

## Optional raw UART capture

`capture_raw.py` records the bytes received on a serial port without interpreting frames. A short capture can help compare real hardware output with a protocol document before anyone relies on a driver. It does **not** decode distances, channel angles, signal strength or validity flags, and it has not been tested with a physical NOVA20.

First confirm the exact pinout, voltage levels, wiring and port for your hardware revision using the applicable manual. Then install [pyserial](https://pyserial.readthedocs.io/) and capture to a new file:

```sh
python3 -m pip install pyserial
python3 capture_raw.py --port /dev/ttyUSB0 --output nova20_capture.bin --seconds 10
```

The default baud rate is 921600, as listed on the current NOVA20 product page; pass `--baudrate` if your device is configured differently. Existing output files are never overwritten. The file may contain device or project information: review it before sharing publicly. A zero-byte file means the serial connection produced no bytes during the capture window, not that the sensor is defective.

## Status and feedback

This is an early geometry worksheet, not a certified avoidance tool or a tested driver. Please open an Issue in this repository if the explanation or calculation is unclear; include the input values and the result you expected. Do not post private robot logs or customer information.

No reuse license is included in this pilot. The page may be viewed and run for evaluation; ask Benewake before copying or redistributing the source. A suitable open-source license can be added after company approval.

