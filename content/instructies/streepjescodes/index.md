---
title: "Streepjescodes"
date: 2024-09-29T20:53:27+02:00
draft: false
toc: true
headercolor: "teal-background"
onderwerp: Javascript
---

Ooit afgevraagd hoe streepjescodes werken?

<!--more-->

<script src="main.js"></script>
  <script>
    //ask before reload source: https://stackoverflow.com/questions/10311341/confirmation-before-closing-of-tab-browser
    window.onbeforeunload = function (e) {
      e = e || window.event;

      // For IE and Firefox prior to version 4
      if (e) {
        e.returnValue = 'Sure?';
      }

      // For Safari
      return 'Sure?';
    };
  </script>

  <div id="myapp"></div>
  <script>
    var app = Elm.Main.init({
      node: document.getElementById('myapp')
    });
  </script>
