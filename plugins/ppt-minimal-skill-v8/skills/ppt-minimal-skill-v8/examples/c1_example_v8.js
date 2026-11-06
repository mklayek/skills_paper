// v8 example section file (adapted from the EM interpretation deck, Telford 7.7).
// Write slides as you would split them by hand. head.js pools the T/S/TB calls of one topic,
// re-splits them at 22 pt so every slide fills, and gives continued slides only the black label.
const CR = 'Telford, Geldart and Sheriff, Applied Geophysics';

SEC('FDEM over Dipping Sheet: Dip-Angle Systems', 'General · Fixed vertical-loop transmitter · Broadside');

// Topic start: title box, body 6.53 H x 13.07 W. The ' › General' part becomes the first sub-point.
T('●  Ground Systems: FDEM over Dipping Sheet › General', '', [
  'Common configuration for conductive zones → a thin sheet, long in the strike direction → variable dip and depth extent',
  'Large conductivity or high frequency → induced current assumed to flow mainly along the top edge → return at depth',
]);

// Figure slide of the same topic: body on the left half, figure on the right half.
// A new sub-part name ('Dip-Angle: Fixed Vertical-Loop Transmitter') is inserted as a bold underlined '#' heading.
S('●  Ground Systems: FDEM over Dipping Sheet › Dip-Angle: Fixed Vertical-Loop Transmitter', '', [
  'Transmitter coil → located if possible over the top of the conductor → pointed at successive receiver stations',
  'Vertical component → entirely due to the secondary field → horizontal the sum of the secondary and primary fields',
], 'fig_7_29', '(a) Plan view, (b) elevation showing receiver signals | ' + CR);

// Same topic continued: no title box, black label only, body 6.87 H x 13.04 W.
// Bullets from here are pulled forward onto the slide above when they fit.
T('●  Ground Systems: FDEM over Dipping Sheet › Dip-Angle: Fixed Vertical-Loop Transmitter (continued)', '', [
  'Tilt of the receiver coil → dip angle δ from the vertical and total horizontal fields',
  '§#13',                                                                  // source equation, kept with its lead-in
  '› δ | dip angle;  H_{z}^{s} | vertical secondary field;  H_{x}^{t} | total horizontal component',
  '# Sign convention',                                                     // explicit sub-point: bold + underlined
  'Dip angle positive to the left, negative to the right of the sheet → traverse proceeding from left to right',
  'Sign convention → could as easily be in the opposite sense → must be consistent to avoid confusion',
]);
