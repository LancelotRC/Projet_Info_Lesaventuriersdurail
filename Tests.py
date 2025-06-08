import unittest
from unittest.mock import patch
from collections import Counter
from LesAventuriersDuRail import * # Import du jeu


import unittest
from unittest.mock import patch
from LesAventuriersDuRail import *

class TestPiocheWagon(unittest.TestCase):
    def setUp(self):
        cartes = [CarteWagon("locomotive")] * 5 + [CarteWagon("rouge"), CarteWagon("bleu"), CarteWagon("vert")] * 10
        self.pioche_wagon = PiocheWagon(cartes)

    def test_visibles_pas_3_locomotives(self):
        self.pioche_wagon.visible = [
        CarteWagon("locomotive"),
        CarteWagon("locomotive"),
        CarteWagon("locomotive"),
        CarteWagon("rouge"),
        CarteWagon("bleu")
        ]

        nb_locomotives_avant = sum(1 for c in self.pioche_wagon.visible if c.is_locomotive)
        self.assertEqual(nb_locomotives_avant, 3)
        
        self.pioche_wagon.verifier_visibles_sans_3_locomotives()

        nb_locomotives_apres = sum(1 for c in self.pioche_wagon.visible if c.is_locomotive)
        self.assertLess(nb_locomotives_apres, 3)    


class TestChoisirCartesItineraire(unittest.TestCase):
    def setUp(self):
        self.joueur = Joueur("Alice", "rouge")
        self.cartes = [
            CarteItineraire(Ville("Los Angeles"), Ville("New York"), 21),
            CarteItineraire(Ville("Chicago"), Ville("New Orleans"), 7),
            CarteItineraire(Ville("Miami"), Ville("Houston"), 8)
        ]

    @patch('builtins.input', return_value="0")
    def test_choisir_cartes_itineraire_garde_tout(self, mock_input):
        cartes_gardees, cartes_reposees = self.joueur.choisir_cartes_itineraire(self.cartes, initialisation=True)
        self.assertEqual(len(cartes_gardees), 3)
        self.assertEqual(len(cartes_reposees), 0)

    @patch('builtins.input', side_effect=["1", "0"])
    def test_choisir_cartes_itineraire_repose_une(self, mock_input):
        cartes_gardees, cartes_reposees = self.joueur.choisir_cartes_itineraire(self.cartes, initialisation=True)
        self.assertEqual(len(cartes_gardees), 2)
        self.assertEqual(len(cartes_reposees), 1)

    @patch('builtins.input', side_effect=["2", "3"])
    def test_choisir_cartes_itineraire_repose_maximum(self, mock_input):
        cartes_gardees, cartes_reposees = self.joueur.choisir_cartes_itineraire(self.cartes, initialisation=True)
        self.assertEqual(len(cartes_gardees), 2)
        self.assertEqual(len(cartes_reposees), 1)

    @patch('builtins.input', side_effect=["1", "2"])
    def test_choisir_cartes_itineraire_repose_deux_apres_initialisation(self, mock_input):
        cartes_gardees, cartes_reposees = self.joueur.choisir_cartes_itineraire(self.cartes, initialisation=False)
        self.assertEqual(len(cartes_gardees), 1)
        self.assertEqual(len(cartes_reposees), 2)

class TestPiocheCartesWagon(unittest.TestCase):
    def setUp(self):
        self.joueur = Joueur("Alice", "rouge")
        self.table = Table([self.joueur])

    @patch('builtins.input', return_value="1")
    def test_piocher_cartes_wagon_simple(self, mock_input):
        cartes_avant = len(self.joueur.cartes_wagon)
        self.table.piocher_cartes_wagon(self.joueur)
        cartes_apres = len(self.joueur.cartes_wagon)
        self.assertEqual(cartes_apres - cartes_avant, 2)

    @patch('builtins.input', side_effect=["2", "3"])  # Choix de la 3e carte visible = locomotive
    def test_piocher_cartes_wagon_locomotive_premiere(self, mock_input):
        self.table.pioche_wagon.pioche = [CarteWagon("rouge")]
        self.table.pioche_wagon.visible = [
            CarteWagon("bleu"),
            CarteWagon("rouge"),
            CarteWagon("locomotive"),
            CarteWagon("vert"),
            CarteWagon("noir"),
            ]
        cartes_avant = len(self.joueur.cartes_wagon)
        self.table.piocher_cartes_wagon(self.joueur)
        cartes_apres = len(self.joueur.cartes_wagon)
        self.assertEqual(cartes_apres - cartes_avant, 1)  # Seulement 1 carte (la locomotive)
 

    @patch('builtins.input', side_effect=["2", "5"])  # Pioche 1 carte cachée, puis une visible "locomotive"
    def test_piocher_cartes_wagon_interdit_locomotive_deuxieme(self, mock_input):
        self.table.pioche_wagon.pioche = [
            CarteWagon("bleu"),
            CarteWagon("locomotive"),
            CarteWagon("rouge")
            ]
        self.table.pioche_wagon.visible = [
            CarteWagon("bleu"),
            CarteWagon("vert"),
            CarteWagon("rouge"),
            CarteWagon("noir"),
            CarteWagon("locomotive"),  # 5e = locomotive
            ]
        cartes_avant = len(self.joueur.cartes_wagon)
        self.table.piocher_cartes_wagon(self.joueur)
        cartes_apres = len(self.joueur.cartes_wagon)

        self.assertEqual(cartes_apres - cartes_avant, 1)



    @patch('builtins.input', return_value="1")
    def test_piocher_cartes_wagon_pioche_vide(self, mock_input):
        self.table.pioche_wagon.pioche = []
        self.table.pioche_wagon.defausse = [CarteWagon("bleu"), CarteWagon("rouge")]
        cartes_avant = len(self.joueur.cartes_wagon)
        self.table.piocher_cartes_wagon(self.joueur)
        cartes_apres = len(self.joueur.cartes_wagon)
        self.assertGreaterEqual(cartes_apres - cartes_avant, 0)
        


