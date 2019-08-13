import json

audience = '[{"error":{"type":false,"value":null},"patternType":"STRING-B","propertyType":"STATIC","async":false,"type":"VisitType","value":["RV"],"condition":"!=","valueOptions":[{"code":"RV","name":" Returning visits"}]},{"error":{"type":false,"value":null},"patternType":"STRING-B","propertyType":"STATIC","type":"TerminalType","value":["1","4"],"condition":"!=","valueOptions":[{"code":"1","name":"Smart phone"},{"code":"4","name":"Tablet"}]},{"error":{"type":false,"value":null},"patternType":"STRING-C","propertyType":"STATIC","type":"browser","value":["Safari","Firefox"],"condition":"![()]","valueOptions":[{"name":"Safari","id":"Safari","code":"Safari"},{"name":"Firefox","id":"Firefox","code":"Firefox"}]},{"error":{"type":false,"value":null},"patternType":"STRING-A","propertyType":"STATIC","type":"eventName","value":["First click"],"condition":"==","valueOptions":[{"id":"First%20click","name":"First click","code":"First click"}]}]'


a = json.loads(audience)

for j    in a:
	b = j['valueOptions']
	for i in b:
		print(i['name'])



