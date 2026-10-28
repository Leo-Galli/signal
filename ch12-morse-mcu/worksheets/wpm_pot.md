# Exercise 1 -- Add a WPM pot

Wire a potentiometer to the ADC pin documented for your board
(ESP32 default `POT_PIN=34`, Uno default `A0`). Power the pot from 3.3 V
on ESP32 (not 5 V into an ADC1 pin).

Record three positions:

| Position | adc_raw | adc_max | computed WPM | serial `# WPM` line |
| --- | ---: | ---: | ---: | --- |
| CCW / min |  |  |  |  |
| Mid |  |  |  |  |
| CW / max |  |  |  |  |

Host check (replace numbers with your mid reading):

```bash
python tools/wpm_from_pot.py --json data/sample_pot.json
python tools/wpm_from_pot.py 2048 --adc-max 4095
```

Confirm the tool WPM matches the firmware `# WPM` line within one step.
Practice oscillator only. Not legal advice.
