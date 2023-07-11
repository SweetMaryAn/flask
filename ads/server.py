from flask import Flask, request, jsonify
from flask.views import MethodView
from db import Ad, Session
from schema import validate_create_ads
from errors import HttpError
from sqlalchemy.exc import IntegrityError

app = Flask('server')

@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    http_response = jsonify({'status': 'error', 'description': error.message})
    http_response.status_code = error.status_code
    return http_response

def get_ad(ad_id: int, session: Session):
    ad = session.query(Ad).get(ad_id)
    if ad is None:
        raise HttpError(404, 'ad not found')
    return ad

class AdView(MethodView):

    def get(self, ad_id: int):
        with Session() as session:
            ad = get_ad(ad_id, session)
            return jsonify({
                'id': ad.id,
                'heading': ad.heading,
                'creation_time': ad.creationt_time.isoformat()
            })

    def post(self):
        json_date = validate_create_ads(request.json)
        with Session() as session:
            new_ad = Ad(**json_date)
            session.add(new_ad)
            try:
                session.commit()
            except IntegrityError:
                raise HttpError(409, 'ad already exists')
            return jsonify(
                {
                    'id': new_ad.id,
                    'creation_time': int(new_ad.creationt_time.timestamp())
                }
            )

    def patch(self, ad_id: int):
        json_data = request.json
        with Session() as session:
            ad = get_ad(ad_id, session)
            for field, value in json_data.items():
                setattr(ad, field, value)
            session.add(ad)
            session.commit()
        return jsonify({'status': 'succes'})

    def delete(self, ad_id: int):
        with Session() as session:
            ad = get_ad(ad_id, session)
            session.delete(ad)
            session.commit()
        return jsonify({'status': 'succes'})


app.add_url_rule('/ads/<int:ad_id>', view_func=AdView.as_view('ads_with_id'), methods=['GET','PATCH','DELETE'])
app.add_url_rule('/ads', view_func=AdView.as_view('ads'), methods=['POST'])

app.run(port=5000)