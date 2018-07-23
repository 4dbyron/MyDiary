"""Get all entries in MyDiary"""
from flask import Flask
from flask_restful import Resource,reqparse, Api

app = Flask(__name__)
api = Api(app)

#Store the entries in a list made of dictionaries thus forming json.
entries = [
    {
        'entry_id': 1,
        'title': 'Andela PreBootCamp',
        'description': 'So there I was, ....'
    },
    {
        'entry_id': 2,
        'title': 'Love',
        'description': 'I have tried, not once or twice. but whenever I approach her..'
    },
    {
        'entry_id': 3,
        'title': 'Love',
        'description': 'I think I need a psychiatrist. last night I almost gave in to...'
    }
]

"""Entry resource parsed during the request"""
class Entry(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title',
                        type=str,
                        required=True,
                        help="Memories are worthless without title!"
                        ),
    parser.add_argument('description',
                        type=str,
                        required=True,
                        help="Please give the description."
                        )

    """get a specific diary entry"""
    def get(self, entry_id):
        entry = next(
            filter(lambda x: x['entry_id'] == entry_id, entries), None)
        return {'entry': entry}, 200 if entry else 404

    """post a new diary entry"""
    def post(self, entry_id):
        if next(filter(lambda x: x['entry_id'] == entry_id, entries), None):
            return {'message': "An entry with ID '{}' already exists.".format(entry_id)}, 400

        data = Entry.parser.parse_args()

        entry = {'entry_id': entry_id,
                 'title': data['title'],
                 'description': data['description']}
        entries.append(entry)
        return entry, 201

    """modify an entry"""
    def put(self, entry_id):
        data = Entry.parser.parse_args()

        entry = next(
            filter(lambda x: x['entry_id'] == entry_id, entries), None)
        if entry is None:
            entry = {'entry_id': entry_id,
                     'title': data['title'],
                     'description': data['description']}
            entries.append(entry)
        else:
            entry.update(data)
        return entry, 200

    """delete an entry from the diary"""
    def deleteEntry(self, entry_id):
        global entries
        entries = list(filter(lambda x: x['entry_id'] != entry_id, entries))
        return {'message': 'Entry successfully deleted'}


class EntryList(Resource):

    """return all entries"""
    def get(self):
        return {'entries': entries}


api.add_resource(Entry, '/api/v1/entry/<int:entry_id>')
api.add_resource(EntryList, '/api/v1/entries')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
