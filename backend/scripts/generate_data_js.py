import json

with open('tickets.json', 'r', encoding='utf-8') as f:
    tickets = json.load(f)

with open('data.js', 'w', encoding='utf-8') as f:
    f.write('// RideOps Support Case Study Data Store\n')
    f.write('var RIDE_OPS_DATA = ')
    json.dump(tickets, f, separators=(',', ':'))
    f.write(';\nif (typeof window !== "undefined") { window.RIDE_OPS_DATA = RIDE_OPS_DATA; }\nif (typeof globalThis !== "undefined") { globalThis.RIDE_OPS_DATA = RIDE_OPS_DATA; }\n')

print(f'Universal data.js successfully written with {len(tickets)} tickets.')
