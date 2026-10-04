const { test } = require('node:test')
const assert = require('node:assert/strict')
const { Sessies } = require('../build/Sessies')

test('keeps a session during a dojo and replaces it after a day away', () => {
  const realNow = Date.now
  let now = 1_000_000
  Date.now = () => now
  try {
    const sessies = new Sessies()
    const first = sessies.verbind(null)
    sessies.zetNaam(first, 'Ninja')

    now += 23 * 60 * 60 * 1000
    const returnToday = sessies.verbind(first.id)
    assert.equal(returnToday.id, first.id)
    assert.equal(returnToday.naam, 'Ninja')

    now += 24 * 60 * 60 * 1000
    const nextDojo = sessies.verbind(first.id)
    assert.notEqual(nextDojo.id, first.id)
    assert.notEqual(nextDojo.naam, 'Ninja')
    assert.notEqual(sessies.verbind('unknown').id, nextDojo.id)
  } finally {
    Date.now = realNow
  }
})
