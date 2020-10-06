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

De pagina's van de site staan allemaal in de [content](https://github.com/coderdojonijmgen/hugo-coderdojo-nijmegen/content) directory volgens de structuur van de site:
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

## Instructies schrijven voor op de site

De `content/instructies` directory is vrijwel leeg. De instructies staan in hun eigen repositories en worden in de `content/instructies` directory gecloned en uiteindelijk mee gebouwd met de rest van de site.

Om een nieuwe instructie te maken, volg je de volgende stappen:

1. maak een repository op GitHub; er is geen vaste naam conventie, maar een aantal repositorynamen bestaat uit `programmeertaal-onderwerp`.
2. clone de _hugo-coderdojo-nijmegen_ repository
3. clone de repository van de nieuwe instructie in de `content/instructies` directory van de _hugo-coderdojo-nijmegen_ checkout, dus: `content/instructies/programmeertaal-onderwerp`
4. maak in de checkout van de nieuwe instructie een `index.md` bestand aan. Hierin wordt de instructie geschreven.
5. 
