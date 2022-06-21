import tsapi as ts

ts.SERVER = 'https://tsapi-demo.azurewebsites.net'

def for_loop(current_variable, data_rows):
    if len(current_variable.looped_variables) > 0 and len(current_variable.values) > 0:
        for value in current_variable.values:
            _a = current_variable.to_dict()
            _a.update(value.to_dict())
            data_rows.append(_a)
            for loop_variable in current_variable.looped_variables:
                for_loop(current_variable=loop_variable, data_rows=data_rows)
    elif len(current_variable.looped_variables) == 0 and len(current_variable.values) > 0:
        _a = current_variable.to_dict()
        for value in current_variable.values:
            _a = current_variable.to_dict()
            _a.update(vv.to_dict())
            data_rows.append(_a)
    elif len(current_variable.looped_variables) > 0 and len(current_variable.values) == 0:
        # check if this is valid

    elif len(current_variable.looped_variables) == 0 and len(current_variable.values) == 0:
        _a = current_variable.to_dict()
        data_rows.append(_a)
    else:
        _a = current_variable.to_dict()
        data_rows.append(_a)





if __name__ == '__main__':

    surveys = ts.get_surveys()

    survey = surveys[0]
    survey_id = survey['id']
    sd = ts.get_survey_detail(s_id=survey_id)
    r = ts.get_survey_detail_json(survey_id)

    s = ts.get_survey(r)

    data_rows = []
    for section in s.sections:
        for v in section.variables:

            if len(v.looped_variables) > 0 and len(v.values) > 0:
                for vv in v.values:
                    a = v.to_dict()
                    a.update(vv.to_dict())
                    data_rows.append(a)

                    for lv in v.looped_variables:
                        for lvv in lv.values:
                            b = lv.to_dict()
                            b.update(lvv.to_dict())
                            parent = {
                                'parent_variable': f'{v.name} - '
                                                   f'{vv.ident} '}

                            b.update(parent)
                            # print(b)
                            data_rows.append(b)
                            for lvlv in lv.looped_variables:
                                for lvvlvv in lvlv.values:
                                    c = lvlv.to_dict()
                                    c.update(lvvlvv.to_dict())
                                    parent = {
                                        'parent_variable': f'{v.name} - '
                                                           f'{vv.ident} - '
                                                           f'{lv.name} - '
                                                           f'{lvv.ident}'}

                                    c.update(parent)
                                    # print(c)
                                    data_rows.append(c)

            elif len(v.looped_variables) == 0 and len(v.values) > 0:

                a = v.to_dict()
                for vv in v.values:
                    a = v.to_dict()
                    a.update(vv.to_dict())
                    data_rows.append(a)
            elif len(v.looped_variables) == 0 and len(v.values) == 0:
                a = v.to_dict()
                data_rows.append(a)
            else:
                a = v.to_dict()
                data_rows.append(a)
            if len(v.otherSpecifyVariables) > 0:
                for osv in v.otherSpecifyVariables:
                    d = osv.to_dict()
                    data_rows.append(d)

    df = pd.DataFrame(data_rows)

    print(data_rows)