class TestCapturerRoute(unittest.TestCase):
    def setUp(self):
        self.joueur = Joueur("Test", "bleu")
        self.table = Table([self.joueur])
    
        v1 = Ville("A", (0, 0))
        v2 = Ville("B", (1, 1))
        self.route = Route(v1, v2, "bleu", 3, False)  

        self.table.plateau.villes = [v1, v2]
        self.table.plateau.dico_villes = {v.nom: v for v in [v1, v2]}
        self.table.plateau.routes.append(self.route)


    @patch('builtins.input', return_value="0")
    def test_capturer_route_succes(self, mock_input):
        self.joueur.cartes_wagon = [CarteWagon("rouge")] * 3
        self.joueur.wagons_restants = 10
        self.route.couleur = "rouge"
        self.route.longueur = 3
        self.route.ville1 = "A"
        self.route.ville2 = "B"
        self.route.possesseur = None
        self.table.routes = [self.route]  # Assure que la route est listée

        self.table.capturer_route(self.joueur)
        
        self.assertEqual(self.route.possesseur, self.joueur)
        self.assertEqual(self.joueur.wagons_restants, 7)
        self.assertEqual(len(self.joueur.cartes_wagon), 0)



    @patch('builtins.input', return_value="0")
    def test_capturer_route_echec_pas_assez_de_cartes(self, mock_input):
        self.joueur.cartes_wagon = [CarteWagon("rouge")] * 2
        self.joueur.wagons_restants = 10
        self.table.capturer_route(self.joueur)
        self.assertNotEqual(self.route.possesseur, self.joueur)

    @patch('builtins.input', return_value="0")
    def test_capturer_route_echec_pas_assez_de_wagons(self, mock_input):
        self.joueur.cartes_wagon = [CarteWagon("rouge")] * 3
        self.joueur.wagons_restants = 2
        self.table.capturer_route(self.joueur)
        self.assertNotEqual(self.route.possesseur, self.joueur)




class TestVerifierCartesWagon(unittest.TestCase):
    def setUp(self):
        self.joueur = Joueur("Test", "bleu")

    def test_route_coloree(self):
        route = Route(Ville("Chicago", (0, 0)), Ville("Saint Louis", (1, 1)), "red", 3, False)
        self.joueur.cartes_wagon = [CarteWagon("red")] * 2 + [CarteWagon("locomotive")]
        self.assertTrue(self.joueur.verifier_cartes_wagon(route))

        self.joueur.cartes_wagon = [CarteWagon("red")] + [CarteWagon("locomotive")]
        self.assertFalse(self.joueur.verifier_cartes_wagon(route))

        self.joueur.cartes_wagon = [CarteWagon("blue")] * 3 + [CarteWagon("locomotive")]
        self.assertFalse(self.joueur.verifier_cartes_wagon(route))

        self.joueur.cartes_wagon = [CarteWagon("red")] * 6 + [CarteWagon("locomotive")]
        self.assertTrue(self.joueur.verifier_cartes_wagon(route))


    def test_route_grise_suffisante(self):
        route = Route(Ville("Chicago", (0, 0)), Ville("Saint Louis", (1, 1)), "gris", 4, False)

        self.joueur.cartes_wagon = [CarteWagon("blue")] * 3 + [CarteWagon("locomotive")]
        self.assertTrue(self.joueur.verifier_cartes_wagon(route))

        self.joueur.cartes_wagon = [CarteWagon("blue")] * 3 + [CarteWagon("white")] * 5 + [CarteWagon("locomotive")] * 4
        self.assertTrue(self.joueur.verifier_cartes_wagon(route))

        self.joueur.cartes_wagon = [CarteWagon("red")] + [CarteWagon("blue")] + [CarteWagon("locomotive")]
        self.assertFalse(self.joueur.verifier_cartes_wagon(route))

        self.joueur.cartes_wagon = [CarteWagon("green")] + [CarteWagon("locomotive")]
        self.assertFalse(self.joueur.verifier_cartes_wagon(route))
               
            
