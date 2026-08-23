const standaardKaarten = [
  { vraag: "Wat is de hoofdstad van Frankrijk?", antwoord: "Parijs" },
  { vraag: "Hoeveel is 8 × 7?", antwoord: "56" },
  { vraag: "Welk dier is het snelst op het land?", antwoord: "De cheeta" }
];

let kaarten = laadKaarten();
let huidigKaartnummer = 0;

function draaiKaartOm() {
  const kaart = document.querySelector(".kaart");
  kaart.classList.toggle("omgedraaid");
}

function toonHuidigeKaart() {
  const kaart = kaarten[huidigKaartnummer];
  document.querySelector("#vraag").textContent = kaart.vraag;
  document.querySelector("#antwoord").textContent = kaart.antwoord;
}

function toonVolgendeKaart() {
  huidigKaartnummer = huidigKaartnummer + 1;
  if (huidigKaartnummer === kaarten.length) {
    huidigKaartnummer = 0;
  }
  const kaart = document.querySelector(".kaart");
  if (kaart.classList.contains("omgedraaid")) {
    const binnenkant = document.querySelector(".kaart-binnenkant");
    binnenkant.addEventListener("transitionend", toonHuidigeKaart, { once: true });
    kaart.classList.remove("omgedraaid");
  } else {
    toonHuidigeKaart();
  }
}

function voegKaartToe() {
  const vraag = document.querySelector("#nieuwe-vraag").value;
  const antwoord = document.querySelector("#nieuw-antwoord").value;
  if (vraag === "" || antwoord === "") {
    document.querySelector("#melding").textContent = "Vul een vraag en een antwoord in.";
    return;
  }
  kaarten.push({ vraag: vraag, antwoord: antwoord });
  bewaarKaarten();
  document.querySelector("#nieuwe-vraag").value = "";
  document.querySelector("#nieuw-antwoord").value = "";
  document.querySelector("#melding").textContent = "Je kaart is toegevoegd.";
}

function bewaarKaarten() {
  const tekst = JSON.stringify(kaarten);
  localStorage.setItem("flashcards", tekst);
}

function laadKaarten() {
  const tekst = localStorage.getItem("flashcards");
  if (tekst === null) {
    return standaardKaarten;
  }
  return JSON.parse(tekst);
}

function downloadKaarten() {
  const tekst = JSON.stringify(kaarten, null, 2);
  const bestand = new Blob([tekst], { type: "application/json" });
  const link = document.createElement("a");
  link.href = URL.createObjectURL(bestand);
  link.download = "mijn-flashcards.json";
  link.click();
  URL.revokeObjectURL(link.href);
  document.querySelector("#bestandsmelding").textContent = "Je kaarten zijn gedownload.";
}

function uploadKaarten(event) {
  const bestand = event.target.files[0];
  if (bestand === undefined) {
    return;
  }

  const lezer = new FileReader();
  lezer.addEventListener("load", function verwerkBestand() {
    const ingeladenKaarten = JSON.parse(lezer.result);
    kaarten = ingeladenKaarten;
    huidigKaartnummer = 0;
    bewaarKaarten();
    toonHuidigeKaart();
    document.querySelector("#bestandsmelding").textContent = "Je kaarten zijn ingeladen.";
  });
  lezer.readAsText(bestand);
}

toonHuidigeKaart();
