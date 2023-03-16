extra = require "extrafuncties"

function love.load()
  -- hierin worden alle stukjes van de slang bijgehouden
  slang = {}

  -- eerste paar stukjes van de slang
  for i = 1, 2 do
    slangStukje = {
      positieX = 5+1*i,
      positieY = 5,
      richtingX = 1,
      richtingY = 0
    }
    table.insert(slang, slangStukje)
  end
  kop = slang[#slang]

  -- de punten waar een stukje van de slang van richting moet veranderen
  keerPunten = {}

  -- hoeveel seconden de slang er over doet om een stukje te bewegen
  tijdSlang = 1

  -- het aantal seconden dat er een stukje fruit wordt toegevoegd
  tijdFruit = 3

  -- de teller telt tot de tijd is bereikt
  tellerSlang = 0
  tellerFruit = 0

  -- de score begint op 0
  score = 0

  -- hierin wordt al het fruit bijgehouden
  fruit = {}

  -- de plaatjes worden hier geladen
  slangKopPlaatje = love.graphics.newImage("plaatjes/slangkop.png")
  slangLichaamPlaatje = love.graphics.newImage("plaatjes/slanglichaam.png")
  appelPlaatje = love.graphics.newImage("plaatjes/appel.png")
  achtergrondPlaatje = love.graphics.newImage("plaatjes/achtergrond.png")

  -- game over
  gameOver = false
end

function love.draw()
  -- teken de achtergrond
  love.graphics.draw(achtergrondPlaatje, 0, 0)

  -- teken het fruit
  for k, stukFruit in pairs(fruit) do
    love.graphics.draw(appelPlaatje, stukFruit.positieX*appelPlaatje:getWidth(), stukFruit.positieY*appelPlaatje:getHeight())
  end

  -- teken de slang
  for k, slangStukje in pairs(slang) do
    if k == #slang then
      love.graphics.draw(slangKopPlaatje, slangStukje.positieX*slangKopPlaatje:getWidth(), slangStukje.positieY*slangKopPlaatje:getHeight(), 0)
    else
      love.graphics.draw(slangLichaamPlaatje, slangStukje.positieX*slangLichaamPlaatje:getWidth(), slangStukje.positieY*slangLichaamPlaatje:getHeight())
    end
  end

  -- toon de punten op het scherm
  love.graphics.print(score .. " punten")

  -- toon een bericht als je game over bent
  if gameOver then
    love.graphics.print("Game Over!", love.graphics.getWidth()/2, love.graphics.getHeight()/2)
  end
end

function love.update(dt)
  -- plaats fruit om de zoveel seconden
  if not gameOver and tellerFruit > tijdFruit then
    plaatsFruit()
    tellerFruit = 0
  end

  -- doe de rest (bewegen van slang, controleren van keerpunten, fruit eten en game over controleren)
  if not gameOver and tellerSlang > tijdSlang then
    beweegSlang()
    extra.controleerKeerPunten(keerPunten, slang)
    eetFruit()
    controleerGameOver()
    tellerSlang = 0
  end

  tellerSlang = tellerSlang + dt
  tellerFruit = tellerFruit + dt
end

function love.keypressed(key)
  -- voeg een nieuw keerpunt toe als er een knop ingedrukt is
  if key == "left" or
    key == "right" or
    key == "up" or
    key == "down" then

    nieuwKeerPunt = {
      positieX = 0,
      positieY = 0,
      richtingX = 0,
      richtingY = 0
    }

    if key == "left" then
      nieuwKeerPunt.richtingX = -1
      nieuwKeerPunt.richtingY = 0
    elseif key == "right" then
      nieuwKeerPunt.richtingX = 1
      nieuwKeerPunt.richtingY = 0
    elseif key == "up" then
      nieuwKeerPunt.richtingY = -1
      nieuwKeerPunt.richtingX = 0
    elseif key == "down" then
      nieuwKeerPunt.richtingY = 1
      nieuwKeerPunt.richtingX = 0
    end

    nieuwKeerPunt.positieX = slang[#slang].positieX
    nieuwKeerPunt.positieY = slang[#slang].positieY

    -- voeg het nieuwe keerpunt toe aan de andere keerpunten
    if not extra.bestaatKeerPunt(keerPunten, nieuwKeerPunt) then
      table.insert(keerPunten, nieuwKeerPunt)
    end

  end
end

function beweegSlang()
  -- verander van richting als een stukje van de slang bij een keerpunt komt
  for k, slangStukje in pairs(slang) do
    for k, keerPunt in pairs(keerPunten) do
      if slangStukje.positieX == keerPunt.positieX and slangStukje.positieY == keerPunt.positieY then
        slangStukje.richtingX = keerPunt.richtingX
        slangStukje.richtingY = keerPunt.richtingY
      end
    end

    -- verander positie van elk slangstukje
    slangStukje.positieX = slangStukje.positieX + slangStukje.richtingX
    slangStukje.positieY = slangStukje.positieY + slangStukje.richtingY
  end
end

function eetFruit()
  -- als de kop van de slang op een stukje fruit zit eet het fruit en verhoog de score
  for k, stukFruit in pairs(fruit) do
    if stukFruit.positieX == kop.positieX and stukFruit.positieY == kop.positieY then
      table.remove(fruit, k)
      score = score + 1
      tijdSlang = tijdSlang * 0.9
      maakSlangLanger()
    end
  end
end

function maakSlangLanger()
  -- voeg een stukje van de slang toe aan de rest van de slang
  staartStukje = slang[1]
  nieuwSlangStukje = {
    positieX = staartStukje.positieX-staartStukje.richtingX,
    positieY = staartStukje.positieY-staartStukje.richtingY,
    richtingX = staartStukje.richtingX,
    richtingY = staartStukje.richtingY
  }
  table.insert(slang, 1, nieuwSlangStukje)
end

function plaatsFruit()
  -- plaats een stukje fruit op een willekeurige plek
  nieuwFruit = {
    positieX = math.random(0, math.floor(love.graphics.getWidth()/appelPlaatje:getWidth())),
    positieY = math.random(0, math.floor(love.graphics.getHeight()/appelPlaatje:getHeight()))
  }
  table.insert(fruit, nieuwFruit)
end

function controleerGameOver()
  -- als de slang buiten het scherm is, is het game over
  if kop.positieX < 0 or kop.positieX > math.floor(love.graphics.getWidth()/slangKopPlaatje:getWidth()) or
    kop.positieY < 0 or kop.positieY > math.floor(love.graphics.getHeight()/slangKopPlaatje:getHeight()) then
    gameOver = true
  end

  -- als de slang tegen zichzelf botst is het ook game over
  for k, slangStukje in pairs(slang) do
    if slangStukje ~= kop and kop.positieX == slangStukje.positieX and kop.positieY == slangStukje.positieY then
      gameOver = true
    end
  end
end
