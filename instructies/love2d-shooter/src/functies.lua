function xRechterRand()
  return love.graphics.getWidth() - speler.plaatje:getWidth()
end

function yOnderRand()
  return love.graphics.getHeight()
end

function xWillekeurig()
  return math.random(50, love.graphics.getWidth() - 50)
end

function tekenVijanden(vijanden)
  for index, vijand in ipairs(vijanden) do
    love.graphics.draw(vijand.plaatje, vijand.x, vijand.y)
  end
end

function tekenKogels(kogels)
  for index, kogel in ipairs(kogels) do
    love.graphics.draw(kogel.plaatje, kogel.x, kogel.y)
  end
end

nieuweVijandInterval = 100
nieuweVijandTimer = 0
function maakNieuweVijand(vijanden)
  if nieuweVijandTimer < 0 then
    nieuweVijand = { x = xWillekeurig(), y = -100, plaatje = vijandPlaatje }
    table.insert(vijanden, nieuweVijand)
    nieuweVijandTimer = nieuweVijandInterval
  else
    nieuweVijandTimer = nieuweVijandTimer - 1
  end
end

nieuweKogelInterval = 20
nieuweKogelTimer = 0
function maakNieuweKogel(kogels, speler)
  if nieuweKogelTimer < 0 then
    nieuweKogel = { x = speler.x + (speler.plaatje:getWidth()/2), y = spelerY, plaatje = kogelPlaatje }
    table.insert(kogels, nieuweKogel)
    nieuweKogelTimer = nieuweKogelInterval
  else
    nieuweKogelTimer = nieuweKogelTimer - 1
  end
end

function isGeraakt(x1, y1, w1, h1, x2, y2, w2, h2)
  return x1 < x2+w2 and
         x2 < x1+w1 and
         y1 < y2+h2 and
         y2 < y1+h1
 end

function spelerHeeftVijandGeraakt()
  heeftGeraakt = false
  for index, vijand in ipairs(vijanden) do
    if isGeraakt(speler.x, speler.y, speler.plaatje:getWidth(), speler.plaatje:getHeight(), vijand.x, vijand.y, vijand.plaatje:getWidth(), vijand.plaatje:getHeight()) then
        heeftGeraakt = true
    end
  end
  return heeftGeraakt
end

function kogelHeeftVijandGeraakt()
  heeftGeraakt = false
  for vijandIndex, vijand in ipairs(vijanden) do
    for kogelIndex, kogel in ipairs(kogels) do
      if isGeraakt(kogel.x, kogel.y, kogel.plaatje:getWidth(), kogel.plaatje:getHeight(), vijand.x, vijand.y, vijand.plaatje:getWidth(), vijand.plaatje:getHeight()) then
        heeftGeraakt = true
        table.remove(vijanden, vijandIndex)
        table.remove(kogels, kogelIndex)
      end
    end
  end
  return heeftGeraakt
end
