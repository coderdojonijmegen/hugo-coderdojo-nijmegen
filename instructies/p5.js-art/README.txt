p5.js-art
=========

Dit archief bevat instructies voor het maken van kunst met de p5.js bibliotheek.

De pagina is zichtbaar via https://coderdojo-nijmegen.nl/instructies/p5.js-art/.

Deze instructie maakt gebruik van https://github.com/toolness/p5.js-widget voor het zelf-hosten van een
p5.js editor. Via https://github.com/toolness/p5.js-widget/archive/gh-pages.zip kun je een copy downloaden van wat
toolness host op zijn/haar site.

Om het geschikt te maken voor gebruik voor dojos zijn er de volgende aanpassingen gedaan:
 - de p5.js bibliotheek wordt lokaal gehost
        //cdnjs.cloudflare.com/ajax/libs/p5.js/"+e+"/p5.js => p5.js_"+e+"/p5.js in preview-frame.bundle.js
        de p5.js bibliotheek gedownload naar p5.js_0.4.23/p5.js
 - het kleine preview-schermpje vergroot naar 800 x 800 px
        zoek op PREVIEW_WIDTH en HEIGHT in p5-widgets.js en main.bundle.js en vervang 150 en 300 door 800 en 800
 zie: https://github.com/coderdojonijmegen/p5.js-art/commit/5690941a0d479ab5d2018a781c40537ea3816521