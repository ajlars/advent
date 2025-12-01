const fs = require('fs');

const read = (name) => {
	try {
		const file = fs.readFileSync(`adventInputs/${name}.txt`, 'utf8');
		const lines = file.split(/\r?\n/);
		return lines;
	} catch (e) {
		console.error('readFileSync', e);
	}
};

const splitNumbers = (list, delimiter = /\s+/) =>
	list.map((line) => line.split(delimiter).map((num) => parseInt(num)));

module.exports = { read, splitNumbers };
