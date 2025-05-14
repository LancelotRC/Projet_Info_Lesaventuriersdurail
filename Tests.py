import unittest
from unittest.mock import patch
from collections import Counter
from LesAventuriersDuRail import * # Import du jeu


class TestPiocheWagon(unittest.TestCase):
    def setUp(self):
        """Initialisation de la pioche avec un mélange contrôlé."""
        cartes = [CarteWagon("locomotive")] * 5 + [CarteWagon("rouge"), CarteWagon("bleu"), CarteWagon("vert")] * 10
        self.pioche_wagon = PiocheWagon(cartes)

    def test_visibles_pas_3_locomotives(self):
        """Test : Vérifier que la pioche visible ne contient pas 3 locomotives."""
        # Forcer la pioche visible à contenir 3 locomotives
        self.pioche_wagon.visible = [CarteWagon("locomotive"), CarteWagon("locomotive"), CarteWagon("locomotive"),
                                     CarteWagon("rouge"), CarteWagon("bleu")]

        # Vérifier avant correction
        nb_locomotives_avant = sum(1 for c in self.pioche_wagon.visible if c.is_locomotive)
        self.assertEqual(nb_locomotives_avant, 3)  # ✅ Vérifier que la situation initiale est bien incorrecte

        # Appliquer la correction
        self.pioche_wagon.verifier_visibles_sans_3_locomotives()

        # Vérifier après correction
        nb_locomotives_apres = sum(1 for c in self.pioche_wagon.visible if c.is_locomotive)
        self.assertLess(nb_locomotives_apres, 3)  # ✅ Vérifier qu'il y a moins de 3 locomotives après correction

class TestChoisirCartesItineraire(unittest.TestCase):
    def setUp(self):
        """Initialisation des données de test"""
        self.joueur = Joueur("Alice", "rouge")
        self.cartes = [
            CarteItineraire("Los Angeles", "New York", 21),
            CarteItineraire("Chicago", "New Orleans", 7),
            CarteItineraire("Miami", "Houston", 8)
        ]

    @patch('builtins.input', return_value="0")
    def test_choisir_cartes_itineraire_garde_tout(self, mock_input):
        """Test : Le joueur garde toutes les cartes"""
        cartes_gardees, cartes_reposees = self.joueur.choisir_cartes_itineraire(self.cartes, initialisation=True)
        self.assertEqual(len(cartes_gardees), 3)  # Doit garder les 3 cartes
        self.assertEqual(len(cartes_reposees), 0)  # Aucune carte reposée

    @patch('builtins.input', side_effect=["1", "0"])
    def test_choisir_cartes_itineraire_repose_une(self, mock_input):
        """Test : Le joueur repose une seule carte"""
        cartes_gardees, cartes_reposees = self.joueur.choisir_cartes_itineraire(self.cartes, initialisation=True)
        self.assertEqual(len(cartes_gardees), 2)  # Doit garder 2 cartes
        self.assertEqual(len(cartes_reposees), 1)  # Une carte est reposée

    @patch('builtins.input', side_effect=["2", "3"])
    def test_choisir_cartes_itineraire_repose_maximum(self, mock_input):
        """Test : Le joueur repose une carte (cas initialisation)"""
        cartes_gardees, cartes_reposees = self.joueur.choisir_cartes_itineraire(self.cartes, initialisation=True)
        self.assertEqual(len(cartes_gardees), 2)  # Doit garder 2 cartes
        self.assertEqual(len(cartes_reposees), 1)  # Une carte reposée (limite initialisation)

    @patch('builtins.input', side_effect=["1", "2"])
    def test_choisir_cartes_itineraire_repose_deux_apres_initialisation(self, mock_input):
        """Test : Le joueur repose deux cartes en cours de partie (autorisé)"""
        cartes_gardees, cartes_reposees = self.joueur.choisir_cartes_itineraire(self.cartes, initialisation=False)
        self.assertEqual(len(cartes_gardees), 1)  # Doit garder 1 carte
        self.assertEqual(len(cartes_reposees), 2)  # Deux cartes reposées (autorisé après initialisation)

