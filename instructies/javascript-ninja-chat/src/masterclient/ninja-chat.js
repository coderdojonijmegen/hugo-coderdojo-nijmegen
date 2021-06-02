var serverIpAdresEnPoort = "https://coderdojo-ninja-chat.herokuapp.com/";


var socket = io(serverIpAdresEnPoort, { forceNew: true });

/**
 * Geeft de gekozen naam door aan de server.
 *
 * @param {jQuery.Event} input
 */
// function zetNaam(input) {
//   var naam = input.target.value
//   socket.emit('zetNaam', naam)
// }

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
  if (bericht != "") {
    socket.emit('maakBericht', bericht)
    berichtInput.val("")
  }
}

/**
 * Als op enter wordt gedrukt, stuur bericht.
 *
 * @param {Event} event
 */
function checkEnter(event) {
  if (event.which === 13) {
      stuurBericht()
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
 * Dit zorgt ervoor dat een bericht op het scherm verschijnt.
 *
 * @param {object} bericht
 */
function toonBericht(bericht) {
  var div = $('<div>').html(berichtNaarHtml(bericht))
  $(".berichten").append(div)
  $("p:last").get(0).scrollIntoView()
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
    <p class='${class_naam} kanaal${bericht.kanaal}'
    <p class="${class_naam}">
      <i>${bericht.gebruiker} ${bericht.tijdstip} op kanaal ${bericht.kanaal}</i>
      <br>
      <span>${bericht.tekst}</span>
    </p>`
}

/**
 * Kijkt of de .deelnemers div al bestaat en verwijdert deze.
 * Als de div nog niet bestaat, wordt deze aangemaakt.
 */
function toonOfVerbergDeelnemers() {
    var div = $('.deelnemers')
    if (div.length > 0) {
        // div is gevonden, verwijder.
        div.remove()
    }
    else {
        // div is niet gevonden, maak aan en verzoek server om deelnemerslijst.
        var div = $('<div>')
            .addClass('deelnemers')

        $("header").append(div)
        socket.emit('vraagDeelnemers')
    }
}

/**
 * Toont de vernieuwde deelnemerslijst, als deze zichtbaar is.
 *
 * @param {string[]} deelnemers
 */
function updateDeelnemers(deelnemers) {
    var div = $('.deelnemers')
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
  // $(".naamInput").change(zetNaam)
  socket.emit("zetMaster")

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
