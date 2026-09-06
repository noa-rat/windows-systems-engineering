from client.shared.api import get_graph_statistics_async

class GraphPresenter:
    def __init__(self):
        pass

    def fetch_category_data(self, on_success, on_error):
        get_graph_statistics_async(on_success, on_error)