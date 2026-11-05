# Self Induction **&** Mutual Induction

_Electromagnetism · Inductance_

## Self induction

Self induction is the phenomenon in which a changing current in a coil induces an emf in the **same coil**.

_(figure drawn with TikZ on the PNG)_

$$ e=-L\,\frac{dI}{dt} $$

- $e$ : induced emf (V)
- $L$ : self inductance (H)
- $dI/dt$ : rate of change of current (A/s)

**Key points**

- Also called the **back emf**.
- Depends on the number of turns, the area of the coil and the core material.
- Unit of inductance: henry (H).

**Example**

- Switch on a fan or a motor: the current does not rise instantly.
- Self induction resists the sudden change.

## Mutual induction

Mutual induction is the phenomenon in which a changing current in one coil induces an emf in **another nearby coil**.

_(figure drawn with TikZ on the PNG)_

$$ e_2=-M\,\frac{dI_1}{dt} $$

- $e_2$ : induced emf in the secondary (V)
- $M$ : mutual inductance (H)
- $dI_1/dt$ : rate of change of the primary current (A/s)

**Key points**

- Needs **two coils**.
- Depends on the distance between the coils, the number of turns and the core material.
- The basis of transformers.

**Example**

- A transformer moves energy from one coil to the other.
- No direct electrical connection between the coils.

## Self induction vs mutual induction

| | Self induction | Mutual induction |
|---|---|---|
| Coils | One coil | Two coils |
| Emf induced in | The same coil | The second coil |
| Cause | Its own current change | Current change in the nearby coil |
| Example | Inductor, choke | Transformer |
