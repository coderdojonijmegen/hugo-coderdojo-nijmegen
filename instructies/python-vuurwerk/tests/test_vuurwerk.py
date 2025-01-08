from vuurwerk import zomaar_een_richting_en_snelheid, stukken


def test_zomaar_een_richting_en_snelheid():
    snelheid = 0.0, 0

    for i in range(stukken):
        print(zomaar_een_richting_en_snelheid(snelheid, i))

    # assert zomaar_een_richting_en_snelheid(snelheid, 0) == (0.3, 2.0)
    # assert zomaar_een_richting_en_snelheid(snelheid, 1) == (0.3, 2.0)
    # assert zomaar_een_richting_en_snelheid(snelheid, 2) == (0.3, 2.0)
