var socket = io(serverIpAdresEnPoort, { forceNew: true });

/**
 * Geeft de gekozen naam door aan de server.
 * 
 * @param {jQuery.Event} input 
 */
function zetNaam(input) {
    var naam = input.target.value
    socket.emit('zetNaam', naam)
}

/**
 * Geeft het gekozen kanaal door aan de server.
 * 
 * @param {jQuery.Event} input 
 */
function zetKanaal(input) {
    var kanaal = input.target.value
  socket.emit('zetKanaal', kanaal)
}

/**
 * Stuurt een bericht naar de server en maakt de bericht-input weer leeg.
 */
function stuurBericht() {
    var berichtInput = $(".berichtInput")
    var bericht = berichtInput.val()
  
    socket.emit('maakBericht', bericht)
    berichtInput.val("")
}

/**
 * Als op enter wordt gedrukt, stuur bericht.
 * 
 * @param {Event} event 
 */
function checkEnter(event) {
    if (event.which === 13) {
        stuurBericht()
        event.preventDefault()
    }
}

/**
 * Dit zorgt ervoor dat de chat-naam zichtbaar is.
 * 
 * @param {string} naam 
 */
function toonNaam(naam) {
    $(".naamInput").val(naam)
}

/**
 * Dit zorgt ervoor dat het huidige kanaal zichtbaar is.
 * 
 * @param {number} kanaal 
 */
function toonKanaal(kanaal) {
    $(".kanaalInput").val(kanaal)
}

/**
 * Dit zorgt ervoor dat een bericht op het scherm komt.
 * 
 * @param {object} bericht 
 */
function toonBericht(bericht) {
    var div = $('<div>').html(berichtNaarHtml(bericht))
    $(".berichten").append(div)
}

/**
 * Hier wordt een bericht vertaald naar mooie HTML.
 * 
 * @param {object} bericht 
 */
function berichtNaarHtml(bericht) {
    var gebruiker = $(".naamInput").val()
    var class_naam = "bericht"
    
    if (gebruiker === bericht.gebruiker) {
        class_naam = "eigen bericht"
    }
  
    return `
        <div class="${class_naam}">
            <i>${bericht.gebruiker} ${bericht.tijdstip}</i>
            <br>
            <span>${bericht.tekst}</span>
        </div>`
}

/**
 * Kijkt of de .deelnemers div al bestaat en verwijderd deze.
 * Als de div nog niet bestaat, wordt het aangemaakt.
 */
function toonOfVerbergDeelnemers() {
    var div = $('.deelnemerLijst')
    if (div.length > 0) {
        // div is gevonden, verwijder.
        div.remove()
    }
    else {
        // div is niet gevonden, maak aan en verzoek server om deelnemerslijst.
        var div = $('<div>')
            .addClass('deelnemerLijst')
  
        $(".deelnemers").append(div)
        socket.emit('vraagDeelnemers')
    }
}

/**
* Toont de vernieuwde deelnemerslijst, als deze zichtbaar is.
* 
* @param {string[]} deelnemers 
*/
function updateDeelnemers(deelnemers) {
    var div = $('.deelnemerLijst')
    if (div.length > 0) {
        div.html(deelnemersNaarHtml(deelnemers))
    }
}

/**
* Hier wordt een lijst van deelnemers vertaald naar HTML.
* 
* @param {string[]} deelnemers 
*/
function deelnemersNaarHtml(deelnemers) {
    var opsomming = deelnemers.join(', ')
  
    return `
        <p>${opsomming}</p>
    `
}

/**
 * Dit is waar alle gebeurtenissen worden ingesteld.
 */
function begin() {
    $(".naamInput").change(zetNaam)
    $(".kanaalInput").change(zetKanaal)
    $(".stuurBericht").click(stuurBericht)
    $(".berichtInput").keypress(checkEnter)
    $(".bekijkDeelnemers").click(toonOfVerbergDeelnemers)
  
    socket.on('krijgKanaal', toonKanaal)
    socket.on('krijgNaam', toonNaam)
    socket.on('krijgBericht', toonBericht)
    socket.on('krijgDeelnemers', updateDeelnemers)
}

$(begin)
