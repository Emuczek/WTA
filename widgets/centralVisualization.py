from PySide6.QtWidgets import QApplication, QVBoxLayout, QScrollArea, QWidget, QLabel
from PySide6.QtWebEngineWidgets import QWebEngineView
from pyvis.network import Network
import os

class GraphWidget(QWidget):
    def __init__(self, data):
        super().__init__()
        self.data = data  # Lista grafów, gdzie graf = [zielone x czerwone wierzchołki z wagami]
        self.layout = QVBoxLayout(self)

        # Tworzymy główny obszar przewijania
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)

        # Główna zawartość scrolla
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_content.setLayout(self.scroll_layout)
        self.scroll_area.setWidget(self.scroll_content)

        # Ścieżka tymczasowa na pliki HTML
        self.temp_dir = "widgets/temp"
        os.makedirs(self.temp_dir, exist_ok=True)

        self.web_views = []
        self.draw_graphs()

    def draw_graphs(self):
        for graph_index, adjacency_matrix in enumerate(self.data):
            # Dodajemy tytuł nad grafem
            title_label = QLabel(f"Moment {graph_index + 1}")
            title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
            self.scroll_layout.addWidget(title_label)

            # Tworzymy sieć PyVis dla każdego grafu osobno
            net = Network(notebook=False, height="600px", width="100%", directed=True)

            num_green = len(adjacency_matrix)
            num_red = len(adjacency_matrix[0])

            # Dodajemy zielone wierzchołki
            for i in range(num_green):
                net.add_node(f"g{graph_index}_{i}", label=f"Broń {i+1}", color="green")

            # Dodajemy czerwone wierzchołki
            for j in range(num_red):
                net.add_node(f"r{graph_index}_{j}", label=f"Cel {j+1}", color="red")

            # Dodajemy krawędzie z wagami
            for i in range(num_green):
                for j in range(num_red):
                    weight = adjacency_matrix[i][j]
                    if weight > 0:
                        # Dodajemy krawędź z etykietą zawierającą wagę
                        net.add_edge(
                            f"g{graph_index}_{i}",
                            f"r{graph_index}_{j}",
                            title=f"Ilość: {weight}",  # Tooltip przy najechaniu
                            label=str(weight),      # Etykieta na krawędzi
                            font={"size": 16, "color": "black"},  # Czcionka etykiety
                        )

            # Zapisujemy graf do osobnego pliku HTML
            html_file = os.path.join(self.temp_dir, f"graph_{graph_index}.html")
            net.save_graph(html_file)

            # Tworzymy i konfigurujemy QWebEngineView dla każdego grafu
            web_view = QWebEngineView()
            web_view.setFixedSize(1100, 600)  # Ustaw stałą wielkość okna z grafem
            with open(html_file, "r") as f:
                html = f.read()
            web_view.setHtml(html)

            # Dodajemy widok do układu w przewijalnym obszarze
            self.scroll_layout.addWidget(web_view)
            self.web_views.append(web_view)
