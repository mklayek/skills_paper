// Example section file for ppt-minimal-skill-v5 (taken from the EM Methods deck).
// Item syntax: 'text' bullet | '§ linear eq' | '§#N' source equation N (eqinv.json) | '› sym | meaning;  sym | meaning'
// Calls: T(title, subtitle, items) full width | S(title, subtitle, items, fig, caption) half + image |
//        TB(title, subtitle, items, rows, colW, caption, fontSize) half + table | SEC(name, contents) divider | SUMMARY()

T('◆  Electromagnetic Methods',
  'Inductive prospecting with alternating and transient fields',[
  'After magnetics, the **electromagnetic (EM)** technique is the most widely used method in mineral exploration. It responds best to **good electrical conductors at shallow depth**.',
  'A transmitter sets up a **primary field**, a buried conductor carries induced currents, and a receiver senses the **secondary field** those currents produce.',
  'The deck follows the chapter in order: theory, equipment and ground systems, airborne systems, interpretation, depth sounding and field examples.',
  'Every equation is a **native PowerPoint equation**, so it can be opened and edited in the equation editor.',
  'Source: ' + SRC + ', chapter on electromagnetic methods.']);

// ============================== Section: Introduction ==============================
SEC('Introduction and History','Where EM is used · frequency domain vs time domain · natural and remote sources');

SEC('Electromagnetic Theory','Potentials · source fields · coupled circuits · phase · mutual inductance · transients');

T('■  Vector and Scalar Potentials','',[
  'EM prospecting uses the same theory as magnetotellurics: **negligible displacement current** and spatial phase shift, with identical boundary conditions. Only the frequencies are somewhat higher.',
  'As in gravity and magnetics, problems are easier to solve through a **potential**, with the field vectors found afterward by differentiation.',
  'Two potentials are introduced: a **vector magnetic potential A** and a **scalar potential φ**. Both electric and magnetic fields follow from them.',
  'A third, the **Hertz vector Π**, is built from A and φ. None of them is physical like the gravity potential, but all are **convenient mathematical tools**.']);

T('■  Vector and Scalar Potentials (continued)','Definition: the vector magnetic potential',[
  'Define the **vector magnetic potential** through the magnetic induction:',
  '§#1',
  '› A | vector magnetic potential (Wb/m);  B | magnetic induction (T)',
  'Faraday’s law, ∇ × E = −∂B/∂t, with B = ∇ × A gives:',
  '§#2',
  'A vector with **zero curl** is the gradient of a scalar, so:',
  '§#3',
  'Rearranging gives the electric field in terms of both potentials:',
  '§#4',
  '› E | electric field (V/m);  φ | scalar potential (V);  t | time (s)',
  '**−∂A/∂t** is the induced emf part of E. **−∇φ** is the potential gradient from current flow in a resistive medium.']);

T('■  Vector and Scalar Potentials (continued)','Definition: the Lorentz condition',[
  'Choose the **Lorentz condition** (Ward, 1967):',
  '§#9',
  'It forces both A and φ to obey the same wave equation as H and E. Substituting into the two coupled equations:',
  '§#10',
  '§#11',
  '› ∇² | Laplacian operator;  με ∂²/∂t² | displacement-current (wave) term;  μσ ∂/∂t | conduction (diffusion) term',
  'So in homogeneous media one **vector** and one **scalar** potential satisfy the **same wave equation as the fields**, the form already met in magnetotellurics.']);

T('■  Vector and Scalar Potentials (continued)','Definition: the Hertz vector',[
  'Still another potential, the **Hertz vector Π**, defines A and φ:',
  '§#12',
  'Manipulation like that for A and φ (Ward, 1967) gives one wave equation with a source term:',
  '§#13',
  '› Π | Hertz vector potential;  K | source term: −P/ε, or −M, or zero;  P, M | electric and magnetic dipole moments per unit volume',
  'The value of **K** depends on the source: electric dipoles, magnetic dipoles or no sources.',
  'Equations for A, φ and Π all share the form of the **MT wave equation**, which is why one solution technique serves every source.']);


SUMMARY();
T('◆  Summary','',[
  'EM methods induce currents in conductors and sense their **secondary field**. The response depends on the **response parameter**, a product of conductivity, permeability, frequency and size.',
  'The secondary field differs in **amplitude and phase** from the primary. The **in-phase to quadrature** ratio separates good from poor conductors.',
  '**FD** systems (dip-angle, VLF, AFMAG, Turam, horizontal loop) are light, cheap and well understood. **TD** systems (PEM, SIROTEM, EM37, UTEM, Input) reach **deeper** and see through conductive overburden.',
  'Interpretation compares field profiles with **model and theoretical curves**, condensed into **characteristic curves** for depth, dip and **conductance σt**.',
  'Overburden, current channeling and loop position can mislead. **Moving the loop**, adding frequencies and combining with **magnetics** reduce the risk.',
  'Airborne EM gives fast reconnaissance and, increasingly, **resistivity mapping**. Ground followup and drilling remain the final test.']);
