// Example section file for ppt-minimal-skill-v7: EVERY bullet is an arrow chain.
// Topic: sources of the induced-polarization effect (Telford-style passage).
// No title slide and no closing slide here: frame.py adds the class title slide (method name,
// method group, lecture number from deck_config.json) and the Thank you slide after the build.
//
// Title syntax (V7.4):
//   '■  Topic'                    first slide of a topic   -> centered, new font + dark color
//   '■  Topic (continued)'        same topic               -> left-aligned, same font + color
//   '■  Topic › Sub-topic'        same topic, sub-topic    -> black label "Topic" + left title "Sub-topic"
//   '★■  Topic'                   very important title     -> gold oval, centered
// Chains (V7.2, V7.3): 2 or 3 segments, one arrow direction, source words kept in the middle segment.

// optional intro topic (the source has an introduction): centered, font 1
T('■  Sources of the IP Effect','',[
  'Induced polarization → energy stored in the rock during current flow → the decay is a return to the original state',
  'Stored energy → possibly mechanical, electrical or chemical → laboratory studies show chemical energy is by far the most important',
  'Two sources → membrane polarization and electrode polarization → indistinguishable by IP measurement']);

SEC('Membrane Polarization','Ions at the pore interface · clay and salinity · background polarization');

// a very important title: gold oval, starts a new topic. Beside an image: 4 chains at most (V7.2)
S('★■  Membrane Polarization','',[
  'Electrolytic conduction → the predominant factor in most rocks → the rock must be somewhat porous',
  'Pore interface → most rock minerals have a net negative charge → positive ions attracted, negative ions repelled',
  'Pore as narrow as the zone → negative ions accumulate at one end of the zone → current flow is impeded',
  // effect first, explained by its cause: read "is caused by" in place of the arrow
  'IP decay after switch-off ← the ions return to their original positions, taking a finite time'],
  'fig_9_2','Membrane and electrode polarization at the pore scale (illustrative schematic after Telford et al.)');

// same topic: left-aligned, same font and color
T('■  Membrane Polarization (continued)','',[
  'Positive-ion zone → may extend into the fluid to about 10^{−6} cm',
  'Strongest membrane effect ← clay minerals, in which the pores are particularly small',
  'Clay content → the polarization does not increase steadily → reaches a maximum and then decreases',
  'Decrease at high clay content ← no alternate passages of larger cross section and very short length',
  'Larger membrane effect ← higher salinity of the pore fluid']);

// same topic continues with a sub-topic: black label "Membrane Polarization" + title "Background Polarization"
T('■  Membrane Polarization › Background Polarization','',[
  'Minor sources → normal dielectric and electrokinetic effects, tiny amounts of conducting minerals',
  'Their size → none is comparable to membrane polarization',
  'Overall background → roughly a rock containing 1 to 2 % conducting minerals',
  'Background polarization → cannot be distinguished from electrode polarization → a level of geological noise']);

SEC('Electrode Polarization','Overvoltage at metallic grains · disseminated versus massive · chargeability');

// new topic: centered, next font
T('■  Electrode Polarization','',[
  'Electrode polarization → exists when metallic material is present → current flow partly electronic and partly electrolytic',
  'Mineral and solution interface → a chemical reaction occurs → electrolysis, called overvoltage in physical chemistry',
  'Ion pile-up at the interface ← current flows much more slowly in the electrolyte than in the metal',
  'Residual voltage after the current stops ← the ions diffusing back to their original state',
  'Surface phenomenon → overvoltage larger for disseminated than for massive mineral']);

// equations sit on chain slides unchanged: the lead-in is a chain ending with a colon
T('■  Electrode Polarization (continued)','Definition: chargeability',[
  'Chargeability → the area under the decay curve, normalized by the voltage during current flow:',
  '§#1',
  '› M | chargeability;  V_{c} | voltage during current flow;  V(t) | decaying voltage;  t_{1}, t_{2} | window start and end',
  'Integration window → between times t_{1} and t_{2} after the current is switched off']);

// the Summary is an ordinary topic: new font, centered
T('◆  Summary','',[
  'Membrane polarization → negative ions accumulate in narrow pores → current flow is impeded',
  'Electrode polarization → overvoltage at the metal and solution interface → larger for disseminated than for massive mineral',
  'Geological noise ← background polarization, indistinguishable from electrode polarization']);
