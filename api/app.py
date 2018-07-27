"""Get all entries in MyDiary"""
from flask import Flask

from flask_restful import Resource, reqparse, Api

app = Flask(__name__)
api = Api(app)

# Store the entries in a list made of dictionaries thus forming json.
entries = [
    {
        'entry_id': 1,
        'title': 'Love',
        'description': 'I have tried, not once or twice. but whenever I approach her..'
    },
    {
        'entry_id': 2,
        'title': 'Love',
        'description': 'I have tried, not once or twice. but whenever I approach her..'
    },
    {
        'entry_id': 3,
        'title': 'Love',
        'description': 'I have tried, not once or twice. but whenever I approach her..'
    }
]

"""Entry resource parsed during the request"""


class Entry(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help="Content Missing"),
    parser.add_argument('description', type=str, required=True, help="Content Description Missing.")

    """get a specific diary entry"""

    def get(self, entry_id):
        entry = next(filter(lambda x: x['entry_id'] == entry_id, entries), None)
        return {'entry': entry}, 200 if entry else 404

    """modify an entry"""

    def put(self, entry_id):
        data = Entry.parser.parse_args()

        entry = next(
            filter(lambda x: x['entry_id'] == entry_id, entries), None)
        if entry is None:
            return 'entry not found', 404
        else:
            entry = {'entry_id': entry_id,
                     'title': data['title'],
                     'description': data['description']}
            entry.update(data)
        return entry, 200

    """delete an entry from the diary"""

    def delete(self, entry_id):
        global entries
        entries = list(filter(lambda x: x['entry_id'] != entry_id, entries))
        return {'message': 'Entry successfully deleted'}


class Entries(Resource):
    """return all entries"""

    def get(self):
        return {'entries': entries}

    """post a new diary entry"""

    def post(self):
        data = Entry.parser.parse_args()

        entry = {'entry_id': 12, 'title': data['title'], 'description': data['description']}
        entries.append(entry)
        return entry, 201


# root : GET /
'''Return details about the api server'''


@app.route('/')
def root():
    return """ [
        {'AppName': 'MyDiary'},
        {'Version': 1},
        {'Author': 'Byron Taaka'},
        {'Email' : '4dbyron@gmail.com'},
        {'host' : 'localhost or github.com or heroku'},
        {'Endpoints': '/api/v1/entries'}]
        """


api.add_resource(Entry, '/api/v1/entries/<int:entry_id>')
api.add_resource(Entries, '/api/v1/entries')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
