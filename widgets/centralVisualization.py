from PySide6.QtWidgets import QApplication, QVBoxLayout, QWidget
from PySide6.QtWebEngineWidgets import QWebEngineView
from pyvis.network import Network
import os

class GraphWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data  # Lista grafów, gdzie graf = [zielone x czerwone wierzchołki z wagami]
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Tworzymy widok WebEngine dla każdego grafu
        self.web_views = []
        for _ in data:
            web_view = QWebEngineView()
            self.layout.addWidget(web_view)
            self.web_views.append(web_view)

        # Ścieżka tymczasowa na pliki HTML
        self.temp_dir = "widgets/temp"
        os.makedirs(self.temp_dir, exist_ok=True)

        self.draw_graphs()

    def draw_graphs(self):
        for graph_index, adjacency_matrix in enumerate(self.data):
            # Tworzymy sieć PyVis dla każdego grafu osobno
            net = Network(notebook=False, height="800px", width="100%", directed=True)

            num_green = len(adjacency_matrix)
            num_red = len(adjacency_matrix[0])

            # Dodajemy zielone wierzchołki
            for i in range(num_green):
                net.add_node(f"g{graph_index}_{i}", label=f"Broń {i}", color="green")

            # Dodajemy czerwone wierzchołki
            for j in range(num_red):
                net.add_node(f"r{graph_index}_{j}", label=f"Cel {j}", color="red")

            # Dodajemy krawędzie z wagami
            for i in range(num_green):
                for j in range(num_red):
                    weight = adjacency_matrix[i][j]
                    if weight > 0:
                        # Dodajemy krawędź z etykietą zawierającą wagę
                        net.add_edge(
                            f"g{graph_index}_{i}",
                            f"r{graph_index}_{j}",
                            value=1,           # Wartość krawędzi (wagę)
                            title=f"Ilość: {weight}",  # Tooltip przy najechaniu
                            label=str(weight),      # Etykieta na krawędzi
                            font={"size": 16, "color": "black"},  # Czcionka etykiety
                            width=1,  # Ustawienie szerokości krawędzi na stałą wartość
                            arrows="to"  # Dodajemy strzałkę na końcu krawędzi (zamiast pogrubiania)
                        )

            # Zapisujemy graf do osobnego pliku HTML
            html_file = os.path.join(self.temp_dir, f"graph_{graph_index}.html")
            net.save_graph(html_file)

            # Ładujemy wygenerowany plik HTML do odpowiedniego QWebEngineView
            with open(html_file, "r") as f:
                html = f.read()
            self.web_views[graph_index].setHtml(html)


# Przykład użycia
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)

    # Przykładowe dane: lista macierzy
    data = [
        # Graf 1: Zielone x Czerwone
        [[1, 2],  # Zielony 0 -> Czerwony 0 (waga 1), Zielony 0 -> Czerwony 1 (waga 2)
         [0, 3]], # Zielony 1 -> Czerwony 1 (waga 3)

        # Graf 2: Zielone x Czerwone
        [[0, 1, 0],  # Zielony 0 -> Czerwony 1 (waga 1)
         [2, 0, 4]]  # Zielony 1 -> Czerwony 0 (waga 2), Zielony 1 -> Czerwony 2 (waga 4)
    ]

    widget = GraphWidget(data)
    widget.show()
    sys.exit(app.exec())
