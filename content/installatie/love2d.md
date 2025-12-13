---
title: "Löve2D"
date: 2025-10-19T07:16:01+01:00
draft: false
toc: true
headercolor: "teal-background"
taal: 
banner: "https://coderdojo-nijmegen.nl/instructies/<some-instruction>/banner.png"
---

We gebruiken voor deze instructie Löve2D. Deze moet je installeren als je die nog niet
hebt.  
Heb je die al wel en weet je hoe je er mee om moet gaan, ga dan verder met het volgende hoofdstuk.

### Downloaden
Tijdens de dojo kun je het installatiebestand sneller downloaden van de CoderDojo server:   
<a class="button" href="https://installers.server.coderdojo-nijmegen.nl">download</a>

Löve2D is eventueel ook beschikbaar vanaf [love2d.org](https://love2d.org/) voor Windows, MacOS en Linux.



#### Windows
Löve is op Windows gemakkelijk te installeren via één van de installers. Als alternatief kun je kiezen voor één van de 
zipbestanden en deze op een gewenste locatie unzippen. Maak het jezelf gemakkelijk door Löve op een eenvoudig te 
onthouden plek te installeren, bijvoorbeeld in de map

    c:\love\

Zie de [Löve download pagina](https://love2d.org/#download) voor de installatie bestanden.
Als je twijfelt tussen de 32- of 64-bits versie, kun je voor de zekerheid kiezen voor 32-bits versie of gewoon even 
[checken](https://support.microsoft.com/nl-nl/help/13443/windows-which-operating-system) welke versie je hebt.

#### Mac
[Download](https://love2d.org/#download) het zip bestand voor Mac en unzip het op de gewenste locatie.

#### Linux
Voor Ubuntu kun je kiezen voor het toevoegen van de 
[Löve PPA](https://launchpad.net/~bartbes/%2Barchive/ubuntu/love-stable)
of voor de installatie van één van de .deb bestanden.  
Onderstaand vind je de instructies voor het gebruiken van de AppImage:

{{< voorbeeld kop="Instructies voor het gebruiken van de Löve AppImage" md=true >}}
1. Download de [Löve `appimage x86_64`](https://love2d.org/#download). 
Zet deze bijvoorbeeld in je `~/Downloads` directory.  

2. Voer hier vervolgens de volgende commands op uit (vanuit `~/Downloads`). 
Je `.AppImage` kan een andere versie/naam hebben dan in het voorbeeld!
{{< highlight bash >}}
chmod u+x love-11.4-x86_64.AppImage
{{< /highlight >}}
3. Zorg nu dat je weet waar je `.lua` bestanden staan (zie onderstaande stap 1). 
In ons voorbeeld is dit in `~/Documents/love2d-shooter-master/src/`. 
Je voert de code dan op de volgende manier uit:
{{< highlight bash >}}
~/Downloads/love-11.4-x86_64.AppImage ~/Documents/love2d-shooter-master/src/
{{< /highlight >}}

Let op dat het scherm in eerste instantie zwart is, omdat we nog geen code geschreven hebben.  
Mocht het niet lukken om de code op deze manier uit te voeren, vraag dan gerust om hulp!
{{< /voorbeeld >}}


### Tekst editor
Als je gaat programmeren is het handig om een editor te installeren met meer mogelijkheden dan 'kladblok'.  
We gebruiken al vaker [Visual Studio Code](https://code.visualstudio.com/), maar als alternatief kun je ook kiezen voor 
[Notepad++](https://notepad-plus-plus.org/download/).
