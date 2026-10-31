# собирает data.js из xlsx с продажами
import json, math
import pandas as pd

src = '../Продажи ЖК, март–сентябрь 2026.xlsx'
d = pd.read_excel(src)

def num(v):
    return None if v is None or (isinstance(v, float) and math.isnan(v)) else v

def dt(v):
    return None if pd.isna(v) else v.strftime('%Y-%m-%d')

rows = []
for _, r in d.iterrows():
    rows.append({
        'id': r['Квартира'],
        'b': r['Корпус'],
        'fl': int(r['Этаж']),
        'rooms': int(r['Комнат']),
        'layout': r['Планировка'],
        'area': float(r['Площадь, м²']),
        'ppm': round(float(r['Цена за м², руб.'])),
        'price': round(float(r['Стоимость, руб.'])),
        'disc': round(num(r['Скидка, руб.']) or 0),
        'sum': round(num(r['Сумма сделки, руб.'])) if num(r['Сумма сделки, руб.']) else None,
        'mgr': r['Менеджер'] if isinstance(r['Менеджер'], str) else None,
        'date': dt(r['Дата сделки']),
        'req': dt(r['Дата обращения']),
        'days': int(r['Дней в работе']) if num(r['Дней в работе']) is not None else None,
        'view': r['Вид'],
    })

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('const FLATS = ')
    json.dump(rows, f, ensure_ascii=False)
    f.write(';\n')
print(len(rows), 'квартир')
