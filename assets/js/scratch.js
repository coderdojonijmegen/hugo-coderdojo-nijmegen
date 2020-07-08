  function parseBlocks(codeBlock) {
    var doc
    var docView
    var svg
    // Parse the source code
    doc = scratchblocks.parse(codeBlock.innerHTML, {languages: ['en','nl']})

    // // Create a DocView with your chosen style
    docView = scratchblocks.newView(doc, {
      style: 'scratch3', // Or 'scratch2'
    })

    // Render to an SVG
    svg = docView.render()

    // Scratch 3 is zoomed out by default, so you probably want to do the same
    svg.style.transform = 'scale(0.5)';
    svg.style.width = 'auto';
    svg.style.height = 'auto';

    // Add that SVG to your page, etc
    svg.style.transformOrigin = '0 0';
    return svg
  }
  var codeblocks = document.getElementsByClassName("scratch")
  var parsedBlock
  for (i = 0; i < codeblocks.length; i++) {
    parsedBlock = parseBlocks(codeblocks[i])
    codeblocks[i].innerHTML = ""
    codeblocks[i].appendChild(parsedBlock)
  }
