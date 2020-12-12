rm -f units.js

wget https://raw.githubusercontent.com/optc-db/optc-db.github.io/master/common/data/units.js

cp units.js modifiedUnits.js
sed -i 's/window.units =/const startUnits =/g' modifiedUnits.js
echo '\nconst unitsJSON = JSON.stringify(startUnits)' >> modifiedUnits.js
echo 'const fs = require("fs");' >> modifiedUnits.js
echo 'fs.writeFile("../data/units.json", unitsJSON, () => console.log("Done"))' >> modifiedUnits.js
node modifiedUnits.js
