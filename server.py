from db import DB
from flask import Flask, render_template, request

app = Flask(__name__)
DB = DB()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form_data = request.form

        weapon_class = form_data["class"].replace("+", " ")
        name = form_data["name"]
        oasis_name_id = form_data["oasis_name_id"]
        price_rp = form_data["price_rp"]
        price_gc = form_data["price_gc"]
        unlock_level = form_data["unlock_level"]

        sku = DB.add_sku(name, oasis_name_id, price_rp, price_gc)
        temp_item = DB.add_templ_item(name, oasis_name_id, weapon_class)
        DB.add_sku_item(temp_item, sku, oasis_name_id)
        DB.add_weapon(weapon_class, temp_item)
        DB.add_compat_bridge(temp_item)
        DB.add_unlock(temp_item, unlock_level)
        comps = DB.add_components(form_data, name)
        DB.add_comp_list(comps, temp_item)
        DB.CONNECTION.commit()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
