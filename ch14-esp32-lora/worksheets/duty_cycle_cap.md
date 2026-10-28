# Worksheet -- software duty-cycle cap

Not legal advice. Map to your Chapter 3 jurisdiction worksheet and ERC/REC 70-03 planning entry if EU SRD.

| Field | Your value |
| --- | --- |
| SRD / licence path cited | |
| Official URL + access date | |
| Planning duty-cycle percent | |
| Packet bytes (from encode tool) | |
| Estimated airtime_ms (SF/BW match firmware) | |
| Ping interval_ms | |
| Max packets / hour (tool or arithmetic) | |

Command used:

```
python tools/duty_cycle_cap.py --percent ... --airtime-ms ... --packets ... --interval-ms ...
```

Sentence stating the constraint you will enforce in firmware (`DUTY_CYCLE_PERCENT`):

>
