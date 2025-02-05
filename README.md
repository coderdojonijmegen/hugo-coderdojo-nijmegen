# coderdojo-nijmegen.nl

Dit archief bevat de site voor CoderDojo Nijmegen zichtbaar op https://coderdojo-nijmegen.nl.

De site is gebouwd met [Hugo](https://gohugo.io).

Mocht je suggesties ter verbetering hebbben, fork dan gerust de site en biedt
een pull-request aan.   

# De website aanpassen

Om de website aan te passen, maak je een clone van deze repository. Maak vervolgens een branch om je wijziging aan te kunnen bieden in een pull-request.

## Live view van je wijzigingen

Het is handig om Hugo te installeren, zodat je direct kunt zien hoe je wijzigingen er in de browser uit zien. Installeer daarvoor de Hugo extended version, want die ondersteund SCSS zoals gebruikt in deze site. 

Je kunt de laatse versie van Hugo downloaden op de [releases pagina](https://github.com/gohugoio/hugo/releases) van de Hugo GitHub repository. De site wordt op dit moment gebouwd met versie [extended_0.74.3](https://github.com/gohugoio/hugo/releases/tag/v0.74.3).

Het installeren is simpel. Download de zip-file, pak 'm uit waar je wilt en je bent klaar. Er staat enkel een `hugo.exe`, een licentie en README.md bestand in. Het is handig om de directory waar in `hugo.exe` staat in je path op te nemen, zodat je het overal eenvoudig kunt starten.

Om de site te kunnen bekijken, start je `hugo server` vanuit de root van de checkout van deze repository (daar waar ook het `config.toml` bestand staat). Je kunt de site vervolgens bekijken op http://localhost:1313.

## Dojo's toevoegen of pagina's aanpassen

De pagina's van de site staan allemaal in de [content](https://github.com/coderdojonijmegen/hugo-coderdojo-nijmegen/tree/master/content) directory volgens de structuur van de site:
```
C:.
├───archetypes
├───assets
│   ├───js
│   └───scss
├───content           <===
│   ├───dojos
│   ├───instructies
│   ├───stichting
│   └───team
├───data
├───layouts
│   ├───dojos
│   ├───instructies
│   ├───partials
│   ├───shortcodes
│   └───_default
└───static
    ├───fonts
    ├───imgs
    └───js
```
De rest van de directorystructuur bevat alle bestanden die nodig zijn om de site te bouwen, zoals templates, plaatjes, lettertypen en JavaScripts.

## Een nieuwe dojo aankondiging maken

Sinds [dojo #74](https://coderdojo-nijmegen.nl/dojos/74-online-websites-maken/), wordt de dojo pagina automatisch
afgeleid van de aankondiging op EventBrite. Zie [dojo.py](utils/dojo.py) voor hoe het werkt. Ieder uur wordt er gekeken
of er een nieuwe aankondiging is en als die er is, dan wordt er een markdown bestand gegenereerd en naar de repository
gepushed. Deze wordt vervolgens gepubliceerd op de site door [deploy.py](deploy.py).

Om een nieuwe dojo aankondiging te maken, maak je een nieuw bestand aan in de `content/dojos` directory. Gebruik als
naam de aflevering van de dojo gecombineerd met het onderwerp, zoals bijvoorbeeld _62-website-bouwen.md_. Handiger is
het om commando `hugo new content/dojos/70-online.md`. Dit maakt het bestand aan en vult het met "front matter":
```
---
title: "#{{ replace .Name "-" " " | title }}"
date: {{ .Date }}
draft: false
headercolor: "orange-background"
wanneer: 
  van: 2020-03-07T12:00:00.0Z
  tot: 2020-03-07T14:30:00.0Z
waar: "Rootnet, Kerkenbos 1059, 6546 BB Nijmegen"
eventbrite:
  inschrijvenvanaf: 2020-01-01T00:00:00.0Z
  inschrijventot: 2020-03-07T00:00:00.0Z
  url: "https://www.eventbrite.nl/e/tickets-coderdojo-nijmegen-62-93475366337"
instructies:
  - /instructies/microbit
---
```
De "front matter" is nodig om de dojo informatie boven aan de pagina te specificeren en om de inschrijfknop te tonen.
Meer gedetailleerd:
* de `title` wordt afgeleid van de bestandsnaam; `62-website-bouwen.md` wordt _#62 Website Bouwen_
* de `date` wordt ook automatisch ingevuld en is gelijk aan de huidige datum en tijd.
* `draft` wordt gebruikt om content voor te bereiden, maar nog niet live te zetten. Wij zetten die op `false`, 
  omdat wij de voorbereiding doen in een branch.
* `headercolor` is een optie van onze eigen site template en bepaald de kleur van de kop van de webpagina. 
  Deze is voor dojos `orange-background`.
* met `wanneer` wordt aangegeven wanneer de dojo plaats vind. `van` geeft de starttijd aan en `tot` de eindtijd. 
  Let er op dat je hetzelfde tijdformaat aanhoud, inclusief eventuele voorloop nullen.
* `waar` geeft de locatie van de dojo aan. Dit wordt omgezet naar een linkje naar Google Maps, dus het is handig om 
  echt een adres te gebruiken.
* `eventbrite` informatie wordt gebruikt om de inschrijfknop te maken. De knop gebruikt de `url` als doel locatie. 
  `inschrijventot` wordt gebruikt om de knop te verwijderen na de opgegeven tijd. Dit is geen exacte tijd, want de 
  knop wordt alleen verwijderd als de site opnieuw gebouwd wordt. Dit gebeurt iedere dag om 1 uur 's nachts (UTC).
* tenslotte is er de `instructies` lijst om te verwijzen naar de instructies die gebruikt worden tijdens de dojo. 
  Deze worden tijdens de dojo op de voorpagina van de MCS getoond, maar zijn niet zichtbaar op de site op internet.
  De lijst dient kan uit lokale paden, zoals _/instructies/microbit_, bestaan, maar mag ook links op internet, 
  zoals https://projects.raspberrypi.org/nl-NL/projects/lost-in-space, bevatten.

## Instructies schrijven voor op de site

### Nieuwe instructie

De `content/instructies` directory is vrijwel leeg. De instructies staan in hun eigen repositories en worden in de `content/instructies` directory gecloned en uiteindelijk mee gebouwd met de rest van de site.

Om een nieuwe instructie te maken, volg je de volgende stappen:

1. maak een repository op GitHub; er is geen vaste naam conventie, maar een aantal repositorynamen bestaat uit `programmeertaal-onderwerp`.
2. clone de _hugo-coderdojo-nijmegen_ repository
3. clone de repository van de nieuwe instructie in de `content/instructies` directory van de _hugo-coderdojo-nijmegen_ checkout, dus: `content/instructies/programmeertaal-onderwerp`
4. maak in de checkout van de nieuwe instructie een `index.md` bestand aan. Hierin wordt de instructie geschreven. Het handigst is om daarvoor commando `hugo new content/instructies/proogrammeertaal-onderwerp/index.md` te gebruiken. Hugo voegt dan automatisch de "front matter" toe aan de kop van het bestand op basis van de locatie (archetype). Ook wordt dan de licentie short-code toegevoegd (zie hoofdstuk [licentie](#licentie)).
5. De "front matter" van een instructie pagina bestaat uit:
   ```
   ---
   title: "{{ replace .Name "-" " - " | title }}"
   date: {{ .Date }}
   draft: false
   toc: true
   headercolor: "teal-background"
   ---
   ```
   * de `title` wordt automatisch ingevuld en is gelijk aan `Programmeertaal - Onderwerp`, afgeleid van de bestandsnaam.
   * de `date` wordt ook automatisch ingevuld en is gelijk aan de huidige datum en tijd.
   * `draft` wordt gebruikt om content voor te bereiden, maar nog niet live te zetten. Wij zetten die op `false`, omdat wij de voorbereiding doen in een branch.
   * `toc` is een optie van onze eigen site template en creëert een inhoudsopgave op de instructie pagina. Deze staat standaard aan, omdat instructie pagina's over het algemeen uit redelijk wat hoofdstukjes bestaan en het handig is om er met een inhoudsopgave doorheen te navigeren.
   * `headercolor` is ook een optie van onze eigen site template en bepaald de kleur van de kop van de webpagina. Deze is voor instructies `teal-background`.

### Inhoudsopgave

De titel van de pagina wordt als `<h1>` gerenderd net als MarkDown `#`. Gebruik dus als hoogste niveau `##` om onderscheid te houden tussen de titel van de pagina en de hoofdstukken. Dit is ook van belang voor de inhoudsopgave, deze gebruikt niveaus `##` en lager.

### Scratch

Voor gebruik van Scratch elementen gebruik je short-code `{{< scratch >}} ... {{< /scratch >}}` met daarin de Scratch code. Deze wordt dan omgezet in Scratch blocks bij het bouwen van de site. Voorbeeld:
```
{{< scratch >}}
    wanneer [pijltje omhoog v] is ingedrukt
    richt naar (0) graden
    neem (5) stappen
{{< /scratch >}}
```

### Verdieping

Als je ter verdieping wat meer gedetaileerde informatie wilt aanbieden, dan kan dat in een verdiepingsvak. Zie als voorbeeld [uitleg over de x en y as](https://coderdojo-nijmegen.nl/instructies/love2d-shooter/#x-en-y-as) in de Löve2D shooter instructie.
Gebruik hiervoor de short-code `{{< verdieping >}} ... {{< /verdieping >}}` met daarin de verdieping. Dit kan MarkDown content zijn. Voorbeeld:
```
{{< verdieping >}}
## Verdieping
We leggen je in dit blok meer uit over onderwerp a.
{{< /verdieping >}}
```

### Voorbeeld

Je kunt code voorbeelden gebruiken in je instructie en deze in eerste instantie verborgen houden. Gebruik hiervoor de `{{< voorbeeld kop="kop tekst" md >}} ... {{< /voorbeeld >}}` short-code. De tekst in parameter `kop` wordt getoond en daarop kan worden geklikt om het voorbeeld zichtbaar te maken. Als je een Scratch voorbeeld hebt, is de kop alleen genoeg. Wil je MarkDown gebruiken, dan moet je parameter `md` toevoegen.
```
{{< voorbeeld kop="Klik om de voorbeeldcode te laten zien om de slang omhoog te laten bewegen" >}}
{{< scratch >}}
      wanneer groene vlag wordt aangeklikt
      herhaal
      als &lt;toets [pijltje omhoog v] ingedrukt?&gt; dan
      richt naar (0) graden
      end
      neem (10) stappen
      wacht (0.1) sec.
{{< /scratch >}}
{{< /voorbeeld >}}
```

### Code highlighting

Hugo heeft een ingebouwde [code highlight short-code](https://gohugo.io/content-management/syntax-highlighting/#highlight-shortcode). Deze kun je voor allerlei talen gebruiken. Voorbeeld:
```
{{< highlight python >}}
    bgcolor('black')
    color('green')
    width(5)
    forward(100)
    right(90)
    forward(100)
    right(90)
    forward(100)
    right(90)
    forward(100)
    right(90)
{{< /highlight >}
```

### Licentie

Onder iedere instructie pagina zetten we de licentie waaronder de content beschikbaar is voor hergebruik. We gebruiken daarvoor de `{{< licentie rel="link" >}}` short-code. De `rel` parameter wordt niet gebruikt bij het genereren van de site, maar is toegevoegd om een link naar de licentie toe te voegen in de kale MarkDown in de instructie repositories.
```
{{< licentie rel="http://creativecommons.org/licenses/by-nc-sa/4.0/">}}
```
