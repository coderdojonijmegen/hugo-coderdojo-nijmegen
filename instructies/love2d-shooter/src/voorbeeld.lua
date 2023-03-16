require 'functies'

-- de stapgrootte van de kogels
stapGrootte = 2
-- bepaalt of het spel afgelopen is
spelIsAfgelopen = false
-- de score van de speler
score = 0

-- variabelen om eigenschappen van de speler in op te slaan
speler = { x = 200, y = 560, plaatje = nil }
-- lijst om vijanden in op te slaan
vijanden = {}
-- lijst om kogels in op te slaan
kogels = {}

function love.load(arg)
   -- laad het plaatje in eigenschap plaatje van de variabele speler
   speler.plaatje = love.graphics.newImage('plaatjes/spelersVliegtuig.png')
   -- laad het plaatje van de vijand
   vijandPlaatje = love.graphics.newImage('plaatjes/vijandsVliegtuig.png')
   -- laad het plaatje van de kogel
   kogelPlaatje = love.graphics.newImage('plaatjes/kogel.png')
end

function love.draw(dt)
   -- als het spel nog niet is afgelopen
   if spelIsAfgelopen == false then
      -- teken het plaatje op het scherm
      love.graphics.draw(speler.plaatje, speler.x, speler.y)
      -- teken de vijanden in de lijst
      tekenVijanden(vijanden)
      -- teken de kogels in de lijst
      tekenKogels(kogels)
   else
      love.graphics.print("game over", 200, 200)
      love.graphics.print("typ 'o' om opnieuw te starten", 150, 250)
   end

   -- zet de tekstkleur op wit
   love.graphics.setColor(255, 255, 255)
   -- en druk de score af
   love.graphics.print("SCORE: " .. tostring(score), 400, 10)

end

function love.update(dt)

   -- als het spel niet is afgelopen, zorgen we dat het speelbaar is
   if spelIsAfgelopen == false then
      schietBijDrukOp('space')
      beweegKogels()
      maakNieuweVijand(vijanden)
      beweegVijanden()
      gameOverBijVijandAanraken()
      puntenBijVijandRaken()
      spelerBesturing()

      -- als het spel wel is afgelopen, kijken we enkel of we opnieuw willen starten
   else
      -- de 'o' van opnieuw
      restartBijDrukOp('o')
   end
end

---------------------------------------------------------------------------
-- Hier volgen alle functies die we in de functie love.update gebruiken. --
---------------------------------------------------------------------------

function restartBijDrukOp(toets)

   -- als toets wordt ingedrukt
   if love.keyboard.isDown(toets) then
      -- wordt het spel opnieuw gestart
      kogels = {}
      vijanden = {}
      score = 0
      spelIsAfgelopen = false
   end
end

function schietBijDrukOp(toets)

   -- als toets wordt ingedrukt
   if love.keyboard.isDown(toets) then
      -- schiet dan
      maakNieuweKogel(kogels, speler)
   end
end

function beweegKogels()

   -- voor elke kogel in de lijst
   for index, kogel in ipairs(kogels) do

      -- beweeg de kogel naar boven
      kogel.y = kogel.y - (2 * stapGrootte)

      -- als de kogel de bovenrand heeft bereikt
      if kogel.y < -20 then
         -- verwijder het uit de lijst
         table.remove(kogels, index)
      end
   end
end

function beweegVijanden()

   -- voor elke vijand in de lijst
   for index, vijand in ipairs(vijanden) do

      -- laat de vijand een stapje naar beneden doen
      vijand.y = vijand.y + stapGrootte

      -- als de vijand de onderrand heeft bereikt
      if vijand.y > yOnderRand() then
         -- verwijder de vijand als ie buiten het venster is verdwenen
         table.remove(vijanden, index)
      end
   end
end

function gameOverBijVijandAanraken()

   -- als de speler een vijand geraakt heeft
   if spelerHeeftVijandGeraakt() then
      -- is het spel afgelopen
      spelIsAfgelopen = true
   end
end

function puntenBijVijandRaken()

   -- als de kogel een vijand geraakt heeft
   if kogelHeeftVijandGeraakt() then
      -- heb je een punt gescoord
      score = score + 1
   end
end

function spelerBesturing()

   -- als pijltje naar links ingedrukt
   if love.keyboard.isDown('left') then
      -- en de linker rand is nog niet bereikt
      if speler.x > 0 then
         -- dan doe een stap naar links
         speler.x = speler.x - stapGrootte
      end

      -- als pijltje naar rechts ingedrukt
   elseif love.keyboard.isDown('right') then
      -- en de rechter rand is nog niet bereikt
      if speler.x < xRechterRand() then
         -- dan doe een stap naar rechts
         speler.x = speler.x + stapGrootte
      end
   end
end