class TestPiocheCartesWagon(unittest.TestCase):
    def setUp(self):
        """Initialisation du joueur et de la table."""
        self.joueur = Joueur("Alice", "rouge")
        self.table = Table([self.joueur])

    @patch('builtins.input', return_value="1")
    def test_piocher_cartes_wagon_simple(self, mock_input):
        """Test : Le joueur pioche 2 cartes normales."""
        cartes_avant = len(self.joueur.cartes_wagon)
        self.table.piocher_cartes_wagon(self.joueur)
        cartes_apres = len(self.joueur.cartes_wagon)

        self.assertEqual(cartes_apres - cartes_avant, 2)  # ✅ Vérifier que 2 cartes ont été ajoutées

    @patch('builtins.input', return_value="1")
    def test_piocher_cartes_wagon_locomotive_premiere(self, mock_input):
        """Test : Si la première carte est une locomotive, le joueur ne pioche pas de deuxième carte."""
        self.table.pioche_wagon.pioche.insert(0, CarteWagon("locomotive"))  # Force une loco en première carte

        cartes_avant = len(self.joueur.cartes_wagon)
        self.table.piocher_cartes_wagon(self.joueur)
        cartes_apres = len(self.joueur.cartes_wagon)

        self.assertEqual(cartes_apres - cartes_avant, 1)  # ✅ Vérifier qu'une seule carte a été ajoutée

    @patch('builtins.input', side_effect=["1", "1"])  # Première carte normale, tentative de loco, puis autre choix valide
    def test_piocher_cartes_wagon_interdit_locomotive_deuxieme(self, mock_input):
        """Test : Le joueur ne peut pas piocher une locomotive en deuxième carte et doit refaire un choix."""
        self.table.pioche_wagon.pioche.insert(0, CarteWagon("bleu"))  # Première carte normale
        self.table.pioche_wagon.pioche.insert(1, CarteWagon("locomotive"))  # Deuxième carte = loco
        self.table.pioche_wagon.pioche.insert(2, CarteWagon("rouge"))  # Troisième tentative = carte valide

        cartes_avant = len(self.joueur.cartes_wagon)
        self.table.piocher_cartes_wagon(self.joueur)
        cartes_apres = len(self.joueur.cartes_wagon)

        self.assertEqual(cartes_apres - cartes_avant, 2)  # ✅ Vérifier que 2 cartes ont été ajoutées
        self.assertNotEqual(self.joueur.cartes_wagon[-1].couleur,
                            "locomotive")  # ✅ La deuxième carte ne doit pas être une loco

    @patch('builtins.input', return_value="1")
    def test_piocher_cartes_wagon_pioche_vide(self, mock_input):
        """Test : Vérifier que la défausse est mélangée si la pioche est vide."""
        self.table.pioche_wagon.pioche.clear()
        self.table.pioche_wagon.defausse = [CarteWagon("bleu"), CarteWagon("rouge")]

        cartes_avant = len(self.joueur.cartes_wagon)
        self.table.piocher_cartes_wagon(self.joueur)
        cartes_apres = len(self.joueur.cartes_wagon)

        self.assertGreater(cartes_apres - cartes_avant, 0)  # ✅ Vérifier qu’au moins une carte a été ajoutée

class TestCapturerRoute(unittest.TestCase):
    def setUp(self):
        """Initialisation du joueur et de la table."""
        self.joueur = Joueur("Bob", "bleu")
        self.table = Table([self.joueur])

        # Ajouter une route pour tester
        self.route = Route("Los Angeles", "San Francisco", "rouge", 3)
        self.table.plateau.routes.append(self.route)

    @patch('builtins.input', return_value="0")  # Simule le choix de la première route
    def test_capturer_route_succes(self, mock_input):
        """Test : Le joueur capture une route avec les bonnes cartes."""
        self.joueur.cartes_wagon = [CarteWagon("rouge")] * 3
        self.joueur.wagons_restants = 10
        self.table.capturer_route(self.joueur)

        self.assertEqual(self.route.possesseur, self.joueur)  # Vérifier que la route est bien capturée
        self.assertEqual(self.joueur.wagons_restants, 7)  # Vérifier que les wagons ont été utilisés
        self.assertEqual(len(self.joueur.cartes_wagon), 0)  # Vérifier que les cartes ont été défaussées

    @patch('builtins.input', return_value="0")  # Simule le choix de la première route
    def test_capturer_route_echec_pas_assez_de_cartes(self, mock_input):
        """Test : Le joueur ne peut pas capturer une route s'il n'a pas assez de cartes."""
        self.joueur.cartes_wagon = [CarteWagon("rouge")] * 2  # Pas assez de cartes
        self.joueur.wagons_restants = 10
        self.table.capturer_route(self.joueur)

        self.assertNotEqual(self.route.possesseur, self.joueur)  # La route ne doit pas être capturée

    @patch('builtins.input', return_value="0")  # Simule le choix de la première route
    def test_capturer_route_echec_pas_assez_de_wagons(self, mock_input):
        """Test : Le joueur ne peut pas capturer une route s'il n'a pas assez de wagons."""
        self.joueur.cartes_wagon = [CarteWagon("rouge")] * 3
        self.joueur.wagons_restants = 2  # Pas assez de wagons
        self.table.capturer_route(self.joueur)

        self.assertNotEqual(self.route.possesseur, self.joueur)  # La route ne doit pas être capturée

class TestVerifierCartesWagon(unittest.TestCase):
    def setUp(self):
        self.joueur = Joueur("Test", "bleu")

    def test_route_coloree_suffisante(self):
        route = Route("Chicago", "Saint Louis", "red", 3)
        self.joueur.cartes_wagon = [CarteWagon("red") for _ in range(2)] + [CarteWagon("locomotive")]
        self.assertTrue(self.joueur.verifier_cartes_wagon(route))

    def test_route_coloree_insuffisante(self):
        route = Route("Chicago", "Saint Louis", "red", 4)
        self.joueur.cartes_wagon = [CarteWagon("red") for _ in range(2)] + [CarteWagon("locomotive")]
        self.assertFalse(self.joueur.verifier_cartes_wagon(route))

    def test_route_grise_suffisante(self):
        route = Route("Chicago", "Saint Louis", "gris", 3)
        self.joueur.cartes_wagon = [CarteWagon("blue")] * 2 + [CarteWagon("locomotive")]
        self.assertTrue(self.joueur.verifier_cartes_wagon(route))

    def test_route_grise_insuffisante(self):
        route = Route("Chicago", "Saint Louis", "gris", 4)
        self.joueur.cartes_wagon = [CarteWagon("green")] + [CarteWagon("locomotive")]
        self.assertFalse(self.joueur.verifier_cartes_wagon(route))

if __name__ == "__main__":
    unittest.main()



if __name__ == '__main__':
    unittest.main()

