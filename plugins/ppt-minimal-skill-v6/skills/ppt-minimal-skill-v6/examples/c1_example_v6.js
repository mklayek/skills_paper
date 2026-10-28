// Example section file for ppt-minimal-skill-v6: source slides and arrow-chain slides.
// Topic: gravity reductions (illustrative wording, written in the style of a textbook passage).
// Every content slide is ONE kind. The comment above each call records the choice (V6.1).
// Chain bullets: 2 or 3 segments, one arrow direction, middle segment keeps source words (V6.2, V6.3).

// kind: source (introduction; the class title slide itself comes from frame.py)
T('◆  Gravity Reductions',
  'From observed gravity to a Bouguer anomaly',[
  'Observed gravity contains effects of **latitude**, **elevation**, **topography** and **tides**, which must be removed before geological interpretation.',
  'The deck follows the source in order: latitude, free-air, Bouguer and terrain corrections.',
  'Source: Telford, Geldart and Sheriff, Applied Geophysics, chapter on gravity data reduction.']);

SEC('Elevation Corrections','Free-air correction · Bouguer correction · terrain correction');

// kind: source (a definition through an equation, with its symbols)
T('■  Free-Air Correction','Definition: the free-air correction',[
  'The **free-air correction** accounts for the decrease of gravity with height above the datum, ignoring the material in between:',
  '§ Δg_{FA} = 0.3086 h',
  '› Δg_{FA} | free-air correction (mGal);  h | station height above the datum (m)',
  'It is **added** to the observed value for a station above the datum.']);

// kind: chain (mechanism and consequence statements)
T('■  Free-Air Correction (continued)','',[
  'Free-air correction → gravity decreases with height above the datum as the distance from the Earth’s center increases → stations at different heights become comparable',
  'Correction sign → added for a station above the datum and subtracted below it → keeps the reduced value referenced to the datum',
  'Height accuracy → an error of 1 m in station height gives an error of about 0.3 mGal → heights must be surveyed to a few centimeters for detailed work',
  // effect first, explained by its cause: the left arrow reads "is caused by"
  'Large free-air anomalies in mountains ← the extra rock between station and datum is ignored by the free-air correction']);

// kind: chain
T('■  Bouguer Correction','',[
  'Bouguer correction → removes the attraction of a slab of rock of thickness h between station and datum → leaves the effect of density variations below the datum',
  'Assumed density → a mean crustal value of 2.67 g/cm^{3} is often used → a wrong density leaves a residual correlated with topography',
  'Anomaly correlated with topography ← a Bouguer density that is too high or too low']);

// kind: source (equation and how to use it). A lettered sub-part of the topic -> black label (V6.7)
T('■  Bouguer Correction › Slab Formula','',[
  'For an infinite horizontal slab of density ρ and thickness h:',
  '§ Δg_{B} = 0.04193 ρ h',
  '› Δg_{B} | Bouguer correction (mGal);  ρ | slab density (g/cm^{3});  h | slab thickness (m)',
  'It is **subtracted** for a station above the datum, opposite in sign to the free-air correction.']);

SUMMARY();
// kind: chain (the points are mechanisms and consequences)
T('◆  Summary','',[
  'Free-air correction → gravity decreases with height above the datum → added for stations above the datum',
  'Bouguer correction → removes the attraction of the slab between station and datum → subtracted for stations above it',
  'Residual tracking topography ← a wrong Bouguer density']);
