# Bill of materials -- Chapter 12

Microcontroller keyer and decoder (practice oscillator / serial decode -- no RF).

| Item | Notes |
| --- | --- |
| ESP32 DevKit (or Arduino Uno / Nano class) | Primary path is ESP32; Uno env is in `platformio.ini` |
| Passivebutton or straight key | Active-low into KEY_PIN with internal pull-up |
| Passive piezo buzzer or small headphone amp | Sidetone on TONE_PIN |
| 10k potentiometer (optional) | WPM control on POT_PIN |
| Breadboard + jumpers | Lab wiring |
| USB cable | Flash and serial monitor |
| Host computer | PlatformIO or Arduino IDE; Python 3.11+ for host tools |
| This companion folder | `ch12-morse-mcu/` in Leo-Galli/signal |

No transmitter module in this chapter. Not legal advice.
