from flask import Flask, make_response, jsonify, Response, request, render_template, send_file


import ais_ras_4


app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# @app.route("/api/v1.0/placing", methods=['POST'])
# def set_params():
#     pass


@app.route("/api/v1.0/get_user_place", methods=['POST'])
def get_user_place():
    social_distance = False
    excel_import = True
    mass_import = []

    user_id = request.json['user_id']

    # mass_import = list(request.json['mass_import'])

    if excel_import is True:
        user_ex = ais_ras_4.imp_ex('База.xlsx', 'Лист1', 'A1', 'F302')
        convert = ais_ras_4.convert_data(user_ex)
        convert_LD = ais_ras_4.convert_list_dict(convert)
    else:
        user_ex = mass_import
        convert_LD = ais_ras_4.convert_list_dict(user_ex)

    prem = ais_ras_4.Premise(8, 29, space_col=[7, 21], space={7: list(range(22, 30))},
                             doclad={
                                 0: list(range(0, 3)) + list(range(4, 7)) + list(range(8, 11)) + list(
                                     range(18, 21)) + list(
                                     range(22, 25)) + list(range(26, 30)),
                                 1: list(range(0, 3)) + list(range(4, 7)) + list(range(8, 11)) + list(
                                     range(18, 21)) + list(
                                     range(22, 25)) + list(range(26, 30)),
                                 2: list(range(0, 3)) + list(range(4, 7)) + list(range(8, 11)) + list(
                                     range(18, 21)) + list(
                                     range(22, 25)) + list(range(26, 30)),
                             })

    prem.gen_shemNone()

    if social_distance is True:
        prem.social_modify(prem.shemNone)

    prem.gen_shem_on_clNone(prem.shemNone)

    for i in convert_LD.keys():
        if i is None:
            continue
        elif (str(i).lower() == 'default') | (len(convert_LD.get(i)) == 1):
            for j in convert_LD.get(i):
                prem.posadkaNone(j[0], j[3], j[4], i, prem.shemNone, prem.shem_on_clNone)
        else:
            prem.groupposadkaNone(convert_LD.get(i), i, prem.shemNone, prem.shem_on_clNone)

    return jsonify({user_id: str(prem.search_id(prem.shemNone, user_id))})

@app.route("/api/v1.0/placing", methods=['POST'])
def get_places():
    social_distance = False
    excel_import = False
    # mass_import = []
    # print(request.data)
    # print('JSON', request.json['guests'])
    # print('JSON', request.json['user'])
    mass = request.json['guests']
    mass_import = []
    # [[i['id'], 0, 0, str(i['last_name'] + ' ' + i['name'] + ' ' + i['second_name']), i['status'], i['organization']] for i in mass_import]
    for i in mass:
        if i['status'] == 'Докладчик':
            i['status'] = 'doclad'
        else:
            i['status'] = 'gost'
        mass_import.append([i['id'], 0, 0, str(i['last_name'] + ' ' + i['name'] + ' ' + i['second_name']), i['status'], i['organization']])

    # row = int(request.json['row'])
    # col = int(request.json['col'])
    row = 8
    col = 29
    # space_col = list(request.json['s_col'])
    # space_row = dict(request.json['s_col'])

    high = int(request.json['user'])


    # mass_import = list(request.json['mass_import'])


    if excel_import is True:
        user_ex = ais_ras_4.imp_ex('База.xlsx', 'Лист1', 'A1', 'F302')
        convert = ais_ras_4.convert_data(user_ex)
        convert_LD = ais_ras_4.convert_list_dict(convert)
    else:
        user_ex = mass_import
        convert_LD = ais_ras_4.convert_list_dict(user_ex)

    prem = ais_ras_4.Premise(row, col, space_col=[7, 21], space={7: list(range(22, 30))})

    prem.gen_shemNone()

    if social_distance is True:
        prem.social_modify(prem.shemNone)

    prem.gen_shem_on_clNone(prem.shemNone)

    for i in convert_LD.keys():
        if i is None:
            continue
        elif (str(i).lower() == 'default') | (len(convert_LD.get(i)) == 1):
            for j in convert_LD.get(i):
                prem.posadkaNone(j[0], j[3], j[4], i, prem.shemNone, prem.shem_on_clNone)
        else:
            prem.groupposadkaNone(convert_LD.get(i), i, prem.shemNone, prem.shem_on_clNone)

    prem.create_imgsvg(prem.shemNone, prem.shem_on_clNone, 'shem_ras', color_organisation=False, highliter=high)
    # print(Response(ais_ras_3.json_ser(ais_ras_3.resp_data(prem.shemNone)),  mimetype='application/json'))
    # svg = open('shem_ras.svg').read
    mass_import.clear()
    return send_file('./shem_ras.svg', attachment_filename='shem_ras.svg')
        # render_template('test.html', svg=Markup(svg))
        # ais_ras_4.json_ser(ais_ras_4.resp_data(prem.shemNone))



    # str(ais_ras_3.json_ser1(ais_ras_3.resp_data(prem.shemNone)))


    # Response(ais_ras_3.json_ser1(ais_ras_3.resp_data(prem.shemNone)),  mimetype='application/json') # Response(ais_ras_3.json_ser(ais_ras_3.resp_data(prem.shemNone)))

    # str(ais_ras_3.json_ser(ais_ras_3.resp_data(prem.shemNone))) # Response(ais_ras_3.json_ser(ais_ras_3.resp_data(prem.shemNone)),  mimetype='application/json') #str(ais_ras_3.json_ser(ais_ras_3.resp_data(prem.shemNone)))


@app.route("/", methods=['GET'])
def Hello():
    return jsonify({'Bobr': 'VPR'})


if __name__ == '__main__':
    app.run(host='10.13.7.65', port='4000')


# social_distance = False
# excel_import = True
# mass_import = []
#
# if excel_import is True:
#     user_ex = ais_ras_3.imp_ex('База.xlsx', 'Лист1', 'A1', 'F302')
#     convert = ais_ras_3.convert_data(user_ex)
#     convert_LD = ais_ras_3.convert_list_dict(convert)
# else:
#     user_ex = mass_import
#     convert_LD = ais_ras_3.convert_list_dict(user_ex)
#
# prem = ais_ras_3.Premise(8, 29, space_col=[7, 21], space={7: list(range(22, 30))},
#                    doclad={
#                        0: list(range(0, 3)) + list(range(4, 7)) + list(range(8, 11)) + list(range(18, 21)) + list(
#                            range(22, 25)) + list(range(26, 30)),
#                        1: list(range(0, 3)) + list(range(4, 7)) + list(range(8, 11)) + list(range(18, 21)) + list(
#                            range(22, 25)) + list(range(26, 30)),
#                        2: list(range(0, 3)) + list(range(4, 7)) + list(range(8, 11)) + list(range(18, 21)) + list(
#                            range(22, 25)) + list(range(26, 30)),
#                    })
#
# prem.gen_shemNone()
#
# if social_distance is True:
#     prem.social_modify(prem.shemNone)
#
# prem.gen_shem_on_clNone(prem.shemNone)
#
# for i in convert_LD.keys():
#     if i is None:
#             continue
#     elif (str(i).lower() == 'default') | (len(convert_LD.get(i)) == 1):
#         for j in convert_LD.get(i):
#             prem.posadkaNone(j[0], j[3], j[4], i, prem.shemNone, prem.shem_on_clNone)
#     else:
#         prem.groupposadkaNone(convert_LD.get(i), i, prem.shemNone, prem.shem_on_clNone)
#
# prem.create_imgsvg(prem.shemNone, prem.shem_on_clNone, 'shem_ras', color_organisation=False)



