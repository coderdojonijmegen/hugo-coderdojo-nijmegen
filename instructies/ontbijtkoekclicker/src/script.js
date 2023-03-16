

/* Een lijst met de icoontjes van de Clickers. */
clickerIcons = [
    "https://pngimg.com/uploads/chef/chef_PNG54.png",
    /* tier 1 */
    /* tier 2 */
    /* tier 3 */
    /* tier 4 */
]

/* De volgende functies beïnvloeden het uiterlijk van de pagina. */

/* Voeg een nieuw icoontje toe aan de lijst met Actieve Clickers van tier tier */
function voegActieveClickerToe(tier) {
    const actieveClickerDiv = document.getElementById("actieveClickers")
    const tierDiv = actieveClickerDiv.getElementsByClassName("tier" + tier)[0]

    const afbeelding = document.createElement("img")
    afbeelding.src = clickerIcons[tier]
    afbeelding.className = "icon"

    tierDiv.appendChild(afbeelding)
}

/* Verander het geld bedrag dat op de pagina word weergegeven naar hoeveelheid. */
function updateGeld(hoeveelheid) {
    const geldH2 = document.getElementById("geld")

    geldH2.innerText = "Geld: " + hoeveelheid + "$"
}

/* Verander het geld per seconde bedrag dat op de pagina word weergegeven naar hoeveelheid. */
function updateGeldPerSeconde(hoeveelheid) {
    const geldPerSecondeH2 = document.getElementById("geldPerSeconde")

    geldPerSecondeH2.innerText = "Geld per seconde: " + hoeveelheid + "$"
}

/* Verwijder de Powerup voor tier tier uit de lijst. */
function verwijderPowerup(tier) {
    const powerupDiv = document.getElementById("powerupWinkel")
    const tierDiv = powerupDiv.getElementsByClassName("tier" + tier)[0]

    tierDiv.remove()
}

/* Vanaf hier focussen we op de functionaliteit! */

/* De volgende gegevens veranderen niet. */
const aantalClickerTiers = 5
const clickerKosten = [1, 10, 50, 100, 500]
const powerupKosten = [10, 100, 500, 1000, 5000]

/* De volgende gevevens kunnen veranderen. */
let geld = 0
let maxAantalClickers = 14 /* Voor de basisfunctie ligt dit aan de grootte van je scherm. */
const clickerInkomsten = [1, 2, 4, 8, 32]
const aantalClickers = [0, 0, 0, 0, 0]
const beschikbarePowerups = [true, true, true, true, true]

/* Voegt 1$ toe en update de pagina */
function onClickCookie() {
    geld = geld + 1

    updateGeld(geld) /* Update de pagina! */
}

/* Berekent het geld dat de Clickers genereren per seconde. */
function berekenGeldPerSeconde() {
    let totaal = 0

    for (let tier = 0; tier < aantalClickerTiers; tier++) {
        const inkomsten = clickerInkomsten[tier]
        const aantal = aantalClickers[tier]
        totaal += inkomsten * aantal
    }

    return totaal
}

/* Koopt een Powerup, mits hier geld voor is en de powerup nog niet gekocht is. Update de pagina. */
function koopPowerup(tier) {
    if (beschikbarePowerups[tier] == false) {
        return
    }
    if (geld < powerupKosten[tier]) {
        return
    }

    beschikbarePowerups[tier] = false;
    geld = geld - powerupKosten[tier]
    clickerInkomsten[tier] = clickerInkomsten[tier] * 2

    /* Update de pagina! */
    verwijderPowerup(tier)
    updateGeldPerSeconde(berekenGeldPerSeconde())
    updateGeld(geld)
}

/* Koopt een Clicker, mits hier geld voor is en er nog ruimte is. Update de pagina. */
function koopClicker(tier) {
    if (aantalClickers[tier] >= maxAantalClickers) {
        return
    }
    if (geld < clickerKosten[tier]) {
        return
    }

    geld = geld - clickerKosten[tier]
    aantalClickers[tier] = aantalClickers[tier] + 1

    /* Update de pagina! */
    voegActieveClickerToe(tier)
    updateGeldPerSeconde(berekenGeldPerSeconde())
    updateGeld(geld)
}

/* Voegt het geld van de Clickers toe aan het geld. Update de pagina. */
function updateClickerGeld() {
    geld = geld + berekenGeldPerSeconde()

    /* Update de pagina! */
    updateGeld(geld)
}

/* Zorgt dat updateClickerGeld elke seconde activeert. */
setInterval(updateClickerGeld, 1000)
