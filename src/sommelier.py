#!python

# import useful Flask libs
from flask import request, Response, jsonify, json

# import broker libs that will interface with the DB
from brokers import SommelierBroker

# import the Sommelier recommender
from recommender import Recommender

class Sommelier:

    def __init__(self, b=SommelierBroker(), r=Recommender()):
        self.broker = b
        self.recommender = r

    # Takes dict of content and generates JSON response with
    # appropriate MIME type, HTTP status code etc.
    def http_success_json(self, content):
        response = json.dumps(content, encoding="utf-8")
        response = ''.join(response.decode('unicode-escape').splitlines())
        return response, { 'status': 200, 'mimetype': 'application/json; charset=utf-8' }

    def wine_page(self, page_num):
        records = self.broker.get_wine_page(page_num)
        num_pages = self.broker.get_num_wine_pages()
        return self.http_success_json({
            'wines': records,
            'num_pages': num_pages
        })

    def wine(self, wine_id):
        record = self.broker.get_wine(wine_id)
        recommendations = self.recommender.wines_for_wine(wine_id)
        return self.http_success_json({
            'wine': record,
            'recommendations': recommendations
        })
    
    def author_page(self, page_num):
        records = self.broker.get_author_page(page_num)
        num_pages = self.broker.get_num_author_pages()
        return self.http_success_json({
            'authors': records, 
            'num_pages': num_pages 
        })

    def author(self, author_id):
        record = self.broker.get_author(author_id)
        recommendations = self.recommender.wines_for_author(author_id)
        return self.http_success_json({
            'author': record,
            'recommendations': recommendations
        })

    def build_sparse_ui_matrix(self):
        self.recommender.create_sparse_ui_matrix()
        matrix = self.recommender.load_sparse_ui_matrix()
        return self.http_success_json({
            'user_item_matrix': matrix
        })

