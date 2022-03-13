rm -f units.js

wget https://raw.githubusercontent.com/optc-db/optc-db.github.io/master/common/data/units.js

units_js_content=$(cat units.js)
echo "const window = {};\n${units_js_content}" > modifiedUnits.js
echo 'const unitsJSON = JSON.stringify(window.units)' >> modifiedUnits.js
echo 'const fs = require("fs");' >> modifiedUnits.js
echo 'fs.writeFile("../data/units.json", unitsJSON, () => console.log("Done"))' >> modifiedUnits.js
node modifiedUnits.js
