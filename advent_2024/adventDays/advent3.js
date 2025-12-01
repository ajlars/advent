const { read } = require('../adventInputs/read');

const getInstructions = (expanded) =>
	read('dayThree')
		.join()
		.match(
			expanded
				? /(mul\(\d+,\d+\))|(do\(\))|(don\'t\(\))/g
				: /mul\(\d+,\d+\)/g
		);

const doMath = (expanded = false) => {
	let sum = 0;
	let enabled = true;
	let problems = [];
	let disabledCount = 0;
	let enabledCount = 0;
	getInstructions(expanded).forEach((str) => {
		if (str.includes("don't")) {
			enabled = false;
			disabledCount++;
		} else if (str.includes('do')) {
			enabled = true;
			enabledCount++;
		} else if (enabled) {
			problems.push(
				str
					.substring(4, str.length - 1)
					.split(',')
					.map((num) => parseInt(num))
			);
		}
	});
	problems.forEach(([a, b]) => (sum += a * b));
	console.log(disabledCount, enabledCount, sum);
};

doMath();
doMath(true);
