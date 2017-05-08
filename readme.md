# Grapher

A super simple graphing calculator. Kind of a joke? I guess?

```
$ python grapher.py
enter a formula to graph in terms of x
functions like sin, tan, ln, floor, and sqrt are allowed
as are pi and e. exponentiation is allowed (e.g. x^2) but for non-integer
exponents e.g. pow(x, 2.2) should be used instead
EXAMPLE: y(x) = 2sin(x)
EXAMPLE: y(x) = ln(0.5x^2)
EXAMPLE: y(x) = pow(x, 3.3)
y(x) = tanx sinx
┌──────────────────────────────────────┬───────────────────────────────────────┐
│                                      │                                       │
│                            ▐         ┼ 4        ▌                            │
│                                      │                                       │
▐                                      ┼ 3                                     │
│                             ▐        │         ▌                             │
│                                      ┼ 2                                     │
│                              ▐       │        ▌                              │
│                               ▐      │       ▌                               │
│                                ▐     ┼ 1    ▌                                │
-5     -4      -3      -2      -1 ▚▚   0    ▞▞ 1       2       3       4       │
├──────┼────▀▀▀┼▀▀▚────┼───────┼────▚▀▀┼▀0▀▞───┼───────┼─────▞▀┼▀▀▀▀───┼───────┤
│        ▞▞▞       ▚▚                  │                   ▞▞       ▚▚▚        │
│       ▌            ▐▐                ┼ -1              ▌▌            ▐       │
│      ▌                               │                                ▐      │
│     ▌                ▐               │                ▌                ▐     │
│                       ▐              ┼ -2            ▌                       │
│    ▌                                 │                                  ▐    │
│                                      ┼ -3                                    │
│                        ▐             │              ▌                        │
│                                      ┼ -4                                    │
│   ▌                                  │                                   ▐   │
└──────────────────────────────────────┴─-5────────────────────────────────────┘
```

What, did you expect it to be pretty? It’s got an effective resolution of
160×48!

# FAQ

*Q:* Can you move the window around or zoom at all?

*A:* No. Maybe one day!

*Q:* Isn’t `tanx sinx` equal to `sin(x)^2 secx`?

*A:* Yes. But one requires parenthesis, so...
