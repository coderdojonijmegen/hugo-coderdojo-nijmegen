local extrafuncties = {}

-- controleer of het keerpunt nog niet bestaat
function extrafuncties.bestaatKeerPunt(keerPunten, keerPunt)
  bestaat = false
  for k, kp in pairs(keerPunten) do
    if keerPunt.positieX == kp.positieX and keerPunt.positieY == kp.positieY then
      bestaat = true
    end
  end
  return bestaat
end

-- verwijder het eerste keerpunt als deze niet meer gebruikt wordt door de slang
function extrafuncties.controleerKeerPunten(keerPunten, slang)
  for kid, keerPunt in pairs(keerPunten) do
    test = nil
    for sid, slangStukje in pairs(slang) do
      if slangStukje.positieX == keerPunt.positieX and slangStukje.positieY == keerPunt.positieY then
        test = kid
      end
    end
    if test == nil then
      table.remove(keerPunten, 1)
    end
  end
end

return extrafuncties