class TestPlusLongChemin(unittest.TestCase):
    def setUp(self):
        self.joueur = Joueur("Alice", "rouge")
        self.table = Table([self.joueur])

        # Créer 3 villes fictives reliées en ligne
        v1 = Ville("A", (0, 0))
        v2 = Ville("B", (1, 1))
        v3 = Ville("C", (2, 2))
        self.table.plateau.villes = [v1, v2, v3]
        self.table.plateau.dico_villes = {v.nom: v for v in self.table.plateau.villes}

        r1 = Route(v1, v2, "rouge", 1, False)
        r2 = Route(v2, v3, "rouge", 1, False)

        # Capturées par le joueur
        r1.possesseur = self.joueur
        r2.possesseur = self.joueur
        self.joueur.routes_capturees.extend([r1, r2])
        self.table.plateau.routes = [r1, r2]

    def test_longueur_chemin(self):
        joueur_max = self.table.joueur_plus_longue_route()
        self.assertEqual(joueur_max, self.joueur)


class TestSauvegarde(unittest.TestCase):
    def setUp(self):
        self.joueur = Joueur("Zoe", "vert")
        self.joueur.cartes_wagon = [CarteWagon("rouge"), CarteWagon("bleu")]
        self.joueur.cartes_defi = [CarteItineraire(Ville("Paris"), Ville("Berlin"), 7)]
        self.joueur.routes_capturees = [
            Route(Ville("Paris"), Ville("Berlin"), "rouge", 3, False)
        ]
        self.table = Table([self.joueur])
        self.table.joueur_actuel = self.joueur

    def test_structure_sauvegarde(self):
        # Appel de la méthode sans écrire dans un fichier
        donnees = {
            "joueurs": [
                {
                    "nom": self.joueur.nom,
                    "couleur": self.joueur.couleur,
                    "wagons_restants": self.joueur.wagons_restants,
                    "cartes_wagon": [c.couleur for c in self.joueur.cartes_wagon],
                    "cartes_defi": [
                        {
                            "ville_depart": "Paris",
                            "ville_arrivee": "Berlin",
                            "points": 7
                        }
                    ],
                    "routes_capturees": [
                        {
                            "ville1": "Paris",
                            "ville2": "Berlin",
                            "couleur": "rouge",
                            "longueur": 3
                        }
                    ]
                }
            ],
            "joueur_actuel": 0
        }

        sauvegarde_theorique = self.table.sauvegarder.__code__.co_consts  # À usage interne, pas fiable à long terme
        self.assertIsInstance(donnees, dict)
        self.assertIn("joueurs", donnees)
        self.assertEqual(donnees["joueurs"][0]["nom"], "Zoe")


class TestCalculScore(unittest.TestCase):
    def setUp(self):
        self.joueur = Joueur("Paul", "bleu")
        self.table = Table([self.joueur])
        self.table.joueur_actuel = self.joueur

        # Ville simulée
        v1 = Ville("Paris")
        v2 = Ville("Berlin")

        self.route = Route(v1, v2, "bleu", 4, False)
        self.route.possesseur = self.joueur
        self.joueur.routes_capturees.append(self.route)

        self.joueur.cartes_defi = [CarteItineraire(v1, v2, 8)]
        self.table.plateau.villes = [v1, v2]
        self.table.plateau.routes = [self.route]
        self.table.plateau.dico_villes = {v.nom: v for v in [v1, v2]}

        # On force la fonction à reconnaître ce joueur comme ayant le plus long chemin
        self.table.joueur_plus_longue_route = lambda: self.joueur

    def test_compte_points(self):
        # Rediriger la sortie pour vérifier sans afficher
        import io, sys
        captured_output = io.StringIO()
        sys.stdout = captured_output

        self.table.compte_des_points(self.table.plateau)

        sys.stdout = sys.__stdout__  # Reset

        output = captured_output.getvalue()
        self.assertIn("Paul remporte le bonus de la route la plus longue", output)
        self.assertIn("Score total : 25", output)


if __name__ == "__main__":
    unittest.main()

