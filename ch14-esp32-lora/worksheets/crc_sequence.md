# Worksheet -- CRC and sequence number

| Field | Your value |
| --- | --- |
| Encode command / hex dump | |
| Decoded seq | |
| Decoded name | |
| CRC match? (yes/no) | |
| What happens if you flip one hex nibble? | |

Commands:

```
python tools/build_packet.py encode --seq 1 --name ping --lat 0 --lon 0
python tools/build_packet.py decode <hex>
```

Why sequence numbers matter on a two-node ping (one sentence):

>
