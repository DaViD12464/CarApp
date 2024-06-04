from waitress import serve
import CarApi


serve(CarApi.app, host='0.0.0.0', port=5000)